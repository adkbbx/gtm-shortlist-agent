"""The agent for one trusted person on their own machine: the agent's routes over a local SQLite file, and the built
pages when they exist. The public demo (shortlist_agent.public) is the hosted way to use it."""
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from shortlist_agent.api import register_agent_routes
from shortlist_agent.public import ui_directory


def create_local_app(db_path: Path, dist_dir: Path | None = None) -> FastAPI:
    app = FastAPI(title="GTM Shortlist agent (local)")
    register_agent_routes(app, db_path)

    @app.exception_handler(KeyError)
    def missing_search(request: Request, exc: KeyError):  # the store raises KeyError for an unknown search
        return JSONResponse({"detail": "This search was not found."}, status_code=404)

    @app.get("/api/health", include_in_schema=False)
    def health():
        return {"status": "ok", "mode": "local"}

    dist = ui_directory(dist_dir)
    if dist is not None:
        app.mount("/", StaticFiles(directory=dist, html=True), name="ui")
    return app
