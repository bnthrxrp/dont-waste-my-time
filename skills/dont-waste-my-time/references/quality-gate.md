# Quality gate: checks, rubric and independent review

Read this before delivering Standard or High-stakes work (SKILL.md section 8). Check the actual artifact (the saved file, its rendered images, its extracted text), never your draft or your intention. After any edit, re-run the checks that edit could affect.

## Contents
- 1. Scope by tier
- 2. Checklist by dimension
- 3. Fast self-tests
- 4. Rubric (High-stakes)
- 5. Blocking defects and disclosure
- 6. Per-format technical checks
- 7. Running the scripts
- 8. Independent review (High-stakes)
- 9. Final-message honesty

## 1. Scope by tier

| Tier | Run | Don't |
|---|---|---|
| Quick | A mental check against SKILL.md sections 4-5: answer first, plain language, numbers unchanged and none invented, caveats kept. | No scripts, rubric, review or report of checks. |
| Standard | The checklist (2) for the dimensions that apply; the self-tests (3) that fit, always including first screen, number trace and consistency when there are numbers; the scripts (7) and format checks (6) for the file type. | No rubric scores or reviewer unless the user asks. |
| High-stakes | Everything in Standard, then the rubric (4) and an independent review (8). Fix, re-run affected checks, re-score. | One review round; a second only after substantial changes. Reviewing never replaces fixing. |

If the tier rises mid-task, the gate rises with it.

## 2. Checklist by dimension

**Strategic relevance**
- The answer sentence from your plan (SKILL.md section 3) appears in the first screen, the first slide after the title, or the first paragraph.
- What the reader must do is explicit: the decision, approval or action, with owner and date when the objective is a decision.
- Every slide, section, chart and KPI maps to a supporting point or to the ask; anything that maps to nothing is cut or moved to the appendix.
- It answers the question asked, not an easier neighbor; if you reframed the question, the material says so.
- Depth matches the audience profile: no operational detail in a board main body, no abstraction without numbers for directors.

**Analytical integrity**
- Every number is in the sources or is a calculation with its basis shown; `numbers_check.py trace` ran on the final file.
- Every derived figure is recomputed from its inputs (totals, growth, shares, margins, variances, CAGR). Parts sum to totals; shares sum to 100% or a note says rounding.
- Comparisons are like-for-like: same period length, perimeter, currency, units and definitions. Percentage-point changes are not written as percent.
- Polarity is right: a fall in a lower-is-better metric (cost, DSO, churn, complaints) shows as favorable.
- No invented or "illustrative" figure anywhere, least of all in the headline or the ask. Gaps are visible `[TBD: ...]` placeholders; partial totals name what they include.
- Each conclusion has its evidence shown; correlation is not stated as cause; a base case is not the best case without a downside shown.
- A recommendation shows at least two genuine alternatives and why each was rejected, or says why none is credible.
- Assumptions and uncertainty sit next to the figures they affect, with a range or sensitivity when they could change the decision.
- Every cited source was opened this session and states the claim on the cited page. Inconsistencies in the user's material are flagged, not silently corrected.

**Communication**
- Titles are full-sentence takeaways; the titles-only read (3) tells the story.
- One message per unit; nothing repeated without a new purpose; numbers replace adjectives, each with unit, period and comparison.
- Interpretation and recommendation are labeled as such; material caveats sit beside the number they qualify.
- Length is within the budget for the detail level. Count words, slides or KPIs; don't estimate.
- One term per concept throughout; number and date formats follow the output language.

**Visuals**
- Each chart answers the question its title states, with a chart type suited to it (ranking, trend, composition, variance).
- Bar and column axes start at zero; a line chart that starts above zero has clearly labeled axis values; charts meant to be compared share a scale.
- A reader who disagrees with the conclusion would still read the same fact from the title and the chart.
- Units, period, source and legend or direct labels are present; no 3-D or decorative effects.
- Highlight color marks what the title talks about; status colors follow polarity; color is never the only cue.
- Chart values equal the values in text, tables and notes.

**Usability**
- Within 30 seconds the reader can see what needs attention and what to decide.
- Each dashboard KPI shows actual, comparison (target, budget or prior period), variance and status, with its definition, period and data latency reachable.
- Every promised interaction (filter, tab, sort, drill-down, link) works and updates everything that depends on it.
- Missing, zero and extreme values display sensibly: no NaN, undefined, blank tiles or empty charts.
- Navigation works (slide or page numbers, headings, appendix references); placeholders are highlighted and easy to find.

