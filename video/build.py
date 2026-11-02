"""Writes the demo film's HyperFrames files (index.html and compositions/s-*.html) from the narration and the
recordings, timing every scene to the voice. Re-run after changing a line, a gap or a shot:

    python build.py && npx hyperframes check

Real footage only for the product (assets/screens/*.mp4, recorded from the live demo); drawn scenes only where there is
no product to show (the hook, the rule, the close).
"""
import json
import math
import wave
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
W, H = 1920, 1080
INK, MUTED, PAPER, ORANGE, DEEP, GREY = "#1b1b1b", "#5c5853", "#f7f7f5", "#d5682f", "#b4501c", "#9c958c"
FONT = """@font-face{font-family:'Schibsted Grotesk';font-weight:500;src:url('assets/fonts/schibsted-500.woff2') format('woff2')}
@font-face{font-family:'Schibsted Grotesk';font-weight:800;src:url('assets/fonts/schibsted-800.woff2') format('woff2')}"""
LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><path fill="#e0692c" fill-rule="evenodd" d="M18 4H46Q48 4 48 6V20Q60 '
        '25 60 38V58Q60 60 58 60H48Q46 60 46 58V36Q46 32 42 32H22Q18 32 18 36V58Q18 60 16 60H6Q4 60 4 58V38Q4 25 16 '
        '20V6Q16 4 18 4ZM24 12V20H30V12ZM36 12V20H42V12Z"/><path fill="#e0692c" d="M22 46L27 41L31 45L39 37L44 42L31 '
        '55Z"/></svg>')
URL = "gtmshortlist--gtm-shortlist-agent-web.us-east.modal.run"

# Silence before each line (seconds). Longer gaps sit where the picture changes world or the music stops.
GAP = {"hook1": 0.35, "hook2": 0.3, "lists": 0.5, "disclose": 1.0, "input": 0.45, "reads": 0.45, "rivals": 0.35,
       "signals": 0.35, "code": 0.4, "checker": 0.35, "out": 0.55, "thrive": 0.35, "quote": 0.3, "opener": 0.35,
       "turn": 1.0, "storable": 0.35, "rule": 0.7, "thrown": 0.5, "needs": 0.4, "nowebsite": 0.4, "cost": 0.45,
       "close": 0.6, "end": 0.6}
TAIL = 4.2  # the end card holds after the last word
NO_CAPTION = {"hook1", "hook2", "rule", "close", "end"}  # the words are already on screen, large
KEYWORD = {"lists": "zero", "disclose": "week", "input": "website.", "reads": "need", "rivals": "proves",
           "signals": "signals,", "code": "code,", "checker": "second", "out": "finished", "thrive": "Shortlisted.",
           "quote": "first", "opener": "checker", "turn": "didn't.", "storable": "out.", "thrown": "third",
           "needs": "missing.", "nowebsite": "own", "cost": "forty-two", "end": "website."}


