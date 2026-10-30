# Analysis: deciding what is true and what to recommend

Read this before writing a report, memo, business review, business case or research-driven recommendation whenever you cannot yet write the answer in one sentence (SKILL.md section 3), or the answer rests on numbers you must interpret. It is a thinking toolkit. The reader sees conclusions and the evidence that carries them, not the method: keep trees, full decompositions and sensitivity tables in an appendix or leave them out. Analysis depth never justifies document length.

## Contents
1. Method selector
2. Hypothesis-driven loop
3. Structuring: issue trees and driver trees
4. Performance and variance analysis
5. Sanity checks before any conclusion
6. Recommendation anatomy
7. Business cases
8. High-stakes decision hygiene
9. Prioritization
- Evidence notes

## 1. Method selector

Name the question type, then use the lightest method that answers it.

| Question | Lightest adequate method | What the reader sees |
|---|---|---|
| "How are we doing?" | Actual vs the one reference the reader is accountable for, plus exceptions | Status in one line, the 2-3 variances that matter, the landing |
| "Why did X change?" | Variance or driver decomposition (section 4) | A bridge from base to actual whose components sum to the total |
| "Where is the problem?" | Drill down the driver tree to where the gap concentrates; claim a root cause only with evidence at each step | Where it is, the cause with its evidence status, what is still unexplained |
| "What should we do?" | 2-4 options, including doing nothing, against explicit criteria (section 6) | Recommendation, trade-offs, decision requested |
| "Is it worth it?" | Business case with breakeven and sensitivity (section 7) | The ask, payback, what must be true |
| "What will happen?" | Driver-based scenarios: each is a set of driver values with a reason, varying several drivers together | A range, the 1-2 drivers that move it; scenarios called plausible, not likely |
| "What first?" | Impact x urgency, then effort (section 9) | Ranked list with a cut line |
| "Is this claim right?" | Trace it to its source, then section 5 | Verdict with evidence status |

**Don't over-frame simple tasks.** If one comparison or one lookup answers the question, give it and stop. Summarizing someone else's report needs no tree, scenario or option set. Combine methods only when the question has two parts (why it changed, then what to do). Never name the framework in the deliverable ("Using an issue tree, we...").

## 2. Hypothesis-driven loop

Use it for diagnoses, recommendations and business cases.

1. **Day-one answer.** Before analyzing further, write the most likely answer from what you already have, in one sentence. Treat it as a hypothesis.
2. **What must be true.** List the 2-4 conditions it depends on ("the decline is in existing stores, not from closures"; "competitors did not cut price").
3. **Test with the data you have**, cheapest decisive test first. For each condition, state the result that would disprove it and look for that result.
4. **Revise or kill.** If a condition fails, change the answer; don't rescue it with qualifiers. If the data cannot test a condition, carry it into the deliverable labeled assumption or hypothesis and name the data that would settle it.

Keep a second candidate answer alive until a test separates the two: a single hypothesis invites a search for confirming evidence only. A tested hypothesis becomes a finding with its evidence; an untested one stays a hypothesis in the text.

**Don't use it** for pure reporting (describe what changed, and hypothesize only to explain material variances), for translation or proofreading, or when the user asks for neutral exploration. In that last case, set out the competing explanations and what would distinguish them, without picking one.

## 3. Structuring

- **Driver tree for a metric.** Split the metric into arithmetic components (revenue = outlets x active rate x orders per outlet x average order value). Children must recombine exactly to the parent; if they don't, the tree is wrong or a residual is missing. Use it for "why did X change" and "what will happen".
- **Issue tree for a question.** Split the question into sub-questions whose answers together answer it ("Can we win in regional chains?" → is the pool big enough / can we get listed / can we serve it profitably). Use it for "where is the problem" and "what should we do". Push each branch down to an analysis you can run or a fact you can look up, and prune branches that cannot change the answer.
- **MECE is a check, not a ritual.** Test any split for three things:
  - **Gaps:** is something unaccounted for? Show it as a quantified "other" or "unexplained"; never drop it.
  - **Overlaps:** could one unit of money or one customer count twice?
  - **Relevance:** does every branch matter to the decision? A complete list can still hold items that don't belong.
