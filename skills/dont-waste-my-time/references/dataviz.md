# Data visualization: charts, tables and numbers

Read this before building or reviewing any chart, KPI visual or data table. A chart exists to answer one question that serves the decision; if you cannot name the question, cut the chart. This file holds the thresholds and integrity checks, not chart basics. When a dataviz skill builds the visuals, check its output against these rules.

## Contents
- Chart chooser
- Encoding priorities
- Integrity rules
- Titles and annotation
- Color
- Uncertainty and forecasts
- Business notation
- Tables
- Number formatting
- Anti-patterns and fixes
- Implementation notes
- Evidence notes

## Chart chooser

Start from the reader's question, then pick the form.

| Question | Use | Avoid |
|---|---|---|
| How do categories compare? | Bars sorted by value (horizontal when labels are long), zero baseline, direct value labels | Pies, bubbles, alphabetical order when the order isn't the point |
| How did it change over time? | Line for many periods or a trend; columns for a few discrete periods whose amounts are the message | Unevenly spaced periods on an even axis; bars for long series |
| What share of the whole? | Sorted bars of shares; one 100% stacked bar per whole to compare 2-3 wholes; pie or donut only for 2-3 labeled slices | Pies with more slices; several pies side by side; exploded, nested or 3D pies |
| How are values spread? | Histogram; box or strip plot to compare groups; n shown | A bar of the mean alone, which hides the spread |
| How do two measures relate? | Scatter with units on both axes, outliers labeled, trend line only if the relationship is the message | Two lines on dual axes; causal wording in the title |
| Actual vs target or plan? | Actual bar with a target marker (bullet), or variance bars; KPI tile: value, Δ vs comparison with sign, optional sparkline | Gauges, dials, traffic lights without the number |
| What drove the change from A to B? | Waterfall (bridge): start total, drivers sorted by size or by logic (price, volume, mix, FX), end total; reconciles exactly | Two totals with no drivers; stacked bars |
| Who ranks where? | Sorted horizontal bars or dot plot; top N + "Other"; slope chart for rank change between two periods | Unsorted bars; a full league table on a slide |
| Where? (only if location drives the decision) | Map of rates (per capita, %, per store), or sorted bars by region | Maps of raw totals, which mostly show size; maps when location isn't the point |
| What is the exact value? | Table | A chart with every mark labeled to two decimals |
| How do many series move? | Up to about 4 overlaid lines with the key one highlighted; beyond that, small multiples on one scale | Spaghetti of overlapping lines |

## Encoding priorities

Magnitude judgments, most to least accurate: **position on a common scale > position on non-aligned scales > length > angle and area > color intensity**. Put the most important quantity on the most accurate channel.

- Put the comparison the decision depends on along one shared axis: bars or dots from a common baseline, next to each other.
- In stacked bars only the bottom segment and the total share a baseline. If readers must compare a middle segment across bars, unstack it (grouped bars or small multiples) or label every segment.
- Angle and area (pies, bubbles, treemaps, gauges) give an impression, not a reading: label the values whenever they matter. Angle alone is the weakest pie cue; a donut reads as accurately as a pie.
- Color intensity (heatmaps, shaded maps) shows pattern, not value: print the numbers in the cells or provide the table.
- Comparing values across subsets is slow and loads working memory. Place compared items side by side on one axis, keep one main comparison per chart, and state the result in the title.
- Two series with close values over a short span: overlay them in one panel. Many series or a wide span: small multiples.
- Use conventional forms; an unfamiliar chart costs decoding time before it delivers anything.

## Integrity rules

Breaking a **Hard** rule makes the chart misleading, a blocking defect at the quality gate.

