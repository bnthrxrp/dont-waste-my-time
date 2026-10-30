# Research and evidence

Read this when a deliverable needs facts from outside the user's material, or before delegating research or validation (SKILL.md sections 6 and 7).

## Contents
- When to research
- Scoping
- Source hierarchy and quality signals
- Search and read discipline (with source log)
- Claim labels and citations
- Synthesis
- Verification before delivery
- Delegation (research-agent and validator briefs)
- Market and competitive research
- Evidence notes

## When to research

Size the effort to the decision, not to the topic. Don't research what the user must supply (see Scoping) or what can't change the conclusion.

| Situation | Do |
|---|---|
| The user's material answers the question | No external research. Work from the material and flag its gaps. |
| A few facts lie outside the material, or must be current (prices, regulation, market data, competitor moves) | Targeted research: search for those facts only, open the pages, cite them. |
| A strategic question with several independent angles (market, competitors, regulation, economics) | Structured research: scope, one stream per angle, delegate when it pays (see Delegation), validate. |

- Quick tasks get no research. If a fact looks doubtful, flag it in one line.
- Your own knowledge is not a source. A decision-critical or recency-sensitive fact needs a page you opened; otherwise state it as general background, without numbers.

## Scoping

Before the first search, write this scope for yourself:

```
Question:      Enter Mexico with our own sales team or through a distributor?
Decision:      COO picks an entry model and approves year-1 budget
Evidence bar:  primary or quality sources; data ≤ 2 years old unless flagged; competitor moves dated
Time box:      about 10 searches; open only pages that could change the answer
Enough when:   each supporting point meets the bar and new searches return sources you already have
User supplies: own margins, export volumes, sales capacity, budget ceiling
```

- **Evidence bar by tier.** Standard: one good source per fact; two independent sources for decision-critical numbers where they exist. High-stakes: decision-critical claims triangulated and independently validated. At "enough", stop: remaining gaps become open questions in the deliverable, not more searching.
- **Company-specific facts are never researched or guessed.** The user's own figures, customers, capabilities, plans and constraints come from the user. If one would change the conclusion, ask one targeted question; otherwise use a placeholder such as `[TBD: margin by channel, owner: Finance]` and list it.

## Source hierarchy and quality signals

Prefer the highest-ranked source that states the claim directly.

| Rank | Source | Use it for | Watch for |
|---|---|---|---|
| 1 | Primary data: regulators, statistics offices, central banks, filings, official results, standards | Facts, figures, rules | Definitions and revisions |
| 2 | Peer-reviewed research and systematic reviews | Effects, causes | Sample, setting, transferability |
| 3 | Reputable research firms and industry associations | Market sizes, surveys | Method disclosure, sponsor, advocacy |
| 4 | Quality press with named sources | Events, deals, recent moves | Repeating a press release |
| 5 | Vendor or self-reported claims | What a company says about itself | Label "self-reported" every time |
| 6 | Blogs, aggregators, content farms, AI summaries, search snippets | Leads to a better source | Never cite as evidence |

Before relying on a source, check:
- **Who measured it, and how?** Method, sample and definition stated. A page reporting someone else's data is secondary: open the original or mark it secondary. Two articles quoting the same report are one source, not two.
- **Data date, not article date.** A recent article often quotes old data. For recurring series (annual reports, statistics, surveys), look for a newer edition.
- **Conflict of interest.** A vendor sizing its own category, an association lobbying for members, a sponsored survey: usable, but say so.

**Comparability.** Figures that look alike often measure different things: scope (segments, channels, geography), base year, currency and nominal vs real, FX rate and date, price level (retail, wholesale, manufacturer), value vs volume, revenue vs GMV, actual vs forecast. Never put two figures in one comparison, sum, chart or growth rate unless these match. If they don't, convert and say how, or show them separately with their definitions.

## Search and read discipline

