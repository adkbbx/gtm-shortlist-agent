"""Writes the demo film's HyperFrames files (index.html and compositions/*.html) from the narration and the
recordings, timing every scene to the voice. Re-run after changing a line, a gap or a shot:

    python build.py && npx hyperframes check

Look: the product always plays inside one browser window on a calm ground, the same size and place in every shot. A
step label sits above the window, plain captions below it, and a soft spotlight dims everything but the part being
talked about. Text cards appear only where there is no product to show (the problem, the rule, the close, the end).
"""
import json
import wave
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
W, H = 1920, 1080
INK, MUTED, PAPER, DEEP, LINE = "#1b1b1b", "#6b665f", "#f3f1ed", "#b4501c", "rgba(27,27,27,.10)"
FONT = "".join(f"@font-face{{font-family:'Schibsted Grotesk';font-weight:{w};src:url('assets/fonts/schibsted-{w}.woff2') "
               f"format('woff2')}}" for w in (500, 600, 800))
LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><path fill="#e0692c" fill-rule="evenodd" d="M18 4H46Q48 4 48 6V20Q60 '
        '25 60 38V58Q60 60 58 60H48Q46 60 46 58V36Q46 32 42 32H22Q18 32 18 36V58Q18 60 16 60H6Q4 60 4 58V38Q4 25 16 '
        '20V6Q16 4 18 4ZM24 12V20H30V12ZM36 12V20H42V12Z"/><path fill="#e0692c" d="M22 46L27 41L31 45L39 37L44 42L31 '
        '55Z"/></svg>')
URL = "eygentic.tech"

# The window: footage scaled into a 1472x828 viewport under a 40 px bar, centred, with room above for the step label
# and below for captions.
K = 1472 / 1920
VX, VY, VW, VH, BAR = 224, 96, 1472, 828, 40
WIN_TOP = VY - BAR

GAP = {"intro": 0.5, "problem": 0.55, "disclose": 0.7, "input": 0.45, "reads": 0.4, "rivals": 0.35, "signals": 0.35,
       "code": 0.35, "checker": 0.35, "out": 0.6, "thrive": 0.3, "quote": 0.3, "opener": 0.35, "email": 0.35, "turn": 0.5,
       "storable": 0.25, "rule": 0.6, "thrown": 0.6, "needs": 0.4, "nowebsite": 0.4, "cost": 0.4, "close": 0.6,
       "end": 1.3}
TAIL = 7.0  # the end card holds after the last word, long enough to read
CARD_LINES = {"problem", "disclose", "rule", "close", "end"}  # text cards say it on screen; no captions under them


