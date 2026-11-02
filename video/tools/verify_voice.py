"""Transcribes a rendered film locally (faster-whisper) and compares it with narration.json word by word, so a voice
line that says the wrong thing is caught without anyone listening. Needs `pip install faster-whisper` (any venv).
Usage: verify_voice.py <video.mp4> [model]"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

HERE = Path(__file__).resolve().parents[1]
NUMBERS = {"eight hundred": "800", "forty-two": "42", "forty two": "42", "ten thousand": "10000", "10,000": "10000"}


def words(text):
    text = text.lower()
    for spoken, digits in NUMBERS.items():
        text = text.replace(spoken, digits)
    return re.findall(r"[a-z0-9']+", text.replace("-", " "))


def samples(path):
    """16 kHz mono float samples, decoded by ffmpeg (faster-whisper's own decoder breaks on some PyAV versions)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


model = WhisperModel(sys.argv[2] if len(sys.argv) > 2 else "small.en", device="cpu", compute_type="int8")
segments, _ = model.transcribe(samples(sys.argv[1]), language="en", vad_filter=True)
heard = " ".join(s.text for s in segments)
expected = " ".join(line["text"] for line in json.loads((HERE / "narration.json").read_text(encoding="utf-8")))
a, b = words(expected), words(heard)
matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
print(f"expected {len(a)} words, heard {len(b)}, match {matcher.ratio():.1%}")
for op, i1, i2, j1, j2 in matcher.get_opcodes():
    if op != "equal":
        print(f"  {op:8} script: {' '.join(a[i1:i2])!r:45} heard: {' '.join(b[j1:j2])!r}")
