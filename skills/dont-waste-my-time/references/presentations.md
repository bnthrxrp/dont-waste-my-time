# Presentations

Read this when building, restructuring or improving a deck. Chart choice, baselines, labels and chart color live in dataviz.md; keep charts native and editable. Profiles and slide-count budgets live in briefing.md: the main body stays within the budget, and the rest goes to the appendix.

## Contents
- Workflow (including the format decision)
- Storyline patterns
- Slide anatomy and density limits
- The two logic tests
- Presented vs pre-read decks
- Visual design defaults
- Production paths
- QA
- Improving an existing deck
- Evidence notes

## Workflow

1. **Brief** (SKILL.md sections 2-3): audience, objective, the answer in one sentence, the decision sought, presented or pre-read, and the **output format** (see below).
2. **Ghost deck.** Write the takeaway titles only, numbered, in order. Read them top to bottom as if nothing else existed. They must tell the whole story on their own: the answer, why, and what is asked. Fix the storyline here, where changes are cheap, not after the build.
3. **Slide plan.** One row per slide. Every number in the evidence column has a source or is a `[TBD: what, owner]`.

   | # | Takeaway title | Role in the argument | Evidence (source) | Visual |
   |---|---|---|---|---|
   | 3 | Price drove all of the +4.0% growth; volume fell 3.1% | Reason 1 for the recommendation | sales_2026.xlsx, tab Bridge | Price-volume bridge, price bar highlighted |

4. **Build the real file** (Production paths). An outline or a plan is not a deck.
5. **Render, inspect and fix** (QA), then do the titles-only read on the final file.

Keep the ghost deck and plan internal and continue in the same turn. Show them and wait only when the user asked to review the outline first, or when the storyline turns on a choice only the user can make (which option to recommend, what can be said to this audience).

### Decide the format before the first build

Settle it before writing any slide; rebuilding in another format doubles the cost of the task.

- The user named a format, supplied a .pptx/.potx or template, or standing defaults set one: use it.
- Otherwise, if a brief is warranted, include Format in it as one of the constraints, with .pptx as the recommended default. If the host offers its own slide-deck type, list it as an option.
- If no brief is warranted ("just do it", "use defaults"), build .pptx (editable, forwardable, opens everywhere) and state it in the confirmation line.
- HTML slides only when asked. PDF is an export of the .pptx, not a separate build.

## Storyline patterns

Pick the pattern that matches the objective. Each arrow is about one slide; drop any step the decision doesn't need. The answer always comes before the support.

- **Decision deck**: Title → Recommendation and the ask (what, cost, who decides, by when) → 2-4 reasons, one slide each → Options compared (at least two real alternatives, including doing nothing, each with why it loses) → Risks and mitigations with owners → Financials and plan → Decision requested and next steps → Appendix.
- **Business / performance review**: Title → Summary: performance vs target and the one thing that needs action → Headline KPIs vs target and prior period → Drivers of the variance (bridge) → Exceptions with root cause → Outlook vs target → Actions (owner, date) and decisions needed → Appendix by unit.
- **Board deck**: **Cover/summary slide** with five lines: purpose (decision, discussion or information), decision required, recommendation, 3-5 key numbers, key risks → Context the board needs, one slide, only what changes the decision → Evidence for the recommendation → Alternatives considered → Risks, mitigations and what would make us stop → Decision or resolution wording → Appendix.
- **Research / insight deck**: Title → The answer to the research question → 3-5 findings, one per slide, each with evidence and confidence → What it means for us → Recommended actions → Method, sample and limits (one slide or appendix) → Appendix.
- **Status update**: Overall status vs plan with a one-line reason → Milestones done vs planned → Issues and risks with owners → Decisions or help needed → Next period. Usually 1-3 slides.

**Never invent process facts**, in board decks above all: who was consulted, who agreed or signed off, what was piloted or validated, which options management reviewed. State them only when the user supplied them; otherwise write `[TBD: who reviewed or approved this, owner]`. Alternatives you generated are "alternatives assessed in this deck", not "options the team considered".

## Slide anatomy

Every content slide has these parts, each in the same position throughout the deck:

