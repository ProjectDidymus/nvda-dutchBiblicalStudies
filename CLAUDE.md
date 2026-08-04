# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an NVDA add-on providing resources for studying Biblical ancient languages (Koine Greek and Biblical Hebrew) for Dutch users. It includes:

- **Custom braille tables** in `addon/brailleTables/`: Liblouis `.utb`/`.uti` files for Greek and Hebrew
- **Speech (pronunciation) dictionaries** in `addon/speechDicts/`: `.dic` files transliterating Greek and Hebrew into Dutch-phonetic text
- **Speech symbol dictionaries** in `addon/locale/<lang>/`: `.dic` files mapping Unicode characters to spoken descriptions
- **Localization** in `addon/locale/nl/LC_MESSAGES/nvda.po`: Dutch translations of add-on strings

The NVDA source lives at `../nvda` — consult its `CLAUDE.md` for NVDA internals.

## Build Commands

Requires Python 3.13 (see `pyproject.toml` for pinned dependencies), gettext tools, and markdown:

```bash
scons              # Build the .nvda-addon package
scons pot          # Generate translation template (.pot file)
scons dev=true     # Development build (date-stamped version)
```

Pre-commit hooks run ruff linting on Python files and the `sconstruct`, pyright, and the unit tests.

## Unit Tests

```bash
uv run python -m unittest discover -s tests -t .
```

- Tests import NVDA's real `speechDictHandler.types` from a **sibling NVDA source checkout** (`../nvda`); `tests/__init__.py` fails fast with instructions when it is missing. Heavy NVDA runtime modules are replaced by stubs in `tests/_stubs.py`.
- Test fixtures are short inline verse quotations only — never add corpus files or paths (the BHS/NA28 texts are copyrighted).
- Hebrew test constants are written as explicit `\uXXXX` escapes; never replace them with literal Hebrew, as editors and normalizers can silently reorder combining marks.

## Key Files

- **`buildVars.py`**: Central configuration — add-on metadata, braille table registration (`brailleTables` dict), and speech dictionary registration (`symbolDictionaries` dict). Both dicts drive manifest generation.
- **`sconstruct`**: SCons build script — generates `manifest.ini` from `manifest.ini.tpl`, compiles `.po` to `.mo`, packages the addon.
- **`manifest.ini.tpl`** / **`manifest-translated.ini.tpl`**: Manifest templates populated from `buildVars.py`.

## Speech (Pronunciation) Dictionary Format

Files at `addon/speechDicts/<name>.dic` are tab-separated, loaded by NVDA's `speechDictHandler`:

```
<pattern>	<replacement>	<caseSensitive>	<type>
```

- `type`: 0 = ANYWHERE (escaped literal), 1 = REGEXP (stdlib `re`), 2 = WORD, 3 = PART_OF_WORD, 4 = START_OF_WORD. Types 2-4 use the `regex` package, where combining marks count as word characters.
- Entries apply **sequentially in file order**; each entry rewrites the output of all previous entries, so section order is load-bearing.
- START_OF_WORD requires a following word character, so it can never match a complete standalone word — pair it with a WORD (type 2) twin.
- Replacement backreferences (`\1`) only work in REGEXP entries.
- One malformed line silently disables the **whole** dictionary at runtime (add-on dicts load with `raiseOnError=True`); the parse test guards this.
- Dictionaries are global (not language-scoped) and run before symbol processing and before Unicode normalization. Patterns must match the source text as-is: BHS Hebrew stores marks in canonical order, i.e. the vowel sits between a consonant and its dagesh or shin/sin dot.
- Register dictionaries in `buildVars.py` under `speechDictionaries`.

## Symbol Dictionary Format

Files at `addon/locale/<lang>/symbols-<name>.dic` are tab-separated:

```
symbols:
<character>	<spoken description>	<level>	<preserve>
```

- `level`: when NVDA speaks the symbol — `none`, `some`, `most`, `all`, `char`
- `preserve`: whether to send the character to the synth — `norep` (don't repeat), `always`, `never`
- The `symbols:` header line is required.
- Dictionaries must be registered in `buildVars.py` under `symbolDictionaries` with a `displayName`.

Example entry (Greek): `ά	Alpha Acutus	most	norep`
Example entry (Hebrew): `ּ	Dagesh	most	norep`

## Braille Table Registration

Tables in `addon/brailleTables/` must be registered in `buildVars.py` under `brailleTables`:

```python
brailleTables = {
    "filename.utb": {
        "displayName": _("Human readable name"),
        "contracted": True,   # or False
        # optionally: "output": True/False, "input": True/False
    },
}
```

## Code Style

- Python uses tabs for indentation, max line length 110 (enforced by ruff, configured in `pyproject.toml`)
- Translatable strings in `buildVars.py` use the local `_()` stub (not real gettext)
