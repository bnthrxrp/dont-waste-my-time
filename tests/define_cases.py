#!/usr/bin/env python3
"""Single source of truth for the evaluation cases. Writes evals/<case>/ in the
`claude plugin eval` layout (prompt.md, case.yaml, graders/, files/, place-files.sh)
plus turns.json for multi-turn cases, which only tests/run_evals.py reads.

Usage: python3 tests/define_cases.py   (from the repo root; run build_fixtures.py too)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"

SETTINGS = """---
tags: [dont-waste-my-time{extra}]
max_turns: {max_turns}
timeout_seconds: {timeout}
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, WebSearch, WebFetch, Task]
---
"""

PROCEED = "Use your best judgment for anything I didn't specify and go ahead."

# Each case: prompt, input file (or None), expected outcome, graders, optional turns.
# "scope" on a grader: "all" (default) or "with_skill" (only meaningful when the skill is loaded).
CASES = [
    {
        "name": "translate-pt-board-deck",
        "tags": ["translation", "core"],
        "max_turns": 60, "timeout": 2400,
        "file": "apresentacao_resultados_3T26.pptx",
        "prompt": "Translate this deck into English — I'm presenting it to the global board next week. Keep it as a PowerPoint.",
        "if_asked": PROCEED,
        "expected": "An English .pptx with the same 6 slides, every number preserved and reformatted to English conventions, "
                    "Brazilian commercial jargon translated by meaning, the September-estimate caveat kept, speaker notes "
                    "translated, and the headline/table budget-variance discrepancy flagged rather than silently changed.",
        "graders": [
            "An English .pptx file was produced (separate from the original) with the same number of slides as the source (6).",
            "Every number in the source survives with the same value, converted to English conventions (e.g. 'R$ 48,7 mi' -> R$48.7M or BRL 48.7 million; '41,2%' -> 41.2%; '-1,8 p.p.' -> -1.8 pp or percentage points; '15/11/2026' -> 15 Nov 2026 or November 15, 2026); none are dropped, altered or added.",
            "Business terms are translated by meaning and used consistently: orçado -> budget, realizado -> actual, meta -> target, ruptura -> out-of-stock, verba promocional -> promotional/trade spend, ticket médio -> average ticket/order value, positivação -> active-outlet coverage / numeric distribution (or an equivalent explained term).",
            "The footnote caveat that IQVIA sell-out data runs only through August and September is estimated is preserved in the translated deck.",
            "The run notices and flags to the user that the headline says 2.1% below budget while the table total implies -2.0% (or flags another genuine ambiguity in the source) instead of silently changing a figure.",
            "Speaker notes are translated too (or the response states explicitly how notes were handled).",
            "Before translating, the run did not send the user a multi-question briefing questionnaire (at most one targeted question).",
        ],
    },
    {
        "name": "dense-report-to-narrative",
        "tags": ["report", "core"],
        "max_turns": 40, "timeout": 1800,
        "file": "commercial_performance_report_sep2026.md",
        "prompt": "Our directors won't read this 10-section report. Turn it into an executive narrative they can read in 3 minutes before Monday's leadership meeting. Save it as executive_narrative.md.",
        "if_asked": PROCEED,
        "expected": "A short answer-first narrative that surfaces the buried story: growth is price-driven with volume falling, "
                    "sell-in is running ahead of sell-out so trade inventory is above the agreed range and the full-year "
                    "forecast is exposed to destocking, promotions are losing money, and it ends with specific actions.",
        "graders": [
            "executive_narrative.md exists and its main body is at most about 600 words (readable in roughly 3 minutes).",
            "The first paragraph states the central conclusion (e.g. growth is price-driven / full-year forecast at risk) rather than background or an introduction.",
            "It states that the +4.0% year-over-year growth is price-driven (price +6.8%) while volume declined (-3.1%).",
            "It identifies the sell-in (+4.0%) vs sell-out (+0.7%) gap and trade inventory of 6.8 weeks against the agreed 4-6 week range as a risk to Q4 / the full-year forecast.",
            "Any figure not stated in the source (e.g. ~$12.6M exposure = 1.6 extra weeks x $7.9M/week, or a revised full-year number) is labeled as an estimate or calculation and its basis is shown; no number contradicts the source.",
            "It flags the deterioration in trade promotion effectiveness (average ROI 0.82 vs 1.07, 3 of 11 national promotions below 1.0, and/or trade spend +18%).",
            "It ends with specific actions or decisions (e.g. reset Q4 sell-in / forecast, stop or redesign negative-ROI promotions, Somnis recovery, OTIF fix), not generic statements like 'continue to monitor'.",
            "It contains no generic filler (e.g. 'in today's rapidly evolving landscape', 'holistic overview') and does not repeat the source's unsupported 'solid performance' framing as fact.",
        ],
    },
    {
        "name": "director-dashboard-spec",
        "tags": ["dashboard", "core"],
        "max_turns": 40, "timeout": 1800,
        "file": "available_data.md",
        "prompt": "Design the spec for a weekly dashboard for our Commercial Director (Brazil consumer health). Our BI team will build it in Power BI, so I need a specification they can build from, not the dashboard itself. This is the data we have.",
        "if_asked": PROCEED,
        "expected": "A buildable specification that starts from the director's decisions and questions, defines a short list of "
                    "headline KPIs with formulas, sources, latency, targets and polarity, handles the weekly-vs-monthly "
                    "latency mismatch and data-quality caveats, defines layout hierarchy, chart choices, RAG logic, "
                    "interactions and states, and does not invent targets.",
        "graders": [
            "The spec starts from the decisions or management questions the Commercial Director must answer, before listing KPIs.",
            "Each headline KPI has a definition, formula or source field, refresh/latency, a target or threshold (or an explicit 'to be confirmed'), and polarity (which direction is good).",
            "It addresses the data latency/grain mismatches and quality caveats in the source (IQVIA sell-out monthly with ~4-week lag versus a weekly dashboard; retail-audit sample skew; CRM outlet duplicates) and says how the dashboard shows them.",
            "It defines a visual hierarchy/layout (what sits at the top vs drill-down) and chart choices justified by the question each answers.",
            "RAG/status colors are defined by business thresholds and metric polarity, not merely by up/down movement.",
            "It specifies interactions (filters, drill-downs) and non-happy-path states (stale data, missing data, loading/empty/error) or explicitly scopes them out.",
            "The top level is limited to a focused set of headline KPIs (roughly 9 or fewer) rather than every available metric.",
            "It does not invent targets absent from the data description; the OOS threshold is labeled informal (5%) or to-be-confirmed.",
        ],
    },
    {
        "name": "research-strategic-question",
        "tags": ["research", "core"],
        "max_turns": 80, "timeout": 3600,
        "file": None,
        "prompt": "Should a mid-sized Brazilian pharmaceutical distributor build its own B2B e-commerce platform for independent pharmacies, or partner with an existing marketplace? I need a 2-page research-backed memo for our CEO, with sources I can verify. Save it as memo.md.",
        "if_asked": PROCEED,
        "expected": "A ~2-page memo that opens with a recommendation (possibly conditional), compares build vs partner (and "
                    "hybrid) on explicit criteria, cites real verifiable sources for market facts, separates facts from "
                    "interpretation and assumptions, and lists the company-specific unknowns instead of inventing them.",
        "graders": [
            "memo.md exists, is roughly two pages (about 600-1,300 words), and opens with a recommendation or direct answer.",
            "It cites sources with URLs; for three cited claims checked by fetching the URLs, each URL resolves and supports the claim attributed to it.",
            "It distinguishes verified facts from estimates, interpretation and assumptions (explicit labels or unambiguous wording).",
            "It compares the options (build vs partner, and possibly a hybrid/phased path) on explicit criteria and states the conditions under which the recommendation would change.",
            "It lists company-specific unknowns the CEO's team must supply (e.g. own margins, customer base, IT capability, capital) instead of inventing company figures.",
            "No statistic is presented without attribution; no fabricated figures or sources.",
        ],
    },
    {
        "name": "improve-weak-deck",
        "tags": ["presentation", "improve", "compose", "core"],
        "max_turns": 80, "timeout": 3600,
        "file": "q3_business_review.pptx",
        "prompt": "This Q3 review deck goes to our division president on Thursday and it's weak — fix it. Give me the improved .pptx.",
        "if_asked": PROCEED,
        "expected": "A rebuilt .pptx that leads with the decision (exit the loss-making Brandt contract before the Dec 31 notice "
                    "deadline; fix raw-material price pass-through), uses action titles, replaces the 3D pie, removes filler "
                    "slides and vague next steps, states the key numbers correctly, plus a short change summary.",
        "graders": [
            "An improved .pptx file was produced (not only advice).",
            "The first content slide states the main message or decision (e.g. exit the Brandt contract — notice due by Dec 31 — and/or fix price pass-through on +14% raw materials) rather than an agenda or background.",
            "Slide titles are action titles (full-sentence takeaways), not topic labels like 'Sales Overview' or 'Market Data'.",
            "The 3D pie chart is replaced by a more appropriate chart (e.g. sorted bar of revenue or variance by region) or removed with a stated reason.",
            "Key numbers are stated correctly where used: revenue $86.2M vs $88.7M prior-year Q3 (-2.8%), gross margin 23.4% vs 27.9% (-4.5 pp), raw materials +14% vs price +2%, Brandt contract ~$1.4M/yr loss.",
            "Filler slides (Agenda, Background, Thank You) and vague next steps ('Continue monitoring', 'Improve communication') are removed or replaced with specific actions (owner and/or date).",
            "The response includes a concise summary of what changed and why.",
            "The produced deck opens and renders (the run verified it, e.g. by rendering to images/PDF, or the grader can render it).",
        ],
    },
    {
        "name": "simple-rewrite",
        "tags": ["writing", "simple", "core"],
        "max_turns": 10, "timeout": 600,
        "file": None,
        "prompt": "Tighten this for an email to my VP:\n\n\"Hi Mark, I just wanted to reach out and touch base regarding the status of the Q4 pricing project. As you may already be aware, we have been working very hard on this initiative over the past several weeks. At this point in time, we have completed the analysis for 8 of the 10 categories, and we expect that we will be able to finish the remaining 2 categories by next Friday, assuming that we receive the data from the finance team on time. I would like to take this opportunity to ask whether it would be possible for you to help us expedite the data request with finance. Please let me know your thoughts at your earliest convenience.\"",
        "expected": "A short rewrite (about 60 words or fewer) that keeps every fact, puts the ask up front, with no questions, "
                    "research, delegation or long commentary.",
        "graders": [
            "The rewritten email is about 60 words or fewer and keeps every fact: 8 of 10 categories done, the remaining 2 by next Friday, dependent on finance data arriving on time, and the request to help expedite the finance data.",
            "The request to Mark is explicit and appears in the first two sentences.",
            "The run spawned no subagents, did no web search, and asked no clarifying questions.",
            "Apart from the rewrite, the response has at most one or two short lines of commentary.",
        ],
    },
    {
        "name": "dashboard-html-directors",
        "tags": ["dashboard", "html", "compose", "core", "briefing"],
        "max_turns": 80, "timeout": 3600,
        "file": "monthly_kpis.csv",
        "prompt": "Build an analytical dashboard for our directors to track commercial performance from this data. A single HTML file is fine.",
        "if_asked": PROCEED,
        "expected": "A self-contained, working HTML dashboard that leads with what needs attention, shows KPI cards with actual vs "
                    "budget/target and prior year with polarity-correct status colors (DSO, inventory weeks and complaints "
                    "are lower-is-better), uses honest charts, working filters if any, values matching the CSV, and "
                    "visible data definitions — without re-asking audience or style.",
        "graders": [
            "A single self-contained HTML file was produced and it loads in a browser without JavaScript errors.",
            "Headline KPI cards show the actual value, a comparison (budget/target and/or prior year) and the variance with direction.",
            "Status coloring respects metric polarity: rising DSO, inventory weeks and customer complaints are shown as unfavorable.",
            "Values shown match the CSV (spot-check: YTD Jan-Sep total net sales across channels, and one monthly value).",
            "The top of the dashboard surfaces what needs attention (exceptions or key insights), not only charts.",
            "Charts state units and periods; no 3D effects; bar charts start at zero; no misleading dual axes.",
            "Every filter or drill-down control present actually changes what is displayed.",
            "Data definitions/provenance (source, period covered, metric definitions) are visible somewhere in the dashboard.",
            "The run did not ask the user for the audience or communication style (both were given in the request).",
        ],
    },
    {
        "name": "incomplete-data-summary",
        "tags": ["report", "data-gaps", "core"],
        "max_turns": 30, "timeout": 1500,
        "file": "regional_kpis_oct2026.csv",
        "prompt": "Write the October performance summary for tomorrow's directors' meeting — performance vs target and vs last year by region, and what needs attention. Save as october_summary.md.",
        "if_asked": PROCEED,
        "expected": "A director-ready October summary that leads with what needs attention, computes variances correctly for "
                    "complete data, and explicitly flags every gap (East October sales missing, North target and September "
                    "row missing, West has no prior year, South 143% margin is invalid) without imputing values or hiding "
                    "gaps inside totals.",
        "graders": [
            "october_summary.md exists.",
            "It explicitly flags each data issue: East October net sales missing; North October target missing (and North September row missing); West has no prior-year data; South October gross margin of 143% is invalid.",
            "It does not fabricate or silently impute any missing value.",
            "Any total or aggregate states which regions it includes or excludes; missing data is never silently mixed into totals.",
            "Variances computed for complete data are correct (e.g. Central October +2.0% vs target and +4.8% vs prior year; South October +6.3% (or +6.2%) vs target and +11.5% vs prior year).",
            "It opens with what needs attention rather than a data description.",
        ],
    },
    {
        "name": "briefing-answers-all",
        "tags": ["briefing", "presentation"],
        "max_turns": 80, "timeout": 3600,
        "file": "pricing_2027.xlsx",
        "prompt": "I need to put together a presentation on our 2027 pricing strategy for the consumer health portfolio. The data is in pricing_2027.xlsx.",
        "turns": ["Audience: C-suite. Style: financial and performance-oriented. Objective: get approval for the pricing plan. Detail: executive standard. Constraints: max 10 slides, English, .pptx."],
        "expected": "Turn 1 is a compact briefing (single message, predefined options, defaults shown, nothing already known re-asked). "
                    "Turn 2 confirms the configuration in one line and builds a <=10-slide English .pptx for the C-suite with a "
                    "financial emphasis that asks for approval, using only numbers from the workbook or labeled estimates.",
        "graders": [
            "Turn 1: the assistant asks a compact briefing in a single message (audience, style, objective, detail level; constraints only if unknown) with predefined numbered options or an equivalent choice widget and stated defaults; it does not ask for information already given (topic, data file).",
            "Turn 1 asks no more than six questions.",
            "Turn 2: the assistant asks no further questions (or one critical question at most), confirms the configuration briefly, and proceeds.",
            "A .pptx of at most 10 slides in English is produced, aimed at the C-suite with a financial/performance emphasis, and explicitly requests approval/decision.",
            "Numbers in the deck come from pricing_2027.xlsx; any derived figure (e.g. revenue impact from price x volume x elasticity) is labeled as an estimate with its assumptions.",
        ],
    },
    {
        "name": "briefing-audience-only",
        "tags": ["briefing", "presentation"],
        "max_turns": 80, "timeout": 3600,
        "file": "pricing_2027.xlsx",
        "prompt": "I need to put together a presentation on our 2027 pricing strategy for the consumer health portfolio. The data is in pricing_2027.xlsx.",
        "turns": ["It's for the directors."],
        "expected": "Turn 1 is a compact briefing. Turn 2 accepts the partial answer, fills the rest with defaults stated in one "
                    "line, does not re-ask, and builds a director-level deck from the workbook without invented numbers.",
        "graders": [
            "Turn 1: the assistant asks a compact briefing in a single message with predefined options and stated defaults.",
            "Turn 2: the assistant accepts the partial answer, applies defaults for the rest (stating them briefly) and does not ask the remaining questions again.",
            "A deck (.pptx or the deck format the run states) is produced at a director level: performance and implications first, balanced detail.",
            "No numbers are invented: figures come from the workbook or are labeled estimates with their basis.",
        ],
    },
    {
        "name": "briefing-use-defaults",
        "tags": ["briefing", "presentation"],
        "max_turns": 80, "timeout": 3600,
        "file": "pricing_2027.xlsx",
        "prompt": "I need to put together a presentation on our 2027 pricing strategy for the consumer health portfolio. The data is in pricing_2027.xlsx.",
        "turns": ["Just use the defaults."],
        "expected": "Turn 1 is a compact briefing. Turn 2 proceeds immediately with the default configuration (directors, balanced, "
                    "executive standard; objective inferred), stated in one line, and builds the deck.",
        "graders": [
            "Turn 1: the assistant asks a compact briefing in a single message with predefined options and stated defaults.",
            "Turn 2: the assistant proceeds immediately with the defaults (stated in about one line) and asks no further questions.",
            "A deck is produced reflecting the default profile (directors, balanced, executive-standard detail).",
            "No numbers are invented: figures come from the workbook or are labeled estimates with their basis.",
        ],
    },
    {
        "name": "quick-translation",
        "tags": ["translation", "simple", "briefing"],
        "max_turns": 8, "timeout": 600,
        "file": None,
        "prompt": "Translate to English, quick: Fechamos o trimestre com faturamento de R$ 12,3 milhões, 4% acima da meta, puxado pelas redes regionais. A margem caiu 1,2 p.p. por conta da verba promocional extra no canal independente.",
        "expected": "An immediate, accurate translation with numbers converted correctly and business terms translated by meaning; "
                    "no questionnaire, no delegation, at most one short note.",
        "graders": [
            "The response gives the translation immediately: no questions, no subagents, no web search.",
            "Numbers are converted correctly: R$12.3 million (or BRL 12.3 million), 4% above target, 1.2 percentage points (pp).",
            "Terms are translated by meaning: faturamento -> revenue/sales, meta -> target, redes regionais -> regional (pharmacy) chains, verba promocional -> promotional/trade spend, canal independente -> independent channel/pharmacies.",
            "Apart from the translation, the response has at most one short note (e.g. on an ambiguous term).",
        ],
    },
    {
        "name": "board-deck-no-data",
        "tags": ["briefing", "presentation", "no-fabrication"],
        "max_turns": 80, "timeout": 3600,
        "file": None,
        "prompt": "I need a board presentation proposing that we enter the Mexican OTC market in 2027.",
        "turns": ["Strategic and financial. Executive standard detail. Max 10 slides, pptx. I don't have the business case numbers with me — build it and mark where the numbers go."],
        "expected": "Turn 1 is a compact briefing that does not re-ask audience (board) or deliverable (presentation) and infers the "
                    "objective (approval) or asks it once. Turn 2 builds a <=10-slide decision deck with the ask up front, "
                    "risks and alternatives, and clearly marked placeholders instead of invented business-case numbers.",
        "graders": [
            "Turn 1: the briefing does not ask who the audience is (the board was stated) or what the deliverable is (a presentation was stated).",
            "Turn 2: a .pptx of at most 10 slides is produced without further questions.",
            "No business-case number is invented: company figures are clearly marked placeholders (e.g. [TBD] / highlighted), and any market figure is attributed to a named source.",
            "The deck is built as a decision: the recommendation/ask appears up front, followed by rationale, financial case (placeholders), risks, alternatives and the decision requested.",
        ],
    },
    {
        "name": "cfo-business-case-memo",
        "tags": ["memo", "briefing", "no-fabrication"],
        "max_turns": 30, "timeout": 1500,
        "file": None,
        "prompt": "I need to get our CFO's approval to hire 3 additional key account managers for the regional pharmacy chains channel. Write the business case memo.",
        "if_asked": "I don't have the numbers with me right now — use clearly marked placeholders and I'll fill them in.",
        "expected": "No questions about audience or objective (both given). Either one targeted question about the missing numbers "
                    "or a memo with clearly marked placeholders; the memo leads with the decision, shows cost, benefit and "
                    "payback logic, risks, alternatives and success metrics, and invents no figures.",
        "graders": [
            "The run does not ask who the audience is or what the objective is (CFO approval was stated).",
            "No cost, revenue or productivity figure is presented as fact without a source; missing numbers are requested in at most one targeted question or shown as clearly marked placeholders/assumptions.",
            "The memo leads with the decision requested and the rationale, and covers cost, expected benefit, payback/break-even logic, risks, alternatives and how success will be measured.",
            "The memo body is concise (about one page, roughly 500 words or fewer excluding placeholders tables).",
        ],
    },
]


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return s.strip("-")[:40]


def main():
    for c in CASES:
        d = EVALS / c["name"]
        (d / "graders").mkdir(parents=True, exist_ok=True)
        for old in (d / "graders").glob("*.md"):
            old.unlink()
        extra = "".join(f", {t}" for t in c["tags"])
        prompt = SETTINGS.format(extra=extra, max_turns=c["max_turns"], timeout=c["timeout"]) + "\n" + c["prompt"]
        if c["file"]:
            prompt += f"\n\nInput files: {c['file']}"
        (d / "prompt.md").write_text(prompt + "\n", encoding="utf-8")
        case_yaml = f'schema_version: "1.1"\nname: {c["name"]}\nexpected_outcome: |\n'
        case_yaml += "".join(f"  {line}\n" for line in c["expected"].splitlines())
        if c["file"]:
            case_yaml += "context:\n  scaffold_script: place-files.sh\n"
            sh = d / "place-files.sh"
            sh.write_text('#!/usr/bin/env bash\nset -eu\ncp -R "$(dirname "$0")/files/." .\n', encoding="utf-8")
            sh.chmod(0o755)
        (d / "case.yaml").write_text(case_yaml, encoding="utf-8")
        for i, g in enumerate(c["graders"], 1):
            body = f"---\ntype: llm\nfocus: trace\nweight: 1\n---\n\n{g}\n"
            (d / "graders" / f"{i:02d}-{slug(g)}.md").write_text(body, encoding="utf-8")
        turns = {"followups": c.get("turns", []), "if_asked": c.get("if_asked")}
        if turns["followups"] or turns["if_asked"]:
            (d / "turns.json").write_text(json.dumps(turns, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {d.relative_to(ROOT)} ({len(c['graders'])} graders)")


if __name__ == "__main__":
    main()
