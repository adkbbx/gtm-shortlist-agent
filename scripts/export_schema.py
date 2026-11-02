"""Write the API schema the browser types come from (web/generated/openapi.json, then `npm run schema`), and the run
schema the browser checks every saved search against (web/generated/AgentRunView.json)."""
import json
import tempfile
from pathlib import Path

from shortlist_agent.api import AgentRunView
from shortlist_agent.local import create_local_app

root = Path(__file__).resolve().parents[1]
out = root / "web" / "generated"
out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as folder:
    schema = create_local_app(Path(folder) / "schema.sqlite3").openapi()
(out / "openapi.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
(out / "AgentRunView.json").write_text(json.dumps(AgentRunView.model_json_schema(mode="serialization"), indent=2),
                                       encoding="utf-8")
print("wrote", out)
