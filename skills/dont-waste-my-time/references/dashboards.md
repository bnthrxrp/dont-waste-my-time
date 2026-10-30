# Dashboards, KPI screens and BI specifications

Read this when building, specifying or improving a dashboard, KPI screen or scorecard (HTML, Power BI, Tableau, Excel). A dashboard is a decision interface, not a collection of charts: maximize decision value per unit of attention, and never mislead.

## Contents
- Logic: 1 Decision-first workflow · 2 KPI specification template · 3 Polarity and status logic · 4 Targets and comparisons · 5 Data latency and freshness
- Design: 6 Layout and hierarchy · 7 Charts that work in dashboards · 8 Interactions · 9 States · 10 Accessibility and responsiveness
- Build and check: 11 HTML implementation · 12 Testing procedure · 13 BI specification template · Evidence notes

## 1. Decision-first workflow

1. **Decisions and questions.** Name the audience, the 3-5 decisions or management questions the screen serves ("Will we hit the month? Where is the gap? Execution or market?"), and the genre: *monitoring* (recurring check against targets), *analytical* (explore drivers) or *narrative* (communicate one finding). The genre decides the first screen. If the user gave only data, infer the questions and state them in the header or the spec's purpose.
2. **KPI logic.** For each question, choose the output KPI that answers it and the 1-3 controllable inputs that drive it. Drop any metric that answers no question. Write a section 2 spec for each headline KPI.
3. **Validate data and definitions.** Profile the source first: periods covered, missing rows, duplicates, units, grain, which comparisons exist (target, budget, prior year, forecast), and oddities such as a prior year that falls every month. Each gap becomes a visible caveat or `[TBD: what, owner]`, never an imputed value.
4. **Targets, comparisons and thresholds** (sections 3-4), only from the user's material or the business.
5. **Information hierarchy** (section 6): zones, headline KPI count, what the first screen holds.
6. **Charts and interactions** (sections 7-8): each chart answers a named question; each control maps to a decision.
7. **Implement or specify**: an HTML file (section 11), a BI spec (section 13), or a handoff to a frontend skill.
8. **Test** values, labels, polarity, states and interactions on the rendered artifact (section 12).
9. **One-minute test.** Look at the desktop screenshot cold. Can a director state the situation and the 1-3 things that need attention within a minute, without scrolling, hovering or touching a filter? If not, fix the hierarchy, not the styling.

## 2. KPI specification template

Fill one per headline KPI and per metric that carries a status. In HTML it becomes the config object that drives cards and status; in a BI spec it becomes the KPI dictionary.

```
Name:               Net sales MTD
Question:           Will we hit this month's sales target?
Definition, formula: Σ invoiced net sales after on-invoice discounts, 1st of month to last closed day; excludes intercompany
Aggregation:        sum across units and days (ratios: Σ numerator / Σ denominator)
Source, grain:      ERP sell-in, SKU × customer × day
Refresh, latency:   daily, D+1
Target, source:     monthly budget phased by working days (FP&A budget v3)  |  [TBD: target, owner: FP&A]
Comparisons:        phased target; prior year like-for-like; same working day last month; forecast
Polarity:           higher is better | lower is better | in range [a-b] | neutral
Status rule:        green ≥ phased target; amber within [TBD: tolerance, owner]; red beyond tolerance
Type:               lagging or leading; output or input (controllable)
Owner:              the person who explains movements and owns the action
Caveats:            known gaps of the proxy; guardrail metric that would expose gaming (e.g. sales vs returns)
```

- **Never invent a target or threshold.** No target: write `[TBD: target, owner]` in the spec and show "No target" on the card. A tolerance band you suggest is a recommendation: label it on the screen itself ("proposed, to be confirmed by <owner>"), not only in your final message.
- **Write formulas two analysts would compute identically**: filters, exclusions, currency, period boundaries, returns, duplicates.
- **Aggregate ratios from components** (margin %, OTIF, DSO, coverage, conversion): Σ numerator / Σ denominator. If only per-unit ratios exist, weight by the denominator and say so in the definition. Never average percentages across channels or months.

## 3. Polarity and status logic

