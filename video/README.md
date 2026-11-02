# Demo film

The 2-minute demo film for the hackathon, made with [HyperFrames](https://hyperframes.heygen.com) (HTML rendered to
video). It follows `docs/demo-video-script.md`.

- **Every product shot is a real screen recording** of the public demo, made with Playwright and Chrome's screencast
  (`tools/record/`). One shot is a real live search for eygentic.com (2 November, $0.50 of model calls); the others
  are the read-only eygentic.com example and the "I don't have a website" popup, which is never submitted.
- **Voice, music and sound effects are made with AI** (ElevenLabs: the voice is "Andre Rene", model `eleven_v3`). The
  end card says so.
- `build.py` writes `index.html` and `compositions/s-*.html` from `narration.json` and the recordings, timing every
  scene to the voice. Captions come from ElevenLabs' word timings (`assets/voice/*.json`).

## Make it again

```sh
# 1. Recordings (from this folder; PW_ROOT is the repository root, which has Playwright)
PW_ROOT=.. node tools/record/shot_example.cjs <out>      # free: the read-only example
PW_ROOT=.. node tools/record/shot_nowebsite.cjs <out>    # free: the popup, never submitted
PW_ROOT=.. node tools/record/shot_live.cjs <out>         # starts ONE real search (about $0.50)
pwsh tools/record/assemble.ps1 -Dir <out>/live -Out assets/screens/live.mp4   # and example, nowebsite

# 2. Voice, effects and music (ElevenLabs credits; ELEVENLABS_API_KEY or ELEVENLABS_ENV=<path to .env>)
python tools/el_tts.py lines narration.json GogJbMCDT0Viv4cU3N4s assets/voice
python tools/el_sfx.py assets/sfx && python tools/el_sfx.py assets/music music
python tools/normalize.py assets/voice voice && python tools/normalize.py assets/sfx peak && python tools/normalize.py assets/music music

# 3. Build, check, look, render
python build.py
npx hyperframes check
npx hyperframes snapshot --at 5,30,60,90,118
npx hyperframes render -o renders/gtm-shortlist-demo.mp4
```

To try another voice, `python tools/el_tts.py samples assets/voice/samples` reads one line on four voices; pass the
chosen voice id to step 2 and rebuild.