def wav_seconds(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


lines = json.loads((HERE / "narration.json").read_text(encoding="utf-8"))
T, t = {}, 0.0
for line in lines:
    lid = line["id"]
    start = t + GAP[lid]
    words = json.loads((HERE / f"assets/voice/{lid}.json").read_text(encoding="utf-8"))["words"]
    T[lid] = {"start": round(start, 3), "dur": round(wav_seconds(HERE / f"assets/voice/{lid}.wav"), 3),
              "words": words, "text": line["text"]}
    t = start + words[-1]["end"]
TOTAL = round(t + TAIL, 2)


def at(lid, word=None):
    """Film time of a line's start, or of the first spoken word containing `word`."""
    if word is None:
        return T[lid]["start"]
    for w in T[lid]["words"]:
        if word.lower() in w["text"].lower():
            return round(T[lid]["start"] + w["start"], 3)
    raise KeyError(f"{word} not in {lid}")


def spot(x, y, w, h, word_line, word=None, until=None):
    """A soft spotlight on a footage rectangle (in 1920x1080 recording pixels)."""
    return {"x": x, "y": y, "w": w, "h": h, "at": at(word_line, word), "until": until}


# The full email and LinkedIn note, from a live search recorded for this shot (tools/record/shot_email.cjs).
EMAIL_RANGE, EMAIL_CAM = (22.0, 34.5), [(0, 1.05, 960, 540), (1, 1.18, 960, 520)]
EMAIL_SCENE = {"id": "s-email", "line": "email", "src": "draft", "m": EMAIL_RANGE, "cam": EMAIL_CAM,
               "label": "Draft outreach: an email and a LinkedIn note, checked by Muse Spark Open"}

# Footage scenes: src, media range, camera keys [(fraction, zoom, focus x, focus y)] in recording pixels, step label.
SCENES = [
    {"id": "s-intro", "line": "intro", "src": "live", "m": (3.1, 5.6), "cam": [(0, 1.0, 960, 540), (1, 1.08, 960, 460)]},
    {"id": "s-problem", "line": "problem", "card": "problem"},
    {"id": "s-disclose", "line": "disclose", "card": "disclose"},
    {"id": "s-input", "line": "input", "src": "live", "m": (8.25, 13.6), "enter": True, "cam": [(0, 1.0, 960, 540), (0.3, 1.45, 960, 730), (1, 1.45, 960, 730)],
     "label": "1  Your website. Nothing else.", "spot": [spot(566, 682, 790, 98, "input", "website")]},
    {"id": "s-reads", "line": "reads", "src": "live", "m": (13.8, 34.0), "cam": [(0, 1.0, 960, 540), (1, 1.15, 760, 640)],
     "label": "2  Reads your site  ·  Muse Spark 1.3"},
    {"id": "s-rivals", "line": "rivals", "src": "live", "m": (38.5, 50.5), "cam": [(0, 1.1, 700, 700), (1, 1.35, 520, 820)],
     "label": "3  Checks your competitors on their own homepages"},
    {"id": "s-signals", "line": "signals", "src": "live", "m": (95.0, 127.0), "cam": [(0, 1.0, 960, 540), (1, 1.12, 760, 560)],
     "label": "4  Finds companies with a need right now"},
    {"id": "s-code", "line": "code", "src": "example", "m": (30.4, 34.7), "cam": [(0, 1.45, 560, 960), (1, 1.55, 560, 980)],
     "label": "Checks which tools they already use", "spot": [spot(155, 935, 790, 120, "code", "site")]},
    {"id": "s-checker", "line": "checker", "src": "live", "m": (127.5, 150.0), "cam": [(0, 1.0, 960, 540), (0.25, 1.4, 1560, 520), (1, 1.45, 1560, 560)],
     "label": "5  A second model checks every quote  ·  Muse Spark Open on Baseten"},
    {"id": "s-out", "line": "out", "src": "example", "m": (3.2, 7.5), "cam": [(0, 1.06, 960, 380), (1, 1.0, 960, 540)],
     "label": "A finished search for eygentic.com"},
    {"id": "s-thrive", "line": "thrive", "src": "example", "m": (7.6, 11.4), "cam": [(0, 1.0, 960, 540), (1, 1.25, 700, 300)],
     "label": "Shortlisted"},
    {"id": "s-quote", "line": "quote", "src": "example", "m": (13.9, 18.6), "cam": [(0, 1.25, 960, 540), (0.3, 1.6, 960, 545), (1, 1.62, 960, 545)],
     "label": "The evidence: their open job post", "spot": [spot(650, 443, 620, 202, "quote", "hiring")],
     "mark": [spot(668, 464, 298, 32, "quote", "first")]},
    {"id": "s-opener", "line": "opener", "src": "example", "m": (19.9, 23.4), "cam": [(0, 1.25, 800, 420), (1, 1.45, 730, 420)],
     "label": "A first line, written from that quote and checked", "spot": [spot(167, 302, 1123, 201, "opener", "writes")]},
    EMAIL_SCENE,
    {"id": "s-turn", "line": "turn", "src": "example", "m": (23.4, 29.9), "cam": [(0, 1.0, 960, 540), (1, 1.1, 700, 320)],
     "label": "storable.com"},
    {"id": "s-storable", "line": "storable", "src": "example", "m": (29.9, 34.7), "cam": [(0, 1.1, 700, 380), (0.3, 1.45, 730, 430), (1, 1.47, 730, 430)],
     "label": "Rejected: too large for who I sell to", "spot": [spot(167, 380, 1123, 108, "storable", "about")]},
    {"id": "s-rule", "line": "rule", "card": "rule"},
    {"id": "s-thrown", "line": "thrown", "src": "example", "m": (41.3, 46.2), "cam": [(0, 1.2, 730, 360), (1, 1.32, 730, 360)],
     "label": "Across 17 searches, the checker threw out 120 of 354 quotes", "enter": True,
     "spot": [spot(167, 215, 1123, 277, "thrown", "thrown")]},
    {"id": "s-needs", "line": "needs", "src": "example", "m": (36.0, 41.0), "cam": [(0, 1.0, 960, 540), (1, 1.12, 700, 500)],
     "label": "Needs a look, with what's missing"},
    {"id": "s-nowebsite", "line": "nowebsite", "src": "nowebsite", "m": (5.4, 18.4), "cam": [(0, 1.0, 960, 540), (1, 1.15, 960, 560)],
     "label": "No website? Describe your business"},
    {"id": "s-cost", "line": "cost", "src": "example", "m": (47.95, 49.35), "cam": [(0, 1.0, 960, 540), (0.3, 1.5, 1420, 360), (1, 1.52, 1420, 360)],
     "label": "5 companies  ·  $0.42", "spot": [spot(1090, 312, 680, 84, "cost", "five")]},
    {"id": "s-close", "line": "close", "card": "close"},
    {"id": "s-end", "line": "end", "card": "end"},
]
for i, s in enumerate(SCENES):
    s["start"] = 0.0 if i == 0 else round(at(s["line"]) - 0.2, 3)
for i, s in enumerate(SCENES):
    s["end"] = SCENES[i + 1]["start"] if i + 1 < len(SCENES) else TOTAL
    s["dur"] = round(s["end"] - s["start"], 3)
MEDIA_LEN = {"live": 228.5, "example": 49.4, "nowebsite": 22.1, "draft": 37.8}


def cam_xy(zoom, fx, fy):
    """Viewport translate that puts a recording point at the centre, kept inside the footage."""
    x = min(0.0, max(VW - VW * zoom, VW / 2 - K * zoom * fx))
    y = min(0.0, max(VH - VH * zoom, VH / 2 - K * zoom * fy))
    return round(x, 1), round(y, 1)


BASE_CSS = f"""{FONT}
#root{{position:absolute;inset:0;overflow:hidden;font-family:'Schibsted Grotesk',sans-serif;color:{INK};
  background:radial-gradient(1400px 700px at 50% -10%,#fbf7f1 0%,{PAPER} 60%)}}"""

WINDOW_CSS = f"""
.win{{position:absolute;left:{VX}px;top:{WIN_TOP}px;width:{VW}px;height:{VH + BAR}px;border-radius:18px;overflow:hidden;
  background:#fff;border:1px solid {LINE};box-shadow:0 50px 110px -45px rgba(40,30,20,.45),0 8px 24px -12px rgba(40,30,20,.12)}}
.bar{{position:absolute;left:0;top:0;width:{VW}px;height:{BAR}px;background:#f7f6f3;border-bottom:1px solid {LINE};
  display:flex;align-items:center}}
.dots{{position:absolute;left:18px;top:14px;display:flex;gap:8px}}.dots i{{width:12px;height:12px;border-radius:50%;background:#dedad3;display:block}}
.url{{margin:0 auto;padding:4px 16px;border-radius:8px;background:#fff;border:1px solid {LINE};font-size:15px;font-weight:500;color:{MUTED}}}
.view{{position:absolute;left:0;top:{BAR}px;width:{VW}px;height:{VH}px;overflow:hidden;background:#f7f7f5}}
.cam{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:0 0}}
.cam video{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:contain}}
.mark{{position:absolute;border-radius:6px;background:rgba(240,150,70,.38);mix-blend-mode:multiply;transform-origin:0 50%;z-index:5}}
.spot{{position:absolute;border-radius:14px;box-shadow:0 0 0 3000px rgba(24,22,20,.42);z-index:4}}
.label{{position:absolute;left:{VX}px;top:12px;height:40px;display:flex;align-items:center;gap:14px;font-size:28px;
  font-weight:600;letter-spacing:-.015em;color:{INK};white-space:nowrap}}
.label b{{color:{DEEP};font-weight:800}}
.speed{{position:absolute;right:{W - VX - VW}px;top:12px;height:40px;display:flex;align-items:center;font-size:28px;font-weight:500;
  color:{MUTED};white-space:nowrap}}"""


def footage_scene(s):
    sid, src = s["id"], s["src"]
    m0, m1 = s["m"]
    rate = round((m1 - m0) / s["dur"], 4)
    assert m0 + rate * s["dur"] <= MEDIA_LEN[src] + 0.01, sid
    keys = s["cam"]
    x0, y0 = cam_xy(*keys[0][1:])
    js = [f'tl.set("#{sid}-cam",{{x:{x0},y:{y0},scale:{round(K * keys[0][1], 4)}}},0);']
    for (f0, z0, fx0, fy0), (f1, z1, fx1, fy1) in zip(keys, keys[1:]):
        xb, yb = cam_xy(z1, fx1, fy1)
        if (z0, fx0, fy0) == (z1, fx1, fy1):
            continue
        d = round((f1 - f0) * s["dur"], 3)
        ease = "power3.inOut" if d < 1.5 else "sine.inOut"
        js.append(f'tl.to("#{sid}-cam",{{x:{xb},y:{yb},scale:{round(K * z1, 4)},duration:{d},ease:"{ease}"}},{round(f0 * s["dur"], 3)});')
    if s.get("enter"):
        js.append(f'tl.fromTo("#{sid}-win",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.7,ease:"expo.out"}},0);')
    spots = []
    for k, sp in enumerate(s.get("spot", [])):
        t0 = round(max(0.3, sp["at"] - s["start"] - 0.15), 3)
        t1 = round((sp["until"] or s["end"]) - s["start"], 3)
        pad = 10
        spots.append(f'<div id="{sid}-sp{k}" class="clip spotclip" data-start="{t0}" data-duration="{round(t1 - t0, 3)}" '
                     f'data-layout-allow-overflow data-layout-ignore><div class="spot" style="left:{sp["x"] - pad}px;'
                     f'top:{sp["y"] - pad}px;width:{sp["w"] + 2 * pad}px;height:{sp["h"] + 2 * pad}px"></div></div>')
        js.append(f'tl.fromTo("#{sid}-sp{k} .spot",{{opacity:0}},{{opacity:1,duration:.6,ease:"power2.inOut"}},{t0});')
    for k, mk in enumerate(s.get("mark", [])):
        t0 = round(max(0.3, mk["at"] - s["start"] - 0.1), 3)
        t1 = round((mk["until"] or s["end"]) - s["start"], 3)
        spots.append(f'<div id="{sid}-mk{k}" class="clip spotclip" data-start="{t0}" data-duration="{round(t1 - t0, 3)}" '
                     f'data-layout-ignore><div class="mark" style="left:{mk["x"]}px;top:{mk["y"]}px;width:{mk["w"]}px;'
                     f'height:{mk["h"]}px"></div></div>')
        js.append(f'tl.fromTo("#{sid}-mk{k} .mark",{{scaleX:0}},{{scaleX:1,duration:.7,ease:"power2.inOut"}},{t0});')
    label = ""
    if s.get("label"):
        text = escape(s["label"])
        if text[:1].isdigit() and text[1:3] == "  ":
            text = f"<b>{text[0]}</b>{text[3:]}"
        label = f'<div id="{sid}-label" class="label">{text}</div>'
        js.append(f'tl.fromTo("#{sid}-label",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.35,ease:"power3.out"}},0.12);')
    speed = ""
    if rate >= 1.4:
        speed = f'<div id="{sid}-speed" class="speed">Sped up {round(rate)}×</div>'
        js.append(f'tl.fromTo("#{sid}-speed",{{opacity:0}},{{opacity:1,duration:.35,ease:"power2.out"}},0.2);')
    return f"""<template>
<style>{BASE_CSS}{WINDOW_CSS}
.spotclip{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}</style>
<div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
  {label}{speed}
  <div id="{sid}-win" class="win">
    <div class="bar" data-layout-ignore><div class="dots"><i></i><i></i><i></i></div><div class="url">{URL}</div></div>
    <div class="view"><div id="{sid}-cam" class="cam">
      <video id="{sid}-video" class="clip" src="assets/screens/{src}.mp4" data-start="0" data-duration="{s['dur']}"
        data-media-start="{m0}" data-playback-rate="{rate}" muted playsinline></video>
      {''.join(spots)}
    </div></div>
  </div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""


CARD_CSS = f"""
.stack{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:44px;text-align:center}}
.eyebrow{{font-size:30px;font-weight:600;color:{DEEP};letter-spacing:-.01em}}
.big{{font-size:84px;font-weight:800;letter-spacing:-.04em;line-height:1.08}}
.soft{{color:{MUTED}}}
.row{{display:flex;flex-direction:column;align-items:center;gap:14px}}"""


def card_scene(s):
    sid, kind = s["id"], s["card"]
    rel = lambda film_t: round(max(0.1, film_t - s["start"]), 3)
    js = []

    def reveal(sel, t0, blur=8, y=0):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y},filter:"blur({blur}px)"}},{{opacity:1,y:0,filter:"blur(0px)",'
                  f'duration:.5,ease:"expo.out"}},{t0});')

    if kind == "problem":
        body = f"""<div class="stack" data-hold>
    <div id="{sid}-q" class="big" style="font-size:72px" data-hold>Who do I reach out to this week?</div>
    <div style="display:flex;gap:120px;margin-top:40px">
      <div id="{sid}-a" class="row"><div class="eyebrow">Lead lists</div><div class="big soft" style="font-size:52px">Thousands of names.<br>No reason to call.</div></div>
      <div id="{sid}-b" class="row"><div class="eyebrow">Chatbots</div><div class="big soft" style="font-size:52px">Plenty of reasons.<br>No way to check them.</div></div>
    </div></div>"""
        reveal(f"#{sid}-q", rel(at("problem", "who")), y=16)
        reveal(f"#{sid}-a", rel(at("problem", "Lead")), y=24)
        reveal(f"#{sid}-b", rel(at("problem", "chatbot")), y=24)
    elif kind == "disclose":
        body = f"""<div class="stack" data-hold>
    <div style="display:flex;gap:140px">
      <div id="{sid}-a" class="row"><div class="eyebrow">Before 26 October</div><div class="big soft" style="font-size:52px">A rough prototype.</div></div>
      <div id="{sid}-b" class="row"><div class="eyebrow">Built this week</div><div class="big" style="font-size:52px">Everything in this video,<br>running on Meta's Muse Spark models.</div></div>
    </div></div>"""
        reveal(f"#{sid}-a", rel(at("disclose")), y=24)
        reveal(f"#{sid}-b", rel(at("disclose", "Everything")), y=24)
    elif kind == "rule":
        body = f"""<div class="stack" data-hold>
    <div id="{sid}-a" class="big">The models collect and check the evidence.</div>
    <div id="{sid}-b" class="big" style="color:{DEEP}">Plain rules in code make the call.</div></div>"""
        reveal(f"#{sid}-a", rel(at("rule")), y=16)
        reveal(f"#{sid}-b", rel(at("rule", "Plain")), y=16)
    elif kind == "close":
        body = f"""<div class="stack" data-hold>
    <div id="{sid}-a" class="big">Who to email this week,</div>
    <div id="{sid}-b" class="big" style="color:{DEEP}">and what to say.</div></div>"""
        reveal(f"#{sid}-a", rel(at("close")), y=16)
        reveal(f"#{sid}-b", rel(at("close", "what")), y=16)
    else:
        body = f"""<div class="stack" style="gap:34px">
    <div id="{sid}-lock" style="display:flex;align-items:center;gap:30px" data-hold><div style="width:120px;height:120px">{LOGO}</div>
      <div class="big" style="font-size:120px">GTM Shortlist</div></div>
    <div id="{sid}-url" style="padding:18px 34px;border-radius:999px;background:{INK};color:#fff;font-size:34px;font-weight:600">{URL}</div>
    <div id="{sid}-credit" style="font-size:30px;font-weight:500;color:{INK};margin-top:24px">Built solo for the Meta Global AI Developer Hackathon  ·  Muse Spark 1.3  ·  Muse Spark Open on Baseten</div>
    <div id="{sid}-note" style="font-size:28px;font-weight:500;color:{MUTED};line-height:1.5">Quotes come from each company's public pages. Verdicts mean fit for my business, not a judgement of the company.<br>
      Voice, music and sound made with AI. Every product shot is a real recording.</div></div>"""
        reveal(f"#{sid}-lock", 0.15, y=20)
        reveal(f"#{sid}-url", 0.55, y=16)
        reveal(f"#{sid}-credit", 0.9, blur=4, y=10)
        reveal(f"#{sid}-note", 1.2, blur=4, y=10)
    return f"""<template>
