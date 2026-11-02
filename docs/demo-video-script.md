# "Who needs you this week?" Demo video production script

For the Meta Global AI Developer Hackathon. Judging: Impact 30, Meta AI tooling 25, Demo 25, Technical depth 20; the video is judged first. Target length **2:00** (fast, never boring), 16:9 at 1920×1080, plus a 30-second 9:16 cut for X.

**Honesty rules for this video.** Every screen is the real product on a real search. Eygentic is the real seller and every company appears under its real name, because judges score whether the product really works. One caption in the video and the description: "Quotes are from each company's public pages; verdicts mean fit for my business, not a judgement of the company." Never show a number or quote that is not on screen.

## Look and sound

- **Palette:** cream `#faf8f5` background, charcoal `#1b1b1b` text, orange `#d5682f` (accent), deep orange `#b4501c` (headlines), soft grey `#9c958c` (the "in" dots). Pills: green for Shortlisted, amber for Needs a look, red for Rejected, exactly as in the app.
- **Type:** Schibsted Grotesk 800 for slams and captions, 500 for small labels. Tight tracking (-0.03em), big sizes (140 to 220 px on 1080p).
- **Signature motif, "the filter":** many fine grey lines with dots flow in from the left; most dots fade out; three orange lines leave to the right. It opens the video, carries every scene change, and closes it. It is the product in one picture: many companies in, a few that need you out.
- **Captions:** every spoken word, word by word, centred low. Charcoal on a cream pill; the key word of each line in orange. Viewers on X watch muted.
- **Pace:** a cut or a motion beat every 1 to 2 seconds. Screen recordings get slow push-ins (105% to 112%) and snap zooms onto quotes.
- **Music:** royalty-free upbeat electronic, 120 to 128 BPM, with a clear drop. Free sources: YouTube Audio Library, Pixabay Music (no credit needed), Uppbeat (credit in the description). Duck the music under the voice by 10 to 12 dB. Hard stop at 0:15 (the turn) and at 1:12 (the plot twist), then back in.
- **Sound effects (royalty-free packs on Pixabay or Mixkit):** bass hit (slams), whoosh (filter transitions), soft key clicks (typing), pop (each pill appearing), bright ding (Shortlisted), record scratch (the turn), rubber-stamp thud (Rejected), highlighter squeak (quote highlight), cash-register tick (the cost).
- **Voice:** your own voice. You are the real user; that is the strongest moment for judges. Speak fast and warm, as if telling a friend. Record in a quiet room (a wardrobe full of clothes works), phone close to your mouth, then run it through a free speech clean-up such as Adobe Podcast's Enhance Speech. If you use an AI voice instead, keep every first-person line true.
- **AI-made assets are fine, with three rules.** (1) Every product shot is a real screen recording; AI makes only B-roll, music, sound and, if needed, the voice. (2) Make the B-roll with Meta's own Muse Image where you can (the logo wall, the "companies flowing in" shots, the end card background): it counts toward Meta AI tooling and the Best Creative Build prize for Muse Image or Muse Wonder. (3) Say so in the description: "Music and some visuals made with AI; every product shot is a real recording." AI music needs a plan whose terms allow public use; royalty-free libraries avoid the question.

## Shots to record (real names, video mode off)

Record the real product. If one company must not be named, blur that card in the edit; video mode (`?video=1`) stays available but the script does not use it. At least 70% of the video is real screen recording.

- **R1, start page:** the hero lines flowing, then typing `eygentic.com`, choosing 5, pressing Find. 1440×900, zoom 110%.

The film is built in `video/` with HyperFrames: these shots recorded with Playwright from the live demo (R2 is a real
live search), an ElevenLabs voice, music and effects, and the narration in `video/narration.json`. That narration
replaces the voice lines below: it is rewritten in plain first-person speech, and the film uses a clean framed-window
look (step labels, spotlights, plain captions) instead of the stamps and slams described here.
- **R2, live board, first minute:** "What we assumed" filling in, competitors, companies being researched, the activity rail.
- **R3, the finished eygentic.com example** (Explore a finished search): ThriveCart in Shortlisted with its quote popover and opening line; Storable in Rejected with its quote; the Needs a look column; the board's footer.
- **R4, the no-website popup:** fill in the three questions slowly; do not submit.
- **R5, the homepage code scan (optional):** a Needs a look card's details showing the places checked.

## The script

