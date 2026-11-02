"""ElevenLabs narration with word timings. Never prints the key.
Usage: el_tts.py samples <outdir>            -> one line on several voices
       el_tts.py lines <narration.json> <voice_id> <outdir> [model]  -> every line: <id>.mp3 + <id>.json (word timings)
"""
import base64
import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import dotenv_values

# The key comes from the environment, or from the .env file named by ELEVENLABS_ENV.
KEY = os.environ.get("ELEVENLABS_API_KEY") or dotenv_values(os.environ["ELEVENLABS_ENV"])["ELEVENLABS_API_KEY"]
SAMPLE = ("I'd started a rough prototype before the hackathon. Everything you'll see here, I built this week on Muse "
          "Spark. One input. My website.")
VOICES = {"andre": "GogJbMCDT0Viv4cU3N4s", "liam": "TX3LPaxmHKxFdv7VOQHJ", "jessica": "cgSgspJ2msm6clMCkdW9",
          "chris": "iP95p4xoKVk53GoZ742B"}


def speak(client, voice, text, model, out: Path, context=None):
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}}
    if model != "eleven_v3" and context:
        body.update(context)
    r = client.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps",
                    params={"output_format": "mp3_44100_192"}, headers={"xi-api-key": KEY}, json=body)
    if not r.is_success:
        raise SystemExit(f"{out.name}: status {r.status_code} {r.text[:300]}")
    data = r.json()
    out.with_suffix(".mp3").write_bytes(base64.b64decode(data["audio_base64"]))
    a = data.get("alignment") or data.get("normalized_alignment")
    words, cur, start = [], "", None
    for ch, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append({"text": cur, "start": start, "end": prev_end})
            cur, start = "", None
            continue
        if start is None:
            start = s
        cur += ch
        prev_end = e
    if cur:
        words.append({"text": cur, "start": start, "end": prev_end})
    out.with_suffix(".json").write_text(json.dumps({"text": text, "words": words}, indent=1), encoding="utf-8")
    print(out.name, "ok", f"{words[-1]['end']:.2f}s")


def main():
    with httpx.Client(timeout=120) as client:
        if sys.argv[1] == "samples":
            out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
            for name, voice in VOICES.items():
                speak(client, voice, SAMPLE, "eleven_v3", out / f"sample-{name}")
        else:
            lines = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
            voice, out = sys.argv[3], Path(sys.argv[4]); out.mkdir(parents=True, exist_ok=True)
            model = sys.argv[5] if len(sys.argv) > 5 else "eleven_v3"
            only = set(sys.argv[6].split(",")) if len(sys.argv) > 6 else None
            for i, line in enumerate(lines):
                if only and line["id"] not in only:
                    continue
                context = {"previous_text": lines[i - 1]["text"] if i else "",
                           "next_text": lines[i + 1]["text"] if i + 1 < len(lines) else ""}
                speak(client, voice, line.get("say", line["text"]), model, out / line["id"], context)


main()