def wav_seconds(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


lines = json.loads((HERE / "narration.json").read_text(encoding="utf-8"))
T, t = {}, 0.0
for line in lines:
    lid = line["id"]
    start = t + GAP[lid]
    words = json.loads((HERE / f"assets/voice/{lid}.json").read_text(encoding="utf-8"))["words"]
    dur = wav_seconds(HERE / f"assets/voice/{lid}.wav")
    T[lid] = {"start": round(start, 3), "dur": round(dur, 3), "end": round(start + words[-1]["end"], 3), "words": words}
    t = start + words[-1]["end"]
TOTAL = round(t + TAIL, 2)


def at(lid, word=None):
    """Film time of a line's start, or of the first word containing `word`."""
    if word is None:
        return T[lid]["start"]
    for w in T[lid]["words"]:
        if word.lower() in w["text"].lower():
            return round(T[lid]["start"] + w["start"], 3)
    raise KeyError(f"{word} not in {lid}")


# --- scenes -----------------------------------------------------------------------------------------------------------
# Footage scenes: (id, first line, src, media from, media to, camera keys [(frac, scale, fx, fy)], overlays)
# Overlays: dicts with kind, at (film seconds), dur, text, x, y, and in_cam (moves with the footage).
LEAD = 0.18


def badge(text, x, y, t0, t1, tone="dark", in_cam=False):
    return {"kind": "badge", "text": text, "x": x, "y": y, "at": t0, "end": t1, "tone": tone, "in_cam": in_cam}


def mark(x, y, w, h, t0, t1, style="underline"):
    return {"kind": style, "x": x, "y": y, "w": w, "h": h, "at": t0, "end": t1, "in_cam": True}


SCENES = [
    {"id": "s-hero", "line": "hook1", "src": "live", "m": (3.1, 5.0), "cam": [(0, 1.0, 960, 420), (1, 1.16, 960, 400)]},
    {"id": "s-lists", "line": "lists", "graphic": "lists"},
    {"id": "s-disclose", "line": "disclose", "src": "live", "m": (5.0, 8.2), "cam": [(0, 1.05, 960, 520), (1, 1.0, 960, 540)],
     "over": [badge("Before 26 Oct: a rough prototype", 110, 100, at("disclose") + 0.2, None, "light"),
              badge("Built 26 Oct to 4 Nov 2026", 110, 168, at("disclose", "Everything"), None)]},
    {"id": "s-input", "line": "input", "src": "live", "m": (8.25, 13.6), "cam": [(0, 1.0, 960, 540), (0.25, 1.55, 960, 730), (1, 1.55, 960, 730)],
     "over": [badge("1 input", 1240, 610, at("input", "website"), None, "orange", True)]},
    {"id": "s-reads", "line": "reads", "src": "live", "m": (13.8, 34.0), "cam": [(0, 1.0, 960, 540), (1, 1.18, 760, 700)],
     "over": [badge("Muse Spark 1.3 · investigator", 700, 36, at("reads") + 0.15, None),
              badge("Live search · sped up", 1440, 100, at("reads") + 0.5, None, "light")]},
    {"id": "s-rivals", "line": "rivals", "src": "live", "m": (38.5, 50.5), "cam": [(0, 1.15, 700, 760), (1, 1.6, 500, 880)],
     "over": [badge("Live search · sped up", 1440, 100, at("rivals"), None, "light")]},
    {"id": "s-signals", "line": "signals", "src": "live", "m": (95.0, 127.0), "cam": [(0, 1.0, 960, 540), (1, 1.15, 760, 560)],
     "over": [badge("Lever", 1380, 330, at("signals", "Live"), None, "light"),
              badge("Greenhouse", 1450, 400, at("signals", "Live") + 0.12, None, "light"),
              badge("Ashby", 1380, 470, at("signals", "Live") + 0.24, None, "light"),
              badge("news", 1450, 540, at("signals", "news"), None, "light"),
              badge("Live search · sped up", 1440, 100, at("signals"), None, "light")]},
    {"id": "s-code", "line": "code", "src": "example", "m": (30.4, 34.7), "cam": [(0, 1.6, 560, 990), (1, 1.75, 560, 1000)],
     "over": [mark(390, 945, 128, 30, at("code", "homepage"), None, "box")]},
    {"id": "s-checker", "line": "checker", "src": "live", "m": (127.5, 150.0), "cam": [(0, 1.0, 960, 540), (0.3, 1.5, 1560, 520), (1, 1.55, 1560, 560)],
     "over": [badge("Muse Spark Open · checker", 700, 36, at("checker", "Muse"), None),
              badge("Live search · sped up", 1440, 100, at("checker"), None, "light")]},
    {"id": "s-out", "line": "out", "src": "example", "m": (3.2, 7.5), "cam": [(0, 1.08, 960, 360), (1, 1.0, 960, 540)],
     "over": [badge("Finished search for eygentic.com", 110, 100, at("out") + 0.2, None, "light")]},
    {"id": "s-thrive", "line": "thrive", "src": "example", "m": (7.6, 11.4), "cam": [(0, 1.0, 960, 540), (1, 1.3, 700, 300)]},
    {"id": "s-quote", "line": "quote", "src": "example", "m": (13.9, 18.6), "cam": [(0, 1.3, 960, 540), (0.3, 1.75, 950, 520), (1, 1.8, 950, 520)],
     "over": [mark(668, 462, 540, 34, at("quote", "as"), None, "sweep"),
              badge("open job post · read during the search", 1150, 120, at("quote") + 0.4, None, "light")]},
    {"id": "s-opener", "line": "opener", "src": "example", "m": (19.9, 25.0), "cam": [(0, 1.3, 800, 420), (1, 1.6, 720, 420)],
     "over": [badge("Checked by Muse Spark Open", 700, 426, at("opener", "checker"), None, "orange", True)]},
    {"id": "s-turn", "line": "turn", "src": "example", "m": (25.0, 29.9), "cam": [(0, 1.0, 960, 540), (1, 1.12, 700, 300)], "dim": True},
    {"id": "s-storable", "line": "storable", "src": "example", "m": (29.9, 34.7), "cam": [(0, 1.15, 700, 350), (0.25, 1.65, 600, 420), (1, 1.7, 600, 420)],
     "over": [{"kind": "note", "text": "Quotes come from each company's public pages. Verdicts mean fit for my "
                                       "business, not a judgement of the company.", "at": at("storable") - 0.1,
               "end": None, "x": 110, "y": 90, "in_cam": False},
              mark(186, 398, 794, 36, at("storable", "Proudly"), None, "sweep"),
              {"kind": "stamp", "text": "REJECTED", "at": at("storable", "out"), "end": None, "x": 960, "y": 560, "in_cam": False}]},
    {"id": "s-rule", "line": "rule", "graphic": "rule"},
    {"id": "s-thrown", "line": "thrown", "src": "example", "m": (41.3, 46.2), "cam": [(0, 1.25, 730, 350), (1, 1.45, 730, 350)],
     "over": [{"kind": "stat", "text": "120 of 354 quotes thrown out across 17 searches", "at": at("thrown", "Across"), "end": None,
               "x": 960, "y": 790, "in_cam": False}]},
    {"id": "s-needs", "line": "needs", "src": "example", "m": (36.0, 41.0), "cam": [(0, 1.0, 960, 540), (1, 1.15, 700, 500)]},
    {"id": "s-nowebsite", "line": "nowebsite", "src": "nowebsite", "m": (5.4, 18.4), "cam": [(0, 1.0, 960, 540), (1, 1.18, 960, 560)],
     "over": [badge("Typing sped up", 1440, 100, at("nowebsite"), None, "light")]},
    {"id": "s-cost", "line": "cost", "src": "example", "m": (47.95, 49.35), "cam": [(0, 1.0, 960, 540), (0.3, 1.7, 1440, 365), (1, 1.75, 1440, 365)],
     "over": [mark(1665, 345, 95, 44, at("cost", "forty-two"), None, "box")]},
    {"id": "s-close", "line": "close", "graphic": "close"},
    {"id": "s-end", "line": "end", "graphic": "end"},
]
for i, s in enumerate(SCENES):
    s["start"] = 0.0 if i == 0 else round(at(s["line"]) - LEAD, 3)
for i, s in enumerate(SCENES):
    s["end"] = SCENES[i + 1]["start"] if i + 1 < len(SCENES) else TOTAL
    s["dur"] = round(s["end"] - s["start"], 3)

MEDIA_LEN = {"live": 228.5, "example": 49.4, "nowebsite": 22.1}


def cam_xy(scale, fx, fy):
    x = min(0.0, max(W - W * scale, W / 2 - scale * fx))
    y = min(0.0, max(H - H * scale, H / 2 - scale * fy))
    return round(x, 1), round(y, 1)


def overlay_html(sid, k, o, s):
    t0 = round(o["at"] - s["start"], 3)
    t1 = round((o["end"] or s["end"]) - s["start"], 3)
    oid = f"{sid}-o{k}"
    dur = round(max(t1 - t0, 0.2), 3)
    common = f'id="{oid}" class="clip ov" data-start="{t0}" data-duration="{dur}"'
    if o["kind"] == "badge":
        tone = o["tone"]
        return (f'<div {common} style="left:{o["x"]}px;top:{o["y"]}px"><div class="badge {tone}"><i></i>'
                f'{escape(o["text"])}</div></div>'), t0, dur, "badge"
    if o["kind"] in ("underline", "sweep"):
        return (f'<div {common} style="left:{o["x"]}px;top:{o["y"]}px;width:{o["w"]}px;height:{o["h"]}px">'
                f'<div class="sweep"></div></div>'), t0, dur, "sweep"
    if o["kind"] == "box":
        return (f'<div {common} style="left:{o["x"] - 8}px;top:{o["y"] - 6}px;width:{o["w"] + 16}px;height:{o["h"] + 12}px">'
                f'<div class="ring"></div></div>'), t0, dur, "ring"
    if o["kind"] == "note":
        return (f'<div {common} style="left:{o["x"]}px;top:{o["y"]}px"><div class="note">{escape(o["text"])}</div></div>'),\
            t0, dur, "badge"
    if o["kind"] == "stamp":
        return (f'<div {common} style="left:0;top:0;width:{W}px;height:{H}px"><div class="stamp">{o["text"]}</div></div>'),\
            t0, dur, "stamp"
    if o["kind"] == "stat":
        return (f'<div {common} style="left:0;top:{o["y"] - 60}px;width:{W}px;height:120px"><div class="stat">'
                f'{escape(o["text"])}</div></div>'), t0, dur, "stat"
    raise ValueError(o["kind"])


SCENE_CSS = f"""{FONT}
#root{{position:absolute;inset:0;overflow:hidden;background:{PAPER};font-family:'Schibsted Grotesk',sans-serif}}
.cam{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:0 0}}
.cam video{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:contain}}
.ov{{position:absolute;z-index:5}}
.badge{{display:inline-flex;align-items:center;gap:14px;padding:16px 26px;border-radius:999px;font-weight:800;
  font-size:34px;letter-spacing:-.02em;white-space:nowrap;box-shadow:0 18px 40px -18px rgba(27,27,27,.45)}}
.badge i{{width:12px;height:12px;border-radius:50%;background:{ORANGE};display:block}}
.badge.dark{{background:{INK};color:#fff}}
.badge.light{{background:rgba(255,255,255,.96);color:{INK};border:1.5px solid rgba(27,27,27,.12)}}
.badge.orange{{background:{DEEP};color:#fff}}.badge.orange i{{background:#fff}}
.sweep{{width:100%;height:100%;background:{ORANGE};border-radius:4px;transform-origin:0 50%}}
.ring{{width:100%;height:100%;border:5px solid {ORANGE};border-radius:12px}}
.stamp{{position:absolute;left:50%;top:50%;margin-left:-430px;margin-top:-120px;width:860px;height:240px;display:flex;
  align-items:center;justify-content:center;border:14px solid #c62f25;border-radius:28px;color:#c62f25;font-weight:800;
  font-size:170px;letter-spacing:.04em;background:rgba(255,255,255,.55)}}
.stat{{margin:0 auto;width:max-content;padding:22px 40px;border-radius:24px;background:{INK};color:#fff;font-weight:800;
  font-size:48px;letter-spacing:-.025em}}
.dim{{position:absolute;inset:0;background:{INK};z-index:3}}
.note{{max-width:900px;padding:16px 24px;border-radius:18px;background:rgba(255,255,255,.96);color:{MUTED};font-weight:500;
  font-size:28px;line-height:1.4;border:1.5px solid rgba(27,27,27,.12)}}"""


def footage_scene(s):
    sid, src = s["id"], s["src"]
    m0, m1 = s["m"]
    rate = round((m1 - m0) / s["dur"], 4)
    assert m0 + rate * s["dur"] <= MEDIA_LEN[src] + 0.01, sid
    inside, outside, anims = [], [], []
    for k, o in enumerate(s.get("over", [])):
        html, t0, dur, kind = overlay_html(sid, k, o, s)
        (inside if o.get("in_cam") else outside).append(html)
        anims.append((f"#{sid}-o{k} > *", t0, dur, kind))
    keys = s["cam"]
    x0, y0 = cam_xy(keys[0][1], keys[0][2], keys[0][3])
    js = [f'tl.set("#{sid}-cam",{{x:{x0},y:{y0},scale:{keys[0][1]}}},0);']
    # A new shot arrives a touch large and settles, so cuts read as moves rather than slides.
    js.append(f'tl.fromTo("#{sid}-settle",{{scale:1.035,transformOrigin:"50% 50%"}},{{scale:1,transformOrigin:"50% 50%",duration:0.45,ease:"expo.out"}},0);')
    for (f0, s0, fx0, fy0), (f1, s1, fx1, fy1) in zip(keys, keys[1:]):
        xa, ya = cam_xy(s0, fx0, fy0)
        xb, yb = cam_xy(s1, fx1, fy1)
        d = round((f1 - f0) * s["dur"], 3)
        ease = "power3.inOut" if d < 1.2 else "sine.inOut"
        if (xa, ya, s0) == (xb, yb, s1):
            continue  # a hold: the camera stays where the last move left it
        js.append(f'tl.to("#{sid}-cam",{{x:{xb},y:{yb},scale:{s1},duration:{d},ease:"{ease}"}},{round(f0 * s["dur"], 3)});')
    for sel, t0, dur, kind in anims:
        if kind == "badge":
            js.append(f'tl.fromTo("{sel}",{{opacity:0,y:18,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"expo.out"}},{t0});')
        elif kind == "sweep":
            js.append(f'tl.fromTo("{sel}",{{scaleX:0,opacity:0.3}},{{scaleX:1,opacity:0.3,duration:1.4,ease:"power1.inOut"}},{t0});')
        elif kind == "ring":
            js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:0.4,ease:"expo.out"}},{t0});')
        elif kind == "stamp":
            js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:2.4,rotation:-14}},{{opacity:1,scale:1,rotation:-8,duration:0.22,ease:"power4.in"}},{t0});')
        elif kind == "stat":
            js.append(f'tl.fromTo("{sel}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.45,ease:"expo.out"}},{t0});')
    dim = ""
    if s.get("dim"):
        dim = f'<div id="{sid}-dim" class="dim clip" data-start="0" data-duration="{s["dur"]}"></div>'
        js.append(f'tl.fromTo("#{sid}-dim",{{opacity:0}},{{opacity:0.28,duration:1.2,ease:"sine.inOut"}},0.2);')
    return f"""<template>
<style>{SCENE_CSS}</style>
<div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
  <div id="{sid}-settle" class="cam"><div id="{sid}-cam" class="cam">
    <video id="{sid}-video" class="clip" src="assets/screens/{src}.mp4" data-start="0" data-duration="{s['dur']}"
      data-media-start="{m0}" data-playback-rate="{rate}" muted playsinline></video>
    {''.join(inside)}
  </div></div>
  {dim}
  {''.join(outside)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""


def rng(seed):
    state = seed
    def nxt():
        nonlocal state
        state = (state * 1103515245 + 12345) % 2 ** 31
        return state / 2 ** 31
    return nxt


def filter_paths(n=26, seed=7):
    """The film's motif: many grey lines flow in from the left into one point; three orange lines leave right."""
    r = rng(seed)
    cx, cy = 980, 540
    grey = []
    for i in range(n):
        y0 = 60 + (H - 120) * i / (n - 1) + (r() - 0.5) * 30
        c1 = (300 + r() * 200, y0 + (cy - y0) * 0.15)
        c2 = (cx - 260 - r() * 120, cy + (y0 - cy) * 0.12)
        grey.append(f"M -20 {y0:.0f} C {c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {cx} {cy}")
    orange = [f"M {cx} {cy} C {cx + 260} {cy} {cx + 420} {cy + dy * 0.6:.0f} {W + 20} {cy + dy:.0f}" for dy in (-170, 0, 170)]
    return grey, orange


