# Dutch Biblical Studies add-on for NVDA
# Copyright 2026 Leonard de Ruijter <alderuijter@gmail.com>
# License: GNU General Public License version 2.0 or later

"""Cross-dictionary tests.

NVDA applies every enabled dictionary sequentially over the same text, in
manifest order (greek before hebrew), so each dictionary must leave the
other's input and output alone.
"""

from __future__ import annotations

import unittest

from ._util import loadSpeechDict, subStrict
from .test_greekDict import DUTCH, JOHN_1_1, greekCodepoints
from .test_hebrewDict import GEN_1_1, hebrewCodepoints

JOHN_1_1_SPOKEN = "en archèi èn ho lógos, kai ho lógos èn pros ton teón, kai teos èn ho lógos."
GEN_1_1_SPOKEN = "bere'shiet baaraa' 'elohiem; 'et hashaamajiem we'et haa'aarets."


class MixedTextTests(unittest.TestCase):
	def test_bothDictsSequential(self) -> None:
		mixed = f"{DUTCH} {JOHN_1_1} {GEN_1_1}"
		result = subStrict(loadSpeechDict("greek"), mixed)
		result = subStrict(loadSpeechDict("hebrew"), result)
		self.assertEqual(result, f"{DUTCH} {JOHN_1_1_SPOKEN} {GEN_1_1_SPOKEN}")
		self.assertEqual(greekCodepoints(result), [])
		self.assertEqual(hebrewCodepoints(result), [])


if __name__ == "__main__":
	_ = unittest.main()