- **Status only where a target or threshold exists.** Without one, show value, comparisons and trend, and no red/amber/green.
- **Thresholds in business terms, with their source**: credit policy 45 days, contract SLA 98%, spend cap 9% of revenue, covenant 3.0×. Write the rule as text on the card or its tooltip, so the color is auditable.
- **Color follows polarity, not direction.** The arrow shows direction (▲/▼); the color and word show whether that is good. Rising DSO, inventory weeks, complaints, cost, churn, stock-outs or lead time is unfavorable. Set polarity explicitly per metric; never infer it from the sign.
- **In-range metrics** (sell-in/sell-out ratio, price index, stock cover where both shortage and excess hurt): favorable inside the band, unfavorable outside it on either side. State the band.
- **Neutral metrics** (units shipped, visits, market size) get no status color; their arrows stay grey.
- **No watermelons** (green outside, red inside). Derive an aggregate's status from its components as well as its total: show "2 of 3 channels off track" on the tile, and never show an aggregate green while a material component is red. Define "material" in the KPI spec (share of sales, value at stake). The same applies to project and program roll-ups.
- **Limit alerts to what needs action.** Flag only breaches someone can act on, ranked by business impact, about five at most on the first screen. Raise a flag on a new or worsening exception, not on every refresh; an unchanged open flag shows its age ("off track 3 weeks") instead of re-alerting. Each flag names the owner and next step, or `[TBD: action, owner]`.
- **One status vocabulary** across the dashboard (e.g. ✓ On track, ! Watch, ✕ Off track): icon, word and color together, same thresholds wherever the metric appears.

## 4. Targets and comparisons

- **Phase period targets.** Compare MTD or QTD actuals with a phased target: by working days elapsed, or by the historical intra-period curve when sales are back-loaded (otherwise every month shows red until its last week). Use calendar-day phasing only when the business confirms it. State the method in the definitions.
- **Like-for-like prior year.** Align working days and calendar effects (moving holidays, leap day, 53-week years), scope (openings, closures, acquisitions, discontinued lines) and currency (constant vs reported). When reported and like-for-like differ materially, show both, labeled.
- **Label every value with its period** ("Sep", "YTD Sep", "MTD to 26 Oct", "L4W"). Show month and YTD together when they tell different stories.
- **Run-rate and landing estimates** carry the label "estimate" and their method (e.g. MTD actual + remaining working days × trailing 20-day average). Draw them hollow or dashed, never styled as actuals.
- **Base effects.** Check the comparison base before reporting growth: a weak or falling prior year inflates growth, a one-off in the base distorts it. Say so beside the number and lead with the undistorted comparison (target, budget, two-year).
- **Variances**: absolute and relative together, signed, labeled favorable or unfavorable by polarity, for each comparison shown. Rate variances are in percentage points (pp).
- **Mixed frequencies**: never combine weekly and monthly sources in one tile without a separate as-of label per source, and never split monthly data into weeks to make it fit.

## 5. Data latency and freshness

- **As-of on every tile or section** ("Sell-in through 26 Oct · Sell-out through Aug"). A single header date is enough only when all sources share it.
- **Stale**: define the expected freshness per source in the spec. When a source is older, show "Stale since <date>", keep the value visible, and grey its status. Never show green on stale data.
- **Partial periods**: label completeness ("MTD, 14 of 21 working days"), compare only with phased targets or the same point of earlier periods, and draw the partial point distinctly on trends. A total built from the units that reported says which ("3 of 4 regions").
- **Sample-based or projected metrics** say so on the card ("Store-audit panel, n = 250, urban stores over-represented"; "projected sell-out"). Name them by what they measure ("Panel out-of-stock", not "National out-of-stock") and suppress breakdowns below the minimum sample stated in the spec.
- **Metadata on every dashboard**, one click away at most: sources, owner, definitions, last refresh, phasing method, proposed thresholds, known limits.

## 6. Layout and hierarchy

Use only the zones that apply, in this reading order (top-left first):

| Zone | Content | Typical form |
|---|---|---|
| 1. Performance at a glance | Headline KPIs vs target and one comparison | KPI cards or a bullet-graph strip |
| 2. Material changes and exceptions, in words | 3-5 generated sentences: what moved, by how much, against what, why if known, owner and next step | Ranked text list |
| 3. Drivers | Controllable inputs; where the gap sits (channel, region, price/volume/mix) | Variance bars, small multiples, conditional table |
| 4. Risks and opportunities | Forward-looking: landing estimate, leading indicators, pipeline | Bullet graphs, short list |
| 5. Decisions and actions | Open decisions, owners, dates, only when the user's material supplies them | Short table |

