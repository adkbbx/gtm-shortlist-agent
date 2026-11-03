# Submission text

Paste-ready text for the Meta Global AI Developer Hackathon form (Indie track) and the X post. Every number comes from
HACKATHON.md, docs/checker-value.md or the live demo.

## Name

GTM Shortlist

## Tagline

Put in your website. It finds the companies that need what you sell right now, and shows you why in their own words.

## Links

- Live demo: https://eygentic.tech
- Code: https://github.com/adkbbx/gtm-shortlist-agent
- Video: (your YouTube link)

## Description

I run Eygentic. We help small B2B teams figure out what brings them customers. And I have the same problem myself:
who do I reach out to this week? Lead lists give me thousands of names and no reason to call any of them. A chatbot gives me
reasons, but I can't tell which ones are real.

GTM Shortlist takes one input, your website. Muse Spark 1.3 reads your site and works out what you sell, who buys it
and what would make a company need you now. It checks your competitors against their own homepages, then looks for
companies showing that need today: open job posts on Lever, Greenhouse and Ashby, news and launches. For each company it
reads the pages itself and files the exact quotes it found.

A second model, Muse Spark Open on Baseten, cannot browse. It sees only each quote and what the quote is meant to prove,
and it throws out anything that doesn't hold up. Then plain rules in code, not a model, sort every company into
Shortlisted, Needs a look or Rejected. Every verdict links to the sentence it rests on. For Shortlisted companies it
writes a first line, and on request a full email and LinkedIn note, from the accepted quotes only, and the second model
checks those too. A five-company search takes two to six minutes and costs about 40 to 50 cents.

## What existed before, and what I built during the event

Before 26 October I had a rough prototype: it researched a few companies at a time with a different model, after a
screen where I typed my offer and criteria. It had no agent, no second model, no public demo and no users. The entry
repository was created during the event and holds event work; the prototype is installed as a library at its
pre-event tag for a few pieces (its safe page fetcher, exact quote matching and page-type rules), and HACKATHON.md
declares every other piece that started from it (its colour and type styles, the icon lookup). Everything else was built between 26
October and 4 November: the agent loop, competitor proof, the hiring-signal search, the homepage code scan, the second
model's check, the verdict rules, the opening lines and emails, the live board and the public demo at eygentic.tech.
HACKATHON.md has the full before-and-after table.

## How it uses Meta's models

- **Muse Spark 1.3 (Meta Model API)** is the investigator: it reads the seller's site, searches with the built-in
  web_search tool, and runs an agent loop per company that calls my fetch_page tool (at most 4 searches, 6 page reads
  and 8 turns per company, five companies at a time). It also writes the opening lines and emails.
- **Muse Spark Open on Baseten** is the checker: no web access, one decision per quote (supports, contradicts or not
  enough) with a reason, and a second check on every message before it is shown.
- **No model decides a verdict.** Code does, from the checker's decisions, so the same evidence always gets the same
  answer and the reason is always visible.

## Results

- **The second model matters.** On 17 saved live searches (82 companies), Muse Spark Open threw out 120 of 354 quotes
  (34%) and changed 31 of 82 verdicts (38%), measured by re-running the verdict code without it on the same evidence.
- **On my own labels.** I labelled 41 real companies from four sellers. I agreed with 30 verdicts (73%). It never threw
  away a company I wanted: all 3 of its Rejections were right, and every company I would contact was on its Shortlist.
  Its Shortlist is too generous: I would contact 7 of its 12, and all 5 misses were too big for the seller, because
  size is rarely stated on the pages it reads. Looking size up is the next step.

## Limits

- Signals favour companies that hire on startup job boards; local businesses such as dental clinics show little
  current evidence.
- Dollar limits on the demo use the agent's own estimates (the demo stops at $50 in total).
- The labelled set is small: 41 companies, one person's judgement.

## AI assets in the video

The voice, music and sound effects were made with ElevenLabs. Every product shot is a real screen recording of the live
demo, including one real search for my own site.

## X post

> Lead lists give me names. Chatbots give me reasons I can't check.
>
> So I built GTM Shortlist for the Meta hackathon: put in your website, and it finds companies that need you right
> now, with the exact quote and link behind every pick. A second model throws out the weak evidence.
>
> Try it on your own site: https://eygentic.tech

The post above needs a longer-post account. Under 280 characters, with the video attached:

> Put in your website. GTM Shortlist finds companies that need you right now, and shows the exact quote behind every
> pick. Built on Muse Spark for the Meta hackathon. Try it: https://eygentic.tech