1. **Takeaway title**: a full sentence that states the so-what in factual terms (no "strong", "disappointing" or a loose "significant"), at most 2 lines (about 15 words), with the decisive number when there is one. If it needs "and" to join two independent claims, split the slide. Put it in the slide's **title placeholder**, not a free text box: outline view, screen readers and the checks read it there.
2. **Body that proves the title and nothing else**: one main visual or table when the evidence is quantitative, otherwise a few short bullets or sentences. Use a second visual only when the comparison between the two is the point. Bullets are for parallel items, at most two levels; anything with a cause, condition, comparison or caveat is a full sentence.
3. **Source/notes line** at the bottom: source with as-of date, period, definitions, and the status of estimates or calculations. Required on every slide with numbers.
4. **Slide number**, from the layout where the tool allows it.

**Appendix** for everything a reader may ask for but doesn't need to follow the argument: detail tables, breakdowns by unit, method, sensitivities. Appendix slides keep source lines and may use descriptive titles ("A3. Gross margin by region, FY2024-26"). Point to them from the main slide ("Detail: A3"). Never put a caveat that changes the recommendation only in the appendix or the notes.

**Placeholders in slides.** Make every `[TBD: what, owner]` visible: bold, in a distinct highlight color. Never plot a missing value as zero or leave it out of a chart silently: chart the known values and annotate the gap.

**Density limits** (heuristic review flags, not research findings; the template, the brief or the audience can override them):

| | Presented | Pre-read |
|---|---|---|
| Body words (excluding title, chart labels, source line) | ≤ 40 | ≤ 100 |
| Bullets | ≤ 4, one line each | ≤ 6, at most 2 lines each |
| Main visuals | 1 | 1, or 2 when comparing |
| Minimum font: title / body / chart labels / source line | 24 / 18 / 14 / 10 pt | 20 / 14 / 10 / 10 pt |

When a slide breaks a limit, cut words, split the slide or move detail to the notes or appendix. Never shrink the font to make it fit.

**Filler slides.** Drop "Thank you", "Questions?" and "Agenda" slides by default; end on the decision or next-steps slide and leave it up during Q&A. Keep an agenda only for decks well above the main-body budget or with several presenters, and write it as the section takeaways, not topic names. Keep a section divider only if it states the section's takeaway. Move background, "about us" and methodology slides to the appendix unless the decision depends on them.

## The two logic tests

Run both on the ghost deck, then again on the built file.

**Horizontal: the titles alone tell the story.** Extract them with `python3 ${CLAUDE_SKILL_DIR}/scripts/doc_text.py deck.pptx --titles` and read the main-body titles as one paragraph. It passes when:
- the answer and the ask appear in the first two content titles;
- every title is a claim, not a topic;
- each title supports the opening answer or follows from the previous one, with no gap a reader must fill;
- nothing repeats and nothing essential is missing;
- someone who reads only the titles can restate the recommendation and its main reason.

A title the story needs but no slide supports means a missing slide. A slide whose title adds nothing to the story gets cut or merged.

**Vertical: everything on a slide supports its title.** For each element (chart, bullet, callout, table row, image), ask whether it proves the title. Move or delete what doesn't. Then check the reverse: does the body prove the claim at the stated number, period and scope? If the evidence supports a weaker claim, weaken the title; never stretch the evidence. The most prominent feature of the visual (the highlight, the annotation) must be the thing the title names. A material caveat sits on the slide it qualifies, as a full sentence next to the number, not as a sub-bullet or in the source line.

## Presented vs pre-read decks

Infer the mode from the request ("for the meeting", "to send ahead", "board pack") and state it in the confirmation line. Board packs and business reviews sent in advance are pre-reads; never ship a sparse presented-style deck as a pre-read. If one deck must do both, build the pre-read and put the speaking points in the notes.

| | Presented (someone talks over it) | Pre-read (read alone, often forwarded) |
|---|---|---|
| Job of the slide | Shows the evidence; the speaker carries the argument | Carries the whole argument by itself |
| Body | One visual, minimal text | Visual plus 2-4 lines of interpretation; definitions and caveats on the slide |
| Executive summary | The opening slide carries the answer | A summary slide right after the title: the whole story on one slide |
| Speaker notes | Required: 3-6 sentences on what to say, the number to stress, the likely question and its answer, the transition | Optional: backup detail, calculation basis, extra sources |

Slides carry claims and evidence, not the speaker's script: never put on the slide, word for word, what the speaker will say. In a pre-read, never leave the argument only in the notes: forwarded decks are read without them.