- **Hard: bars and columns start at zero.** Bar length must stay proportional to value; the exaggeration persists even when the truncation is flagged. If zero hides the difference that matters, a bar is the wrong form: switch to dots or a line with a labeled range, or plot the differences (variance bars) directly. Never break a bar axis.
- **Line and dot charts may zoom**: print the axis range, label the start and end values, and state the change in numbers in the title or an annotation. Set the range from the size of change that matters to the decision, not from the software's autoscale: a noise-level move must not look dramatic, and a forced zero must not flatten a material trend.
- **Hard: no 3D**, perspective or shadows on data marks.
- **Avoid dual y-axes.** Use indexed lines (base period = 100, absolute values labeled at the endpoints) or two aligned panels sharing the x-axis. If the user insists: color each axis like its series, label both units, keep a bar axis at zero, and give the crossing points no meaning.
- **Hard: one scale across small multiples** and across charts placed side by side for comparison. If scales must differ because shape matters more than size, write "scales differ" in the subtitle.
- **Hard: time is proportional.** Equal intervals get equal spacing; space irregular dates by date or mark the gap; never mix months and quarters on one axis. Label partial periods ("Oct MTD", "YTD to 15 Oct") and never set them against full periods unlabeled.
- **Hard: label cumulative vs period values** ("YTD", "cumulative", "per month") in the subtitle or axis title. A cumulative line rises whenever flows are positive; never present that rise as momentum.
- **Show n** when a share or average rests on a small or unequal base ("n = 37 stores"). Below about 20 observations, show counts ("7 of 18"), not percentages (heuristic).
- **Hard: never imply precision you don't have.** Decimals follow the data's accuracy, estimates are labeled as estimates, and ranges appear where they could change the decision.
- **Like-for-like**: compared marks share definition, currency, perimeter and price basis; state the basis in the subtitle (constant currency, LFL stores, restated).

## Titles and annotation

- **Title**: the takeaway as a sentence with the number ("Price drove all of the +4.0% growth; volume fell 3.1%").
- **Subtitle**: what is measured: metric, unit, period, scope, basis ("Net revenue, € M, FY22-FY25, Europe, constant currency").
- **Faithfulness test.** Readers take the title as the chart's message and tend to assume charts are neutral, so the title must not outrun the data. Check that:
  1. every claim in the title is visible in the chart, or labeled as interpretation;
  2. the title doesn't upgrade the evidence: no causation from co-movement, no "trend" from two points, no "record" without the history shown, no evaluative adjectives;
  3. a reader who disagrees with the recommendation would read the same fact from title and chart.
- **Make the chart say what the title says.** The accent color, annotation or most prominent mark sits on the feature the title names. Words don't beat a stronger visual pattern: if the chart's dominant pattern differs from the message, redesign it (highlight, reorder, re-baseline, split), don't add text.
- **Declutter, then focus.** Remove non-critical gridlines, redundant labels and extra colors; then add one accent and one or two annotations at the data, giving value and reason ("Plant B outage, −1.2 kt"). Decluttering alone looks professional; the focus is what carries the message.
- **Direct labels over legends.** Label line ends and the bars that matter. Keep a legend only when marks are too many or too small to label, and order it like the data. Label the values the message needs, not every point.
- **Axes**: unit in the axis title or tick labels (€ M, %, pp, days). Drop a value axis when every bar is labeled.
- **Source line** under every chart: source, extract date or version, n, definitions, and estimate markers ("Source: ERP sales ledger, extract of 3 Oct; FY plan v3. n = 412 outlets. E = estimate").

## Color

Default to grey plus one accent on what the title names. Add a color only when it carries meaning.

| Role | Default | Contrast on white |
|---|---|---|
| Context data | grey #8C8C8C | 3.4:1 |
| Accent | blue #0072B2, or the brand color if it reaches 3:1 | 5.2:1 |
| Favorable | bluish green #009E73 | 3.4:1 |
| Unfavorable | vermilion #D55E00 | 3.9:1 |
| Gridlines (decorative) | #D9D9D9 | n/a |
| Primary text | #222222 | 15.9:1 |
| Secondary text (subtitle, axes, source) | #595959; never lighter than #767676 | 7.0:1 (#767676: 4.5:1) |