- **Headline KPI count** follows the dashboard row of the length budgets in briefing.md. Everything else goes to drivers or drill-down.
- **First screen**: zones 1-2 fit a laptop screen without scrolling. Beyond that, progressive disclosure: overview → driver → detail, one click each, with a visible way back.
- **Fixed structure for recurring dashboards**: same order, positions and encodings every period, so readers spot change instead of re-learning the page.
- **Link outputs to inputs**: each output card sits above, or links to, the driver view that explains it.

KPI card anatomy (drop the sparkline before the comparison):

```
┌──────────────────────────────────────────────┐
│ Net sales · MTD to 26 Oct        ✕ Off track │  label with period · status: icon + word + color
│ $41.2M                                       │  value with unit
│ vs phased target  −$2.3M (−5.3%)  ▼          │  absolute and % variance, signed, by polarity
│ vs PY like-for-like  +$1.1M (+2.7%)  ▲       │  second comparison only if it changes the reading
│ ▁▂▃▃▄▅▅▆ last 8 weeks                        │  optional sparkline, same window on every card
│ ERP through 26 Oct · Target: budget v3       │  as-of and target source
└──────────────────────────────────────────────┘
```

## 7. Charts that work in dashboards

General chart rules (baselines, color, labels, honesty) are in dataviz.md; these are the dashboard-specific choices:

- **Actual vs target: bullet graph.** A bar for the actual, a thin marker for the target, and up to three bands in shades of one muted hue, drawn only where thresholds exist. It replaces gauges, takes less space, and lines up for comparison.
- **Trend inside a card: sparkline.** No axes, the same window on every card, last point marked. It shows shape; the number lives in the card.
- **Recurring-review trend**: trailing 6 weeks beside trailing 12 months, prior year faded behind the current year, target markers only where targets exist, growth rate beside the absolute value.
- **Same metric across units: small multiples** on a shared axis, sorted by gap or size, not alphabetically.
- **Variance bars** from a zero line, colored favorable or unfavorable by polarity (not by sign) and labeled with the signed value.
- **Scorecard tables with conditional formatting**: status icon and word, right-aligned numbers, consistent decimals, rows sorted by impact.
- **Avoid** gauges and dials, donuts or pies for status, 3D, and decorative maps. Use a map only when location drives the decision (territories, routes); otherwise a sorted bar by region is easier to compare.

## 8. Interactions

- **Only filters that map to decisions**: period, region, channel, product, account owner. No control nobody would change to decide something.
- **Defaults are the view the reader needs on open**: last complete period, all units, or the reader's own scope under row-level security.
- **Drill-down path**: KPI or exception → driver breakdown → detail table, with a visible way back. One **reset** control restores defaults.
- **Every control changes the view.** If an element ignores a filter, label it ("not filtered by week"); otherwise wire it or remove the control. No decorative controls.
- **Keep state visible**: active filters appear as chips or in titles ("Net sales · Retail · YTD Sep"), so screenshots and prints carry them. Titles and exception sentences recompute for every filter state and stay true in each.
- Tooltips add detail (definition, exact value, as-of); never put information needed for the one-minute read only in a tooltip.

## 9. States

| State | What it shows | Never |
|---|---|---|
| Loading | Fixed-layout skeleton, "Loading <source>…" | Zeros, or the previous selection's numbers |
| Empty | "No <metric> for <selection> in <period>" and a reset link | A 0 that reads as a real value; a blank chart |
| Error | Which source failed, last good as-of, affected tiles marked | Old numbers presented as current |
| Stale | Value with "Stale since <date>"; status greyed | Red or green on stale data |
| Partial | Completeness label ("14 of 21 working days", "3 of 4 regions"); phased comparisons only | A partial period compared with a full one |
| No target | Value, comparisons, trend, and "No target" or `[TBD: target, owner]` | A status color or an invented target |

## 10. Accessibility and responsiveness

