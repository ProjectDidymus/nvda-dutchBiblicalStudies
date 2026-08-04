# Dutch Biblical Studies add-on for NVDA
# Copyright 2026 Leonard de Ruijter <alderuijter@gmail.com>
# License: GNU General Public License version 2.0 or later

"""Light-weight stand-ins for NVDA runtime modules.

Only leaf modules are stubbed; ``speechDictHandler.types`` and its relative import
``speechDictHandler.dictFormatUpgrade`` are executed for real from the sibling NVDA
source checkout. A stub ``speechDictHandler`` package whose ``__path__`` points at
the real package directory lets those submodules import without ever running
``speechDictHandler/__init__.py``, which pulls in the synthesizer runtime.
"""

from __future__ import annotations

import gettext
import importlib
import sys
import types
from pathlib import Path
from types import SimpleNamespace

_NVDA_SOURCE = Path(__file__).resolve().parent.parent.parent / "nvda" / "source"


class FakeLogger:
	"""Stands in for ``logHandler.log``; swallows all messages."""

	def debug(self, *args: object, **kwargs: object) -> None:
		pass

	def info(self, *args: object, **kwargs: object) -> None:
		pass

	def debugWarning(self, *args: object, **kwargs: object) -> None:
		pass

	def warning(self, *args: object, **kwargs: object) -> None:
		pass

	def error(self, *args: object, **kwargs: object) -> None:
		pass

	def exception(self, *args: object, **kwargs: object) -> None:
		pass


def _module(name: str) -> types.ModuleType:
	mod = types.ModuleType(name)
	sys.modules[name] = mod
	return mod


def _shouldWriteToDisk() -> bool:
	return False


def _filterFileName(name: str) -> str:
	return name


def install() -> None:
	"""Install all stub modules. Idempotent; must run before importing ``speechDictHandler.types``."""
	if "speechDictHandler" in sys.modules:
		return

	# Binds `_` into builtins, which modules imported from the NVDA checkout expect.
	gettext.NullTranslations().install()

	logHandler = _module("logHandler")
	setattr(logHandler, "log", FakeLogger())

	config = _module("config")
	setattr(config, "conf", {"featureFlag": {"speechDictsUseModernRegex": False}})

	NVDAState = _module("NVDAState")
	setattr(NVDAState, "shouldWriteToDisk", _shouldWriteToDisk)
	setattr(NVDAState, "WritePaths", SimpleNamespace())

	api = _module("api")
	setattr(api, "filterFileName", _filterFileName)

	_ = _module("globalVars")

	speechDictHandler = _module("speechDictHandler")
	speechDictHandler.__path__ = [str(_NVDA_SOURCE / "speechDictHandler")]
	setattr(speechDictHandler, "types", importlib.import_module("speechDictHandler.types"))
