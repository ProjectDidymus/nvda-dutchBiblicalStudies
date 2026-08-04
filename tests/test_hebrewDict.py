# Dutch Biblical Studies add-on for NVDA
# Copyright 2026 Leonard de Ruijter <alderuijter@gmail.com>
# License: GNU General Public License version 2.0 or later

"""Behavioral tests for ``addon/speechDicts/hebrew.dic``.

Verse excerpts are short quotations from the BHS text, embedded inline
(no corpus dependency). All Hebrew constants are written as explicit
``\\uXXXX`` escapes because the combining marks are stored in Unicode
canonical order (vowel between consonant and dagesh/shin dot, cantillation
last); an editor or normalizer must never silently reorder them.
"""

from __future__ import annotations

import functools
import unittest

from speechDictHandler.types import SpeechDict  # bootstrap runs via tests/__init__ import

from ._util import loadSpeechDict, subStrict

# --- Genesis 1:1, word by word, with real cantillation (tipcha, munach, merkha, meteg) ---
# בְּרֵאשִׁ֖ית — bet+sheva+dagesh (canonical order), shin+hiriq+shin dot+tipcha
BERESHIT = "\u05d1\u05b0\u05bc\u05e8\u05b5\u05d0\u05e9\u05b4\u05c1\u0596\u05d9\u05ea"
# בָּרָ֣א — bet+qamats+dagesh, munach
BARA = "\u05d1\u05b8\u05bc\u05e8\u05b8\u05a3\u05d0"
# אֱלֹהִ֑ים — atnach (U+0591) between hiriq and yod
ELOHIM_ATNACH = "\u05d0\u05b1\u05dc\u05b9\u05d4\u05b4\u0591\u05d9\u05dd"
# אֵ֥ת — merkha
ET = "\u05d0\u05b5\u05a5\u05ea"
# הַשָּׁמַ֖יִם — shin+qamats+dagesh+shin dot, tipcha
HASHAMAYIM = "\u05d4\u05b7\u05e9\u05b8\u05bc\u05c1\u05de\u05b7\u0596\u05d9\u05b4\u05dd"
# וְאֵ֥ת — merkha
VEET = "\u05d5\u05b0\u05d0\u05b5\u05a5\u05ea"
# הָאָֽרֶץ׃ — meteg, sof pasuq
HAARETS = "\u05d4\u05b8\u05d0\u05b8\u05bd\u05e8\u05b6\u05e5\u05c3"
GEN_1_1 = " ".join((BERESHIT, BARA, ELOHIM_ATNACH, ET, HASHAMAYIM, VEET, HAARETS))

# --- Targeted phenomena ---
# אֱלֹהִ֔ים — zaqef qatan instead of atnach
ELOHIM_ZAQEF = "\u05d0\u05b1\u05dc\u05b9\u05d4\u05b4\u0594\u05d9\u05dd"
# יִשְׂרָאֵל — sin dot separated from shin by the sheva (canonical order)
YISRAEL = "\u05d9\u05b4\u05e9\u05b0\u05c2\u05e8\u05b8\u05d0\u05b5\u05dc"
# שַׁבָּת — dagesh forte in bet after a full vowel
SHABBAT = "\u05e9\u05b7\u05c1\u05d1\u05b8\u05bc\u05ea"
# הַמֶּלֶךְ — dagesh forte in mem; word-final sheva under kaf sofit
HAMMELECH = "\u05d4\u05b7\u05de\u05b6\u05bc\u05dc\u05b6\u05da\u05b0"
# אַתָּה — dagesh forte in tav
ATTAH = "\u05d0\u05b7\u05ea\u05b8\u05bc\u05d4"
# וַיִּקַּח — dagesh forte in qof directly after the dagesh of the yod
VAYIQQACH = "\u05d5\u05b7\u05d9\u05b4\u05bc\u05e7\u05b7\u05bc\u05d7"
# Elohim with a combining grapheme joiner / zero width joiner next to the
# atnach, as produced by sources that use joiners to control mark ordering
ELOHIM_CGJ = "\u05d0\u05b1\u05dc\u05b9\u05d4\u05b4\u034f\u0591\u05d9\u05dd"
ELOHIM_ZWJ = "\u05d0\u05b1\u05dc\u05b9\u05d4\u05b4\u200d\u0591\u05d9\u05dd"
# רוּחַ — furtive patach under word-final het
RUACH = "\u05e8\u05d5\u05bc\u05d7\u05b7"
# \u05de\u05b4\u05d6\u05b0\u05d1\u05b5\u05bc\u05d7\u05b7 \u2014 furtive patach after tsere; silent sheva; lene bet with tsere and dagesh
MIZBEACH = "\u05de\u05b4\u05d6\u05b0\u05d1\u05b5\u05bc\u05d7\u05b7"
# גָּבֹהַּ — mapiq he with furtive patach
GAVOAH = "\u05d2\u05b8\u05bc\u05d1\u05b9\u05d4\u05b7\u05bc"
# לֶךְ־לְךָ — word-final sheva before maqaf
LECH_LECHA = "\u05dc\u05b6\u05da\u05b0\u05be\u05dc\u05b0\u05da\u05b8"
# אֵלֶיךָ — silent yod after segol
ELECHA = "\u05d0\u05b5\u05dc\u05b6\u05d9\u05da\u05b8"
# אֵלָיו — word-final qamats-yod-vav suffix
ELAV = "\u05d0\u05b5\u05dc\u05b8\u05d9\u05d5"