def motif_svg(sid, opacity=1.0):
    grey, orange = filter_paths()
    gp = "".join(f'<path class="{sid}-g" d="{d}" pathLength="1"/>' for d in grey)
    op = "".join(f'<path class="{sid}-o" d="{d}" pathLength="1"/>' for d in orange)
    return (f'<svg class="motif" viewBox="0 0 {W} {H}" style="opacity:{opacity}"><g fill="none" stroke="{GREY}" '
            f'stroke-width="2" stroke-opacity=".55">{gp}</g><g fill="none" stroke="{ORANGE}" stroke-width="4">{op}</g>'
            f'<circle id="{sid}-core" cx="980" cy="540" r="9" fill="{ORANGE}"/></svg>')


GRAPHIC_CSS = f"""{FONT}
#root{{position:absolute;inset:0;overflow:hidden;background:{PAPER};font-family:'Schibsted Grotesk',sans-serif;color:{INK}}}
.glow{{position:absolute;left:460px;top:-380px;width:1000px;height:900px;border-radius:50%;
  background:radial-gradient(closest-side,rgba(213,104,47,.16),rgba(213,104,47,0))}}
.motif{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}
.motif path{{stroke-dasharray:1;stroke-dashoffset:1}}
.big{{position:absolute;left:0;width:{W}px;text-align:center;font-weight:800;letter-spacing:-.045em;line-height:1}}
.word{{display:inline-block}}"""


