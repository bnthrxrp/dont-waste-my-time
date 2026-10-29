#!/usr/bin/env python3
"""Run the evals/ cases headlessly with Claude Code, with or without this plugin loaded.

Each run gets a fresh working directory seeded with the case's input files. Multi-turn
cases (turns.json "followups") are continued with --resume. Single-turn cases that end
with a question and no new files get the case's "if_asked" reply once.

Outputs per run: <workspace>/<iteration>/<case>/<mode>/
  work/               the working directory (deliverables land here)
  turn-N.jsonl        raw stream-json transcript per turn
  transcript.md       condensed, human-readable transcript (for graders)
  meta.json           per-turn metrics: tools used, skills invoked, subagents, cost, duration

Usage:
  python3 tests/run_evals.py --mode with --iteration iter-1 [--cases a,b] [--parallel 4]
  python3 tests/run_evals.py --mode without --iteration baseline
  python3 tests/run_evals.py --mode with --iteration iter-1-haiku --model haiku --cases a,b
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
# Outside the repo so test sessions cannot see evals/ (graders) or other repo files.
DEFAULT_WORKSPACE = Path(os.environ.get("DWMT_WORKSPACE", "/home/user/dwmt-workspace"))

# Variables that tie a child process to the parent remote session's event stream.
ISOLATE_ENV = [
    "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_REMOTE_SDK_URL", "CLAUDE_CODE_REMOTE_SESSION_ID",
    "CLAUDE_CODE_MESSAGING_SOCKET", "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDE_CODE_TEE_SDK_STDOUT",
    "CLAUDE_CODE_CCR_EVENT_FLUSH_POLICY", "CLAUDE_CODE_POST_FOR_SESSION_INGRESS_V2",
    "CLAUDE_CODE_SYNC_SESSION_REFS", "CLAUDE_CODE_REMOTE_SEND_KEEPALIVES", "CLAUDE_CODE_SESSION_ATTENDED",
    "CLAUDE_PID", "CLAUDECODE", "CLAUDE_CODE_DEBUG", "CLAUDE_AFTER_LAST_COMPACT", "CLAUDE_CODE_DIAGNOSTICS_FILE",
]

# Scoped permissions for the child session: file tools, web, skills/subagents, and Bash
# limited to the document tooling these tasks need.
ALLOWED_TOOLS = [
    "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "WebSearch", "WebFetch", "Skill", "Task", "Agent",
    "TodoWrite", "ToolSearch", "NotebookEdit",
    *[f"Bash({c}:*)" for c in (
        "python3", "python", "pip", "pip3", "soffice", "libreoffice", "node", "npm", "npx", "ls", "mkdir", "cp", "mv",
        "cat", "head", "tail", "wc", "unzip", "zip", "pdftoppm", "pdftotext", "file", "echo", "find", "grep", "sed",
        "awk", "sort", "diff", "cd", "date", "jq", "markitdown")],
]

PLUGIN_STAGE = DEFAULT_WORKSPACE / "_plugin-stage"


def stage_plugin(workspace: Path) -> Path:
    """Copy only what a user would install (.claude-plugin/ and skills/) so runs can't reach evals/ or tests/."""
    global PLUGIN_STAGE
    PLUGIN_STAGE = workspace / "_plugin-stage"
    if PLUGIN_STAGE.exists():
        shutil.rmtree(PLUGIN_STAGE)
    PLUGIN_STAGE.mkdir(parents=True)
    for part in (".claude-plugin", "skills", "LICENSE", "README.md"):
        src = ROOT / part
        if src.is_dir():
            shutil.copytree(src, PLUGIN_STAGE / part, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "render"))
        elif src.exists():
            shutil.copy2(src, PLUGIN_STAGE / part)
    return PLUGIN_STAGE


QUESTION_TAIL = re.compile(r"\?\s*(\*\*)?\s*$|\?\s*\n", re.M)


def parse_prompt(case_dir: Path) -> str:
    text = (case_dir / "prompt.md").read_text(encoding="utf-8")
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    return text.strip()