<style>{BASE_CSS}{CARD_CSS}
.stack svg{{width:100%;height:100%;display:block}}</style>
<div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
  {body}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""


def caption_chunks():
    """Sentence pieces of up to twelve words, timed from the spoken words (the caption shows the written form)."""
    chunks = []
    for line in lines:
        lid = line["id"]
        if lid in CARD_LINES:
            continue
        shown, spoken = line["text"].split(), T[lid]["words"]
        piece = []
        for i, word in enumerate(shown):
            piece.append(i)
            if len(piece) >= 12 or word[-1] in ".,?:" or i == len(shown) - 1:
                a = round(piece[0] * len(spoken) / len(shown))
                b = min(len(spoken) - 1, round((piece[-1] + 1) * len(spoken) / len(shown)) - 1)
                chunks.append({"text": " ".join(shown[j] for j in piece),
                               "start": T[lid]["start"] + spoken[a]["start"], "end": T[lid]["start"] + spoken[b]["end"]})
                piece = []
    # Short pieces join the next one in the same sentence so captions don't flicker.
    merged = []
    for c in chunks:
        if merged and len(merged[-1]["text"].split()) < 4 and not merged[-1]["text"].endswith((".", "?")) \
                and len((merged[-1]["text"] + " " + c["text"]).split()) <= 11:
            merged[-1] = {"text": merged[-1]["text"] + " " + c["text"], "start": merged[-1]["start"], "end": c["end"]}
        else:
            merged.append(c)
    return merged