def words_html(sid, text, cls=""):
    return " ".join(f'<span class="word {cls}" id="{sid}-w{i}">{escape(w)}</span>' for i, w in enumerate(text.split()))


def graphic_scene(s):
    sid, kind, d = s["id"], s["graphic"], s["dur"]
    rel = lambda film_t: round(film_t - s["start"], 3)
    js = []
    if kind == "lists":
        r = rng(3)
        tiles = []
        for row in range(14):
            for col in range(11):
                shade = 0.06 + r() * 0.1
                tiles.append(f'<div class="tile" style="left:{80 + col * 160}px;top:{row * 130}px;'
                             f'background:rgba(27,27,27,{shade:.2f})"></div>')
        body = f"""<div id="{sid}-wall" class="wall">{''.join(tiles)}</div>
  <div id="{sid}-fade" class="fade"></div>
  <div id="{sid}-count" class="count clip" data-start="{rel(at('lists', 'ten'))}" data-duration="{round(d - rel(at('lists', 'ten')), 3)}">
    <div class="inner"><b id="{sid}-n">10,000</b><span>logos</span></div></div>
  <div id="{sid}-zero" class="count zero clip" data-start="{rel(at('lists', 'zero'))}" data-duration="{round(d - rel(at('lists', 'zero')), 3)}">
    <div class="inner"><span>reasons why</span><b>0</b></div></div>
  <div id="{sid}-chat" class="chat clip" data-start="{rel(at('lists', 'Chatbots'))}" data-duration="{round(d - rel(at('lists', 'Chatbots')), 3)}">
    <div class="inner"><p>Chatbots give reasons</p><p class="muted">you still have to check.</p></div></div>"""
        css = f""".wall{{position:absolute;left:0;top:0;width:{W}px;height:{14 * 130}px}}
.tile{{position:absolute;width:132px;height:100px;border-radius:18px}}
.fade{{position:absolute;inset:0;background:linear-gradient(180deg,{PAPER} 0%,rgba(247,247,245,.2) 30%,rgba(247,247,245,.2) 70%,{PAPER} 100%)}}
.count{{position:absolute;left:0;top:300px;width:{W}px;text-align:center}}
.count .inner{{display:inline-flex;align-items:baseline;gap:28px;padding:30px 60px;border-radius:36px;background:{PAPER};
  box-shadow:0 30px 80px -30px rgba(27,27,27,.4)}}
.count b{{font-size:180px;font-weight:800;letter-spacing:-.05em;font-variant-numeric:tabular-nums}}
.count span{{font-size:64px;font-weight:800;color:{MUTED};letter-spacing:-.03em}}
.zero{{top:560px}}.zero b{{color:#c62f25}}
.chat{{position:absolute;left:0;top:300px;width:{W}px;text-align:center}}
.chat .inner{{display:inline-block;padding:40px 70px;border-radius:40px;background:{INK};color:#fff;text-align:left}}
.chat p{{margin:0;font-size:84px;font-weight:800;letter-spacing:-.04em;line-height:1.08}}.chat .muted{{color:{GREY}}}"""
        js += [f'tl.fromTo("#{sid}-wall",{{y:0}},{{y:-760,duration:{d},ease:"power1.in"}},0);',
               f'tl.fromTo("#{sid}-count .inner",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.4,ease:"expo.out"}},{rel(at("lists", "ten"))});',
               f'const n={{v:0}};tl.fromTo(n,{{v:0}},{{v:10000,duration:.9,ease:"power3.out",onUpdate:()=>{{document.getElementById("{sid}-n").textContent=Math.round(n.v).toLocaleString("en-US");}}}},{rel(at("lists", "ten"))});',
               f'tl.fromTo("#{sid}-zero .inner",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},{rel(at("lists", "zero"))});',
               f'tl.to("#{sid}-count .inner, #{sid}-zero .inner",{{opacity:0,y:-30,duration:.2,ease:"power3.in"}},{rel(at("lists", "Chatbots")) - 0.2});',
               f'tl.fromTo("#{sid}-chat .inner",{{opacity:0,scale:.9,filter:"blur(8px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.4,ease:"expo.out"}},{rel(at("lists", "Chatbots"))});']
    elif kind == "rule":
        a, b = rel(at("rule")), rel(at("rule", "Plain"))
        body = f"""<div class="glow"></div>{motif_svg(sid, 0.5)}
  <div class="big l1" style="top:330px;font-size:190px">{words_html(sid + 'a', 'Models gather.')}</div>
  <div class="big l2" style="top:560px;font-size:190px;color:{DEEP}">{words_html(sid + 'b', 'Code decides.')}</div>"""
        css = ""
        js += [f'tl.fromTo(".{sid}-g",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.4,ease:"power2.out",stagger:.02}},0);',
               f'tl.fromTo(".{sid}-o",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.9,ease:"power2.inOut",stagger:.08}},{b});']
        for i in range(2):
            js.append(f'tl.fromTo("#{sid}a-w{i}",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:.16,ease:"power4.out"}},{a + 0.08 + i * 0.32});')
            js.append(f'tl.fromTo("#{sid}b-w{i}",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:.16,ease:"power4.out"}},{b + i * 0.32});')
    elif kind == "close":
        body = f"""<div class="glow"></div>{motif_svg(sid)}
  <div class="big" style="top:130px;font-size:84px">{words_html(sid, 'Find the companies that need you this week.')}</div>"""
        css = ""
        js += [f'tl.fromTo(".{sid}-g",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.2,ease:"power2.out",stagger:.025}},0);',
               f'tl.to(".{sid}-g",{{strokeOpacity:.18,duration:.8,ease:"sine.inOut"}},1.3);',
               f'tl.fromTo(".{sid}-o",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.1,ease:"power2.inOut",stagger:.12}},1.1);',
               f'tl.fromTo("#{sid}-core",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.5,ease:"back.out(1.6)"}},0.9);']
        for i in range(8):
            js.append(f'tl.fromTo("#{sid}-w{i}",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.14,ease:"power4.out"}},{0.3 + i * 0.08});')
    elif kind == "end":
        body = f"""<div class="glow"></div>
  <div class="lockup"><div id="{sid}-mark" class="mark">{LOGO}</div><div id="{sid}-name" class="name">GTM Shortlist</div></div>
  <div id="{sid}-url" class="url">{URL}</div>
  <div id="{sid}-credit" class="credit">Built solo for the Meta Global AI Developer Hackathon · Muse Spark 1.3 · Muse Spark Open on Baseten</div>
  <div id="{sid}-note" class="note">Voice, music and sound made with AI. Every product shot is a real recording.</div>"""
        css = f""".lockup{{position:absolute;left:0;top:300px;width:{W}px;display:flex;justify-content:center;align-items:center;gap:36px}}
.mark{{width:150px;height:150px}}.mark svg{{width:150px;height:150px;display:block}}
.name{{font-size:150px;font-weight:800;letter-spacing:-.05em}}
.url{{position:absolute;left:0;top:520px;width:{W}px;text-align:center;font-size:46px;font-weight:800;color:{DEEP};letter-spacing:-.02em}}
.credit{{position:absolute;left:0;top:640px;width:{W}px;text-align:center;font-size:32px;font-weight:500;color:{INK}}}
.note{{position:absolute;left:0;top:800px;width:{W}px;text-align:center;font-size:30px;line-height:1.5;font-weight:500;color:{MUTED}}}"""
        js += [f'tl.fromTo("#{sid}-mark",{{opacity:0,scale:.4,rotation:-20}},{{opacity:1,scale:1,rotation:0,duration:.6,ease:"back.out(1.5)"}},0.15);',
               f'tl.fromTo("#{sid}-name",{{opacity:0,x:-40,filter:"blur(8px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:.45,ease:"expo.out"}},0.45);',
               f'tl.fromTo("#{sid}-url",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},0.9);',
               f'tl.fromTo("#{sid}-credit",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},1.15);',
               f'tl.fromTo("#{sid}-note",{{opacity:0}},{{opacity:1,duration:.5,ease:"sine.out"}},1.5);']
    return f"""<template>
<style>{GRAPHIC_CSS}
{css}</style>
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


def captions_scene():
    words = []
    for line in lines:
        lid = line["id"]
        if lid in NO_CAPTION:
            continue
        for k, w in enumerate(T[lid]["words"]):
            words.append({"text": w["text"], "start": round(T[lid]["start"] + w["start"], 3),
                          "end": round(T[lid]["start"] + w["end"], 3), "key": w["text"] == KEYWORD.get(lid),
                          "last": k == len(T[lid]["words"]) - 1})
    # Groups of up to 4 words, broken at punctuation, pauses and line ends.
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (len(cur) >= 4 or w["last"] or w["text"][-1] in ",.?:!" or not nxt or nxt["start"] - w["end"] > 0.15):
            groups.append(cur)
            cur = []
    out, js = [], []
    for g, group in enumerate(groups):
        nxt = groups[g + 1][0]["start"] if g + 1 < len(groups) else TOTAL
        start = max(0.1, group[0]["start"] - 0.05)
        end = min(nxt - 0.02, group[-1]["end"] + 0.35)
        spans = "".join(f'<span id="cap{g}-{k}" class="cw{" key" if w["key"] else ""}">{escape(w["text"])}</span>'
                        for k, w in enumerate(group))
        out.append(f'<div id="cap{g}" class="cap clip" data-start="{start:.3f}" data-duration="{end - start:.3f}">'
                   f'<div class="pill">{spans}</div></div>')
        js.append(f'tl.fromTo("#cap{g} .pill",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.14,ease:"power3.out"}},{start:.3f});')
        for k, w in enumerate(group):
            color = DEEP if w["key"] else INK
            js.append(f'tl.fromTo("#cap{g}-{k}",{{color:"#857e75"}},{{color:"{color}",duration:.08,ease:"none"}},{max(start, w["start"] - 0.04):.3f});')
    return f"""<template>
