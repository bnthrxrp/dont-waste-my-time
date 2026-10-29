# Baseline observations (RED phase): Claude Code without the skill

Date: 2026-10-29. Harness: `tests/run_evals.py --mode without --iteration baseline` (isolated headless `claude -p`, default model claude-opus-5-5, scoped tool allowlist). Transcripts and outputs: `$DWMT_WORKSPACE/baseline/` (default `/home/user/dwmt-workspace`, outside the repo; not committed).

## Headline

The bare model is strong at executive work. On most cases it already writes answer-first content, uses takeaway titles, labels derived numbers, flags data gaps and source inconsistencies, renders its own files and composes with the pptx skill. On Opus, the skill's value comes from the specific failure modes below, not from teaching basics. It must not add overhead to what already works. Weaker models (Sonnet, Haiku) are expected to benefit more; see the test report.

## Failure modes the skill must fix

| # | Case | What happened | Skill countermeasure |
|---|---|---|---|
| F1 | cfo-business-case-memo | Invented a full financial model (salaries of $110k, $1.5M incremental sales per KAM, 40% contribution margin, 12-month payback) and put the figures **unbracketed in the headline ask**. Only the softer context got `[brackets]`. A drafting note disclosed this, but if the note is deleted the CFO sees fabricated numbers. | SKILL.md §5: no "illustrative" numbers a reader could mistake for real; one targeted question or visible placeholders; analysis.md business-case conventions. |
| F2 | board-deck-no-data, briefing-* | Never asks anything. Built a 12-slide **HTML** deck in turn 1, then rebuilt it as pptx when the user specified the format: two full builds, $2.79. | SKILL.md §2 briefing. One message, asks only for material unknowns, including format. |
| F3 | cfo memo (~1,400 words), research memo (~1,200 words), incomplete-data summary (~900 words) | Long, thorough documents where the audience needs about a page. | Length budgets by detail level (briefing.md); "shorter whenever nothing material is lost". |
| F4 | dashboard-html-directors | Excellent dashboard, but the channel scorecard table overflows its container (Complaints column clipped). The run did not catch it. | Quality gate: render at desktop and mobile widths, check overflow (render.py reports scrollWidth). |
| F5 | translate-pt-board-deck | Kept "p.p." in a quick translation; deck translation was otherwise excellent (notes, chart labels, discrepancy and misplaced-footnote flags). | translation.md locale table (p.p. → pp / percentage points). |
| F6 | Haiku: board-deck-no-data, cfo-business-case-memo | Saved the finished deck and memo in its own **scratchpad** directory instead of the working directory. The board-deck run never gave the user the path. The work exists, but the user can't find it. | SKILL.md §6: save deliverables in the working directory next to the inputs, never overwrite originals, give paths in the final message (§9). |

## Haiku 5.5 baseline (7 cases, `--model haiku`)

Content quality is close to Opus on the narrative and data-gap cases (answer-first, every gap flagged, derived numbers labeled; ~660-670 words). Haiku's distinctive failure is F6 (deliverables written to scratch space). It also never briefs (F2) and builds the full deck before knowing the format. Outputs: `$DWMT_WORKSPACE/baseline-haiku/`.

## Strengths to preserve (don't regress)

- Flags inconsistencies instead of silently fixing them (translation: -2.1% vs -2.0%, misplaced asterisk; weak deck: price +2% vs revenue per tonne -5.6%; GM 27.9% vs 27.7%).
- Incomplete data: every gap flagged, no imputation, partial totals labeled with the regions they include.
- Dense report: 635 words, answer-first, derived destocking exposure labeled with its basis.
- Dashboard spec: latency-aware, phasing, informal OOS target labeled, outlet duplicates handled.
- Weak deck: used the pptx skill, rebuilt 8 slides with action titles, replaced the 3D pie, rendered and inspected.
- Quick tasks (rewrite, quick translation): immediate, short, no overhead.

## Cost and time reference (baseline)

| Case | Turns | Cost (USD) | Wall time (s) |
|---|---|---|---|
| simple-rewrite | 1 | 0.15 | 8 |
| quick-translation | 1 | 0.14 | 8 |
| incomplete-data-summary | 1 | 0.27 | 46 |
| dense-report-to-narrative | 1 | 0.31 | 52 |
| cfo-business-case-memo | 1 | 0.36 | 84 |
| director-dashboard-spec | 1 | 0.48 | 133 |
| research-strategic-question | 1 | 0.70 | 141 |
| translate-pt-board-deck | 1 | 0.75 | 115 |
| improve-weak-deck | 1 | 1.58 | 303 |
| board-deck-no-data | 2 | 2.79 | 370 |
| briefing-answers-all | 2 | 2.84 | 400 |
| dashboard-html-directors | 1 | 1.83 | 453 |
