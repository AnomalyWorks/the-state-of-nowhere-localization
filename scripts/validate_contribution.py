#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path


ALLOWED_ROOT = "locales/"
ALLOWED_EXTENSION = ".txt"

OPEN_MARKER = "<<<"
CLOSE_MARKER = ">>>"
PLACEHOLDER = "<TRANSLATION_CONTENT>"


class ValidationError(Exception):
    pass


def run_git(*args):
    result = subprocess.run(
        ["git", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise ValidationError(
            "Git command failed:\n"
            f"git {' '.join(args)}\n\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout


def get_changed_files(base_sha):
    """
    Return a list of (status, path) entries changed between the PR base
    and the checked-out PR/merge result.

    Renames/copies are deliberately requested without rename detection so
    they appear as delete + add and are therefore rejected.
    """
    output = run_git(
        "diff",
        "--name-status",
        "--no-renames",
        base_sha,
        "HEAD",
    )

    changes = []

    for raw_line in output.splitlines():
        if not raw_line.strip():
            continue

        parts = raw_line.split("\t", 1)

        if len(parts) != 2:
            raise ValidationError(
                f"Could not parse changed-file entry: {raw_line!r}"
            )

        status, path = parts
        changes.append((status.strip(), path.strip()))

    return changes


def read_base_file(base_sha, path):
    try:
        return run_git("show", f"{base_sha}:{path}")
    except ValidationError as exc:
        raise ValidationError(
            f"Could not read the base version of:\n{path}\n\n{exc}"
        ) from exc


def read_current_file(path):
    file_path = Path(path)

    if not file_path.is_file():
        raise ValidationError(
            f"Changed localization file does not exist in the PR result:\n{path}"
        )

    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(
            f"Localization file is not valid UTF-8:\n{path}"
        ) from exc


def mask_translation_content(text, path, version_label):
    """
    Replace only the editable contents between <<< and >>> with a constant
    placeholder while preserving every protected character outside the block.

    If masked base text == masked PR text, the contributor changed only
    translation bodies.
    """
    lines = text.splitlines(keepends=True)

    masked = []
    inside_translation = False
    block_count = 0
    current_translation_has_content = False

    for line_number, line in enumerate(lines, start=1):
        logical_line = line.rstrip("\r\n")

        if not inside_translation:
            if logical_line == OPEN_MARKER:
                inside_translation = True
                block_count += 1
                current_translation_has_content = False

                # Preserve the marker exactly, including its newline.
                masked.append(line)

                # The body itself is intentionally ignored.
                masked.append(PLACEHOLDER + "\n")
                continue

            if logical_line == CLOSE_MARKER:
                raise ValidationError(
                    f"{path} ({version_label}): unexpected {CLOSE_MARKER!r} "
                    f"at line {line_number}."
                )

            masked.append(line)
            continue

        # We are inside an editable translation block.
        if logical_line == OPEN_MARKER:
            raise ValidationError(
                f"{path} ({version_label}): nested {OPEN_MARKER!r} "
                f"at line {line_number}."
            )

        if logical_line == CLOSE_MARKER:
            if not current_translation_has_content:
                raise ValidationError(
                    f"{path} ({version_label}): empty translation block "
                    f"ending at line {line_number}."
                )

            inside_translation = False
            masked.append(line)
            continue

        if logical_line.strip():
            current_translation_has_content = True

    if inside_translation:
        raise ValidationError(
            f"{path} ({version_label}): translation block opened with "
            f"{OPEN_MARKER!r} but never closed with {CLOSE_MARKER!r}."
        )

    if block_count == 0:
        raise ValidationError(
            f"{path} ({version_label}): no translation blocks were found."
        )

    return "".join(masked), block_count


def validate_changed_path(status, path):
    if status != "M":
        raise ValidationError(
            f"Only modifications of existing localization files are allowed.\n"
            f"Detected status {status!r} for:\n{path}\n\n"
            "Adding, deleting, moving, or renaming files through a community "
            "localization pull request is not allowed."
        )

    normalized = path.replace("\\", "/")

    if not normalized.startswith(ALLOWED_ROOT):
        raise ValidationError(
            "Community localization pull requests may only modify files "
            f"inside {ALLOWED_ROOT!r}.\n"
            f"Changed file:\n{path}"
        )

    if not normalized.endswith(ALLOWED_EXTENSION):
        raise ValidationError(
            "Community localization pull requests may only modify "
            f"{ALLOWED_EXTENSION} localization files.\n"
            f"Changed file:\n{path}"
        )


def validate_file(base_sha, path):
    base_text = read_base_file(base_sha, path)
    current_text = read_current_file(path)

    masked_base, base_blocks = mask_translation_content(
        base_text,
        path,
        "base",
    )
    masked_current, current_blocks = mask_translation_content(
        current_text,
        path,
        "pull request",
    )

    if base_blocks != current_blocks:
        raise ValidationError(
            f"{path}: number of translation blocks changed "
            f"({base_blocks} -> {current_blocks})."
        )

    if masked_base != masked_current:
        raise ValidationError(
            f"Protected localization structure was modified in:\n{path}\n\n"
            "Only text inside the translation regions may change:\n"
            "<<<\n"
            "editable translation\n"
            ">>>\n\n"
            "KEY, reference text, CONTEXT, GLOSSARY, structural markers, spacing "
            "outside translation blocks, and all other protected content "
            "must remain unchanged."
        )

    if base_text == current_text:
        raise ValidationError(
            f"{path} is marked as modified but contains no textual change."
        )

    return current_blocks


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Validate that a localization pull request changes only the "
            "contents of existing <<< >>> translation blocks."
        )
    )
    parser.add_argument(
        "--base",
        required=True,
        help="Base commit SHA of the pull request.",
    )
    args = parser.parse_args()

    try:
        changes = get_changed_files(args.base)

        if not changes:
            raise ValidationError(
                "No changed files were found between the PR and its base."
            )

        print("=" * 78)
        print("THE STATE OF NOWHERE - LOCALIZATION PR VALIDATION")
        print("=" * 78)
        print()
        print(f"Base commit: {args.base}")
        print(f"Changed files: {len(changes)}")
        print()

        validated_files = 0
        validated_blocks = 0

        # First reject any path/status that should never be part of a
        # community localization PR.
        for status, path in changes:
            validate_changed_path(status, path)

        # Then inspect the protected structure of every changed locale file.
        for status, path in changes:
            print(f"Checking: {path}")
            block_count = validate_file(args.base, path)
            validated_files += 1
            validated_blocks += block_count
            print(f"  OK - {block_count} translation blocks protected.")

        print()
        print("=" * 78)
        print("VALIDATION PASSED")
        print("=" * 78)
        print(f"Files validated: {validated_files}")
        print(f"Translation blocks checked: {validated_blocks}")
        print()
        print("Only translation contents were modified.")
        return 0

    except ValidationError as exc:
        print()
        print("=" * 78)
        print("VALIDATION FAILED")
        print("=" * 78)
        print(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