1. **Search to find candidates; open to read.** A result list, snippet or title is not a source. Cite only pages you opened in this session.
2. **Get the exact words.** If the fetch tool returns a summary rather than page text, ask it for the verbatim sentence containing the figure, the publication date and the data period. Quote that; treat the rest as a reading aid.
3. **Log as you go**, one row per fact with its definition (what is counted, where, when, at what price level), in a scratch file, not the deliverable. The log feeds citations, the traceability check and any validator.
4. **Can't open it** (paywall, 403, unreadable PDF): try another legitimate copy (publisher PDF, official release, author's copy). Otherwise log it as not accessed and don't use its content.
5. **Triangulate decision-critical numbers** with a second independent source. If none exists, label the number source-reported and say it is single-sourced.
6. **Search for the case against** your emerging answer at least once. Log what you found, including nothing.
7. **Search in the market's language** as well as English; local regulators, associations and press often publish only locally.

```
| # | Fact (unit, scope, period) | Quote or locator | Publisher | Published / data date | URL | Accessed | Type |
|---|---|---|---|---|---|---|---|
| S3 | Registered distributors, 2025 (count, Mexico) | "…" (table 2) | National statistics office | YYYY-MM-DD / 2025 | https://… | yes | primary |
```

## Claim labels and citations

Use the status labels from SKILL.md section 5 with these meanings:

| Label | Meaning | How it reads |
|---|---|---|
| Verified fact | Stated by a primary or authoritative source you opened, or by two independent sources you opened | Plain statement + [n] |
| Source-reported | Stated by one opened source you couldn't confirm independently, including self-reported claims and secondary coverage | "X reports…" + [n] |
| Calculated | Derived by you from cited inputs | "(calculated: A ÷ B, from [2], [4])" |
| Estimate | A quantified judgment or model output with a stated basis | "(estimate; basis: …)" |
| Assumption | Taken as given, not established | "Assumption: …", listed with the others |
| Hypothesis | A proposed explanation still to be tested | "Hypothesis: …; it would be wrong if …" |
| Recommendation | What you advise | In the recommendation, never mixed into findings |
| Unknown | Not established, possibly needed | `[TBD: …, owner: …]` or the open questions list |

Label where the wording doesn't already make the status unambiguous; don't tag every sentence. A number seen only in a search result has no valid label: open the page or drop the number.

Cite inline with `[n]` after the claim, and close with a numbered list:

```
[3] "Original title." Publisher, YYYY-MM-DD. https://… (accessed YYYY-MM-DD)
[6] "About us." Competitor X, n.d. Self-reported figures. https://… (accessed YYYY-MM-DD)
[9] "Title." Trade publication, YYYY-MM-DD. Secondary: reports <firm>'s survey; original not opened. https://… (accessed YYYY-MM-DD)
```

- Link the page that states the claim (the article, PDF or table), not a home page or search page. Add the data period when it differs from the publication date ("data: 2020"), use "n.d." for undated pages (never guess a date), and mark limits: self-reported, secondary, abstract or summary only.
- The list holds only sources with Accessed = yes. It is not a record of everything you saw.
- In decks and dashboards, put a short source line on the slide or tile and the full list in the appendix.

## Synthesis

- **Order:** findings (what the evidence says) → implications (what it means for this decision) → recommendation (what to do, under what conditions). The deliverable still opens with the recommendation; the reasoning behind it runs in this order.
- **Facts and interpretation in separate sentences.** Mark interpretation ("This suggests…"). Every recommendation traces to named findings; if it rests on an assumption, say which. For proxy evidence from another country, industry or period, say so, and why it transfers or may not.
- **Conflicting evidence:** show both figures with source, date and definition; explain the gap if you can (definition, year, method); say which you rely on and why. If the conflict could change the decision, give the range and test the recommendation at both ends. Never average incompatible figures or silently keep the convenient one.
- **What would change the answer:** state the conditions or thresholds under which the recommendation flips, and what the search for the case against found.
- **Confidence** on the main conclusion and each decision-critical finding, always with a reason:

