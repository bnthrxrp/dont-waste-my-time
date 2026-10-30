# Iteration 1: blind A/B results (with skill vs without)

Run 2026-10-30. Skill snapshot `ad8c818`. Default model claude-opus-5-5, headless `claude -p`, isolated sessions, the plugin loaded from a staged copy. Graders: independent Sonnet agents, blind to which run had the skill (paths and skill names redacted, A/B order alternated per case). Each grader checked the case's assertions in `evals/<case>/graders/`, gave a 1-10 quality score and stated a pairwise preference.

| Case | Assertions with | Assertions without | Quality with | Quality without | Preferred |
|---|---|---|---|---|---|
| board-deck-no-data | 4/4 | 3/4 | 8 | 6 | **with**, clear |
| briefing-answers-all | 5/5 | 2/5 | 7 | 6 | **with**, clear |
| cfo-business-case-memo | 4/4 | 2/4 | 7 | 4 | **with**, clear |
| dashboard-html-directors | 9/9 | 8/9 | 8 | 7 | **with**, clear |
| director-dashboard-spec | 8/8 | 5/8 | 8.5 | 6.5 | **with**, clear |
| dense-report-to-narrative | 8/8 | 8/8 | 8 | 7 | **with**, slight |
| incomplete-data-summary | 6/6 | 5/6 | 8 | 7 | **with**, slight |
| quick-translation* | 4/4 | 4/4 | 9 | 9 | tie |
| translate-pt-board-deck | 7/7 | 7/7 | 8 | 8 | tie |
| improve-weak-deck | 8/8 | 8/8 | 7 | 8 | without, slight |
| simple-rewrite* | 3/4 | 3/4 | 6 | 7 | without, slight |
| research-strategic-question | not graded | | | | |
| briefing-audience-only | not graded | | | | |
| briefing-use-defaults | not graded | | | | |

\* The skill did not trigger on these two quick tasks. Those "with" runs are effectively a second baseline sample.

**Totals over 11 graded cases:** 66/67 assertions with the skill, 55/67 without. Preferred: with 7, tie 2, without 2. Mean quality 7.7 with, 6.9 without. In the 9 cases where the skill triggered, it never lost on assertions.

## What the skill fixed (grader evidence)

- **Fabrication (F1):** the baseline CFO memo put an invented $585K / $4.5M / 12-month payback model unbracketed in the ask. The skill used `[TBD]` placeholders with owners and a breakeven formula.
- **Invented thresholds (F8):** the baseline dashboard spec silently invented about a dozen RAG bands. The skill labeled suggested bands "proposed" and showed the informal 5% OOS only as a grey reference line.
- **Source integrity:** the baseline board deck called one IMARC figure "two independent estimates" (the Research and Markets page resells the IMARC report) and invented time-to-shelf ranges. The skill's figures were attributed correctly.
- **Wasted builds (F2):** without the briefing, the baseline built an unrequested HTML deck and then rebuilt it as pptx. The skill asked one compact briefing, confirmed in one line and built once.
- **Chart honesty:** the baseline dashboard drew a bridge from a truncated $136M axis, and its scorecard was clipped (F4). All the skill's bars started at zero.
- **Correctness:** the skill's weak-deck rebuild gives the correct $4.6M gross-profit decline (88.7 × 27.9% − 86.2 × 23.4%); the baseline's $4.4M is wrong.

## Weaknesses found, and the fixes applied after iteration 1

1. **Placeholder overuse.** Fifteen `[TBD]` markers on seven slides made the improved deck unsendable, which lost improve-weak-deck. Fix: placeholder discipline in SKILL.md §5, presentations.md and writing.md. Placeholders only for decision-relevant missing facts, none in titles, owners proposed by role or collected in one list.
2. **Plain decks.** Graders found the baseline decks better-looking, and the bridge was drawn as plain columns. Fix: presentations.md "Professional, not plain": a visual system, no half-empty slides, true waterfalls.
3. **Quick tasks didn't trigger the skill.** Fix: the description now names quick jobs and the no-overhead fast path (`c13ddd3`); not yet re-tested.
4. **Research overhead.** The research memo ran 3 Haiku streams, a Sonnet validator and a Sonnet reviewer: 585 s and $3.33, against 141 s and $0.70. It was not graded. Fix: SKILL.md now reserves delegated research for multi-stream research deliverables and board or investment decisions resting on outside facts.
5. **Translation polish.** The skill left the Portuguese gloss on a slide and ended with an unneeded "please confirm". Fix in translation.md.
6. **Business-case length.** About 1.5 pages against a one-page memo budget. A business-case row was added to the length budgets.

## Cost and time

Cases where the skill triggered generally cost more, because of reference reading, QA scripts and research. For example:

| Case | With skill | Without |
|---|---|---|
| CFO memo | $0.97 | $0.36 |
| Dashboard spec | $1.10 | $0.48 |
| Board deck | $4.67 | $2.79 |
| Briefing-answers-all | $2.03 | $2.84 |

The briefing case cost less, because the briefing avoided a rebuild.

## Not done in this session

- Iteration 2 (re-running all cases after the fixes above) was not run. The fixes are tested only by review, not by re-run.
- The research memo and the two briefing variants were not graded. Their outputs are in `$DWMT_WORKSPACE`.
- Haiku and Sonnet with-skill runs were not done. Only the Haiku baseline was run (`baseline-observations.md`).