def captions_scene():
    out, js = [], []
    chunks = caption_chunks()
    for g, c in enumerate(chunks):
        nxt = chunks[g + 1]["start"] if g + 1 < len(chunks) else TOTAL
        start = max(0.1, c["start"] - 0.06)
        end = min(nxt - 0.03, c["end"] + 0.4)
        out.append(f'<div id="cap{g}" class="cap clip" data-start="{start:.3f}" data-duration="{end - start:.3f}">'
                   f'<span>{escape(c["text"])}</span></div>')
        js.append(f'tl.fromTo("#cap{g} span",{{opacity:0,y:8}},{{opacity:1,y:0,duration:.18,ease:"power2.out"}},{start:.3f});')
    return f"""<template>
<style>{FONT}
#root{{position:absolute;inset:0;pointer-events:none;font-family:'Schibsted Grotesk',sans-serif}}
.cap{{position:absolute;left:0;top:{VY + VH + 34}px;width:{W}px;text-align:center}}
.cap span{{display:inline-block;font-size:38px;font-weight:500;letter-spacing:-.01em;color:{INK};white-space:nowrap}}</style>
<div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
  {chr(10).join(out)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["captions"] = tl;
</script>
</template>
"""


# --- sound ------------------------------------------------------------------------------------------------------------
def media_to_film(scene_id, media_t):
    s = next(x for x in SCENES if x["id"] == scene_id)
    return round(s["start"] + (media_t - s["m"][0]) / ((s["m"][1] - s["m"][0]) / s["dur"]), 3)