- **Semantic color follows business meaning and metric polarity, not direction.** Cost +5% vs plan is unfavorable; churn −1 pp is favorable. Once a color means something, it means it everywhere in the deliverable: never reuse the favorable or unfavorable color as a neutral accent or a category. Keep one color per entity (product, region) across all charts.
- **Hard: never encode meaning by color alone.** Pair it with a sign (+/−), label, icon (▲▼), position (left or right of zero) or pattern. Never rely on red vs green: about 8% of men have some color-vision deficiency, and red-green deficiency makes the two nearly indistinguishable. The pair above stays distinct under simulated deficiency; a typical red/green pair does not.
- **Categorical palette (Okabe-Ito)**, in order of use on white: blue #0072B2, reddish purple #CC79A7, black #000000, vermilion #D55E00, bluish green #009E73 (all ≥ 3:1). Orange #E69F00 and sky blue #56B4E9 (2.3:1) need a dark outline or a dark background; yellow #F0E442 (1.3:1) never on white. When polarity colors are in use, drop vermilion and bluish green from the categorical set. On a dark background recompute: #0072B2 falls to 3.2:1 on #1E1E1E, while orange and sky blue exceed 7:1.
- **At most 6-7 categorical colors per chart.** Beyond that, group the tail into "Other", split into small multiples, or use direct labels in one color.
- **Hard: contrast ≥ 3:1** for every graphical object the reader needs (bars, lines, markers, segment boundaries) against adjacent colors, and **≥ 4.5:1 for text** (3:1 for large text: 18 pt, or 14 pt bold). So write data labels in #222222, not in the series color, unless that color reaches 4.5:1: #0072B2 does; #009E73, #D55E00 and #8C8C8C don't.
- Ordered values (low to high): one hue, light to dark. Values around a meaningful midpoint (zero, target, average): two hues diverging from a neutral color at that midpoint. Never a rainbow scale.

## Uncertainty and forecasts

- **Show a range whenever the uncertainty could change the decision**: a forecast band that crosses the target, options whose intervals overlap. Otherwise state the uncertainty in the subtitle or a note.
- **Hard: label what every interval is**: "80% prediction interval", "low/high scenario", "min-max of last 12 months", "±1 SD". Unlabeled error bars are common and ambiguous.
- Show uncertain estimates as a dot with an interval line, or a line with a shaded band, not as bars with error bars: a bar makes the values inside it look more likely than those above it.
- Don't make readers judge significance from overlapping intervals. Say it: "B's range overlaps A's; the data can't separate them."
- **Forecasts look different from actuals**: dashed lines or hatched bars, a vertical rule at the last actual marked "Actual | Forecast", the range as a light band, and the forecast's basis and vintage ("FC, Sep update").
- **Hard: never present an estimate as a point fact.** Write "≈ €4.2 M (range €3.8-4.6 M), estimate" in the title or label, and round estimates more coarsely than actuals.
- Translate the range into the decision: "Even at the low end, payback stays under 3 years."

## Business notation

A practical convention inspired by IBCS (standardized as ISO 24896), not a mandate. Use it when a deliverable compares scenarios, unless the user's template or company standard defines its own; then follow theirs. The point is that one encoding means one scenario throughout the deliverable.

| Scenario | Label | Bars and columns | Lines |
|---|---|---|---|
| Actual | AC | solid dark grey #404040 | solid dark |
| Prior year | PY | solid grey #8C8C8C | solid grey |
| Plan / budget | PL (or BU) | outlined: no fill, dark border | thin dark, dotted |
| Forecast | FC | hatched: dark diagonal lines on white | dashed |

