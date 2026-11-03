"""The public agent demo (shortlist_agent.public) on Modal: one always-on CPU container serving the built UI and the
agent API, with each search saved as a JSON file on a Modal Volume. Setup and limits: docs/agent-public-demo.md.

    npm ci && npm run build          # the UI goes into dist/, which this image copies
    modal deploy deploy/modal_agent.py

Provider keys and the demo's own settings come from the Modal secret `gtm-shortlist-agent`; nothing secret is in here.
"""
import threading
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "gtm-shortlist-agent"

volume = modal.Volume.from_name("gtm-shortlist-agent-runs", create_if_missing=True)
image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git")  # pip installs the pre-event prototype from its git tag
    .pip_install_from_requirements(str(ROOT / "requirements.runtime.txt"))
    # Modal's proxy sets X-Forwarded-For, so the hourly limit counts visitors rather than the proxy.
    .env({"PYTHONPATH": "/app/src", "AGENT_PUBLIC_DATA": "/data/runs", "AGENT_PUBLIC_DIST": "/app/dist",
          "AGENT_PUBLIC_TRUST_PROXY": "on"})
    .add_local_dir(str(ROOT / "dist"), "/app/dist")
    .add_local_dir(str(ROOT / "src" / "shortlist_agent"), "/app/src/shortlist_agent")
)
app = modal.App(APP_NAME, image=image)

# Served at https://eygentic.tech through a Cloudflare Worker (deploy/eygentic-proxy), which reaches this app by its
# modal.run name. The spending limits live here so they are visible and certain: at most $0.50 a search, $10 a day, and
# $50 in all from 3 November, after which the demo starts nothing new. Not secret; listed after the secret so these win
# over any older values in it.
PUBLIC_SETTINGS = modal.Secret.from_dict({
    "AGENT_PUBLIC_URL": "https://eygentic.tech",
    "AGENT_PUBLIC_ALSO_HOSTS": "gtmshortlist--gtm-shortlist-agent-web.us-east.modal.run",
    "AGENT_RUN_BUDGET_USD": "0.50",
    "AGENT_PUBLIC_DAILY_USD": "10",
    "AGENT_PUBLIC_TOTAL_USD": "50",
    "AGENT_PUBLIC_TOTAL_SINCE": "2026-11-03T00:00:00+00:00",
})


class VolumeCommits:
    """Saves are atomic files on the volume; commit them every few seconds instead of on every progress event."""

    def __init__(self, every: float = 3.0):
        self.pending = threading.Event()
        threading.Thread(target=self.loop, args=(every,), name="volume-commits", daemon=True).start()

    def __call__(self):
        self.pending.set()

    def loop(self, every: float):
        while True:
            self.pending.wait()
            self.pending.clear()
            try:
                volume.commit()
            except Exception as exc:  # noqa: BLE001 - thread boundary: retry with the next change, keep serving
                print(f"Volume commit failed: {exc}")
                self.pending.set()
            threading.Event().wait(every)


# One container keeps the per-visitor limits, the running searches and the files in one place.
@app.function(secrets=[modal.Secret.from_name("gtm-shortlist-agent"), PUBLIC_SETTINGS], volumes={"/data": volume},
              min_containers=1, max_containers=1, timeout=1800, memory=1024)
@modal.concurrent(max_inputs=100)
@modal.asgi_app()
def web():
    from shortlist_agent.public import create_public_app
    return create_public_app(after_write=VolumeCommits())
