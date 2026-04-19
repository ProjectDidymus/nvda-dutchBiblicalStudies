# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an NVDA add-on providing resources for studying Biblical ancient languages (Koine Greek and Biblical Hebrew) for Dutch users. It includes:

- **Custom braille tables** in `addon/brailleTables/`: Liblouis `.utb`/`.uti` files for Greek and Hebrew
- **Speech symbol dictionaries** in `addon/locale/<lang>/`: `.dic` files mapping Unicode characters to spoken descriptions
- **Localization** in `addon/locale/nl/LC_MESSAGES/nvda.po`: Dutch translations of add-on strings

The NVDA source lives at `../nvda` — consult its `CLAUDE.md` for NVDA internals.

## Build Commands

Requires Python 3.11, SCons 4.5.2+, gettext tools, and markdown:

```bash
scons              # Build the .nvda-addon package
scons pot          # Generate translation template (.pot file)
scons dev=true     # Development build (date-stamped version)
```

Pre-commit hooks run ruff linting on Python files and the `sconstruct`.

## Key Files

- **`buildVars.py`**: Central configuration — add-on metadata, braille table registration (`brailleTables` dict), and speech dictionary registration (`symbolDictionaries` dict). Both dicts drive manifest generation.
- **`sconstruct`**: SCons build script — generates `manifest.ini` from `manifest.ini.tpl`, compiles `.po` to `.mo`, packages the addon.
- **`manifest.ini.tpl`** / **`manifest-translated.ini.tpl`**: Manifest templates populated from `buildVars.py`.

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