- **Variance**: show absolute (ΔPL, € M) and relative (ΔPL %) together, each with an explicit sign. Variance bars grow from a zero line and are colored by polarity, not by sign: costs +€0.4 M vs PL carry "+0.4" in the unfavorable color.
- Relative variance = (AC − PL) / |PL|. When the base is negative or near zero, show the absolute variance only and mark the relative one "n.m." (not meaningful).
- A change in a rate is in percentage points: "EBITDA margin −1.2 pp vs PY".
- **Scenario labels**: define them once and use the same words in titles, legends and tables. Never use "Budget", "Plan" and "Target" for the same thing.
- **Bridges**: start and end totals in the scenario encoding, from zero; drivers as floating bars colored by polarity with signed labels. Drivers must sum exactly to the difference; add an "Other / rounding" bar rather than leave a gap.

## Tables

Use a table when the reader needs exact values, looks up their own row, or compares several measures per item.

- Right-align numbers, with tabular figures (`font-variant-numeric: tabular-nums` in HTML) so decimals line up; left-align text; align each header with its column.
- Use the same decimals within a column and put units in the header ("Revenue, € M"), not in every cell.
- Sort by the decision metric (largest gap or worst performer first) unless readers look rows up by a natural order (region, time, alphabet).
- Highlight exceptions only: cells that breach a threshold, with polarity color plus sign or icon. If more than a few cells are highlighted, nothing stands out; raise the threshold.
- Place compared columns side by side: AC | PL | ΔPL | ΔPL %. Set totals apart with a rule and bold; use light horizontal rules, not a full grid.
- On a slide, show the rows that carry the message (top N + "Other", about 10 rows at most, heuristic) and put the full table in the appendix.

## Number formatting

- **Digits follow the decision**: usually 2-3 significant digits in charts and titles ("€12.4 M", not "€12,403,887"); more only when the decision turns on the difference. Values that are compared get the same decimals.
- **Scale**: one unit per axis or column ("€ M"); don't mix 950k and 1.2M in one comparison. Suffixes in English: k, M, B (or bn); in Portuguese: mil, mi, bi.
- **Locale**: separators follow the deliverable's language: en 1,234.5; pt-BR 1.234,5 (R$ 1,2 mi).
- **True minus sign** (−, U+2212) in text and labels, and an explicit + on changes ("+4.0%", "−3.1%"). In spreadsheets keep cells numeric and use a number format for signs or finance parentheses; never type numbers as text. Pick minus or parentheses for a deliverable, not both.
- **% vs pp**: margin from 20% to 22% is +2.0 pp, or +10% relative. When both readings are possible, say which one you mean.
- **Name the base** of every percentage ("% of net revenue", "% of stores").
- **Rounding**: compute from unrounded values and round only for display, with one rule across the deliverable, so a number never appears as 4.0% on one slide and 3.97% or 4% on another. When rounded parts don't add up to the rounded total, keep the correct total and footnote "Totals may not add due to rounding"; never adjust a part to force the sum.

## Anti-patterns and fixes

| Anti-pattern | Fix |
|---|---|
| 3D charts | The 2D equivalent |
| Pie with more than 3 slices, or several pies compared | Sorted bars of shares; one 100% stacked bar per whole |
| Rainbow or arbitrary palette | Grey + one accent; Okabe-Ito for true categories; single-hue ramp for ordered values |
| Truncated bar axis | Zero baseline, or dots/line with a labeled range, or variance bars |
| Dual y-axes | Indexed lines, or two aligned panels |
| Spaghetti (more than about 4 overlapping lines) | Highlight 1-2 series and grey the rest, or small multiples on one scale |
| Unlabeled axes or missing units | Axis title with unit, or direct labels and no axis |
| Legend hunting | Direct labels at line ends and on bars |
| Decorative icons, clip art, background images | Remove them; at most one data-relevant image for the single message to remember, never replacing labels or axes |
| Gauges, speedometers, dials | The number + Δ vs target with sign; a bullet bar |
| Chartjunk competing with data (heavy grids, borders, shadows, labels on every point) | Declutter, then one accent and one annotation |
| Bars with error bars for estimates | Dot + labeled interval |
| Red/green status alone | Polarity color + sign or icon + the value |
| Stacked bars used to compare middle segments | Grouped bars or small multiples |

