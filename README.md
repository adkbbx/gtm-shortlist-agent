# GTM Shortlist

Put in your website. GTM Shortlist tells you which companies need what you sell right now, and why, in their own words,
with a link to where they said it. No website yet? Describe what you sell and who buys it.

**Try it:** https://eygentic.tech

Built solo for the Meta Global AI Developer Hackathon (Indie track). [HACKATHON.md](HACKATHON.md) says exactly what
existed before the event and what was built during it.

## How it works

1. **Muse Spark 1.3** (Meta Model API) reads your site and writes down what you sell, who buys it, which checks a good
   fit passes and what would show a company needs it now, each with a quote from your own pages.
2. It finds your competitors with web search, and only calls one direct when that company's own homepage proves the same
   job for the same buyer.
3. It looks for companies showing a need right now: open job posts on Lever, Greenhouse and Ashby first, then news and
   launches. Each company gets its own agent loop: up to four searches and six page reads with our `fetch_page` tool, its
   own job board, and a scan of its homepage code for a competitor's widget.
4. **Muse Spark Open** (open weights, on Baseten) reads each quote without the web or the company's name and keeps only
   the ones that really support the claim.
5. Plain code, not a model, makes the verdict: **Shortlisted**, **Needs a look** (with what is missing) or **Rejected**
   (with the quote that ruled it out). A claim whose exact sentence is not on a page the agent fetched never appears.
6. For each Shortlisted company it writes why now and an opening line from those quotes only, and Muse Spark Open checks
   every statement before it is shown.

Every model call is logged with tokens, searches and dollars; a search of five companies costs about $0.40.

Measured on 17 saved live searches: Muse Spark Open threw out 120 of 354 quotes and changed 31 of 82 verdicts
([docs/checker-value.md](docs/checker-value.md)).

## Run it

```sh
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
npm ci && npm run build
shortlist-agent run https://seller.example/ --synthetic --output run.json   # labelled synthetic data: no keys, no network
```

With `META_MODEL_API_KEY` and `BASETEN_API_KEY` in `.env` (see `.env.example`), drop `--synthetic` and use your own
website. The public demo and its limits: [docs/agent-public-demo.md](docs/agent-public-demo.md).

Tests: `pytest`, `ruff check src tests scripts`, `npx playwright test`.

## Licence

MIT. See [LICENSE](LICENSE).
