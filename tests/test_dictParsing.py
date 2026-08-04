# Dutch Biblical Studies add-on for NVDA
# Copyright 2026 Leonard de Ruijter <alderuijter@gmail.com>
# License: GNU General Public License version 2.0 or later

"""Parse-level tests for all shipped speech dictionaries.

NVDA loads add-on dictionaries with ``raiseOnError=True``: a single malformed
line silently disables the entire dictionary at runtime. These tests make that
failure mode a hard test failure instead.
"""

from __future__ import annotations

import unittest

from speechDictHandler.types import EntryType, SpeechDict  # bootstrap runs via tests/__init__ import

from ._util import SPEECH_DICTS_DIR

#: The entry types the shipped dictionaries are expected to restrict themselves to.
EXPECTED_ENTRY_TYPES = frozenset(
	{
		EntryType.ANYWHERE,
		EntryType.REGEXP,
		EntryType.WORD,
		EntryType.PART_OF_WORD,
		EntryType.START_OF_WORD,
	},
)


class SpeechDictParsingTests(unittest.TestCase):
	def test_allDictsLoadStrict(self) -> None:
		paths = sorted(SPEECH_DICTS_DIR.glob("*.dic"))
		self.assertTrue(paths, f"No dictionaries found in {SPEECH_DICTS_DIR}")
		for path in paths:
			with self.subTest(dictionary=path.name):
				dictionary = SpeechDict()
				dictionary.load(str(path), raiseOnError=True)
				self.assertGreater(len(dictionary), 0)

	def test_entryTypesAreExpected(self) -> None:
		for path in sorted(SPEECH_DICTS_DIR.glob("*.dic")):
			dictionary = SpeechDict()
			dictionary.load(str(path), raiseOnError=True)
			for entry in dictionary:
				with self.subTest(dictionary=path.name, pattern=entry.pattern):
					self.assertIn(entry.type, EXPECTED_ENTRY_TYPES)


if __name__ == "__main__":
	_ = unittest.main()