def settings(case_dir: Path) -> dict:
    text = (case_dir / "prompt.md").read_text(encoding="utf-8")
    out = {}
    if text.startswith("---"):
        for line in text.split("---", 2)[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip()
    return out


def child_env() -> dict:
    env = dict(os.environ)
    for k in ISOLATE_ENV:
        env.pop(k, None)
    return env


def snapshot(work: Path) -> dict:
    return {str(p.relative_to(work)): p.stat().st_mtime for p in work.rglob("*") if p.is_file()}


def summarize_stream(lines: list[str]) -> dict:
    info = {"texts": [], "tool_uses": [], "skills": [], "subagents": 0, "web_searches": 0, "web_fetches": 0,
            "ask_user_question": 0, "result": None, "session_id": None, "events": []}
    for line in lines:
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = e.get("type")
        if t == "system" and e.get("subtype") == "init":
            info["session_id"] = e.get("session_id")
            info["model"] = e.get("model")
        elif t == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "text" and c["text"].strip():
                    info["texts"].append(c["text"])
                    info["events"].append(("text", c["text"]))
                elif c.get("type") == "tool_use":
                    name, inp = c["name"], c.get("input", {})
                    info["tool_uses"].append(name)
                    info["events"].append(("tool", f"{name} {json.dumps(inp, ensure_ascii=False)[:600]}"))
                    if name == "Skill":
                        info["skills"].append(inp.get("skill") or inp.get("command") or str(inp)[:80])
                    elif name in ("Task", "Agent"):
                        info["subagents"] += 1
                    elif name == "WebSearch":
                        info["web_searches"] += 1
                    elif name == "WebFetch":
                        info["web_fetches"] += 1
                    elif name == "AskUserQuestion":
                        info["ask_user_question"] += 1
        elif t == "user":
            content = e.get("message", {}).get("content")
            if isinstance(content, list):
                for c in content:
                    if c.get("type") == "tool_result":
                        val = c.get("content")
                        if isinstance(val, list):
                            val = " ".join(x.get("text", "") for x in val if isinstance(x, dict))
                        info["events"].append(("result", str(val)[:500]))
        elif t == "result":
            info["result"] = {k: e.get(k) for k in ("subtype", "is_error", "num_turns", "duration_ms", "total_cost_usd")}
            info["session_id"] = e.get("session_id") or info["session_id"]
            info["final_text"] = e.get("result")
    return info


def run_turn(prompt: str, work: Path, out_jsonl: Path, mode: str, max_turns: int, timeout: int, resume: str | None,
             model: str | None = None):
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns),
           "--permission-mode", "acceptEdits", "--allowedTools", *ALLOWED_TOOLS]
    if mode == "with":
        cmd += ["--plugin-dir", str(PLUGIN_STAGE)]
    if resume:
        cmd += ["--resume", resume]
    if model:
        cmd += ["--model", model]
    t0 = time.time()
    with out_jsonl.open("w", encoding="utf-8") as f, open(out_jsonl.with_suffix(".stderr.txt"), "w") as ferr:
        try:
            subprocess.run(cmd, cwd=work, env=child_env(), stdout=f, stderr=ferr, stdin=subprocess.DEVNULL,
                           timeout=timeout, check=False)
            timed_out = False
        except subprocess.TimeoutExpired:
            timed_out = True
    info = summarize_stream(out_jsonl.read_text(encoding="utf-8").splitlines())
    info["wall_seconds"] = round(time.time() - t0, 1)
    info["timed_out"] = timed_out
    return info


def ended_with_question(info: dict) -> bool:
    final = (info.get("final_text") or (info["texts"][-1] if info["texts"] else "")).strip()
    return bool(QUESTION_TAIL.search(final[-800:])) or info.get("ask_user_question", 0) > 0