HEBREW_SAMPLES = (
	GEN_1_1,
	ELOHIM_ZAQEF,
	ELOHIM_CGJ,
	ELOHIM_ZWJ,
	YISRAEL,
	SHABBAT,
	HAMMELECH,
	ATTAH,
	VAYIQQACH,
	RUACH,
	MIZBEACH,
	GAVOAH,
	LECH_LECHA,
	ELECHA,
	ELAV,
)

DUTCH = "Dit is gewone tekst; met leestekens, en 3-4 blijft ook staan."


def hebrewCodepoints(text: str) -> list[str]:
	return [f"U+{ord(c):04X}" for c in text if "\u0590" <= c <= "\u05ff"]


@functools.cache
def _dictionary() -> SpeechDict:
	return loadSpeechDict("hebrew")


class HebrewDictTests(unittest.TestCase):
	@property
	def dictionary(self) -> SpeechDict:
		return _dictionary()

	def test_genesis_1_1(self) -> None:
		"""Full verse: canonical shin/dagesh order, cantillation stripping, atnach, sof pasuq.

		Vowel policy, judged by Dutch orthography as a Dutch synth reads it:
		hiriq is always "ie"; the e-vowels split three ways — "e" is vocal sheva
		(Dutch unstressed e is schwa), "ê" is segol and hataf segol, "ee" is tsere.
		The mater rules exist to silence the yod, not to change the vowel.
		"""
		self.assertEqual(
			subStrict(self.dictionary, GEN_1_1),
			"beree'shiet baaraa' 'êlohiem; 'eet hashaamajiem we'eet haa'aarêts.",
		)

	def test_sin_in_canonical_order(self) -> None:
		"""Sin must be spoken "s" although the sin dot follows the sheva in the stream."""
		self.assertEqual(subStrict(self.dictionary, YISRAEL), "jiesraa'eel")

	def test_bkp_forte_gemination(self) -> None:
		self.assertEqual(subStrict(self.dictionary, SHABBAT), "shabbaat")

	def test_nonbkp_forte_gemination(self) -> None:
		self.assertEqual(subStrict(self.dictionary, HAMMELECH), "hammêlêch")

	def test_tav_forte_gemination(self) -> None:
		self.assertEqual(subStrict(self.dictionary, ATTAH), "'attaah")

	def test_forte_after_dagesh_cluster(self) -> None:
		"""Gemination also fires when the previous letter carries a vowelless dagesh."""
		self.assertEqual(subStrict(self.dictionary, VAYIQQACH), "wajiekkach")

	def test_furtive_patach(self) -> None:
		self.assertEqual(subStrict(self.dictionary, RUACH), "roeach")

	def test_furtive_patach_after_tsere(self) -> None:
		self.assertEqual(subStrict(self.dictionary, MIZBEACH), "miezbeeach")

	def test_mapiq_he_furtive_patach(self) -> None:
		self.assertEqual(subStrict(self.dictionary, GAVOAH), "gaavoah")

	def test_sheva_before_maqaf(self) -> None:
		"""Word-final sheva before maqaf is silent; sheva after maqaf is vocal."""
		self.assertEqual(subStrict(self.dictionary, LECH_LECHA), "lêch-lechaa")

	def test_atnach_relocation(self) -> None:
		"""Atnach pause punctuation lands after the word, not inside it."""
		self.assertEqual(subStrict(self.dictionary, ELOHIM_ATNACH), "'êlohiem;")

	def test_zaqef_relocation(self) -> None:
		self.assertEqual(subStrict(self.dictionary, ELOHIM_ZAQEF), "'êlohiem,")

	def test_invisible_joiners_around_accents(self) -> None:
		"""Joiners that sources insert to control mark ordering must not break the word."""
		self.assertEqual(subStrict(self.dictionary, ELOHIM_CGJ), "'êlohiem;")
		self.assertEqual(subStrict(self.dictionary, ELOHIM_ZWJ), "'êlohiem;")

	def test_joiners_outside_hebrew_untouched(self) -> None:
		"""The dictionary is global: emoji ZWJ sequences and Latin joiners must survive."""
		family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
		self.assertEqual(subStrict(self.dictionary, family), family)
		self.assertEqual(subStrict(self.dictionary, "a\u200bb"), "a\u200bb")

	def test_segol_yod_suffix(self) -> None:
		self.assertEqual(subStrict(self.dictionary, ELECHA), "'eelêchaa")

	def test_qamats_yod_vav_suffix(self) -> None:
		self.assertEqual(subStrict(self.dictionary, ELAV), "'eelaaw")

	def test_rare_marks_stripped(self) -> None:
		"""Puncta extraordinaria, nun hafukha, paseq and bidi marks must not reach the synth."""
		sample = "\u05d0\u05c4 \u05d1\u05c5 \u05c6 \u05c0 \u200e\u200f"
		result = subStrict(self.dictionary, sample)
		for codepoint in ("\u05c0", "\u05c4", "\u05c5", "\u05c6", "\u200e", "\u200f"):
			self.assertNotIn(codepoint, result)

	def test_dutch_text_unchanged(self) -> None:
		"""Speech dictionaries are global; ordinary Dutch must pass through untouched."""
		self.assertEqual(subStrict(self.dictionary, DUTCH), DUTCH)

	def test_no_hebrew_leakage(self) -> None:
		"""Transliteration must be total: no Hebrew codepoints may reach the synthesizer."""
		for sample in HEBREW_SAMPLES:
			with self.subTest(sample=sample[:20]):
				self.assertEqual(hebrewCodepoints(subStrict(self.dictionary, sample)), [])


if __name__ == "__main__":
	_ = unittest.main()