| Level | Typical basis |
|---|---|
| High | Primary or several independent sources agree; recent; directly on point |
| Medium | One good source, or agreement among secondary, dated or proxy sources |
| Low | Single self-reported or secondary source, conflicting evidence, distant proxy, or mostly assumptions |

## Verification before delivery

Run this on the draft, not your notes, before the quality gate.

1. **List the decision-critical claims**: those that would change the recommendation if wrong, plus every number in the opening summary or headline.
2. **Re-open each URL behind them** with a fresh fetch. Confirm the page states the claim, and that figure, unit, period, geography, definition, qualifiers ("up to", "about", "of respondents") and date match what you wrote.
3. **Check the source list against the log.** Every entry needs Accessed = yes. Open any that lacks it now, or remove it and every claim that depends on it.
4. **Recompute calculations.** Check units, currencies, periods, and percent vs percentage points.
5. **Run `numbers_check.py trace`** (SKILL.md section 8) with the source log and the user's inputs as sources. Each untraced number gets a source, becomes a labeled calculation, or goes.
6. **Fix, don't decorate.** Correct mismatches; downgrade labels that overstate (verified → source-reported); remove what you can't support; turn gaps into open questions.
7. **Report only checks you ran**, with counts: "Re-opened the 6 sources behind the key claims; one figure corrected." Never write "all sources verified" unless you re-opened all of them.

## Delegation

Delegation buys parallelism, independent checking and a cleaner context, at a cost in minutes and tokens. Use it only when it pays.

| Delegate | Do it inline |
|---|---|
| 2 or more independent streams, each needing its own searches (e.g. market, competitors, regulation) | A Standard memo or brief with one line of inquiry |
| Broad scans: many competitors, countries, products or regulations | Streams that depend on each other's results (run them in sequence) |
| Validating many sources, or the key claims of any High-stakes deliverable | Quick tasks, always |

How, in Claude Code:
1. **Scope first**, then split the work into non-overlapping streams with one brief each from template (a). Agents can't ask the user, so the brief must hold everything they need.
2. **Launch all research agents in one message** with the agent tool (Agent or Task) so they run in parallel: a general-purpose agent with web search and fetch, `model: "haiku"` when the tool accepts a model.
3. **Inspect what comes back.** Discard as evidence any finding with Accessed = no or without URL and quote. Look for gaps, overlaps and contradictions; spot-check one or two URLs yourself. Request targeted revisions (follow up with the same agent if the tool allows, or send a narrow new brief); don't rerun whole streams.
4. **Validate** with one agent using template (b), `model: "sonnet"` when available, given the decision-critical claims with URL and quote, not whole dossiers. Apply the verdicts: verified, use; partially supported, narrow the claim; unsupported or contradicted, drop or replace; inaccessible, don't cite.
5. **Keep final judgment.** You write the synthesis, the recommendation and the confidence levels.

Rules:
- If agents or model choice aren't available, run the same steps inline with the same standards and output fields. Don't mention it to the user. Never claim an agent or model was used unless it was; agent counts and model names don't belong in the deliverable.
- Avoid research theater: more citations, searches or agents don't make a better answer. Cite what is decision-critical or likely to be checked; don't pad the source list; keep method notes to one or two lines, in the appendix or the final message.

**(a) Research agent brief**

```
Research one stream of a business question. Return evidence, not prose.
Question: <stream question>        Decision it informs: <decision>
Scope: <geography, segment, period>; out of scope: <…>. Already known (don't re-find): <facts, sources>
Time box: about <N> searches; stop when new searches return sources you already have.
Rules:
- Open every page you report; a search result or snippet is not a source. accessed: yes only if
  you opened the page in this session and it states the finding.
- If your fetch tool summarizes, ask it for the exact sentence and the page date; use them as quote.
- Prefer regulators, statistics offices and filings, then peer-reviewed work, research firms and
  quality press. Label self-reported claims. Open the original behind a secondary report, or mark it secondary.
- Record each number's definition (scope, period, currency, price level). Never invent figures,
  URLs, titles, dates or quotes; "not found" is a valid answer. Search once for the case against.
Output, Markdown only:
- Findings, one block each: id | finding with unit and period | quote | publisher | publication and
  data date | URL | accessed: yes/no | evidence type (primary, peer-reviewed, research firm, quality
  press, self-reported, secondary) | limitations | implication for the decision
- Disagreements (positions, ids, likely reason). Open questions. Failed sources (URL, reason).
```

