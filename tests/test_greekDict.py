# Dutch Biblical Studies add-on for NVDA
# Copyright 2026 Leonard de Ruijter <alderuijter@gmail.com>
# License: GNU General Public License version 2.0 or later

"""Behavioral tests for ``addon/speechDicts/greek.dic``.

Verse excerpts are short quotations from the NA28 text, embedded inline
(no corpus dependency). The Greek is precomposed (NFC), matching the
dictionary's patterns.
"""

from __future__ import annotations

import functools
import unittest

from speechDictHandler.types import SpeechDict  # bootstrap runs via tests/__init__ import

from ._util import loadSpeechDict, subStrict

JOHN_1_1 = "Ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν, καὶ θεὸς ἦν ὁ λόγος."
# Ano teleia is U+00B7, the question mark is an ASCII semicolon, as in the NA28 text.
JOHN_1_38B = "λέγει αὐτοῖς· τί ζητεῖτε;"
COR_13_4 = "Ἡ ἀγάπη μακροθυμεῖ, χρηστεύεται ἡ ἀγάπη, οὐ ζηλοῖ, [ἡ ἀγάπη] οὐ περπερεύεται,"
GREEK_SAMPLES = (JOHN_1_1, JOHN_1_38B, COR_13_4)

DUTCH = "Dit is gewone tekst; met puntkomma, en 3·4 blijft ook staan."


def greekCodepoints(text: str) -> list[str]:
	return [c for c in text if "Ͱ" <= c <= "Ͽ" or "ἀ" <= c <= "῿"]


@functools.cache
def _dictionary() -> SpeechDict:
	return loadSpeechDict("greek")


class GreekDictTests(unittest.TestCase):
	@property
	def dictionary(self) -> SpeechDict:
		return _dictionary()

	def test_john_1_1(self) -> None:
		"""Standalone words (three times the article ὁ) and uppercase Ἐν via case folding."""
		self.assertEqual(
			subStrict(self.dictionary, JOHN_1_1),
			"en archèi èn ho lógos, kai ho lógos èn pros ton teón, kai teos èn ho lógos.",
		)

	def test_john_1_38_punctuation(self) -> None:
		"""Ano teleia and the Greek question mark (ASCII ;) in Greek context."""
		self.assertEqual(
			subStrict(self.dictionary, JOHN_1_38B),
			"légei autois; tí zèteite?",
		)

	def test_1cor_13_4_standalone_words(self) -> None:
		"""Standalone Ἡ/ἡ/οὐ; NA28 editorial brackets pass through."""
		self.assertEqual(
			subStrict(self.dictionary, COR_13_4),
			"hè agápè makrotumei, chrèstéuetai hè agápè, oe zèloi, [hè agápè] oe perperéuetai,",
		)

	def test_unambiguous_punctuation_codepoints(self) -> None:
		"""U+037E (Greek question mark) and U+0387 (Greek ano teleia) need no context."""
		self.assertEqual(subStrict(self.dictionary, "; ·"), "? ;")

	def test_dutch_text_unchanged(self) -> None:
		"""Speech dictionaries are global; ordinary Dutch must pass through untouched."""
		self.assertEqual(subStrict(self.dictionary, DUTCH), DUTCH)

	def test_no_greek_leakage(self) -> None:
		"""Transliteration must be total: no Greek codepoints may reach the synthesizer."""
		for sample in GREEK_SAMPLES:
			with self.subTest(sample=sample[:30]):
				self.assertEqual(greekCodepoints(subStrict(self.dictionary, sample)), [])


if __name__ == "__main__":
	_ = unittest.main()