- **When not to force it.** When causes interact (price and promotion, coverage and distribution), show the interaction instead of forcing exclusivity. Overlapping views (by customer and by product) can sit side by side if each is internally consistent and you never add them together. Show the tree to the reader only when the tree is the argument.

## 4. Performance and variance analysis

**Pick the comparison the decision needs.**
- Budget or target: are we delivering what we committed?
- Prior year: is the business growing underneath?
- Latest forecast: what is new since the last update?

Lead with the comparison the reader is accountable for; add another only when it tells a different story. Call variances favorable or unfavorable by polarity (a cost increase is unfavorable), not by sign.

**Decompose, and state the method.** Choose additive (money) or multiplicative (growth rates) and say which. Also say the order of effects, because the order changes the split. Unless the organization has its own convention, use:

```
V, R = total volume and revenue; i = item; 0 = base period, 1 = current period
AvgP0  = R0 / V0
Volume = (V1 - V0) x AvgP0
Mix    = Σ(V1,i x P0,i) - V1 x AvgP0     (needs item-level data)
Price  = Σ(P1,i - P0,i) x V1,i           (at constant currency)
Volume + Mix + Price = R1 - R0 exactly. FX, scope and other effects are separate bridge steps.
```

- Mix depends on the level you compute it at: an SKU-level analysis moves into mix some of what a category-level analysis calls price. State the level.
- Multiplicative: (1 + g_revenue) = (1 + g_volume)(1 + g_mix)(1 + g_price). The rates don't add; never present them as points summing to total growth unless you show the cross term.
- Costs: rate x volume with the same logic (freight = cost per tonne x tonnes). FX: restate the current period at prior-period rates; the difference is the FX effect.
- A material residual or "other" means the decomposition is incomplete; say so next to the bridge.

**Adjust before you interpret.**

| Effect | Rule |
|---|---|
| Run-rate vs one-offs | Strip one-offs from both periods and show reported → adjusted as a bridge. An item that recurs every year is not a one-off. |
| Working days, seasonality | When day counts differ, compare per selling day and state the counts. In seasonal businesses, compare with the same period last year, not the prior month. |
| Base effects | For a big % on a depressed or tiny base, give the absolute change and name the base-period anomaly. |
| Controllable vs uncontrollable | Separate management actions from FX, commodities, regulation and weather, then say which response is controllable. "Uncontrollable" never explains the gap left after those effects. |
| Sell-in vs sell-out | When shipments outrun offtake, check channel inventory (weeks of cover): pipeline fill or pre-buying ahead of a price increase reverses later. Report the measure closer to end demand, or both. |
| Scope changes | Report like-for-like separately from the effect of acquisitions, disposals, openings and closures. |

**End with the landing.** State what the variance means for the period outcome: current landing vs target, the gap, and what closing it requires per remaining month. Label it calculated and give the basis (run-rate, seasonal profile or latest forecast).

## 5. Sanity checks before any conclusion

Run these on every number that carries a conclusion. A failure means you fix it, put the caveat next to the number, or drop the conclusion.

- [ ] **Denominators and bases:** is it the right base (per outlet, per selling day, per active customer)? A ratio of totals, not an average of ratios, unless stated? Is the base period named?
- [ ] **Mix / Simpson's paradox:** does the aggregate trend hold inside each major segment? If the segment mix shifted, decompose before calling it performance.
- [ ] **Small samples:** would one or two observations flip the result? Then say so, and don't rank or extrapolate.
- [ ] **Survivorship:** are closed stores, lost customers, delisted SKUs or abandoned projects missing from the set?
- [ ] **Correlation vs causation:** does the causal claim have a mechanism, the right timing, a comparison group and no obvious confounder (promotion, season, price change)? If not, label it hypothesis.
- [ ] **Regression to the mean:** was the unit chosen because it was extreme? Expect partial reversal with no action, and don't credit the action for it.
- [ ] **Units, currency, nominal vs real:** same unit, scale (k vs M), currency and FX basis, and price level; % vs percentage points; gross vs net.
- [ ] **Period alignment:** same calendar or fiscal weeks, cut-off dates and YTD/LTM/month basis; same metric definition in both periods.
- [ ] **Polarity:** is up good for this metric? Labels, colors and "favorable" follow it.
- [ ] **Totals with missing parts:** does every total cover what its label claims? If not, say so in the label ("3 of 4 regions") and don't compare it with a complete total.
- [ ] **Rounding consistency:** each number appears the same way everywhere (summary, table, chart, appendix). Rounded parts that don't sum to the rounded total carry a note.

