# Contributing

Thank you for helping improve the localization of **The State of Nowhere**.

## What you may edit

Localization files contain structured entries with reference information and one editable translation region.

Only edit text inside:

```text
# [TRANSLATION]
<<<
This text may be edited.
>>>
```

Do not modify the `<<<` or `>>>` markers themselves.

## What you should not edit

Do not modify:

- `[KEY]`
- `[ENGLISH]`
- `[CONTEXT]`
- `[GLOSSARY]`
- glossary IDs
- canonical glossary terms
- structural markers
- file names
- folder organization

Those sections are maintained as reference and metadata for the localization system.

## English reference

`[ENGLISH]` contains the English version of the game line and should be used as the primary translation reference.

## Context

`[CONTEXT]` explains information that may not be obvious from the English text alone, such as who is speaking, what is happening, where a UI label appears, or what a line refers to.

## Glossary

When `[GLOSSARY]` is present, use the canonical localized term shown for the current language.

Example:

```text
# [GLOSSARY]
# ID: MALIGNISM
# English: Malignism
# Russian: Малигнизм
```

The glossary information is included directly with each relevant line so contributors do not have to consult separate reference files.

## Pull requests

Keep changes focused on translation improvements.

Repository validation may reject a pull request if protected metadata or structural content has been modified. If that happens, restore the protected content and keep only the intended translation changes.