## Visual design defaults

**If the user provides a template, master or brand guide, use it.** Build on its layouts and placeholders, fonts and colors, and change nothing structural. The defaults below apply only when there is none.

- **Grid**: 16:9, margins of at least 0.5". Title, body area, source line and slide number sit in the same place on every content slide. Left-align text; center only on the title slide.
- **Type**: one typeface family, two at most (titles and body). Build hierarchy with size and weight, not more fonts or colors. Sentence titles at 24-28 pt: the 36-44 pt that the pptx skill suggests is sized for short labels and forces long titles onto three lines.
- **Palette**: a neutral base (dark gray text, light gray for context data, white background) plus **one accent** for the data the title is about. Add a second color only for a second meaning, such as plan vs actual.
- **Semantic color**: color means something in business terms, never decoration. Favorable and unfavorable follow business polarity (rising cost is unfavorable), stay the same across the deck, and always come with a sign, label or arrow, never color alone. The same series has the same color on every slide.
- **No decoration that carries no evidence** in decision, review and board decks: no stock photos, decorative icons, clip art, 3D effects, gradients, shadows or title underlines. A keynote or training talk built for engagement may use imagery. Where the pptx skill's design ideas (a bold mood palette, icons in circles, a visual on every slide, varied layouts for variety's sake) conflict with this file, this file wins for executive material. A clear claim on a plain slide beats a decorated one; change the layout only when the shape of the content changes.
- **Numbers**: one unit, precision and format per metric across the whole deck ($86.2M everywhere, not $86M on one slide and 86,200,000 on another). Put units in titles, axis labels or column headers. Write percentage-point changes as pp, not %. Use a minus sign or parentheses for negatives, consistently. Round to what the decision needs, usually 2-3 significant digits. Totals add up as displayed, or a note says they don't because of rounding.
- **Tables**: about 7 rows × 6 columns at most in the main body. Right-align numbers and highlight the row or column the title is about. Bigger tables go to the appendix.

## Production paths

**(a) A pptx skill, if this session has one: preferred for creating or editing .pptx.** Load it and follow its build, validation and rendering steps. This file supplies what it doesn't: the storyline, the slide plan (titles, body content, chart data, notes, source lines), the design defaults above, and the QA below. Put titles in title placeholders, keep charts native, put notes in the notes pane, and use its render-and-inspect loop as the render step of QA.

**(b) python-pptx fallback**, when no pptx skill is available. `plan` holds the slide-plan rows; every value comes from the sources.

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

prs = Presentation(template_path) if template_path else Presentation()
if not template_path:                                    # the blank default is 4:3
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
layout = next(l for l in prs.slide_layouts if l.name == "Title Only")  # by name; names vary

def text_box(slide, text, x, y, w, h, size):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    run = tf.paragraphs[0].add_run(); run.text = text; run.font.size = Pt(size)

for n, row in enumerate(plan, start=1):
    s = prs.slides.add_slide(layout)
    s.shapes.title.text = row["title"]                   # takeaway title in the title placeholder
    s.shapes.title.text_frame.paragraphs[0].runs[0].font.size = Pt(26)
    if row.get("chart"):                                 # native, editable chart
        data = CategoryChartData()
        data.categories = row["chart"]["categories"]
        data.add_series(row["chart"]["series"], row["chart"]["values"])
        ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(1.5),
                                Inches(7.6), Inches(4.9), data).chart
        ch.has_legend = False
        ch.value_axis.minimum_scale = 0
        ch.plots[0].has_data_labels = True
    if row.get("table"):                                 # list of rows, header first
        cells = row["table"]
        t = s.shapes.add_table(len(cells), len(cells[0]), Inches(8.5), Inches(1.5),
                               Inches(4.2), Inches(0.4 * len(cells))).table
        for r, values in enumerate(cells):
            for c, v in enumerate(values): t.cell(r, c).text = str(v)
    text_box(s, row["source"], 0.6, 6.85, 11.5, 0.35, 10)   # source line
    text_box(s, str(n), 12.4, 6.85, 0.5, 0.35, 10)         # slide number
    s.notes_slide.notes_text_frame.text = row.get("notes", "")