<style>{FONT}
#root{{position:absolute;inset:0;pointer-events:none;font-family:'Schibsted Grotesk',sans-serif}}
.cap{{position:absolute;left:0;bottom:92px;width:{W}px;text-align:center;z-index:50}}
.pill{{display:inline-flex;gap:18px;padding:16px 40px 20px;border-radius:26px;background:rgba(250,248,245,.97);
  box-shadow:0 22px 50px -20px rgba(27,27,27,.5);font-size:60px;font-weight:800;letter-spacing:-.025em;white-space:nowrap}}
.cw{{color:#857e75}}</style>
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
    rate = (s["m"][1] - s["m"][0]) / s["dur"]
    return round(s["start"] + (media_t - s["m"][0]) / rate, 3)


# (file, film time of the picture, volume). Each clip is placed so its measured peak lands just after its picture.
PEAK = {"whoosh-a": 0.118, "whoosh-b": 0.125, "pop-a": 0.005, "pop-b": 0.018, "click": 0.03, "keys": 0.05,
        "stamp": 0.045, "scratch": 0.15, "thump": 0.012, "riser": 0.968, "impact": 0.0, "register": 0.104}
SFX = [
    ("impact", at("hook1") + 0.05, 0.55),
    ("whoosh-a", SCENES[1]["start"], 0.5),
    ("pop-a", at("lists", "ten"), 0.6), ("pop-b", at("lists", "zero"), 0.6), ("whoosh-b", at("lists", "Chatbots"), 0.45),
    ("scratch", at("disclose") - 0.45, 0.55),
    ("keys", media_to_film("s-input", 8.35), 0.35), ("click", media_to_film("s-input", 13.05), 0.6),
    ("pop-a", at("input", "website"), 0.5),
    ("pop-b", at("reads") + 0.15, 0.45), ("pop-b", at("checker", "Muse"), 0.45),
    ("whoosh-a", SCENES[[s["id"] for s in SCENES].index("s-out")]["start"], 0.45),
    ("click", media_to_film("s-thrive", 8.6), 0.55), ("click", media_to_film("s-quote", 14.6), 0.55),
    ("pop-a", at("opener", "checker"), 0.5),
    ("thump", at("turn") - 0.05, 0.7),
    ("stamp", at("storable", "out") + 0.2, 0.9),
    ("whoosh-b", SCENES[[s["id"] for s in SCENES].index("s-rule")]["start"], 0.45),
    ("pop-a", at("thrown", "Across"), 0.5),
    ("keys", media_to_film("s-nowebsite", 7.2), 0.3),
    ("pop-b", at("cost", "forty-two"), 0.55),
    ("whoosh-a", SCENES[[s["id"] for s in SCENES].index("s-close")]["start"], 0.45),
    ("riser", SCENES[-1]["start"] + 0.15, 0.5),
]
MUSIC_CUT, MUSIC_BACK = at("turn") - 0.1, at("storable", "out") + 0.2


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
    audio.append(f'<audio id="music-a" class="clip" src="assets/music/music.wav" data-start="0" data-duration="{MUSIC_CUT:.3f}" '
                 f'data-track-index="5" data-volume="0.5" data-fade-in="0.3" data-fade-out="0.12"></audio>')
    audio.append(f'<audio id="music-b" class="clip" src="assets/music/music.wav" data-start="{MUSIC_BACK:.3f}" '
                 f'data-duration="{TOTAL - MUSIC_BACK:.3f}" data-media-start="{MUSIC_BACK:.3f}" data-track-index="5" '
                 f'data-volume="0.5" data-fade-in="0.2" data-fade-out="2.5"></audio>')
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
    for s in SCENES:
        html = graphic_scene(s) if "graphic" in s else footage_scene(s)
        (comp / f"{s['id']}.html").write_text(html, encoding="utf-8")
    (comp / "captions.html").write_text(captions_scene(), encoding="utf-8")
    (HERE / "index.html").write_text(index_html(), encoding="utf-8")
    footage = sum(s["dur"] for s in SCENES if "src" in s)
    print(f"total {TOTAL:.2f}s, real screen {footage:.1f}s ({footage / TOTAL:.0%}), {len(SCENES)} scenes")
    for s in SCENES:
        rate = f' x{(s["m"][1] - s["m"][0]) / s["dur"]:.2f}' if "m" in s else ""
        print(f'  {s["start"]:7.2f}  {s["dur"]:5.2f}s  {s["id"]}{rate}')


main()