def scene_start(sid):
    return next(s["start"] for s in SCENES if s["id"] == sid)


# Where each clip peaks after its start, measured with `npx hyperframes audio`; a clip is placed so its peak lands a
# frame after its picture.
PEAK = {"swoosh-a": 0.125, "swoosh-b": 0.333, "click": 0.158, "keys": 0.05, "tick": 0.159, "swell": 1.659}
SFX = [
    ("swoosh-a", scene_start("s-problem"), 0.35),
    ("swoosh-b", scene_start("s-disclose"), 0.3),
    ("keys", media_to_film("s-input", 8.35), 0.3),
    ("click", media_to_film("s-input", 13.05), 0.5),
    ("tick", at("input", "website"), 0.25),
    ("click", media_to_film("s-thrive", 8.6), 0.45),
    ("click", media_to_film("s-quote", 14.6), 0.45),
    ("tick", at("quote", "hiring") - 0.15, 0.22),
    ("tick", at("storable", "about") - 0.15, 0.22),
    ("swoosh-a", scene_start("s-rule"), 0.3),
    ("swoosh-b", scene_start("s-thrown"), 0.3),
    ("keys", media_to_film("s-nowebsite", 7.2), 0.25),
    ("tick", at("cost", "five") - 0.15, 0.22),
    ("swoosh-a", scene_start("s-close"), 0.3),
    ("swell", scene_start("s-end") + 0.2, 0.4),
]