prs.save("deck.pptx")
```

**(c) HTML deck only if the user asks for one**: a single self-contained file, one fixed 16:9 section per slide, keyboard navigation and print CSS so it exports to PDF. Same anatomy, logic tests and QA; render it with render.py.

**Editing an existing deck.** Preserve its masters, layouts, theme, fonts and placeholders, and work inside them. Edit in place when the storyline holds and the fixes are local (titles, numbers, one chart, a few slides cut or moved). Rebuild on the same template when the order of the argument changes or most slides need new titles and bodies, which is typical for "this deck is weak, fix it". Save to a new file name; never overwrite the original. Move the user's content to the appendix or list its removal in the change log; never drop it silently.

## QA

Run on the actual file before saying it is done. Assume the first render has defects.

1. **Render and look**: `python3 ${CLAUDE_SKILL_DIR}/scripts/render.py deck.pptx`, then open every PNG. Check for text overflow or clipping, overlapping elements, legibility at the minimum sizes, titles at the same position on every slide, alignment, leftover template text, visible `[TBD]` placeholders, and chart correctness: values match the plan, bars start at zero, units and labels present, the highlight on the series the title names. If the pptx skill's render loop already produced these images, inspect those instead of rendering twice.
2. **Fluff and density**: `python3 ${CLAUDE_SKILL_DIR}/scripts/fluff_lint.py deck.pptx`. Fix label titles, dense slides, filler and vague actions; ignore false positives.
3. **Numbers**: `python3 ${CLAUDE_SKILL_DIR}/scripts/numbers_check.py trace deck.pptx --sources <inputs...>`. Each flagged number (including chart data and notes) becomes a sourced figure, a labeled calculation, a `[TBD]`, or is removed.
4. **Titles-only read**: run the horizontal test on the final file.
5. **File opens**: the render succeeded, python-pptx loads the file, and the pptx skill's validator passes if one is available.

Fix, re-render the changed slides and re-run any check the fix could affect. Report any check you could not run.

## Improving an existing deck

Read the real file first (`doc_text.py deck.pptx` and a render). Write the ghost deck its current titles imply, then the one it should have, and mark every existing slide keep, rewrite, merge, cut or move to appendix: editing drifts toward adding. Implement the plan and deliver the file, not advice.

| Symptom | Fix |
|---|---|
| Topic titles ("Sales overview", "Q3 results") | Rewrite each as the takeaway the slide proves, with its number |
| The ask is buried at the end or missing | Put the recommendation and the decision requested right after the title slide; restate the decision on the closing slide |
| Agenda, background, "about us", thank-you or Q&A slides | Delete; fold any context the decision needs into one line on the slide that needs it |
| Bullet dumps (more than 4-6 bullets, paragraphs on slides) | Find the claim and make it the title; keep the bullets that prove it or turn them into a chart or table; move the rest to notes or the appendix |
| 3D charts, pies with more than 3 slices, exploded pies | Replace with a native sorted bar or 100% stacked bar |
| The same metric with different values or formats across slides | Trace each to the source and use the sourced figure; flag the discrepancy in the change log, never pick one silently |
| Numbers without source or period | Add the source line; if the material has no source, mark `[TBD: source, owner]` |
| Vague next steps ("continue monitoring", "align with stakeholders") | Specific action, owner, date and measure of done; a `[TBD: what, owner]` placeholder where the material doesn't name them |
| Decorative visuals (stock photos, icons, clip art, gradient boxes) | Remove, or replace with the evidence that proves the title |
| Several messages on one slide, or one message on several | Split or merge so each slide has one job |

End the final message with a change log of at most five lines:

```
Changes (11 → 7 slides + 2 appendix):
1. Storyline: recommendation and decision moved to slide 2; agenda, background and thank-you slides removed.
2. Titles: all rewritten as takeaways; the titles alone now tell the story.
3. Evidence: 3D pie replaced with a sorted bar of variance by region; sources added to 5 slides.
4. Flag: EBITDA margin is 12.4% on slide 3 and 12.1% on slide 6; used the workbook's 12.4%, please confirm.
5. Open: owners for 2 of 4 next steps are [TBD].
```

## Evidence notes

Most rules here are practitioner defaults. The studies behind them are small, mostly lab or crowdsourced, and measure learning or recall, not executive decisions; storyline-first and the ghost deck have no study behind them. Never cite any of this in a deliverable as a measured effect.

- **Takeaway titles are a default with moderate support, not a proven effect.** Garner, Alley et al. found better comprehension with assertion-evidence slides (sentence headline plus visual evidence) than with topic-and-bullet slides: conference version with 111 participants (abstract: https://pure.psu.edu/en/publications/assertion-evidence-slides-appear-to-lead-to-better-comprehension--2/); journal version with 110 engineering students ("How the design of presentation slides affects audience comprehension: A case for the assertion-evidence approach", International Journal of Engineering Education 29(6), 2013, 1564-1579). Limits: run by the method's developers, one short narrated lecture, and control slides built to violate six multimedia principles, so a bundle of changes was tested and the headline's own effect is not isolated.
- Farkas, informal assessment of Alley's slide design (2010), https://faculty.washington.edu/farkas/dfpubs/Farkas-Assessment%20Of%20Alleys%20Slide%20Design.pdf: calls the claims "sweeping and poorly supported", says the weak controls make the gains "surprisingly modest" and that the speaker's role is ignored, yet sees "a good case for sentence-style slide titles" and finds brief, well-phrased bullets harmless. Hence sentence titles everywhere, bullets allowed, visuals where the evidence is quantitative.
- Stratrix, "The pyramid principle" (practitioner page, undated), https://stratrix.com/craft/pyramid-principle: a topic heading leaves the thinking to the reader; moving the answer to the front without rewriting topic headings as claims doesn't fix a deck. Its pricing-deck story is hypothetical; no outcome data.
- **No script on slides and no decoration rest on multimedia-learning research, extrapolated to decks and verified only at abstract or summary level.** Adesope and Nesbit, Journal of Educational Psychology 104(1), 2012 (meta-analysis): keyword-style on-screen text, not a verbatim transcript, carried most of the benefit of adding text to narration. Yue, Bjork and Bjork, Journal of Educational Psychology, 2013, doi 10.1037/a0031971: on-screen text identical to the narration reduced recall and transfer. Sundararajan and Adesope, Educational Psychology Review 32(3), 2020: interesting but irrelevant details reduced learning (g ≈ -0.33 across 58 studies, per secondary summaries; moderator findings conflict). Noetel et al., Review of Educational Research 92(3), 2022, https://doi.org/10.3102/00346543211052329: design matters more for complex material and for system-paced settings such as live presentations.
- Columbia Accident Investigation Board, Report Vol. 1 (2003), ch. 7 p. 191 and ch. 8 p. 201, https://govinfo.library.unt.edu/caib/news/report/pdf/vol1/chapters/chapter7.pdf: on one briefing slide the decisive fact sat at the bottom of six levels of bullets, "significant" was used with meanings from trivial to fatal, and the headings, arrangement and bullet size "served to highlight what management already believed". One illustrative case (the slide analysis is Tufte's, quoted by the Board) within a multi-causal account. Hence the decisive number in the title, at most two bullet levels, and caveats as sentences.
- Ajani, Lee, Xiong, Nussbaumer Knaflic, Kemper and Franconeri, "Declutter and Focus", IEEE TVCG, 2021, https://par.nsf.gov/servlets/purl/10350268: with 24 undergraduates and 10-second views, a headline stating the pattern plus one highlight and an annotation made recall of the focal conclusion more likely; decluttering alone raised professionalism ratings, not comprehension.
- Kim, Setlur and Agrawala, CHI 2021 (crowdsourced, line charts), https://arxiv.org/abs/2101.08235: readers adopt a caption's message only when the chart also emphasizes that feature; hence the highlight must match the title. Kong, Liu and Karahalios, CHI 2018, https://mail.zcliu.cs.umd.edu/vistitles/CHI18-VisTitles.pdf: a title's slant shapes the message readers take from the same chart; the no-evaluative-words rule extends this finding.
- Adams, Converse, Hales and Klotz, "People systematically overlook subtractive changes", Nature 592, 2021 (read via https://www.gwern.net/doc/design/2021-adams.pdf): people default to adding, and an explicit cue to consider removing raised the share who subtracted. Mostly online samples and non-business tasks. Hence the explicit keep/cut mark for every slide.
- W3C, WCAG 2.1 SC 1.4.1 Use of Color, https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html: color is never the only means of conveying information.