On embellishment: embellished charts were read as accurately as plain ones and remembered better weeks later, and unusual charts are more memorable. But memorability is not comprehension, and imagery can bias how readers read the data. So use standard forms for analysis, allow at most one memorable element for the single message, and never trade accuracy for it.

## Implementation notes

- **pptx**: build native, editable charts (python-pptx `CategoryChartData` + `add_chart`, or the pptx skill), not pasted images. Per-point color: `series.points[i].format.fill`; hatching: `fill.patterned()` with `MSO_PATTERN`; dashes: `format.line.dash_style`; label formats: `data_labels.number_format` with `number_format_is_linked = False`. For an actual-to-forecast line, use two series that share the last actual point.
- **HTML**: inline SVG, or a charting library loaded at an exact pinned version; set explicit sizes and test desktop and mobile widths.
- **matplotlib** only if installed (`python3 -c "import matplotlib"`). Set colors, fonts and labels explicitly, because the defaults break several rules above. Export SVG, or PNG at 200 dpi or more.
- Render and look: `python3 ${CLAUDE_SKILL_DIR}/scripts/render.py <file>`. Check that labels don't overlap or clip, hatching and colors survived, and axes start where intended.

## Evidence notes

- **Encoding ranking**: Heer & Bostock 2010 (crowd replication of Cleveland & McGill: position > length > angle/area, for proportion judgments). The place of color intensity and the stacked-bar implication are inferences from that ranking. Pie cues, donut ≈ pie, angle weakest, and distorted pie variants: Skau & Kosara 2016. Subset comparison is slow; working memory, conventions, audience: Franconeri et al. 2021 (abstract).
- **Zero baseline**: Correll, Bertini & Franconeri 2020 (truncated bars exaggerate perceived effect size even when truncation is cued; for trend messages, refusing to zoom can also mislead; size the axis to the meaningful effect). Datawrapper (bars from zero; dots and lines may start elsewhere).
- **Dual axes**: Datawrapper practitioner guidance resting on one small study. The consensus is stronger than the evidence, hence a default, not a Hard rule.
- **Overlay vs small multiples**: Javed et al. 2010; Ondov et al. 2018. Results depend on task and visual span; "about 4 lines" is a heuristic.
- **Titles and focus**: Kong et al. 2018 (title slant shapes the perceived message; viewers think charts are neutral). Kim et al. 2021 (readers adopt a caption's point only when the chart emphasizes it; line charts). Ajani et al. 2021 (decluttering raises professionalism; adding a headline, a highlight and annotations improves clarity and memory of the pattern; memory tasks only).
- **Embellishment**: Bateman et al. 2010 (no accuracy loss, better recall; the authors caution against generalizing). Borkin et al. 2013 (unusual types and recognizable objects aid memorability).
- **Uncertainty**: Correll & Gleicher 2014 (error bars often unlabeled; containment bias; the encoding changes decisions). The paper recommends gradient or violin plots; dot + interval is an adaptation for executive readers, not a tested form.
- **Color**: WCAG 2.1 SC 1.4.11 (3:1 for needed graphics, strict) and SC 1.4.1 (not color alone). The 4.5:1 text threshold is SC 1.4.3, a standard not covered by the research base. Okabe-Ito hex values, ~8% of men with a color-vision deficiency, direct labels beyond ~8 categories: Wilke (ch. 19). Contrast ratios are computed with the WCAG luminance formula. The 6-7 color ceiling is a heuristic, tighter than Wilke's because only five Okabe-Ito colors pass 3:1 on white. The favorable/unfavorable pair was checked with a deficiency simulation during drafting.
- **Business notation**: IBCS (Lapajne 2015): consistent encodings for scenarios and variances, absolute and relative variance (ΔPY, ΔPY %). The table's specific encodings are an IBCS-inspired convention, not checked against IBCS 2.0 or ISO 24896 text.
- **Convention, not tested in the research base**: forms for distribution, relationship, ranking and maps; no 3D; time axes; n and table-size thresholds; table and number formatting; gauges.