| Time | Picture | Voice | On-screen text and motion | Sound |
|---|---|---|---|---|
| 0:00 | Cream screen. The filter lines draw in from the left, fast. | "Building got easy." | "Building got easy." slams in, charcoal, word by word. | Bass hit on each word, music starts (intro, no drums). |
| 0:03 | Same, lines keep flowing. | "Finding customers didn't." | "Finding customers didn't." in deep orange underneath. | Bass hit. |
| 0:06 | A wall of grey logo squares scrolls up fast (abstract tiles, no real logos), then freezes on a red "0". | "Lead lists give you ten thousand logos and zero reasons. Chatbots give you reasons you still have to check." | Counter 0 → 10,000, then "Reasons why: 0". | Rising whoosh, pop. |
| 0:10 | Record scratch. Hard cut to R1: the hero. | "I'd started a rough prototype before the hackathon. Everything you'll see here, I built this week on Muse Spark." | Logo mark pops top-left; small caption: "Built 26 Oct to 4 Nov 2026". | Record scratch, then the drop. |
| 0:18 | R1: typing `eygentic.com`, press Find. Snap zoom on the field. | "One input. My website." | "1 input" sticker on the field. | Key clicks, pop. |
| 0:22 | R2: "What we assumed" filling in. Push in. | "Muse Spark 1.3 reads it and works out what I sell, who buys it, and what makes a company need me now." | Badge slides in: "Muse Spark 1.3 · investigator". Each assumption gets a small "quoted ✓" tick as it appears. | Pops on each tick. |
| 0:30 | R2: competitors. | "It proves my competitors from their own homepages." | Two competitor chips flash "direct". | Whoosh. |
| 0:34 | R2: companies being researched; the filter motif overlays the left half. | "Then it hunts signals, not a database: live job posts, news, launches." | Floating labels: "Lever", "Greenhouse", "Ashby", "news". | Rapid whooshes on the beat. |
| 0:40 | R2 or R5: page code with a script tag highlighted. | "It even reads their homepage code to see which tools they already use." | Code panel slides in; a line glows orange: "already uses a competitor → out". | Glitch tick. |
| 0:45 | R2: the activity rail, zoomed on the "Verify" steps ("Kept 3 of 4; the rest were too weak or contradicted"). | "Then a second model, Muse Spark Open on Baseten, reads each quote cold, without the web, and throws out the weak ones." | Badge over the real rail: "Muse Spark Open · checker". | Soft pop on each Verify line. |
| 0:53 | Filter transition to R3. | "Here's what came out." | Counter: "10 found → 5 researched → 1 shortlisted". | Whoosh, then ding. |
| 0:56 | R3: ThriveCart card, Shortlisted pill. Snap zoom. | "ThriveCart. Shortlisted." | Pill pops. | Ding. |
| 0:59 | R3: the quote popover. Highlighter sweeps across the quote. | "Their open job post: 'As one of the first three SDRs in this enterprise initiative.'" | Quote enlarges to full width, the words highlight in orange as you say them. Label: "open job post · read during the search". | Highlighter squeak. |
| 1:06 | R3: the opening line. Typewriter effect. | "It writes my first line from that quote only. And the skeptic checks it before I ever see it." | "checked ✓ by a second model" stamp. | Key clicks, pop. |
| 1:12 | Music cuts. R3: Storable card, slow push. | "Storable looked like a fit. Until it didn't." | Screen dims slightly. | Silence, then a single heartbeat thump. |
| 1:16 | R3: Storable's quote. | "'Proudly employs over 800 employees.' I sell to seed to Series A. It's out." | "REJECTED" rubber stamp slams across the card in red; the quote sits under it. | Stamp thud, music back in. |
| 1:23 | Text slam over the board. | "The models gather the evidence. Plain code makes the call." | "Models gather. Code decides." | Two bass hits. |
| 1:27 | R3: the Needs a look column, quick pan. | "Everything else? Needs a look, and it tells me exactly what's missing." | Each card's missing-item line glows briefly. | Soft pops. |
| 1:33 | R4: the popup, typing the answers. | "No website yet? Describe what you sell. It quotes your own words." | "No website? No problem." sticker. | Key clicks. |
| 1:40 | R3: the board footer. Counters animate. | "Five companies, forty-two cents. And I can click through to every sentence it used." | Big numbers: "5 companies · $0.42". | Cash-register tick on "$0.42". |
| 1:48 | Filter motif, full screen, slowing down. Three orange dots exit right. | "Now I know who to email this week, and what to say." | "Find the companies that need you this week." | Music builds. |
| 1:53 | End card: logo, URL, credits. | "GTM Shortlist. Try it with your website." | URL large; "Built solo for the Meta hackathon · Muse Spark 1.3 · Muse Spark Open on Baseten"; small line: "Quotes are from each company's public pages; verdicts mean fit for my business, not a judgement of the company." | Final bass hit, music out. |
| 2:00 | End. | | | |

About 230 spoken words: fast but clear at 2:00.

## Rules while editing

- The caption "Quotes are from each company's public pages; verdicts mean fit for my business, not a judgement of the company." appears once on screen (first board shot) and in the description.
- No real company name or logo anywhere, including the chatbot bubble and the logo wall (use plain shapes).
- Never show anyone's name, email or location; record in a clean browser profile.
- Quotes on screen must match the app exactly (real quotes, exactly as the app shows them).
- Do not add accuracy numbers until the review sheet is labelled.
- Say it like a person: no slogans such as "receipts", "no mercy" or "100% sourced". Plain words about what you saw.

## 30-second vertical cut for X (1080×1920)

0:00 "Building got easy. Finding customers didn't." → 0:04 lead-list logo wall, "0 reasons" → 0:07 record scratch, typing `eygentic.com` → 0:10 the filter motif, "10 found → 1 shortlisted" → 0:14 ThriveCart quote highlight → 0:19 Storable REJECTED stamp → 0:23 "Models gather. Code decides." → 0:26 URL and "Built with Muse Spark". Same music, captions larger (top third safe area).

Suggested post: "Put in your website. It tells you which companies need what you sell right now, and why, in their own words, with the link to where they said it. Built solo for the Meta hackathon on Muse Spark. Try it on yours:" followed by the link.
