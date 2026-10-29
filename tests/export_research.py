#!/usr/bin/env python3
"""Export research dossiers and validation reports from a research workflow journal to research/.

Usage: python3 tests/export_research.py <path/to/journal.jsonl>
Writes research/dossiers/<stream>.md (raw Haiku dossier) and research/validation/<stream>.md
(Sonnet validation report). Re-run as more results land; files are overwritten.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STREAMS = {"A": "A-strategy", "B": "B-dataviz", "C": "C-storytelling", "D": "D-dashboards", "E": "E-translation"}


def stream_name(raw: str) -> str:
    """Agents sometimes shorten the stream key; normalize to the canonical file name."""
    return STREAMS.get(raw.strip()[:1].upper(), raw) if raw else raw


def md_dossier(d: dict) -> str:
    out = [f"# Research dossier {d['stream']} (Layer 1, unvalidated)\n",
           f"**Research question.** {d['research_question']}\n",
           "## Key findings\n"]
    for f in d["key_findings"]:
        out.append(f"### {f['id']}. {f['source_title']}\n")
        out.append(f"- **Source:** {f.get('author_or_publisher', 'n/a')}, {f['publication_date']}, <{f['url']}>")
        out.append(f"- **Accessed this session:** {'yes' if f['accessed'] else 'no'} | **Evidence type:** {f['evidence_type']} | **Confidence:** {f['confidence']}")
        out.append(f"- **Finding:** {f['finding']}")
        if f.get("interpretation"):
            out.append(f"- **Interpretation (agent):** {f['interpretation']}")
        out.append(f"- **Limitations:** {f['limitations']}")
        out.append(f"- **Implication for the skill:** {f['implication_for_skill']}\n")
    if d.get("disagreements"):
        out.append("## Disagreements\n")
        for x in d["disagreements"]:
            out.append(f"- **{x['topic']}:** {x['positions']} ({', '.join(x.get('finding_ids', []))})")
        out.append("")
    out.append("## Implementation recommendations\n")
    for r in d["implementation_recommendations"]:
        out.append(f"- [{r['placement_hint']}] {r['rule']} ({', '.join(r['finding_ids'])}). {r['rationale']}")
    out.append("\n## Open questions\n")
    out += [f"- {q}" for q in d["open_questions"]]
    out.append("\n## Sources attempted but not accessed\n")
    out += [f"- <{s['url']}>: {s['reason']}" for s in d["sources_attempted_not_accessed"]]
    return "\n".join(out) + "\n"


def md_validation(v: dict) -> str:
    q = v["dossier_quality"]
    out = [f"# Validation report {v['stream']} (Layer 2, Sonnet)\n",
           f"**Dossier quality:** {q['score_1_to_5']}/5\n"]
    out += [f"- {i}" for i in q["issues"]]
    out.append("\n## Claim checks\n\n| Finding | Verdict | Method | Notes |\n|---|---|---|---|")
    for c in v["claim_checks"]:
        notes = c["notes"].replace("|", "/").replace("\n", " ")
        out.append(f"| {c['finding_id']} | {c['verdict']} | {c['check_method']} | {notes} |")
    if v.get("gap_fills"):
        out.append("\n## Gap fills (validator research)\n")
        for g in v["gap_fills"]:
            out.append(f"- **{g['id']}** {g['finding']} Source: {g['source_title']}, {g['publication_date']}, <{g['url']}>. Why critical: {g['why_critical']}")
    out.append("\n## Operational rules\n\n| Rule | Evidence | Strength | Scope | Placement |\n|---|---|---|---|---|")
    for r in v["operational_rules"]:
        rule = r["rule"].replace("|", "/").replace("\n", " ")
        out.append(f"| {rule} | {', '.join(r['evidence_ids'])} | {r['evidence_strength']} | {r['scope'].replace('|', '/')} | {r['placement']} |")
    out.append("\n## Exclusions\n")
    out += [f"- **{x['concept']}:** {x['reason']}" for x in v["exclusions"]]
    out.append("\n## Unresolved contradictions\n")
    out += [f"- {x}" for x in v["unresolved_contradictions"]]
    out.append("\n## Needs verification\n")
    out += [f"- {x}" for x in v["needs_verification"]]
    return "\n".join(out) + "\n"


def main():
    journal = Path(sys.argv[1])
    (ROOT / "research" / "dossiers").mkdir(parents=True, exist_ok=True)
    (ROOT / "research" / "validation").mkdir(parents=True, exist_ok=True)
    for line in journal.read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        r = e.get("result")
        if not isinstance(r, dict):
            continue
        if "key_findings" in r:
            p = ROOT / "research" / "dossiers" / f"{stream_name(r['stream'])}.md"
            p.write_text(md_dossier(r), encoding="utf-8")
            print("wrote", p.relative_to(ROOT))
        elif "claim_checks" in r:
            p = ROOT / "research" / "validation" / f"{stream_name(r['stream'])}.md"
            p.write_text(md_validation(r), encoding="utf-8")
            print("wrote", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