**Technical**
- The file opens, renders and passes the checks for its format (6). Links, citations, cross-references and formulas resolve to the right target.
- The file you deliver is the file you checked: same path, after the last edit.

## 3. Fast self-tests

| Test | Do this | Fails when → fix |
|---|---|---|
| Titles-only read | Read only titles and headings, in order (`doc_text.py <file> --titles` lists deck titles). | They don't carry the story and the answer without the body → rewrite as takeaways, reorder. |
| First screen | Look only at the first rendered screen: slide 2, the top of page 1, a dashboard above the fold. | The reader couldn't stop there knowing the answer and the ask → move both up. |
| 30 seconds | Skim the whole rendered piece as a busy reader would: titles, highlighted numbers, chart shapes. Then state the message and the ask from memory. | You can't, or the eye lands on decoration, a legend or a minor number → fix emphasis, size or order. |
| So-what pass | For each paragraph, bullet, tile and chart, name which so-what question (SKILL.md section 4) it answers. | None → cut it or make it answer one. |
| Hostile reader | Write the 3 questions a skeptical CFO or board member would ask first (compared with what? what if the key assumption is wrong? what else did you consider? what does it cost, and who pays?). | The material doesn't answer or pre-empt each one in the body, notes or appendix → add the answer, or disclose why it can't be answered. |
| Number trace | Trace every headline number (titles, KPI cards, summary, the ask) to its source cell or page, or to a shown calculation; run `numbers_check.py trace` for the rest. | Any number you can't trace → handle it as in section 7. |
| Consistency | Search the extracted text (`doc_text.py`) for each headline number and metric. | The same quantity differs in value, unit, rounding or period anywhere (summary, slide, chart, table, notes, appendix) → make it identical or explain the difference. |
| Generic sentence | Ask of each sentence: could it appear unchanged in another company's document? | Yes → make it specific (names, numbers, dates) or cut it. |
| Delete test | For each slide or section, state what the reader loses if it disappears. | Nothing that changes understanding or the decision → delete it or move it to the appendix. |

## 4. Rubric (High-stakes)

Score after the checklist, self-tests and scripts. The rubric is internal: never show scores or mention the rubric unless the user asks. Score a dimension that doesn't apply (no charts in a memo) as N/A, not 5.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Strategic relevance | Answers another question or none; conclusion absent or buried. | Answers the question, but the answer or ask isn't in the first screen, or some units don't serve the objective. | Answer and ask in the first screen; every unit serves the objective at the audience's altitude. |
| Analytical integrity | Wrong, untraced or invented numbers, or conclusions the evidence doesn't support. | Numbers correct and traced, but some comparisons aren't like-for-like, assumptions are implicit, or alternatives and downside are thin. | Every number traced and recomputed; definitions, assumptions and uncertainty visible where they bite; alternatives weighed; conclusions follow. |
| Communication | Topic titles, filler, repetition, length far over budget. | Mostly takeaway titles and plain language; some repetition, generic sentences or excess length. | Titles-only read tells the story; every sentence passes the so-what test; within budget. |
| Visuals | Misleading (truncated bars, 3-D, colors against polarity) or charts that answer nothing. | Honest and labeled, but chart type or emphasis makes the reader work to see the point. | Each chart proves its title at a glance, with honest scales, units, periods and emphasis on what matters. |
| Usability | Reader can't tell what needs attention or what to decide; a broken interaction or navigation. | Attention points findable with effort; interactions work, but some states, definitions or navigation are missing. | What needs attention and what to decide is obvious in 30 seconds; every interaction and state works. |
| Technical | Doesn't open, renders broken, formula errors, clipped content, broken links. | Opens and renders; cosmetic issues that hide no content. | Passes every format check at every target viewer and width; editable and clean. |

**Pass rule:** every applicable dimension scores ≥ 4 and no blocking defect remains. Otherwise fix the lowest-scoring dimension first (a 5 elsewhere never offsets it), re-run the affected checks and re-score. If a dimension stays below 4 for a reason you can't fix (missing data, a user constraint), say so in the final message, in the disclosure format (5) if a blocking defect is involved.

