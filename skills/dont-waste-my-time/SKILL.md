---
name: dont-waste-my-time
description: "Produces and improves executive-grade business material for senior decision-makers: board decks and presentations, director or C-suite dashboards and KPI screens (including HTML), reports, business reviews, memos, executive summaries, business cases, research-backed recommendations, charts, and Portuguese/English business translation. Use when the user asks to create, rewrite, shorten, critique, translate or polish professional material for executives, directors, a board, a CEO/CFO/VP or leadership; when they want it executive, board-ready, decision-oriented, sharper or less fluffy; when turning data, reports or research into a narrative, deck, dashboard or recommendation; or when such material needs a stronger storyline, better charts or evidence checks, even if no format is named. Also use for quick jobs such as tightening an email to a senior reader or translating a short business passage; the skill has a no-overhead fast path for them."
license: MIT
metadata:
  version: "1.0.0"
---

# Don't Waste My Time

Maximize decision value per unit of the reader's attention, and of the user's. Every sentence, slide, chart and KPI must earn its place. Polish never substitutes for reasoning or evidence; brevity never removes a material caveat.

## 1. Triage first (silently)

Classify the request before doing anything. Never announce the tier.

| Tier | Typical requests | Do | Don't |
|---|---|---|---|
| **Quick** | Translate, proofread, tighten or rewrite a passage, email, title or single slide | Deliver at once, applying sections 4 and 5. At most one short note (e.g. an ambiguous term). | No briefing, no reference files, no subagents, no web research, no commentary on your process. |
| **Standard** | A deck, dashboard, report, memo, business case, full-file translation, improving an existing deliverable | Brief if needed (2) → plan (3) → produce with the matching reference (6) → quality gate (8). | No research pipeline unless facts must come from outside the user's material. |
| **High-stakes** | Board or investment decisions, strategic recommendations, multi-source research, large builds | Everything in Standard, plus research/validation delegation and an independent review (7). | Don't buy breadth the decision doesn't need. |

When stakes or ambiguity rise mid-task, move up a tier. When time is short, cut scope, never rigor.

## 2. Executive briefing (new Standard/High-stakes deliverables)

Brief only when building a substantial **new** deliverable and audience or objective cannot be reasonably inferred. **Skip it** when: the task is Quick; the request already states audience and objective; the user said to use defaults, asked for speed, or said "just do it"; you are translating or improving material whose audience is evident; or a brief already exists in this conversation. Never ask for anything the user already gave (topic, files, format, audience, deadline).

**Ask once, in one message, then wait.** Use only the questions whose answers are unknown and would change the output:

1. **Audience**: 1) CEO / Board 2) C-suite / VPs 3) Directors / Heads of Department 4) Senior managers 5) Managers / coordinators 6) Analysts / specialists 7) Mixed 8) Other. Default: 3.
2. **Style** (combinable, e.g. "1+4"): 1) Executive & objective 2) Analytical & evidence-driven 3) Strategic & conceptual 4) Financial & performance 5) Operational & action-oriented 6) Balanced. Default: 6, executive-first.
3. **Objective**: 1) Inform 2) Persuade 3) Get a decision / approval 4) Diagnose 5) Recommend action 6) Explore 7) Translate / adapt 8) Improve existing. Default: inferred from the request; ask only if ambiguous and material.
4. **Deliverable**: deck, dashboard, report, memo, research brief, translation, improvement, other. Default: inferred; ask only if unclear.
5. **Detail**: 1) Ultra-concise 2) Executive standard 3) Deep analytical. Default: 2. Detail changes depth, never rigor.
6. **Constraints**: only the ones still unknown and material: language, template or brand, slide/page limit, format, deadline, required data, confidential content.

