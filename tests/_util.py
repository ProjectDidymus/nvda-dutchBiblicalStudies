# Dutch Biblical Studies add-on for NVDA
# Copyright 2026 Leonard de Ruijter <alderuijter@gmail.com>
# License: GNU General Public License version 2.0 or later

"""Helpers shared by the speech dictionary tests."""

from __future__ import annotations

from pathlib import Path

from speechDictHandler.types import SpeechDict  # bootstrap runs via tests/__init__ import

SPEECH_DICTS_DIR = Path(__file__).resolve().parent.parent / "addon" / "speechDicts"


def loadSpeechDict(name: str) -> SpeechDict:
	"""Load an add-on dictionary exactly like production does (one bad line raises)."""
	dictionary = SpeechDict()
	dictionary.load(str(SPEECH_DICTS_DIR / f"{name}.dic"), raiseOnError=True)
	return dictionary


def subStrict(dictionary: SpeechDict, text: str) -> str:
	"""``SpeechDict.sub`` silently deletes entries whose regex raises at match time;
	fail loudly instead."""
	entryCountBefore = len(dictionary)
	result = dictionary.sub(text)
	if len(dictionary) != entryCountBefore:
		raise AssertionError("SpeechDict.sub dropped invalid entries")
	return result
