"""Shared setup for the script tests: import path, fixture locations, a CLI runner."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "skills" / "dont-waste-my-time" / "scripts"
EVALS = REPO / "evals"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

PT_DECK = EVALS / "translate-pt-board-deck" / "files" / "apresentacao_resultados_3T26.pptx"
WEAK_DECK = EVALS / "improve-weak-deck" / "files" / "q3_business_review.pptx"
REPORT_MD = EVALS / "dense-report-to-narrative" / "files" / "commercial_performance_report_sep2026.md"
PRICING_XLSX = EVALS / "briefing-answers-all" / "files" / "pricing_2027.xlsx"
KPI_CSV = EVALS / "dashboard-html-directors" / "files" / "monthly_kpis.csv"


def run_script(name: str, *args: str, env: dict | None = None) -> subprocess.CompletedProcess:
    """Run a helper script as a subprocess, exactly as Claude would."""
    return subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)],
                          capture_output=True, text=True, timeout=300, env=env)
