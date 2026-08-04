# Dutch Biblical Studies add-on for NVDA
# Copyright 2026 Leonard de Ruijter <alderuijter@gmail.com>
# License: GNU General Public License version 2.0 or later

"""Unit test package bootstrap.

Importing this package prepares an environment in which NVDA's
``speechDictHandler.types`` can be imported without a running NVDA instance:

* The sibling NVDA source checkout (``../nvda/source``) is put on ``sys.path``.
* Light-weight stand-ins for NVDA runtime modules are installed into ``sys.modules``
  (see :mod:`tests._stubs`) before anything imports them.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_NVDA_SOURCE = (_REPO_ROOT.parent / "nvda" / "source").resolve()
_CANARY = _NVDA_SOURCE / "speechDictHandler" / "types.py"
if not _CANARY.is_file():
	raise RuntimeError(
		"The unit tests require an NVDA source checkout in a directory next to this repository. "
		+ f"Expected to find {_CANARY}. "
		+ "Clone https://github.com/nvaccess/nvda.git as a sibling of this repository.",
	)
sys.path.insert(0, str(_NVDA_SOURCE))

from . import _stubs  # noqa: E402

_stubs.install()