## 6. Recommendation anatomy

The answer and the ask come first; everything else supports them.

| Element | Passes when | Fails when |
|---|---|---|
| The answer | One sentence: the action, its scale, its timing | "We should consider exploring..." |
| Options | 2-4 real options plus doing nothing, with the cost of doing nothing; each rejected option says why | Strawmen that flatter the pick; doing nothing is missing or costed at zero |
| Criteria | Set before comparing, in the reader's terms (cash, risk, time to impact, reversibility, capability); weighted if they conflict | Criteria chosen after the fact to justify the pick |
| Trade-offs | What the pick gives up versus the runner-up | Only upsides |
| Risks and mitigations | The 2-4 that could sink it, each with a mitigation or early-warning signal and an owner | Generic entries ("execution risk", "market risk") |
| What would change it | The threshold or signal that flips the call ("stop if pilot conversion < `[TBD: threshold, owner: Sales]` by month 3") | Absent |
| Decision requested | What exactly is approved, by whom, by when, and the cost of delay | "For discussion" when a decision is needed |
| Next steps | An owner and a date for each | Actions without owners |

When several parties are involved, name:
- who recommends;
- the single person who decides;
- who must sign off before the decision, and whether each sign-off can block it and what happens if they object (state it explicitly: frameworks, including Bain's own articles on RAPID, disagree on whether sign-off is a veto);
- who executes;
- who only gives input.

**Scale to the decision.** A routine or easily reversed decision needs only a short statement: the ask, one alternative, the main risk, the deadline. Use the full anatomy for consequential or hard-to-reverse calls.

## 7. Business cases

**Structure.**
- **Costs:** keep one-time costs (recruiting, capex, implementation, exit costs) separate from recurring ones (fully loaded pay, licenses, maintenance). Include what owners forget: management time, travel, systems, overlap during ramp-up.
- **Benefits:** incremental to a stated counterfactual (what happens if we don't do it), in margin or cash rather than revenue, net of cannibalization, with a ramp (time to hire or build, then time to full productivity).
- **Payback:** say whether it is simple or discounted, and from which date it is counted (approval, hire, go-live).
- **NPV/IRR:** only when timing matters (multi-year horizon, uneven cash flows, capex). Take the discount rate from Finance, `[TBD: hurdle rate, owner: Finance]`; never assume one. A one-year opex request needs only payback and breakeven.

**Sensitivity and breakeven.** Find the 1-3 inputs that swing the answer most and give each a breakeven: "the case holds as long as each hire adds at least X in incremental margin". A breakeven turns missing data into a question the reader can test. Build scenarios from explicit driver values, each with a reason ("downside: ramp of `[TBD]` months instead of `[TBD]`, because listings follow annual line reviews"). Never apply a blanket ±10% to the result.

**Missing inputs (the most common failure).** When the numbers that decide the case are not in the user's material:
1. If the user can probably supply them, ask one targeted question, folded into the brief if one is being asked: "Do you have the fully loaded cost per KAM and current KAMs' first-year incremental sales? If not, I'll build the case with placeholders."
2. Otherwise build the full logic with visible placeholders and formulas, e.g. `[TBD: fully loaded cost per KAM, owner: HR]`. Calculate everything the given data allows; express the rest as formulas and breakevens. Figures the user supplies are inputs; label unverified ones assumption.
3. Never put invented, "illustrative", "typical" or "assumed" figures in the body, the headline or the ask. A drafting note does not fix this: notes get deleted and the numbers stay. Use a benchmark only if you opened its source in this session, cite it and label it source-reported.
4. If the user explicitly asks for a worked example, or asks you to assume the numbers, put them in a separate section titled "Hypothetical example: not company data". Use obviously round numbers, and keep them out of the headline, the summary and the ask.
5. List every placeholder in your final message (SKILL.md section 9).

Before (invented figures in the ask):
> Hiring 3 KAMs ($585K/yr fully loaded) will add $4.5M in net sales and $1.8M in contribution, paying back in 12 months.

After (the logic, with placeholders the CFO can fill):
> Approve 3 KAMs for regional pharmacy chains. The case turns on one test: at steady state, each KAM must add incremental annual sales of at least `[TBD: fully loaded cost per KAM, owner: HR]` ÷ `[TBD: contribution margin after trade spend, owner: Finance]`. Current KAMs' first-year results, `[TBD: year-1 incremental sales per KAM, owner: Sales Ops]`, show whether that bar is realistic.

## 8. High-stakes decision hygiene

Apply this to High-stakes work and to any recommendation that commits significant money or is hard to reverse. Skip it for routine decisions.

- **Real alternatives.** Evaluate at least two serious alternatives and give the reason each was dropped. A single-option recommendation says why no alternative is credible. Imposing a pre-chosen solution and cutting the search for alternatives short are associated with failed decisions.
- **Outside view.** Anchor base-case timing, cost, ramp and adoption on a named reference class: comparable past projects, the company's own track record, or base rates from a source you opened in this session. Show the gap between that and the internal estimate. If none exists, label the figure "inside-view estimate, not benchmarked", give a range, and never invent a base rate. Large-sample forecasts are systematically optimistic (transport-infrastructure data); assume corporate plans share the bias until shown otherwise.
- **Worst case with an origin.** Say where the downside comes from, including competitor response. Base case minus 10% is not a worst case.
- **Pre-mortem.** Assume the decision has failed by the review date and list 3-7 specific causes, each with a mitigation or early-warning signal and an owner. Carry the ones that change the plan or need monitoring into the risks; leave out generic ones.
- **Disconfirming evidence.** State what would prove the recommendation wrong, that you looked for it, and what you found.
- **Separate advocates from evaluators.** If you built the case, you are its advocate and can't reliably see its biases. For High-stakes work, use the independent review in SKILL.md section 7, briefed to attack the recommendation, not to polish it. When evaluating someone else's proposal, review how it was produced as well as what it says: where the numbers came from, which alternatives were dropped and why, who benefits, and how optimistic the base case is.
- **Weakest link.** Before sending, check the frame, the objectives, the alternatives, the information and its uncertainty, the reasoning, and the commitment to act. Fix the weakest first: strong analysis does not rescue a wrong frame or a missing alternative.

## 9. Prioritization

- Score impact in one common unit (margin, cash, risk avoided) and urgency as the cost of delay or a hard deadline; break ties on effort (time, money, scarce people). Show the scoring basis and label judgment calls estimate.
- With fewer than about eight items, a ranked list with a cut line beats a 2x2. Say what to do now, what to defer and what to stop.
- 80/20 is a hypothesis to check, not a fact to assert. Measure the real concentration ("top N of M SKUs = X% of the gap", calculated) before writing it, keep the tail visible as one "other" line, and flag small items that are growing fast.

## Evidence notes

Sections 2, 6 and 8 draw on the sources below. Each was opened in full or in part and checked by an independent validator (research/validation/A-strategy-combined.md in the skill's repository). They are practitioner guidance, interviews or small and correlational studies; none shows that a given checklist improves outcomes. The structuring, variance and business-case conventions are standard practice and are not sourced here.

**Never cite these as established:**
- Klein's "30%" premortem improvement (not traceable to the underlying study);
- Schoemaker's student-experiment figures (not reproduced);
- Bain's "95% correlation" (no method given);
- Nutt's "half fail" without its definition (not in sustained, full use after two years).

**When quoting the decision-process literature**, give the study, sample, definition and limitation. For example: "Lovallo and Sibony (McKinsey Quarterly, 2010): in 1,048 self-reported decisions, top-quartile decision process went with ROI 6.9 percentage points higher than the bottom quartile (673 with ROI data); correlational."

- **Flyvbjerg, "From Nobel Prize to Project Management: Getting Risks Right"** (Project Management Journal, 2006; arXiv full text):
  - transport-infrastructure cost forecasts were systematically low, with no improvement over the 70-year period studied;
  - basis for reference-class forecasting.
- **Camuffo, Cordova, Gambardella and Spina** (Management Science, 2020):
  - randomized trial with 116 early-stage startups;
  - training in hypothesis testing improved performance;
  - setting is startups, not corporate analysis.

- **Kahneman, Lovallo and Sibony, "Before You Make That Big Decision...", Harvard Business Review, June 2011** (read via a university-hosted reprint, <https://faculty.washington.edu/pathaksd/BBUS549/Required%20Readings/Before%20You%20Make%20that%20Big%20Decision.pdf>):
  - review the process behind a proposal, not only its content;
  - demand real alternatives, and look for evidence against the main hypothesis;
  - beware perfunctory risk lists and strawman options;
  - use the outside view, and question where the worst case comes from;
  - keep reviewers independent of the recommending team;
  - the checklist is not meant for routine, rubber-stamped decisions.
- **Klein, "Performing a Project Premortem", Harvard Business Review, September 2007** (reprint, <https://comprobo24.github.io/assignments/performing_a_project_premortem.pdf>): the premortem method; the supporting evidence is anecdotal.
- **Nutt, "Surprising but true: Half the decisions in organizations fail", Academy of Management Executive, 1999** (<https://cebma.org/assets/Uploads/Nutt-1999-gecomprimeerd.pdf>): in 356 senior-manager decisions, imposed solutions and a limited search for alternatives went with failure. Success is defined by implementation (sustained use).
- **Eisenhardt, "Making fast strategic decisions in high-velocity environments", Academy of Management Journal, 1989** (abstract and editors' summary only, <https://www.cambridge.org/core/books/strategy-as-practice/making-fast-strategic-decisions-in-highvelocity-environments/4397236CC78572C22EA205AE1E6B7795>): in eight firms, faster decision makers developed more alternatives, not fewer.
- **Spetzler, "The six elements of a good decision", CBS News interview** (page updated 2009, <https://www.cbsnews.com/news/carl-spetzler-the-six-elements-of-a-good-decision>): decision quality is capped by its weakest element.
- **Bain & Company, decision-rights articles** (<https://www.bain.com/insights/decisions-who-does-what/>, <https://www.bain.com/insights/decision-insights-3-make-decisions-work>): one decider per decision for single-point accountability. Input roles advise but cannot veto. State the decision, its owner, the process and the deadline explicitly. These are practitioner articles with anecdotal examples.
- **Minto (barbaraminto.com) and the McKinsey Alumni News profile of Barbara Minto**: a heading summarizes the ideas grouped beneath it, and grouped ideas must be the same kind and in logical order.
- **Secondary sources:**
  - Wikipedia, "MECE principle" (<https://en.wikipedia.org/wiki/MECE_principle>): MECE tests coverage and distinctness, not relevance, and can exclude useful redundancy.
  - Wikipedia, "Pareto principle" (<https://en.wikipedia.org/wiki/Pareto_principle>): 80/20 is a rule of thumb; real splits vary.
- **Schoemaker, "Scenario Planning: A Tool for Strategic Thinking", MIT Sloan Management Review, Winter 1995** (<https://sloanreview.mit.edu/article/scenario-planning-a-tool-for-strategic-thinking/>): scenarios vary several uncertainties together. The warning that vivid, coherent scenarios can seem more probable than they are was read in the PDF by one validator and not reproduced by a second; treat it as plausible guidance, not a finding.
