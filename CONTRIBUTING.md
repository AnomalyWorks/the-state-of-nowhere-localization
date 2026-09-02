# Contributing

Thank you for helping improve the localization of **The State of Nowhere**.

There are two ways to contribute translation improvements:

* Submit a **Pull Request** by editing the localization files directly.
* Submit a **Translation Suggestion** issue if you prefer not to edit the repository yourself.

Both methods are welcome.

## Localization entries

Localization files contain structured entries with reference information and one editable translation region.

Only text inside the following region may be edited:

```text id="k73d8f"
# [TRANSLATION]
<<<
This text may be edited.
>>>
```

Do not modify the `<<<` or `>>>` markers themselves.

## What you may edit

Only the translation text between `<<<` and `>>>`.

You may correct or improve translations for accuracy, grammar, spelling, naturalness, consistency, tone, or other localization issues.

## What you should not edit

Do not modify:

* `[KEY]`
* `[ENGLISH]`
* `[CONTEXT]`
* `[GLOSSARY]`
* glossary IDs
* canonical glossary terms
* structural markers
* file names
* folder organization

Those sections are maintained as reference and metadata for the localization system.

If you notice a problem in protected information such as the English reference, context, glossary, key, or repository structure, please report it through an issue instead of modifying it directly.

## English reference

`[ENGLISH]` contains the English version of the game line and should be used as the primary translation reference.

## Context

`[CONTEXT]` explains information that may not be obvious from the English text alone, such as who is speaking, what is happening, where a UI label appears, or what a line refers to.

Always take the provided context into account when evaluating or modifying a translation.

## Glossary

When `[GLOSSARY]` is present, use the canonical localized term shown for the current language.

Example:

```text id="q9kj3v"
# [GLOSSARY]
# ID: MALIGNISM
# English: Malignism
# Russian: Малигнизм
```

The glossary information is included directly with each relevant line so contributors do not have to consult separate reference files.

## Contributing through a Pull Request

If you are comfortable using GitHub, you can edit the relevant localization files and submit a pull request.

Keep pull requests focused on translation improvements and modify only the contents of `[TRANSLATION]` blocks.

Do not add, delete, rename, or move localization files.

Repository validation automatically checks pull requests to ensure that protected metadata and structural content have not been modified.

If validation fails, restore the protected content and keep only the intended translation changes.

## Contributing through a Translation Suggestion

If you do not want to edit the repository directly, you can open a **Translation Suggestion** issue.

Use the provided issue form and include the requested information, such as:

* language;
* localization key;
* current translation;
* suggested translation;
* reason or explanation, when useful.

You do not need to create a fork, edit files, or submit a pull request when using this method.

If the suggestion is accepted, the repository maintainer can incorporate the change into the localization files.

## Reporting problems with reference information

The information outside `[TRANSLATION]` blocks is protected and must not be modified directly through pull requests. However, feedback about this information is welcome.

If you notice a problem with the reference information, please open a **Localization Reference Issue**.

This includes cases such as:

* a `[CONTEXT]` section that is missing important information;
* context that is unclear, incomplete, misleading, or could be improved;
* a glossary term that you believe is incorrect or unnatural in a particular language;
* a glossary term that should be added to a line;
* an `[ENGLISH]` reference that appears to contain an error or does not accurately represent the intended meaning;
* any other problem with protected localization information that could affect translation quality.

Please explain the problem and, when possible, suggest how you think it could be improved.

Do not modify protected reference information directly in a pull request. If the proposed change is accepted, the repository maintainer will update the corresponding reference data.

## Contribution terms

By submitting a pull request, translation suggestion, or localization reference report to this repository, you confirm that you have the right to submit the contributed content.

You grant the developer of **The State of Nowhere** permission to use, reproduce, modify, adapt, integrate, distribute, and commercially exploit your contribution as part of the game and its related materials.

This permission allows accepted contributions to be incorporated into current or future versions of **The State of Nowhere**, including commercially distributed versions.

Submitting a contribution does not grant you ownership or other rights over **The State of Nowhere**, its source material, characters, names, text, assets, trademarks, or other game content.

By submitting a pull request, translation suggestion, or localization reference report, you agree to these contribution terms.

## Contributor credits

Contributors whose accepted pull requests, translation suggestions, or localization reference reports result in meaningful localization improvements may be credited in the localization credits of **The State of Nowhere**.

By default, your GitHub username may be used for attribution. You may provide another preferred nickname instead or request not to be credited.

Minor, automated, spam, or purely technical contributions may be excluded from the localization credits.

Credits acknowledge localization contributions and do not imply ownership of the game or its intellectual property.

Thank you for helping make **The State of Nowhere** accessible to more players.