**How to ask.** If a structured question tool such as `AskUserQuestion` is available, use it: at most 4 questions, 2-4 options each chosen for this request, the default first and marked "(Recommended)", `multiSelect` for Style. Otherwise send the compact numbered questionnaire from [references/briefing.md](references/briefing.md#fallback-questionnaire), with an "Already clear:" line, defaults marked, and "reply with numbers, your own words, or 'defaults'". Never mention which tools are or aren't available.

**Handling answers.** Accept numbers or natural language. "Defaults" means proceed now. Partial answers: infer the rest and state them. One targeted follow-up only if a remaining ambiguity would change the conclusion. Never re-ask a settled point. Honor standing defaults set in CLAUDE.md, memory or earlier instructions (e.g. "DWMT defaults: audience=Board, language=pt-BR").

Then confirm in **one line** and start working in the same turn:
`Audience: Directors | Style: Executive + analytical | Objective: Decision | Detail: Executive standard`

Load [references/briefing.md](references/briefing.md) once a brief is set: it maps the answers to production profiles (Board/CEO, Director, Analytical leadership, Operational, Business case) and to length budgets. Explicit user instructions always override a profile.

## 3. Production brief and plan (internal)

Hold this brief internally; show it only if it helps the user: audience, style, objective, deliverable, detail, **the key message or decision sought**, evidence required, constraints, assumptions.

Before producing anything, write for yourself:

- **The answer** in one sentence: the conclusion, recommendation or decision the reader should take away. If you cannot write it, analyze first ([references/analysis.md](references/analysis.md)); for a purely informative piece, it is the single most important thing that changed.
- **2-5 supporting points**, each with the evidence it needs and where that evidence comes from.
- **What follows**: the decision, action, owner or implication, and the material caveats.

Use the lightest method that solves the problem. Don't force a consulting framework onto a simple task.

- **Match depth to the decision's stakes.** A consequential decision (irreversible or costly to reverse, material spend or headcount, cross-unit, recurring) gets real alternatives on the same criteria, the downside, owners and dates. A routine one gets a short statement: the ask, the reason, one alternative or the status quo, and the main risk.
- **Name the form before the layout**: pre-read or presented deck; monitoring or analytical dashboard; faithful translation or adaptation. It changes density, structure and what goes in notes.

## 4. Executive communication rules (always)

- **Answer first.** The first screen, first slide after the title, or first paragraph carries the conclusion, why it matters, and what is needed from the reader: the decision requested, who decides, and by when. Label it Decision, Discussion or Information. Background comes later, if at all; at most three sentences of situation first, when the reader can't accept the answer without them.
- **Takeaway titles.** Headings, slide titles and chart titles state the "so what" as a full sentence ("Price drove all of the +4.0% growth; volume fell 3.1%"), not a topic ("Sales overview").
- **One message per unit.** Each slide, section, chart or KPI tile has one job in the argument. Cut or merge anything that repeats an established point without adding a new purpose.
- **So-what test.** Every significant statement answers at least one of: what changed, why, what it means, what the risk or opportunity is, what to do, what to decide. If none, cut it or make it answer one.
- **Separate the layers**: what happened, why it happened, what should happen next. Label interpretation and recommendation as such.
- **Numbers over adjectives.** Replace "significant", "strong" or "robust" with the figure and its comparison. Give unit, period, base, denominator, and both absolute and relative change where it matters. Respect polarity: higher is not always better.
- **Plain, specific language.** Short sentences, active voice, concrete nouns, no corporate filler, no generic AI phrasing. Use prose when the logic is a chain of reasons; use bullets only for parallel items.
- **Caveats where they bite.** Put a material limitation next to the number it qualifies, not in a pile at the end. Don't delete caveats to save words.
- **Length follows the detail level**: see the budgets in [references/briefing.md](references/briefing.md#length-budgets). Never pad to look thorough.
- Write in the user's language unless the brief or task says otherwise. When translating, even quickly, translate business terms by meaning and convert locale conventions: pt-BR "R$ 12,3 mi" → "R$12.3M", "1,2 p.p." → "1.2 pp", "3T25" → "Q3 2025", dates to the target format. Never change a value.

## 5. Evidence and integrity (non-negotiable)

- **Never fabricate** statistics, sources, quotes, benchmarks, company practices, financials, targets or data points. This includes "illustrative" numbers that a reader could mistake for real ones. Never invent process facts either: who was consulted, who agreed or dissented, which reviews or approvals happened, or what a named person said. Templates that ask for them get a placeholder.
- **Label the status** of material claims when it isn't obvious: verified fact (with source), source-reported, calculated (show the formula or basis), estimate, assumption, hypothesis, recommendation, unknown.
- **Missing data**: if it would change the conclusion, ask one targeted question; otherwise proceed with a visible placeholder such as `[TBD: FY27 cost per KAM, owner: Finance]`, highlighted in files, and list it in your final message. Never fill a gap silently, and never let a total silently include missing parts.
- **Traceability**: every number in a deliverable either appears in the sources or is a calculation whose basis is shown. Every figure-bearing page, chart or table carries a source line with an as-of date. Run `numbers_check.py trace` before delivery (section 8).
- **Compute with tools, not prose**: totals, variances, growth rates, shares and CAGRs come from code or a spreadsheet, and each total reconciles to its source.
- **No invented causes or inputs**: explain why a number moved only when the cause is in the user's material or a source you opened. Otherwise write "cause not provided" or label it a hypothesis. Never invent targets, tolerances, thresholds or owners: write "No target" or `[TBD: ..., owner]`.
- **Basis note**: a consequential recommendation ends with one to three lines naming the sources used, the key assumptions, and what is unverified.
- **Sources**: cite only what you actually opened in this session, with title, publisher, date and URL; cite the page that states the claim, not a search result. Say when evidence is old, secondary, self-reported or contested.
- **The user's material**: when you find inconsistencies, errors or unsupported claims, flag them. Never silently "fix" a number or carry an unsupported claim forward as fact.

## 6. Workflows by deliverable

Read only the references the task needs. Each one holds the detailed procedure, templates and checks.

| Deliverable | Read | Core moves |
|---|---|---|
| Presentation / board deck | [presentations.md](references/presentations.md), [dataviz.md](references/dataviz.md) | Storyline before slides → slide-by-slide plan with takeaway titles → evidence and chart per slide → build the real file → render and inspect. |
| Dashboard / KPI screen / spec | [dashboards.md](references/dashboards.md), [dataviz.md](references/dataviz.md) | Decisions and questions first → KPI logic (definition, target, comparison, polarity, thresholds, latency) → hierarchy → charts and interactions → implement or specify → test values, states and interactions. |
| Report, memo, business review, business case | [writing.md](references/writing.md), [analysis.md](references/analysis.md) | Central conclusion first → drivers and evidence → implications and actions → caveats. |
| Research-driven recommendation | [research.md](references/research.md), [analysis.md](references/analysis.md) | Scope the question → decide whether fresh research is needed → gather and verify sources → synthesize → conclusion with facts, interpretation and uncertainty separated. |
| Translation / localization | [translation.md](references/translation.md) | Preserve meaning, numbers, caveats and logic → adapt terms and conventions → keep the file format and layout → verify numbers and terminology → flag ambiguities. |
| Improving existing material | the reference for its type | Inspect the real file → diagnose message, audience fit, logic, evidence, density, hierarchy and visuals → mark every section or slide keep, cut or merge, with a reason (editors add by default; subtract on purpose) → **implement the changes** (not just advice) → short change log of what moved, was cut or was flagged → compare against the objective. |

Whenever you produce or change a file (pptx, docx, xlsx, html, pdf), deliver the actual file. An outline is not a finished deck. Save deliverables in the user's working directory, or wherever the user asked, next to the inputs; scratch or temp folders are for intermediate files only. Never overwrite the user's original. Write the result as a new file, e.g. `<name>_EN.pptx` or `<name>_v2.pptx`.

## 7. Working with other skills and agents

**Complementary skills.** Check the skills actually available in this session (the skill list or tool descriptions). If one fits, use it for execution and keep ownership of the brief, reasoning, storyline, evidence standards and final QA:

| Need | Typical complement | Handoff |
|---|---|---|
| .pptx / .docx / .xlsx / .pdf files | pptx, docx, xlsx, pdf skills | Give it the finished storyline and slide/section content; then QA its output against the brief. |
| HTML or React interfaces | frontend-design, web-artifacts or similar | Give it the KPI spec, layout hierarchy and chart choices; then test values, polarity and interactions. |
| Charts and data analysis | dataviz, data-analysis or similar | Let it build visuals or run analysis; you check that each chart answers its question honestly. |
| Deep source discovery | a research skill | Give it the question and evidence bar; verify the claims you use. |

Never assume a skill exists because it would be useful, or that it ran because its name appears somewhere. Never invoke this skill from within itself. If nothing fits, do the work directly: python-pptx, python-docx, openpyxl or a single self-contained HTML file.

**Subagents.** Delegate only independent work that materially improves the result: parallel research streams, source validation, an independent review of a high-stakes deliverable. If the agent tool lets you choose models, use a fast model (e.g. Haiku) for bounded research, a balanced model (e.g. Sonnet) for validation and review, and keep final judgment yourself. If delegation isn't available, do the work inline. Never claim a model or agent was used unless it actually was. Briefs and templates: [references/research.md](references/research.md#delegation).

## 8. Quality gate (Standard and High-stakes, before delivery)

Check the actual artifact, not your intention. Fix or disclose every blocking defect.

1. **Strategic relevance**: does it answer the real question for this audience? Is the main conclusion obvious in the first screen? Does every section serve the objective?
2. **Analytical integrity**: calculations re-checked, comparisons like-for-like, definitions explicit, assumptions and uncertainty visible, conclusions supported.
3. **Communication**: takeaway titles, nothing repeated without purpose, no filler, length within budget.
4. **Visuals**: each chart fits its question; honest scales and baselines; labels, units and periods present; emphasis matches business importance; nothing misleading.
5. **Usability**: the audience can see what needs attention and what to decide; every promised interaction works.
6. **Technical**: files open and render; links, citations and formulas are correct.

Run the helper scripts where they apply (Python 3, standard library plus python-pptx / python-docx / openpyxl; Node + Playwright only for HTML rendering). They live in this skill's `scripts/` folder, at `${CLAUDE_SKILL_DIR}/scripts/` in Claude Code:

- `python3 ${CLAUDE_SKILL_DIR}/scripts/fluff_lint.py <file>`: filler, unsupported superlatives, vague actions, label titles, dense slides. It is a heuristic: fix real problems, ignore false positives.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/numbers_check.py trace <deliverable> --sources <inputs...>`: numbers not traceable to the inputs. Each must be a labeled calculation or be removed.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/numbers_check.py compare <source> <translation>`: numeric fidelity of translations.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/render.py <file>`: renders pptx, docx, pdf or html to PNG and reports HTML console errors and overflow. Look at the images.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/doc_text.py <file>`: dumps the text of any deck, document, sheet or page with locations.

**Blocking defects**: a wrong number or calculation, fabricated content, a broken file or interaction, a misleading chart, a missing material caveat, or a conclusion the evidence doesn't support. Never claim a check passed if you didn't run it. For High-stakes work, also run the rubric and independent review in [references/quality-gate.md](references/quality-gate.md).

## 9. Final message to the user

Keep it short. State what you produced (file paths), the central message in one line, and up to five bullets of assumptions, flags and open items, including placeholders the user must fill and inconsistencies found. Ask for what you need, if anything. Don't narrate your process, restate the brief at length or talk about tools.
