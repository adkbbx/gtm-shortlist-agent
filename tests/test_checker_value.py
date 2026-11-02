"""scripts/checker_value.py over a SYNTHETIC search: the checker's decisions are counted and, without it, the company
that only integrates with the competitor would be wrongly Rejected."""
import sys
from pathlib import Path

from shortlist_agent.pipeline import AgentRunner
from shortlist_agent.synthetic import synthetic_providers

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from checker_value import markdown, measure


def test_the_checker_s_work_is_measured_without_model_calls():
    result = AgentRunner(synthetic_providers(), budget_usd=1.0).run("https://seller.example/")
    measured = measure([result])
    assert measured["searches"] == 1 and measured["quotes_judged"] > 0
    assert sum(measured["decisions"].values()) == measured["quotes_judged"]
    # Oak and Pine only integrates with RivalDesk: the checker keeps it out of Rejected; without it, it is Rejected.
    assert {"seller": "https://seller.example/", "company": "oakandpine.example", "with": "needs_look",
            "without": "rejected"} in measured["changed"]
    report = markdown(measured)
    assert "would have been Rejected" in report and "oakandpine.example" in report