- **Contrast**: text at WCAG AA text contrast; chart marks, status icons and focus outlines at least 3:1 against what surrounds them, in every theme offered.
- **Never color alone**: status is icon + word + color; variances carry a sign; series are labeled directly. The page must still read correctly printed in greyscale.
- **Keyboard**: every control reachable by Tab and operable by Enter, Space or arrows, with a visible focus outline. Use native `<button>`, `<select>` and `<input>`, not clickable `<div>`s.
- **Text alternatives**: each chart has an accessible name stating its takeaway (`role="img"` with `aria-label`, or a caption), and its data is available as a table.
- **Reflow at 390 px**: cards stack in priority order, charts resize (SVG `viewBox`, no fixed pixel widths), and the page never scrolls horizontally.
- **Tables scroll inside their own container**: wrap each table in a block with `overflow-x: auto` and keep the first column sticky. Never let a table widen or clip its card; `overflow: hidden` on the card hides the defect without fixing it.
- **Print**: `@media print` hides controls, prints the active filters and as-of dates, avoids page breaks inside cards.

## 11. HTML implementation

If a frontend or design skill is available, hand it the spec (KPI dictionary, zones, chart per question, interactions, states), then QA its output with section 12. Otherwise, or when the user wants a single file:

- **One self-contained file that opens offline**: inline CSS and JS; charts in vanilla SVG (or Canvas). If a library is worth it, pin an exact version and inline it, so opening the file requires nothing external. Light/dark is optional; if offered, use CSS color variables and check status colors in both.
- **Embed the raw source rows, not results.** Generate a `<script type="application/json" id="data">` block from the source file with a script, so no figure is typed by hand. Compute every displayed number in code from those rows: totals, variances, ratios, statuses, exception sentences, titles. Print the period the embedded data covers.
- **Drive cards from a KPI config** that mirrors section 2 (field, aggregation, target field, polarity, status rule, format, period), with one status function (higher, lower, range, neutral) and one formatter per unit. No per-card special cases.

## 12. Testing procedure

Test the rendered artifact, not the code. Fix, re-render, repeat until clean.

