"""What the second model (Muse Spark Open, the checker) changes, measured on saved live searches with no model calls.

For every live search that used the checker, the same evidence is judged again as if the checker accepted every quote
found on its page (evaluation.without_skeptic), and the same verdict code runs. The difference is the checker's work.

    python scripts/checker_value.py <run.json | folder of run JSON files | agent SQLite file> ... [--markdown out.md]
"""
import argparse
import json
import sqlite3
from collections import Counter
from pathlib import Path

from shortlist_agent.evaluation import without_skeptic
from shortlist_agent.models import RunResult


def load(sources: list[str]) -> list[RunResult]:
    runs: dict[str, RunResult] = {}
    for source in map(Path, sources):
        payloads = []
        if source.is_dir():
            payloads = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(source.glob("*.json"))]
        elif source.suffix in (".sqlite3", ".db"):
            with sqlite3.connect(source) as db:
                payloads = [json.loads(row[0]) for row in db.execute("select payload from agent_runs")]
        else:
            payloads = [json.loads(source.read_text(encoding="utf-8"))]
        for payload in payloads:
            payload = payload.get("payload", payload)  # the demo's files wrap the run in a record
            try:
                run = RunResult.model_validate(payload)
            except ValueError:
                continue
            if run.synthetic or not run.skeptic or run.status != "complete" or run.profile is None:
                continue
            runs.setdefault(run.id, run)
    return list(runs.values())


def label(kind: str | None) -> str:
    return {"shortlisted": "Shortlisted", "needs_look": "Needs a look", "rejected": "Rejected"}.get(kind or "", "none")


def measure(runs: list[RunResult]) -> dict:
    decisions = Counter()
    changed, examples = [], []
    companies = 0
    for run in runs:
        ablated = {c.domain: c for c in without_skeptic(run).companies}
        for company in run.companies:
            if company.status not in ("done", "budget_reached") or company.verdict is None:
                continue
            companies += 1
            judged = [d for d in company.decisions if d.decided_by == "skeptic"]
            decisions.update(d.decision for d in judged)
            evidence = {e.id: e for e in company.evidence}
            for decision in judged:
                item = evidence.get(decision.evidence_id)
                if decision.decision != "supports" and item and decision.reason:
                    examples.append({"seller": run.website, "company": company.domain, "claim": item.claim,
                                     "kind": item.claim_type, "quote": item.quote.text, "source": item.quote.source_type,
                                     "decision": decision.decision, "reason": decision.reason})
            other = ablated.get(company.domain)
            without = other.verdict.kind if other and other.verdict else None
            if without != company.verdict.kind:
                changed.append({"seller": run.website, "company": company.domain, "with": company.verdict.kind,
                                "without": without})
    return {"searches": len(runs), "companies": companies, "decisions": dict(decisions),
            "quotes_judged": sum(decisions.values()), "changed": changed, "examples": examples}


def markdown(result: dict) -> str:
    d = result["decisions"]
    judged = result["quotes_judged"] or 1
    weak = d.get("insufficient", 0) + d.get("contradicts", 0)
    promoted = [c for c in result["changed"] if c["without"] == "shortlisted"]
    demoted = [c for c in result["changed"] if c["without"] == "rejected"]
    lost = [c for c in demoted if c["with"] == "shortlisted"]
    lines = ["# What the checker changes", "",
             (f"Measured on {result['searches']} saved live searches ({result['companies']} companies researched), "
             "with no model calls: each search's evidence is judged again as if the checker accepted every quote found "
             "on its page, and the same verdict code runs."), "",
             (f"- Muse Spark Open judged **{result['quotes_judged']} quotes**: kept {d.get('supports', 0)}, "
             f"found {d.get('insufficient', 0)} too weak and {d.get('contradicts', 0)} contradicted "
             f"(**{weak} thrown out, {weak / judged:.0%}**)."),
             (f"- It changed **{len(result['changed'])} of {result['companies']} verdicts "
             f"({len(result['changed']) / max(result['companies'], 1):.0%})**."),
             f"- Without it, **{len(promoted)} companies would have been Shortlisted** on quotes it threw out.",
             (f"- Without it, **{len(demoted)} companies would have been Rejected**, {len(lost)} of them companies it "
             "Shortlisted. Without a judge, the verdict code counts every quote filed under a disqualifier against the "
             "company: an integration read as using a competitor, but also quotes the agent gathered to show the "
             "opposite (that the company is still operating, or within the seller's size range). The checker decides "
             "which way each quote points, so this number shows how much the design relies on it, not only mistakes it "
             "caught."), ""]
    if result["changed"]:
        lines += ["| Seller | Company | With the checker | Without it |", "|---|---|---|---|"]
        lines += [f"| {c['seller']} | {c['company']} | {label(c['with'])} | {label(c['without'])} |"
                  for c in result["changed"]]
        lines += [""]
    lines += ["## Quotes it threw out (8 of them: disqualifiers it contradicted first, then need and timing)", ""]
    order = {"disqualifier": 0, "need": 1, "timing": 2, "fit": 3}
    examples = sorted(result["examples"], key=lambda e: (e["decision"] != "contradicts", order.get(e["kind"], 4)))
    for e in examples[:8]:
        lines += [f"- **{e['company']}** ({e['kind']}, {e['source'].replace('_', ' ')}): \"{e['quote'][:220]}\"",
                  f"  - Claim: {e['claim'][:200]}", f"  - Checker ({e['decision']}): {e['reason'][:300]}"]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sources", nargs="+")
    parser.add_argument("--markdown")
    args = parser.parse_args()
    result = measure(load(args.sources))
    print(json.dumps({k: v for k, v in result.items() if k != "examples"}, indent=1))
    if args.markdown:
        Path(args.markdown).write_text(markdown(result), encoding="utf-8")


if __name__ == "__main__":
    main()