**(b) Validator brief**

```
Independently validate claims against their sources. Do no new research unless asked.
Claims (id | claim as it will appear | URL | recorded quote):
<list>
For each claim, re-open the URL yourself (don't rely on the recorded quote) and compare figure,
unit, period, geography, definition and qualifiers ("up to", "about", "N respondents").
Verdict: verified | partially supported (which part) | unsupported | contradicted (quote the page)
| inaccessible (why). Flag outdated data (give the data date), secondary coverage posing as primary,
self-reported figures stated as fact, and dates that differ from the one recorded.
Output: a table of id | verdict | what the page says (quote) | flag | suggested fix, then
"Still needs verification": claims you could not settle and what would settle them.
Mark a claim verified only if you opened the page in this session and it states the claim.
```

## Market and competitive research

**Market sizing.** Record every market figure with its full definition before using it:

```
Market:    what is counted (products, channels, customer type)   Geography: …
Base year: year of the data, not of publication                  Measure: value or volume
Currency:  …, nominal or real; FX rate and date if converted     Price level: retail / wholesale / manufacturer
Source:    [n]; method (census, survey, model); publisher type and any interest in the number
Growth:    CAGR x% for years a-b, from [n]; or calculated: (end ÷ start)^(1 ÷ years) − 1
```

- Size the market the decision needs (the segment, region and channel the user can serve), not the largest headline number. Estimates from different publishers often differ: show the range with each definition rather than picking one.
- A CAGR always names whose forecast it is and its period. Never extend it past its horizon or apply a global or national rate to a local segment, unless you label that as an assumption.
- **Triangulate** decision-critical sizes with a second method: top-down (published market × segment share), bottom-up (customers × purchase frequency × average order, each input sourced or labeled) or supply-side (sum of the main players' revenues). If the methods disagree materially, show the range and the reason. Don't average.

**Competitors.** For each: offer, scale indicators, business model and pricing, recent moves, each dated and sourced. Figures from its website, press releases or pitch material are self-reported. Note what you couldn't establish.

**What we don't know about our own company.** Close market and competitive work with this list instead of inventing company figures, each item with why it matters to the decision and who supplies it. Typical items: margins, active customers and order frequency, cost to serve, IT capability, capital available, contract constraints, risk appetite. Where a company figure would appear, use a `[TBD]` placeholder. An industry benchmark may stand in only when labeled as a benchmark with its source, and never in the headline ask.

## Evidence notes

- **Snippets drop qualifiers; one hypothesis invites confirmation.** In this skill's own research, a search snippet gave a McKinsey study's bias-reduction return as "seven percentage points"; Harvard Business Review's account of the same study says "up to seven". That article also warns that people generate one plausible hypothesis and then seek only supporting evidence, and says its review checklist is not meant for routine decisions. Source: Kahneman, Lovallo and Sibony, "Before You Make That Big Decision…", HBR, June 2011 (read from a university-hosted reprint). Basis for open-before-cite, the case-against search and sizing effort to the decision.
- **Unopened sources get cited.** In the project's baseline evaluation (research-strategic-question, run without this skill), the memo listed 9 sources under "Sources (accessed …)", but the run had fetched only 7 pages; the other 2 appeared only in search results. Basis for verification step 3. No published rate of citation errors by language models is cited here.
- **Inline is enough for Standard research.** In the same case, the model without the skill produced a structured, sourced memo inline in under 2.5 minutes with 9 searches and 7 fetches. Basis for keeping single-stream research inline.