## 5. Blocking defects and disclosure

A blocking defect stops delivery until it is fixed or explicitly disclosed:
- A wrong number or calculation, or the same quantity with different values in different places.
- Fabricated content: invented numbers, sources, quotes or benchmarks; an "illustrative" figure not shown as a placeholder.
- A number traceable to neither a source nor a shown calculation.
- A broken file or interaction: doesn't open, render errors, formula errors, a control that does nothing, content clipped or overflowing so that data is hidden.
- A misleading chart: truncated bar baseline, mismatched scales on compared charts, status colors against polarity, an undisclosed cherry-picked period.
- A missing material caveat, or a conclusion the evidence doesn't support.
- A citation to a source not opened this session, or one that doesn't state the claim.
- In a translation: a changed number, reversed meaning or dropped caveat.
- An outline or description delivered where the user asked for the file.

When you can't fix one, disclose it first in the final message, and, where the file allows, put a visible marker at the defect's location:

```
Unresolved: <the defect, in one line>
Where: <file and location, e.g. deck.pptx slide 6 chart; model.xlsx 'P&L'!F12>
Impact: <what it does to the conclusion or the reader, e.g. "savings may be overstated by up to $0.4M">
Action: <what the user should do, e.g. "confirm FY26 headcount with HR and replace [TBD] in F12">
```

If the defect undermines the central conclusion, say so in the first line. Never bury a disclosure in a footnote or relabel a blocking defect as an "open item".

## 6. Per-format technical checks

