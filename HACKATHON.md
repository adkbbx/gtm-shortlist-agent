# Meta Global AI Developer Hackathon: GTM Shortlist agent

Put in your website. The agent works out what you sell and who buys it, proves who your competitors are, finds
companies that show a need right now (open job posts, launches, funding), investigates each one, and sorts them into
**Shortlisted**, **Needs a look** and **Rejected**, with the exact quote and source link behind every verdict. Without a
website, three short answers stand in for it. For each Shortlisted company it writes an opening line, and a second Meta
model checks every statement in it against the quotes.

Live demo: https://eygentic.tech

## What existed before, and what this repository is

Before the hackathon I had started an unfinished prototype, GTM Shortlist (https://github.com/adkbbx/GTM_Shortlist). It
researched one to three companies at a time with a different model (Gemma, through search APIs), after a required
screen where you typed your offer and fit criteria. It had no agent, no second model, no public demo and no users.

**Everything in this repository was built during the event** (26 October to 4 November 2026), with three exceptions,
each declared:

- **The prototype as a library, not copied.** `pyproject.toml` installs it from its own repository at the tag
  `pre-meta-hackathon` (commit `b620235`, 19 October), the last commit before the event. The agent uses its safe page
  fetcher (`shortlist.fetch`: HTTPS only, public addresses only, pinned TLS, same-site redirects), its exact quote
  matching (`shortlist.relevance`), its page-type rules and `shortlist.selection.discussion_page`, unchanged.
- **Base styles.** `web/base.css` carries over the prototype's colour and type tokens and its base element styles, so
  the pages keep the same look.
- **Started from prototype code.** `src/shortlist_agent/icons.py` began as the prototype's icon lookup and was changed
  during the event (its docstring lists the changes). `src/shortlist_agent/pagefetch.py` and `staffing.py` hold code
  written during the event that first lived in the prototype's files.

The work was first built on a branch of the prototype's repository; this repository holds only that branch's new work.
Every change made during the event can be checked there:
https://github.com/adkbbx/GTM_Shortlist/compare/pre-meta-hackathon...meta-hackathon

## Before and during the event

| | Built before the event (tag `pre-meta-hackathon`, commit `b620235`, 19 October) | Built during the event (this repository) |
|---|---|---|
| Input | Company name or website, then a required screen to confirm the offer, target and typed fit criteria | Website only; typing a company name offers matching companies with their logos (Brandfetch search, a new combobox written during the event) and choosing one fills in its website. No confirmation screen. A vague site gets up to three clickable readings, never a required text box. Without a website, three short answers (what you sell, your ideal customer, which markets) stand in for it: every claim about the seller quotes those words, labelled "from your description" |
| Seller understanding | One model call drafts an offer and target from the homepage for the person to edit | Homepage plus up to five chosen pages (pricing, product, customers, about, integrations or the seller's own comparison page). Offer, buyer, existing customers, 2 to 5 fit checks, need and timing signals and any stated size or region, each with quotes |
| Competitors | Same-category companies set aside by a word-overlap rule | Found with web search, then proven from each candidate's own homepage: `direct` needs a quote for the same job and one for the same buyer. Direct competitors become disqualifiers |
| Research | `worker.execute_run`: Tavily or SerpApi search and an OpenAI-compatible Gemma model, one to three companies | An agent loop per company on Muse Spark with built-in `web_search` and a `fetch_page` tool, 10 companies by default (up to 20), five at a time, at most 4 searches, 6 page reads and 8 turns each |
| Competitor use | Not checked | A model-free scan of each fetched page's code (script sources, badges, "powered by" lines, integrations pages), targeted searches, and competitor customer pages that name the company. Every place checked is listed |
| Judging quotes | The same model verifies its own assessments | An independent skeptic (Muse Spark Open on Baseten) with no web access sees only the quote, the check, the source type and dates |
| Verdict | Fits / Needs verification / Does not fit | Plain code: Rejected for a skeptic-supported disqualifier; Shortlisted only with every required fit check, need or timing evidence dated within 180 days and a completed competitor check; otherwise Needs a look with the list of what is missing |
| Hiring signals | Not checked | Discovery searches Lever, Greenhouse and Ashby postings first and confirms each is still listed on a board that names the company. Every investigation reads the company's own job board, found only from links on its own site (`shortlist_agent/jobboards.py`); a posting page that cannot be read is built from the board's own posting text |
| What to say | Not offered | For each Shortlisted company, Muse Spark writes why now and an opening line from the quotes the skeptic supported; Muse Spark Open checks every statement against those quotes, and a note that claims more is rewritten once or dropped (`shortlist_agent/outreach.py`). On request, a short email and a LinkedIn note, held to the same quotes and the same check |
| Cost control | Per-run caps on searches and model calls | Every model call recorded with tokens, searches, latency and estimated dollars; a per-run budget stops new research. Work that finishes companies already researched (the skeptic's checks, a Shortlisted company's opening line, a requested email) may use a small reserve past it: $0.15, never more than a third of the budget |
| Storage | `runs`, `records` and related tables | New `agent_runs` table (id, created_at, status, payload JSON, events JSON) in a local SQLite file |
| Interface | Classic workspace, landing page and demo | New start page with one field, a replay of a real search and a snapshot of a real result; a live board with a pinned monitor, an activity rail, "What we assumed", verdict columns, quote popovers with text-fragment links and a cost footer; a "Your shortlist" page for this browser's Shortlisted companies; a video mode (`?video=1`) that shows every company except the recording seller under an invented `.example` name, with a "company names changed" tag |
| Command line and evaluation | `shortlist run`, `export` and earlier evaluation scripts | `shortlist-agent run` and `shortlist-agent eval` with agreement, shortlist precision, disqualifier recall, cost per company, p50/p95 latency and a no-skeptic ablation |
| Public access | Hosted accounts with signup credits | A separate public demo app (`shortlist_agent/public.py`) that needs only a website: capped companies per search, an hourly limit per visitor, a cap on searches working at once, a daily dollar cap and optional Turnstile. Shareable read-only links; only the starting browser can correct a search. Runs are JSON files (`shortlist_agent/files.py`). Live at https://eygentic.tech (`deploy/modal_agent.py` on Modal, served at that address by a Cloudflare Worker in `deploy/eygentic-proxy`: one always-on container, searches saved on a Modal Volume so shared links last). Three real finished searches ship as read-only examples, one per seller (vanta.com, crisp.chat, eygentic.com), and finished boards have link previews |
| Tests | 838 backend tests and the existing browser journeys | 149 backend tests in `tests/` and 8 browser journeys in `tests/ui/agent.spec.ts` and `tests/ui/agent-public.spec.ts`, each on laptop and phone |

## Which Meta model does what

- **Muse Spark 1.3 on the Meta Model API** (`https://api.meta.ai/v1`, Responses endpoint, model from `META_MODEL`, default `muse-spark-1.3`) is the investigator. It reads the seller's pages, searches for competitors and companies with the built-in `web_search` tool, and runs the per-company loop, calling our `fetch_page` function tool. Raw search results are requested with `include: ["web_search_call.results"]`.
- **Muse Spark Open on Baseten** (`meta-models/muse-spark-open-1026`, OpenAI-compatible Chat Completions) is the skeptic. It never sees the web or the company name. For each quote it answers `supports`, `contradicts` or `insufficient`, with a reason, under two written rules: the company's own site can support fit only, never need, and a disqualifier must show current use, not an integration, a comparison or past use. Its JSON is validated strictly with one repair attempt.
- **No model decides a verdict.** `src/shortlist_agent/verdict.py` does, from the skeptic's decisions. The own-site rule is also enforced in code after the skeptic answers.

Every claim shown carries an exact quote found verbatim in a page the agent fetched, with its URL, source type and dates. A claim whose quote is not on the page is dropped and listed in the run's `dropped` log. A model's publication date is kept only when the page states it. The agent qualifies companies only: there are no person, name or role fields anywhere in its data, and it never records, scores or judges people.


## Run it

Python 3.11 or later and Node 20 or later.

```sh
python -m venv .venv && .venv/bin/pip install -e ".[dev]"   # also installs the prototype library at its pre-event tag
npm ci && npm run build
```

**Synthetic demo, no keys and no network.** `src/shortlist_agent/synthetic.py` is a labelled synthetic world: invented
companies on reserved `.example` domains and scripted model answers.

```sh
shortlist-agent run https://seller.example/ --synthetic --output run.json
shortlist-agent eval tests/fixtures/labels.synthetic.csv --run run.json
shortlist-agent eval tests/fixtures/labels.synthetic.csv --run run.json --no-skeptic
```

**Live.** Put `META_MODEL_API_KEY` and `BASETEN_API_KEY` in `.env` (see `.env.example`), then
`shortlist-agent run https://yourcompany.com --companies 3 --output run.json`.

**Public demo.** `docs/agent-public-demo.md`: limits, a local trial with synthetic data, and deploying on Modal.

**Tests.** `pytest` (149 tests, synthetic providers only), `ruff check src tests scripts`, and
`npx playwright test` (8 browser journeys, each on laptop and phone).

## What the second model changes (measured)

On 17 saved live searches (82 companies), each search's evidence was judged again as if Muse Spark Open accepted every
quote found on its page, with the same verdict code and no model calls (`scripts/checker_value.py`, full report in
[docs/checker-value.md](docs/checker-value.md)):

- Muse Spark Open judged 354 quotes and threw out 120 of them (34%): 99 too weak, 21 contradicted.
- It changed 31 of 82 verdicts (38%). Without it, 6 companies would have been Shortlisted on quotes it threw out, and 25
  would have been Rejected, because without a judge every quote filed under a disqualifier counts against the company,
  including quotes gathered to show the opposite ("still operating", "within the seller's size range").

## Limits

- **Live runs so far are spot checks, not an evaluation.** Live runs from 30 October to 2 November for vanta.com, crisp.chat, eygentic.com, usepylon.com and a seller without a website gave Shortlisted companies with dated need quotes, Rejected companies with the quote that ruled them out, and problems we then fixed (each in the commit history, here and on the branch it was first built on). Found on 2 and 3 November: a run that reached its budget lost its opening lines (now kept within a small reserve); a search without a website Shortlisted a clinic for listing a phone number (need signals must now set likely buyers apart); and a check whose answer ran out of room was reported as a rejection (the check now starts with more room and an unreadable answer is logged as such). Tests use synthetic providers and recorded-shape HTTP fakes only.
- **Signals favour companies that hire on startup job boards.** Discovery searches Lever, Greenhouse and Ashby postings first. Local businesses such as dental clinics post front-desk roles elsewhere, so a search for a seller who serves them finds little current evidence: a re-run on 3 November for an AI phone receptionist found one Shortlisted clinic, on a weak signal (it has three locations), and three held back as Needs a look.
- Built-in web search runs on the provider's side, so the agent cannot stop a single response from making more searches than asked. It removes the search tool once a company has used four.
- Searches are stored in a local SQLite file, or as JSON files in the public demo. There are no accounts: the public demo is the hosted way to use the agent.
- The public demo runs on one always-on Modal container with searches on a Modal Volume. Its dollar limits use the agent's own estimates, so provider-side spend limits are still needed.
- The synthetic evaluation proves the plumbing and the rules, not real-world accuracy. A labelled set of real companies is the next step.
