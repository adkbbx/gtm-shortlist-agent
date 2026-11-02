"""Peak-normalise audio files in place-safe copies: each *.mp3 in a folder -> <name>.wav at a target loudness with a
true-peak ceiling. Voice and music use loudnorm; short effects use a peak gain. Usage: normalize.py <dir> <mode>"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

FF = shutil.which("ffmpeg") or str(Path.home() / "AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe")


def peak_db(path):
    out = subprocess.run([FF, "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"max_volume: (-?[\d.]+) dB", out).group(1))


folder, mode = Path(sys.argv[1]), sys.argv[2]
for src in sorted(folder.glob("*.mp3")):
    dst = src.with_suffix(".wav")
    if mode == "peak":
        gain = -1.5 - peak_db(src)
        af = f"volume={gain:.2f}dB"
    else:
        target = "-16" if mode == "voice" else "-20"
        af = f"loudnorm=I={target}:TP=-1.5:LRA=11"
    subprocess.run([FF, "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", "48000", str(dst)], check=True)
    print(dst.name, "peak after", peak_db(dst))
