# The State of Nowhere — Community Localization

This repository contains the community-editable localization files for **The State of Nowhere**.

The files are organized by language and by game content so contributors can work on specific areas without having to search through one large translation file.

## Languages

- Spanish (es)
- English (en)
- Portuguese (pt)
- French (fr)
- German (de)
- Italian (it)
- Polish (pl)
- Turkish (tr)
- Romanian (ro)
- Russian (ru)
- Ukrainian (uk)
- Korean (ko)
- Japanese (ja)
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)

## File structure

Each localization entry is presented in a human-readable structured block:

```text
# [KEY]
# INTERNAL_KEY#1

# [ENGLISH]
# English reference text

# [CONTEXT]
# Context explaining where or how the line is used

# [GLOSSARY]
# ID: TERM_ID
# English: Canonical English term
# Target language: Canonical localized term

# [TRANSLATION]
<<<
Editable translation
>>>
```

### KEY

The internal identifier of the game line. It is reference information and must not be changed.

### ENGLISH

The English version of the line. It is provided as the main translation reference and must not be changed.

### CONTEXT

Additional information explaining the meaning, speaker, situation, interface usage, or other relevant details for the line. It must not be changed.

### GLOSSARY

When a line uses controlled terminology, this section shows the associated glossary term or terms.

Each glossary item includes:

- its internal glossary ID;
- the canonical English term;
- the canonical term for the current language.

This information is provided so contributors do not need to search through separate glossary files.

### TRANSLATION

The text between `<<<` and `>>>` is the translation for the current language.

**This is the only part of a localization entry contributors should edit.**

See [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.
