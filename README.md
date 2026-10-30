# dont-waste-my-time

An executive-grade communication skill for Claude Code, also portable to claude.ai skills. It makes Claude research, reason, write, design, translate and quality-check material for senior decision-makers: board decks, director dashboards, management reports, memos, business cases, research-backed recommendations, and Portuguese/English business translation.

Governing rule: **maximize decision value per unit of the reader's attention, and of the user's.** Polish never substitutes for reasoning or evidence, and brevity never removes a material caveat.

## What it changes

- **Executive briefing protocol.** For a substantial new deliverable, Claude asks for the audience, style, objective, detail level and constraints once, as one compact message with predefined options and defaults. It skips anything you already said, and "defaults" means go. Quick tasks (a rewrite, a short translation) get no questions at all.
- **Production profiles.** Board/CEO, Director, Analytical leadership, Operational and Business case. Profiles combine with each other and with length budgets per detail level. Explicit instructions always override them.
- **Answer-first reasoning.** Takeaway titles, the "so what" test, and facts kept separate from interpretation and recommendation.
- **Evidence integrity.**
  - No fabricated numbers, sources or "illustrative" figures, and no invented consultations or approvals.
  - Visible `[TBD: what, owner]` placeholders where data is missing.
  - Only sources actually opened are cited.
  - Inconsistencies in your material are flagged, not silently fixed.
- **Domain playbooks**, loaded only when needed:
  - decks (storyline before slides);
  - dashboards (decisions before KPIs; polarity-aware status);
  - charts (evidence-based encoding, honesty and contrast rules);
  - documents (memo, board paper, business case templates);
  - research (source log, verification, delegation);
  - translation (locale conventions, PT→EN glossary).
- **A quality gate on the actual artifact**, with helper scripts:
  - a heuristic fluff linter (EN/PT);
  - a numeric tracer that flags numbers not traceable to the inputs;
  - a translation numeric-fidelity check;
  - a renderer that screenshots decks, documents and HTML, reports console errors and overflow, and finds clipped containers.
- **Composition.** It works alone, and it cooperates with available skills (pptx, docx, xlsx, frontend, data). It keeps ownership of the brief, the storyline, the evidence standards and the final QA.

## Install

**As a Claude Code plugin (recommended).** In Claude Code 2.1.275 or later:

```
/plugin install dont-waste-my-time --marketplace bnthrxrp/dont-waste-my-time
```

On earlier versions:

```
/plugin marketplace add bnthrxrp/dont-waste-my-time
/plugin install dont-waste-my-time@dont-waste-my-time
```

**As a personal skill.** Copy the skill folder:

```
git clone https://github.com/bnthrxrp/dont-waste-my-time
cp -r dont-waste-my-time/skills/dont-waste-my-time ~/.claude/skills/
```

**On claude.ai.** Zip `skills/dont-waste-my-time/` and upload it under Settings → Capabilities → Skills. The frontmatter uses only portable fields (name, description, license, metadata).

**Requirements for the helper scripts:**
- Python 3 with python-pptx, python-docx and openpyxl;
- LibreOffice and pdftoppm for rendering decks and documents;
- Node with Playwright for rendering HTML.

Every script degrades gracefully and says what is missing.

## Use

The skill triggers automatically on executive-material requests: "make this board-ready", "turn this report into a 3-minute narrative", "build a dashboard for our directors", "translate this deck into English", "tighten this email to my VP". To invoke it explicitly, use `/dont-waste-my-time:dont-waste-my-time` (plugin) or `/dont-waste-my-time` (personal skill).

**Standing defaults.** Add a line to CLAUDE.md, memory or project instructions to skip those briefing questions every time, for example:

```
dont-waste-my-time defaults: audience=Board/CEO; style=financial+executive; detail=ultra-concise; language=pt-BR; deck format=pptx
```

## Layout

```
.claude-plugin/            plugin.json, marketplace.json
skills/dont-waste-my-time/
  SKILL.md                 core operating model (triage, briefing, rules, composition, quality gate)
  references/              loaded on demand
    briefing.md            questionnaire (EN/PT), profiles, length budgets
    analysis.md            method selector, variance analysis, business cases, decision hygiene
    writing.md             structures, templates, sentence rules, anti-fluff (EN/PT)
    presentations.md       storyline-first workflow, slide anatomy, production paths, deck QA
    dataviz.md             chart chooser, integrity rules, color and contrast, business notation
    dashboards.md          decision-first workflow, KPI spec, polarity/status logic, HTML build and tests
    research.md            source discipline, verification, delegation briefs (Haiku research, Sonnet validation)
    translation.md         PT↔EN locale conventions, glossary, file handling, QA
    quality-gate.md        checklist, rubric, blocking defects, independent review
  scripts/                 doc_text.py, fluff_lint.py, numbers_check.py, render.py
evals/                     14 test cases (claude plugin eval format; multi-turn cases add turns.json)
tests/                     fixtures generator, headless eval harness, blind grading helpers, script unit tests, results
research/                  research dossiers (Layer 1), validation reports (Layer 2), synthesis
```

## How it was built

1. **Research.** Five Haiku research streams covered strategy and problem solving, data visualization, storytelling and writing, dashboards and board materials, and translation. A targeted Haiku revision followed for the weakest stream.
2. **Validation and synthesis.** Sonnet validators re-opened sources, issued claim-by-claim verdicts and turned the evidence into operational rules. A Sonnet synthesis integrated them. Claims that couldn't be verified are excluded or labeled; see `research/`.
3. **Baseline (RED).** The 14 test cases ran without the skill on Opus, and 7 on Haiku. That recorded where the bare model actually fails (`tests/results/baseline-observations.md`), so the skill targets real failure modes instead of re-teaching what the model already does well.
4. **Implementation and testing.** Opus wrote the core and orchestrated domain writers. All files were reviewed, contrast ratios recomputed and scripts tested (unit tests in `tests/scripts/`). The skill was tested headlessly with real skill discovery and blind A/B grading against the baselines; see `tests/results/`.

## Running the tests

```
python3 tests/fixtures/build_fixtures.py        # regenerate input files
python3 tests/define_cases.py                    # regenerate evals/ from the case definitions
python3 tests/run_evals.py --mode with --iteration my-run --parallel 4      # with the skill
python3 tests/run_evals.py --mode without --iteration my-baseline           # without
python3 -m unittest discover -s tests/scripts    # script unit tests
```

Runs are isolated headless `claude -p` sessions, so they are real, billed model runs. Outputs go to `$DWMT_WORKSPACE`, which defaults to `~/dwmt-workspace`, outside the repo so test sessions can't see the graders. The single-turn cases also run under `claude plugin eval . --scaffold`.

## License

MIT