| Format | Check |
|---|---|
| pptx | Opens with python-pptx; `render.py` gives one image per slide and you look at every one: no text overflowing its box or the slide, no overlaps, no table cut at the edge, no leftover placeholder text. Body ≥ 12 pt and labels, sources and footnotes ≥ 10 pt unless the template sets larger. Content slides carry speaker notes (talk track, sources, caveats that didn't fit). Charts are native, editable chart objects whose data equals the numbers on the slide, not pasted images. Slide numbers on every slide but the title. The user's template, if given, is used. |
| docx | Opens and renders; headings use real heading styles; tables fit the page width and repeat header rows across pages; page numbers present; no stray comments or tracked changes; placeholders highlighted; table of contents updated if present. |
| xlsx | Recalculate (LibreOffice headless where available), then reload with openpyxl `data_only=True`: no formula without a calculated value (`doc_text.py` flags these), no #REF!, #DIV/0!, #VALUE!, #N/A or #NAME? on any sheet, no #### from narrow columns. Spot-check totals against an independent calculation. Number formats fit the content (%, currency, thousands separators, consistent decimals, real dates); inputs are distinguishable from formulas. If you can't recalculate, say the values are uncalculated. |
| html | `render.py` at desktop (about 1440 px) and mobile (about 390 px) widths: zero console errors, no horizontal overflow on the page or inside any table, card or chart; look at both images. Exercise every interaction (filter, tab, sort, toggle, tooltip, drill-down): it updates every dependent element, and reset restores the initial state. Without a browser, report interactions as untested. Text contrast ≥ 4.5:1 (≥ 3:1 for large text); every control reachable with Tab, with a visible focus ring. Spot-check 3-5 displayed values per section against the data. |
| markdown | Renders cleanly: tables have separator rows, code fences close, lists don't break; relative links, anchors and images resolve. |
| pdf | Opens; page count as expected; rendered pages show embedded fonts (no missing-glyph boxes), nothing clipped at the margins, page numbers; text is selectable unless intended otherwise; links work. |

## 7. Running the scripts

Run each script on the final file, read its output, and act on every finding. If a script is missing or fails, do that check by hand where you can and report it as not run (9). A clean script result is evidence for one check, not proof of quality.

- **`doc_text.py <file>`** dumps the text the reader will see, with locations. Use it for the titles-only read, the consistency test and length counts. HTML text created by JavaScript at runtime isn't extracted: check it in the rendered page.
- **`fluff_lint.py <file>`** flags filler, unsupported superlatives, vague actions, label titles and dense slides. It is a heuristic: look at every high-severity flag, fix each real problem, and ignore false positives without comment (an adjective whose number sits in the chart beside it, a label title on an agenda or appendix divider, quoted or legally required wording). Never weaken a good sentence just to silence a flag.
- **`numbers_check.py trace <deliverable> --sources <inputs...>`** lists numbers it can't find in the inputs. Pass every input file, including data you gathered. Treat an untraced number as invented until shown otherwise. For each one: if it is a calculation, recompute it and show its basis next to it or in the notes ("calculated: 12.4 / 10.9 − 1"); if it is from an outside source, cite the source; if it is a rounding, unit or locale variant of a source value (4.04 → 4.0; 1,200k → $1.2M; 4,0 → 4.0), confirm it is the same value correctly converted. Otherwise remove it or replace it with a `[TBD: ...]` placeholder. Years, dates and slide numbers are usually noise.
- **`numbers_check.py compare <source> <translation>`**: each mismatch is either a correct locale conversion (decimal comma, thousands separator, p.p. → pp) or a defect to fix. A number missing from the translation can mean dropped content.
- **`render.py <file>`** renders pptx, docx, pdf or html to PNG and reports HTML console errors and overflow. Open the images and look: clipped or overflowing text, overlaps, tables cut at an edge, unreadable small text, empty or dataless charts, placeholder text, colors against polarity, misalignment. Then run the first-screen and 30-second tests on them. Investigate every reported console error or overflow; overflow that hides content is blocking. If rendering fails, say the file wasn't rendered; never imply it was.

## 8. Independent review (High-stakes)

If an Agent or Task tool is available, spawn one reviewer after your own gate passes, using model "sonnet" if the tool lets you choose. Give it only the brief and absolute paths (deliverable, sources, rendered images), never your reasoning, plan or self-assessment: it must meet the material the way the reader will. Copy this prompt and fill the brackets:

```
You are reviewing a business deliverable before it goes to [audience]. You did not write it.

Brief: objective [objective]; decision sought [decision]; constraints [constraints].
Deliverable: [absolute path(s)]
Rendered pages: [absolute paths to PNGs, or "none"]
Source material: [absolute path(s), or "none provided"]

Open the files and read the deliverable as its audience would. Find the most important problems in:
1. Logic: does the conclusion follow? Gaps, leaps, contradictions, missing alternatives.
2. Evidence: unsupported claims, weak or outdated sources, correlation presented as cause.
3. Numbers: recompute totals, growth rates and shares; check figures against the sources; flag any quantity that differs between places.
4. Clarity: is the answer and the ask clear on the first screen? Titles that don't state a takeaway, filler, excess length.
5. Missing objections: questions a skeptical CFO or board member would ask that the material doesn't answer.
6. Visual honesty: truncated or mismatched axes, misleading color or emphasis, missing units, periods or labels, rendering defects.

Return at most 12 findings, ranked from most to least important. For each: severity (blocking = wrong number, fabricated or unsupported claim, misleading chart, broken file, missing material caveat; major; minor), location (file and slide, page, section or cell), the problem in one or two sentences, and why it matters to the reader. End with the 3 questions you would ask as a skeptical executive.
Do not rewrite the deliverable, do not edit any file, and do not praise it.
```

Triage every finding. Valid and material: fix it. Valid and minor: fix it if cheap. Out of scope or a matter of taste: drop it. Before dismissing a flagged number, check it against the source. Then re-run the checks your fixes affect (`numbers_check.py` after a number changes, `render.py` after a layout change) and re-score. Don't pass the reviewer's report to the user; carry only unresolved material findings into the final message.

If no agent tool is available, do a fresh-eyes pass yourself: work from the rendered images and extracted text, not your draft; run the hostile-reader test top to bottom; list the five most important problems; fix them. Don't call this an independent review.

## 9. Final-message honesty

- Report only checks that actually ran on the delivered version. Mention verification only when it changes the user's trust or next step ("every figure traces to pricing_2027.xlsx"; "not rendered: check slides 4-6 for overflow").
- Never write "verified", "tested", "all numbers checked" or "renders correctly" for a check you skipped, couldn't run or ran before your last edit.
- Remaining flags, within the bullet limit of SKILL.md section 9: unresolved blocking defects first (in the disclosure format), then placeholders the user must fill, inconsistencies found in their material, checks not run, and unresolved material reviewer findings. Group minor items if they don't fit.
- No rubric scores, no "quality gate passed", no account of the review process.
