# Public agent demo

A separate app for letting anyone try the website-only agent from a public link: `src/shortlist_agent/public.py`. It serves only the agent's start page and board, never the classic workspace, accounts or credits, and it shares nothing with the local or hosted GTM Shortlist apps.

## What it enforces

| Limit | Setting | Default |
|---|---|---|
| Companies per search | `AGENT_PUBLIC_MAX_COMPANIES` | 5 |
| Searches per visitor per hour (address hashed with the secret, never stored raw) | `AGENT_PUBLIC_RUNS_PER_HOUR` | 3 |
| Searches working at once | `AGENT_PUBLIC_MAX_ACTIVE` | 3 |
| Estimated dollars per day across all visitors, resets 00:00 UTC | `AGENT_PUBLIC_DAILY_USD` | 10 |
| Estimated dollars in all since a start date; once reached, no new searches ("Spending limit reached") | `AGENT_PUBLIC_TOTAL_USD` + `AGENT_PUBLIC_TOTAL_SINCE` | off (eygentic.tech: 50 from 3 Nov) |
| Estimated dollars per search | `AGENT_RUN_BUDGET_USD` | 1.00 (0.50 suggested here) |
| Cloudflare Turnstile before a search starts | `AGENT_PUBLIC_TURNSTILE_SITE_KEY` + `AGENT_PUBLIC_TURNSTILE_SECRET` | off |

A new search (or email draft) is refused when the day's estimate, or the total since `AGENT_PUBLIC_TOTAL_SINCE`, plus a full budget for every working search would pass its cap. The eygentic.tech values are set in `deploy/modal_agent.py`. Estimates come from the agent's own telemetry (published token and search prices), not the providers' bills, so also set spend limits on the Meta billing page and in Baseten.

A search page is readable by anyone with its link; ids are random 128-bit hex. There is no list of searches. Only the browser that started a search holds its edit token (in that browser's local storage), so only it can correct the assumptions; everyone else sees a read-only shortlist. Requests from other origins and other host names are refused. A search left working by a restart is marked failed with a note to start again.

## Try it locally with synthetic data

No keys, no network, no spending. From the repository root after `npm run build`:

```powershell
$env:AGENT_PUBLIC_URL="http://127.0.0.1:8020"
$env:AGENT_PUBLIC_SECRET=(python -c "import secrets; print(secrets.token_hex(32))")
$env:AGENT_PUBLIC_SYNTHETIC="on"
.venv\Scripts\python.exe -m uvicorn --factory shortlist_agent.public:create_public_app --host 127.0.0.1 --port 8020
```

Open http://127.0.0.1:8020 and search for `seller.example`. Remove `AGENT_PUBLIC_SYNTHETIC` and put `META_MODEL_API_KEY` and `BASETEN_API_KEY` in `.env` to run live locally.

## Deploy on Modal

1. Install the Modal CLI and sign in once: `pip install modal`, then `modal setup`.
2. Build the UI: `npm ci`, then `npm run build`.
3. Create the secret. The URL is `https://<your-modal-workspace>--gtm-shortlist-agent-web.modal.run`; if the first deploy prints a different one, recreate the secret with that URL and deploy again.

   ```powershell
   modal secret create gtm-shortlist-agent `
     META_MODEL_API_KEY=... BASETEN_API_KEY=... `
     AGENT_PUBLIC_URL=https://<your-modal-workspace>--gtm-shortlist-agent-web.modal.run `
     AGENT_PUBLIC_SECRET=<64 random hex characters> `
     AGENT_RUN_BUDGET_USD=0.50 AGENT_PUBLIC_DAILY_USD=10
   ```

   To change a value later, run the same command with `--force`, then deploy again.
4. Deploy: `modal deploy deploy/modal_agent.py`.
5. Check it: open `/api/health` (free: it only lists models) and confirm `investigator_model_available` is `true`. If it is `false`, Meta does not offer the model where the server runs: `server_location` and `investigator_models_offered` say where it runs and what Meta offers there. Then open the URL, confirm the page says "Free demo: up to 5 companies per search", run one search for your own website, and watch the cost in the board's footer. Set spend limits on the Meta billing page and in Baseten.

The deployment keeps one small CPU container running (`min_containers=1`, `max_containers=1`), so the per-visitor limits and the working searches stay in one process. Searches are JSON files on the Modal Volume `gtm-shortlist-agent-runs`, committed every few seconds. To stop the demo, run `modal app stop gtm-shortlist-agent`.

## Serve it at your own domain (eygentic.tech)

Modal custom domains need its Team plan, so the demo is served at https://eygentic.tech by a free Cloudflare Worker
(`deploy/eygentic-proxy/`) that forwards every request to the Modal app. The browser only sees eygentic.tech.

1. In Cloudflare (free plan), add the site `eygentic.tech`, then set the two nameservers Cloudflare gives you at the
   registrar (Namify). Remove the old CNAME to Render once Cloudflare has imported the records.
2. `cd deploy/eygentic-proxy && npx wrangler login && npx wrangler deploy`. This attaches the Worker to `eygentic.tech`
   and `www.eygentic.tech` (www redirects to the bare domain).
3. In the Modal secret, set `AGENT_PUBLIC_URL=https://eygentic.tech` and
   `AGENT_PUBLIC_ALSO_HOSTS=gtmshortlist--gtm-shortlist-agent-web.us-east.modal.run`, then deploy the app again. From then
   on, searches start only from eygentic.tech: the app refuses a browser whose origin is not `AGENT_PUBLIC_URL`.
## Checks

- `pytest tests/test_public_demo.py`: limits, edit tokens, Turnstile, origin and host checks, run-id validation, the file store and restart recovery.
- `npx playwright test tests/ui/agent-public.spec.ts`: the public start page and a shared read-only link at 1366px and 390px, served by `scripts/public_demo_test_server.py` with synthetic providers.
- Live on Modal since 2 Nov 2026 in the `gtmshortlist` workspace: https://gtmshortlist--gtm-shortlist-agent-web.us-east.modal.run. The URL carries a region (`.us-east`), unlike step 3's pattern, so the secret uses it. A new secret reaches only a new container: after `modal secret create --force`, run `modal container list` and `modal container stop <id> --yes`, and the always-on container restarts with it. Do not set `AGENT_PUBLIC_DATA` in the secret: the image points it at the Volume.
