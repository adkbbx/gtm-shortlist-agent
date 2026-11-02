"""The local agent (shortlist_agent.local) with LABELLED SYNTHETIC providers, for browser tests on port 8015.

Invented .example companies and scripted model answers: no network, no keys, nothing spent."""
import tempfile
from pathlib import Path

import uvicorn

from shortlist_agent.local import create_local_app
from shortlist_agent.settings import AgentSettings
from shortlist_agent.synthetic import synthetic_providers

data = tempfile.TemporaryDirectory(prefix="gtm-shortlist-local-")
application = create_local_app(Path(data.name) / "agent.sqlite3")
service = application.state.agent_service
service.settings = lambda: AgentSettings()
service.providers = lambda agent_settings: synthetic_providers(pace=0.08)
service.history_days = None  # journeys share one database but are independent: no earlier-search history

if __name__ == "__main__":
    try:
        uvicorn.run(application, host="127.0.0.1", port=8015, log_level="warning")
    finally:
        data.cleanup()