def run_case(case: str, mode: str, iteration: str, workspace: Path, model: str | None = None) -> dict:
    case_dir = EVALS / case
    run_dir = workspace / iteration / case / ("with_skill" if mode == "with" else "without_skill")
    if run_dir.exists():
        shutil.rmtree(run_dir)
    work = run_dir / "work"
    work.mkdir(parents=True)
    if (case_dir / "files").is_dir():
        shutil.copytree(case_dir / "files", work, dirs_exist_ok=True)
    st = settings(case_dir)
    max_turns, timeout = int(st.get("max_turns", 40)), int(st.get("timeout_seconds", 1800))
    turns_cfg = json.loads((case_dir / "turns.json").read_text()) if (case_dir / "turns.json").exists() else {}
    prompts = [parse_prompt(case_dir)] + list(turns_cfg.get("followups", []))

    turns, session, n = [], None, 0
    queue = list(prompts)
    used_if_asked = False
    while queue:
        msg = queue.pop(0)
        n += 1
        before = snapshot(work)
        info = run_turn(msg, work, run_dir / f"turn-{n}.jsonl", mode, max_turns, timeout, session, model)
        session = info.get("session_id") or session
        after = snapshot(work)
        info["new_or_changed_files"] = sorted(k for k, v in after.items() if before.get(k) != v)
        info["user_message"] = msg
        turns.append(info)
        if (not queue and not used_if_asked and turns_cfg.get("if_asked") and not turns_cfg.get("followups")
                and ended_with_question(info) and not info["new_or_changed_files"]):
            queue.append(turns_cfg["if_asked"])
            used_if_asked = True

    # Condensed transcript for graders.
    md = [f"# {case} — {mode} skill — iteration {iteration}\n"]
    for i, t in enumerate(turns, 1):
        md.append(f"\n## Turn {i}\n\n**User:** {t['user_message']}\n")
        for kind, val in t["events"]:
            if kind == "text":
                md.append(f"\n**Assistant:** {val}\n")
            elif kind == "tool":
                md.append(f"\n`tool_use` {val}\n")
            else:
                md.append(f"\n`tool_result` {val[:300]}\n")
        md.append(f"\n_Files new/changed this turn: {t['new_or_changed_files']}_\n")
        md.append(f"_Result: {t['result']} wall={t['wall_seconds']}s timed_out={t['timed_out']}_\n")
    (run_dir / "transcript.md").write_text("\n".join(md), encoding="utf-8")

    meta = {
        "case": case, "mode": mode, "iteration": iteration, "requested_model": model,
        "turns": [{k: t.get(k) for k in ("user_message", "skills", "subagents", "web_searches", "web_fetches",
                                         "ask_user_question", "result", "wall_seconds", "timed_out",
                                         "new_or_changed_files", "session_id", "model")} | {"tool_counts": _counts(t["tool_uses"])}
                  for t in turns],
    }
    meta["total_cost_usd"] = round(sum((t["result"] or {}).get("total_cost_usd") or 0 for t in turns), 4)
    meta["total_wall_seconds"] = round(sum(t["wall_seconds"] for t in turns), 1)
    meta["skill_invoked"] = any("dont-waste-my-time" in s for t in turns for s in t["skills"])
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def _counts(names):
    out = {}
    for n in names:
        out[n] = out.get(n, 0) + 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["with", "without"], required=True)
    ap.add_argument("--iteration", required=True)
    ap.add_argument("--cases", default="all")
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    ap.add_argument("--model", default=None, help="model alias or id passed to claude --model (default: account default)")
    args = ap.parse_args()
    cases = sorted(p.name for p in EVALS.iterdir() if (p / "prompt.md").exists()) if args.cases == "all" else args.cases.split(",")
    ws = Path(args.workspace)
    if args.mode == "with":
        stage_plugin(ws)
    results = []
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futs = {ex.submit(run_case, c, args.mode, args.iteration, ws, args.model): c for c in cases}
        for fut in as_completed(futs):
            c = futs[fut]
            try:
                m = fut.result()
                results.append(m)
                print(f"[done] {c}: skill={m['skill_invoked']} turns={len(m['turns'])} "
                      f"cost=${m['total_cost_usd']} wall={m['total_wall_seconds']}s", flush=True)
            except Exception as exc:  # keep the batch going
                print(f"[error] {c}: {exc!r}", flush=True)
    summary = ws / args.iteration / f"summary-{args.mode}.json"
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(sorted(results, key=lambda m: m["case"]), indent=2, ensure_ascii=False))
    print(f"summary: {summary}")


if __name__ == "__main__":
    sys.exit(main())
