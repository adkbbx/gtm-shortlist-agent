"""ElevenLabs sound effects and a music bed. Never prints the key. Usage: el_sfx.py <outdir> [music]"""
import os
import sys
from pathlib import Path

import httpx
from dotenv import dotenv_values

# The key comes from the environment, or from the .env file named by ELEVENLABS_ENV.
KEY = os.environ.get("ELEVENLABS_API_KEY") or dotenv_values(os.environ["ELEVENLABS_ENV"])["ELEVENLABS_API_KEY"]
SFX = {
    "whoosh-a": ("Fast clean airy whoosh transition, short, modern UI video", 0.8),
    "whoosh-b": ("Quick swish whoosh pass by, bright and light, video transition", 0.7),
    "pop-a": ("Soft bubbly UI pop, short, clean", 0.5),
    "pop-b": ("Tiny bright click pop for a badge appearing, clean UI", 0.5),
    "click": ("Single soft mouse click, close mic, clean", 0.5),
    "keys": ("Soft laptop keyboard typing, quick light keystrokes, no room noise", 2.0),
    "stamp": ("Heavy rubber stamp slamming onto paper on a wooden desk, single hit", 0.8),
    "scratch": ("Short vinyl record scratch stop, DJ, single", 0.8),
    "thump": ("Single deep cinematic heartbeat thump, low, short", 1.0),
    "riser": ("Short bright riser building into a punchy impact hit, modern trailer", 2.0),
    "impact": ("Deep punchy bass hit impact, cinematic, short tail", 1.2),
    "register": ("Small cash register ka-ching, short, clean", 1.0),
}


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=300) as client:
        if len(sys.argv) > 2 and sys.argv[2] == "music":
            r = client.post("https://api.elevenlabs.io/v1/music", params={"output_format": "mp3_44100_192"},
                            headers={"xi-api-key": KEY},
                            json={"prompt": "Upbeat modern electronic instrumental for a tech product demo, 122 BPM, "
                                            "warm bright synth plucks, tight punchy drums, confident and optimistic, "
                                            "builds to a clear drop around 15 seconds then keeps a steady groove, "
                                            "clean ending, no vocals",
                                  "music_length_ms": 140000, "force_instrumental": True})
            if not r.is_success:
                raise SystemExit(f"music: status {r.status_code} {r.text[:300]}")
            (out / "music.mp3").write_bytes(r.content)
            print("music ok", len(r.content))
            return
        only = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None
        if only:
            SFX["stamp"] = ("Loud single rubber stamp hit, heavy thud on a desk, punchy, close", 1.0)
        for name, (prompt, seconds) in SFX.items():
            if only and name not in only:
                continue
            r = client.post("https://api.elevenlabs.io/v1/sound-generation", params={"output_format": "mp3_44100_192"},
                            headers={"xi-api-key": KEY},
                            json={"text": prompt, "duration_seconds": seconds, "prompt_influence": 0.6})
            if not r.is_success:
                raise SystemExit(f"{name}: status {r.status_code} {r.text[:300]}")
            (out / f"{name}.mp3").write_bytes(r.content)
            print(name, "ok")


main()