def index_html():
    hosts, audio = [], []
    for s in SCENES:
        hosts.append(f'<div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" '
                     f'data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="{W}" data-height="{H}"></div>')
    hosts.append(f'<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" '
                 f'data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" '
                 f'data-width="{W}" data-height="{H}" style="z-index:50"></div>')
    for line in lines:
        lid = line["id"]
        audio.append(f'<audio id="vo-{lid}" class="clip" src="assets/voice/{lid}.wav" data-start="{T[lid]["start"]}" '
                     f'data-duration="{T[lid]["dur"]}" data-track-index="3" data-volume="1"></audio>')
    free = {4: 0.0, 6: 0.0, 7: 0.0}  # effect lanes and when each is next free, so effects never overlap on a lane
    for k, (name, picture, vol) in enumerate(SFX):
        start = round(max(0.0, picture + 0.033 - PEAK[name]), 3)
        length = round(wav_seconds(HERE / f"assets/sfx/{name}.wav"), 3)
        lane = next(lane for lane, until in free.items() if until <= start)
        free[lane] = start + length
        audio.append(f'<audio id="sfx-{k}-{name}" class="clip" src="assets/sfx/{name}.wav" data-start="{start}" '
                     f'data-duration="{length}" data-track-index="{lane}" data-volume="{vol}"></audio>')
    # One continuous bed: no cuts, faded in at the top and out under the end card.
    music_len = wav_seconds(HERE / "assets/music/music.wav")
    audio.append(f'<audio id="music" class="clip" src="assets/music/music.wav" data-start="0" '
                 f'data-duration="{min(TOTAL, music_len):.3f}" data-track-index="5" data-volume="0.32" '
                 f'data-fade-in="1.5" data-fade-out="4"></audio>')
    return f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>GTM Shortlist: demo film</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: {PAPER}; }}
      #root {{ width: 100%; height: 100%; position: relative; }}
    </style>
  </head>
  <body>
    <!-- Generated by build.py: edit there, or edit here and stop re-running it. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
      {chr(10).join('      ' + h for h in hosts).strip()}
      {chr(10).join('      ' + a for a in audio).strip()}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def main():
    comp = HERE / "compositions"
    comp.mkdir(exist_ok=True)
    for old in comp.glob("s-*.html"):
        old.unlink()
    for s in SCENES:
        html = card_scene(s) if "card" in s else footage_scene(s)
        (comp / f"{s['id']}.html").write_text(html, encoding="utf-8")
    (comp / "captions.html").write_text(captions_scene(), encoding="utf-8")
    (HERE / "index.html").write_text(index_html(), encoding="utf-8")
    footage = sum(s["dur"] for s in SCENES if "src" in s)
    print(f"total {TOTAL:.2f}s, real screen {footage:.1f}s ({footage / TOTAL:.0%}), {len(SCENES)} scenes")
    for s in SCENES:
        rate = f' x{(s["m"][1] - s["m"][0]) / s["dur"]:.2f}' if "m" in s else ""
        print(f'  {s["start"]:7.2f}  {s["dur"]:5.2f}s  {s["id"]}{rate}')


main()