1. **Render and look**: `python3 ${CLAUDE_SKILL_DIR}/scripts/render.py dashboard.html` produces desktop and mobile screenshots and reports console errors and horizontal overflow. Open the images and read them. Zero console errors and zero page overflow are required.
2. **Exercise every filter and find clipped containers.** Page-level overflow checks miss a table clipped inside its card. Run this (Node + Playwright), extend the loop to buttons and toggles, and treat each `NO CHANGE` or clipped element as a defect:
```js
// NODE_PATH=$(npm root -g) node qa.js dashboard.html
const { chromium } = require('playwright'), { resolve } = require('path');
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1440, height: 900 } }), errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.goto('file://' + resolve(process.argv[2]));
  const view = () => p.locator('body').innerHTML();  // Canvas charts: compare p.screenshot() buffers instead
  for (const s of await p.locator('select').all()) {
    const vals = await s.locator('option').evaluateAll(o => o.map(x => x.value)), base = await view();
    for (const v of vals.slice(1)) { await s.selectOption(v); if (await view() === base) console.log('NO CHANGE:', await s.getAttribute('id'), v); }
    await s.selectOption(vals[0]);
  }
  for (const w of [1440, 390]) {
    await p.setViewportSize({ width: w, height: 900 });
    console.log(w, 'clipped:', await p.evaluate(() => [...document.querySelectorAll('body *:not(svg *)')]
      .filter(e => e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1 && !/auto|scroll/.test(getComputedStyle(e).overflowX))
      .map(e => e.tagName + '.' + e.getAttribute('class'))));
  }
  console.log('errors:', errs); await b.close();
})();
```
3. **Recompute 2-3 headline numbers independently** from the source file with a separate script (not the dashboard's code): the top-left KPI, one variance, and one value under a filter. Compare with the rendered text. A mismatch is a blocking defect.
4. **Polarity audit**: list every colored element (cards, arrows, variance bars, table cells, exception wording) with its metric, polarity, direction and the color shown. Fix any unfavorable move shown as good and any status on a metric without a target.
5. **Read the "needs attention" text against the data** in the default state and at least one filter state: every number matches, "improved" and "worsened" agree with polarity, and no off-track item is missing.
6. **States**: force at least the empty, stale and no-target cases once and compare what appears with section 9.
7. **One-minute test** (section 1, step 9) on the desktop screenshot.

## 13. BI specification template

For Power BI, Tableau or Looker teams. Page 1 of the spec carries purpose, decisions and headline KPIs; the rest is as long as the builders need.

```
1. Purpose and users     Who uses it, in which meeting or routine, to decide what; primary and secondary users; genre.
2. Decisions supported   3-5 management questions, in the order page 1 answers them.
3. Pages                 Page list, one line of purpose each; page 1 wireframe.
4. KPI dictionary        One row per KPI. Columns: KPI | Question | Definition and formula | Aggregation | Source, grain |
                         Refresh, latency | Target (source) | Comparisons | Polarity | Status rule | Lead/lag | Input/output | Owner | Caveats
5. Data                  Sources with grain, refresh, latency and expected freshness; model (facts at native grain,
                         conformed dimensions, mapping tables); calendar (working days, holidays, week definition).
6. Security              Row-level rules per role, test user per role, who sees everything.
7. Interactions          Slicers with defaults and sync scope, visuals that ignore them, drill paths, tooltips, reset.
8. States                Loading, empty, error, stale, partial and no-target behavior (section 9).
9. Acceptance tests      Checks the builder can run (below).
10. Open questions       Question | owner | needed by | what it blocks.
```

Page 1 wireframe (adapt it, keep it to one screen):

```
┌──────────────────────────────────────────────────────────────────────┐
│ Takeaway title (generated) · Period ▾ · Region ▾ · Channel ▾ · Reset │
│ ERP through dd/mm · Sell-out through mmm · Finance through mmm       │
├───────────┬───────────┬───────────┬───────────┬───────────┬──────────┤
│ KPI 1     │ KPI 2     │ KPI 3     │ KPI 4     │ KPI 5     │ KPI 6    │
├───────────┴───────────┴───────────┼───────────┴───────────┴──────────┤
│ Needs attention: 3-5 ranked       │ Gap to target by channel/region  │
│ sentences with owner, next step   │ (variance bars, sorted by gap)   │
├───────────────────────────────────┴──────────────────────────────────┤
│ Drivers: inputs vs target (bullet graphs) → drill-through to page 2  │
└──────────────────────────────────────────────────────────────────────┘
```

Acceptance tests to include:
- Each headline KPI reconciles to its source system for one closed period, within `[TBD: tolerance, owner]`.
- Each status rule returns the expected result at, just above and just below every threshold, for each polarity.
- Every visual shows an as-of date; no tile mixes frequencies without per-source labels.
- Every slicer changes every visual it is synced to; visuals that ignore it say so.
- Each row-level-security role sees only its rows; empty, stale and no-target states render as specified.

Before delivery, run `python3 ${CLAUDE_SKILL_DIR}/scripts/numbers_check.py trace spec.md --sources <inputs>`: every target and threshold must trace to the inputs or be marked proposed or `[TBD]`.

## Evidence notes

- Genre before layout; named patterns for metadata (source, definitions, disclaimer, update date), explicit thresholds, screenfit and detail on demand: Bach et al., "Dashboard Design Patterns", IEEE TVCG 29(1), 2023 (arXiv 2205.00757), and the authors' pattern catalogue. It catalogues practice; it does not show that the patterns improve decisions.
- Bullet graph as a gauge replacement: Few's design, via the Wikipedia "Bullet graph" article (secondary). One eye-tracking study (Wu et al., Springer, 2019; 40 participants) reports more efficient reading than gauges, measured as time to first fixation, not accuracy.
- Controllable inputs vs outputs, a fixed format each period, targets only where they exist, growth beside absolute values, prior year faded: Commoncog, "The Amazon Weekly Business Review" (practitioner account of one company).
- Alert limits: Ancker et al., BMC Medical Informatics and Decision Making 17:36, 2017. Each additional reminder per encounter was associated with 30% lower acceptance, and repeated reminders also lowered acceptance. Clinical setting; the transfer to KPI alerts is an inference.
- Watermelon reporting: practitioner guidance only (Pragmatic Coders, 2026), with no outcome data; the component-status rule is a design choice. Guardrail metrics: Manheim and Garrabrant, "Categorizing Variants of Goodhart's Law", arXiv 1803.04585 (conceptual).
- Color and contrast: W3C, Understanding WCAG 2.1 SC 1.4.1 Use of Color and SC 1.4.11 Non-text Contrast (3:1). Angle and area are judged less accurately than position and length (Heer and Bostock, CHI 2010), hence no gauges or donuts for comparison. Absolute and relative variance side by side: IBCS example in Lapajne, AFP Exchange, November 2015.
