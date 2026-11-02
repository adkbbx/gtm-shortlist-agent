"""ElevenLabs sound effects and the music bed. Never prints the key.
Usage: el_sfx.py <outdir>            -> the effects kit
       el_sfx.py <outdir> music      -> music.mp3, one continuous bed for the whole film
       el_sfx.py <outdir> name,name  -> only those effects"""
import os
import sys
from pathlib import Path

import httpx
from dotenv import dotenv_values

# The key comes from the environment, or from the .env file named by ELEVENLABS_ENV.
KEY = os.environ.get("ELEVENLABS_API_KEY") or dotenv_values(os.environ["ELEVENLABS_ENV"])["ELEVENLABS_API_KEY"]
QUIET = "clean studio recording, no background noise, no music"
SFX = {
    "swoosh-a": (f"Soft airy swoosh for a premium product video transition, smooth and subtle, no low rumble, {QUIET}", 0.9),
    "swoosh-b": (f"Gentle short air whoosh passing by, light and silky, minimal tech product video, {QUIET}", 0.8),
    "click": (f"One single soft trackpad click, crisp and quiet, close microphone, {QUIET}", 0.5),
    "keys": (f"Light quiet typing on a modern laptop keyboard, a few soft keystrokes, {QUIET}", 2.0),
    "tick": (f"One very short soft glassy UI tick, subtle and gentle, minimal interface sound, {QUIET}", 0.5),
    "swell": (f"Soft warm airy swell rising gently and resolving, elegant cinematic transition, {QUIET}", 2.5),
    "settle": (f"Soft low warm thud with a short airy tail, subtle cinematic emphasis, {QUIET}", 1.2),
}
MUSIC = ("Warm, optimistic modern instrumental for a startup product demo video, 104 BPM. Clean electric piano chords, "
         "soft plucked synths, light airy pads, subtle tight drums with a gentle shaker, warm round bass. Focused and "
         "understated, premium tech feel like a Linear or Apple product video. Steady energy the whole way with no "
         "drops, breaks or stops, a gentle lift in the last thirty seconds, and a clean resolved ending. No vocals.")


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    arg = sys.argv[2] if len(sys.argv) > 2 else ""
    with httpx.Client(timeout=600) as client:
        if arg == "music":
            r = client.post("https://api.elevenlabs.io/v1/music", params={"output_format": "mp3_44100_192"},
                            headers={"xi-api-key": KEY},
                            json={"prompt": MUSIC, "music_length_ms": 160000, "force_instrumental": True})
            if not r.is_success:
                raise SystemExit(f"music: status {r.status_code} {r.text[:300]}")
            (out / "music.mp3").write_bytes(r.content)
            print("music ok", len(r.content))
            return
        only = set(arg.split(",")) if arg else None
        for name, (prompt, seconds) in SFX.items():
            if only and name not in only:
                continue
            r = client.post("https://api.elevenlabs.io/v1/sound-generation", params={"output_format": "mp3_44100_192"},
                            headers={"xi-api-key": KEY},
                            json={"text": prompt, "duration_seconds": seconds, "prompt_influence": 0.7})
            if not r.is_success:
                raise SystemExit(f"{name}: status {r.status_code} {r.text[:300]}")
            (out / f"{name}.mp3").write_bytes(r.content)
            print(name, "ok")


main()

