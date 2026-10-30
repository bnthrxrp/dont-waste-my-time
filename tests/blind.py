#!/usr/bin/env python3
"""Prepare blind A/B copies of with-skill and baseline runs for grading, and un-blind the results.

  python3 tests/blind.py prepare --with-iter iter-1 --without-iter baseline [--cases a,b]
      -> tests/workspace/blind-<with-iter>/<case>/{A,B}/ (work/ + redacted transcript.md) and mapping.json
  python3 tests/blind.py report --with-iter iter-1
      -> reads grading-A.json / grading-B.json / comparison.json written by graders and prints a summary table,
         writing tests/workspace/blind-<with-iter>/results.json

Redaction removes the skill name, run-mode directory names and skill reference paths from transcripts so graders
cannot tell which run had the skill. Order alternates by case index so "A" is not always the skill.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = Path(os.environ.get("DWMT_WORKSPACE", str(Path.home() / "dwmt-workspace")))
REDACT = [
    (re.compile(r"dont-waste-my-time:dont-waste-my-time"), "[skill]"),
    (re.compile(r"dont[-_ ]waste[-_ ]my[-_ ]time", re.I), "[project]"),
    (re.compile(r"with(out)?_skill"), "run"),
    (re.compile(r"\$\{CLAUDE_SKILL_DIR\}|/skills/\[project\]/(references|scripts)/"), "<skill-dir>/"),
]


def redact(text: str) -> str:
    for pat, rep in REDACT:
        text = pat.sub(rep, text)
    return text


def prepare(with_iter: str, without_iter: str, cases: list[str] | None):
    out = WS / f"blind-{with_iter}"
    out.mkdir(parents=True, exist_ok=True)
    mapping = {}
    all_cases = sorted(p.name for p in (WS / with_iter).iterdir() if p.is_dir())
    for i, case in enumerate(c for c in all_cases if not cases or c in cases):
        w = WS / with_iter / case / "with_skill"
        b = WS / without_iter / case / "without_skill"
        if not (w.exists() and b.exists()):
            print(f"skip {case}: missing run(s)")
            continue
        order = {"A": w, "B": b} if i % 2 == 0 else {"A": b, "B": w}
        mapping[case] = {k: ("with" if v == w else "without") for k, v in order.items()}
        for label, src in order.items():
            dst = out / case / label
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src / "work", dst / "work")
            (dst / "transcript.md").write_text(redact((src / "transcript.md").read_text(encoding="utf-8")), encoding="utf-8")
        print(f"prepared {case}: A={mapping[case]['A']}")
    (out / "mapping.json").write_text(json.dumps(mapping, indent=2))


def report(with_iter: str):
    out = WS / f"blind-{with_iter}"
    mapping = json.loads((out / "mapping.json").read_text())
    rows = []
    for case, m in sorted(mapping.items()):
        row = {"case": case}
        for label in ("A", "B"):
            g = out / case / f"grading-{label}.json"
            if g.exists():
                d = json.loads(g.read_text())
                exp = d.get("expectations", [])
                row[m[label]] = {"passed": sum(e["passed"] for e in exp), "total": len(exp),
                                 "quality": d.get("quality_score")}
        c = out / case / "comparison.json"
        if c.exists():
            d = json.loads(c.read_text())
            win = d.get("winner")
            row["preferred"] = m.get(win, "tie") if win in ("A", "B") else "tie"
            row["margin"] = d.get("margin")
        rows.append(row)
    (out / "results.json").write_text(json.dumps(rows, indent=2))
    print(f"{'case':32} {'with':>10} {'without':>10} {'q_with':>7} {'q_wo':>5}  preferred")
    for r in rows:
        w, wo = r.get("with", {}), r.get("without", {})
        print(f"{r['case']:32} {w.get('passed','-')}/{w.get('total','-'):<8} {wo.get('passed','-')}/{wo.get('total','-'):<8} "
              f"{w.get('quality','-'):>7} {wo.get('quality','-'):>5}  {r.get('preferred','-')} {r.get('margin') or ''}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--with-iter", required=True)
    p.add_argument("--without-iter", required=True)
    p.add_argument("--cases")
    r = sub.add_parser("report")
    r.add_argument("--with-iter", required=True)
    a = ap.parse_args()
    if a.cmd == "prepare":
        prepare(a.with_iter, a.without_iter, a.cases.split(",") if a.cases else None)
    else:
        report(a.with_iter)


if __name__ == "__main__":
    main()
