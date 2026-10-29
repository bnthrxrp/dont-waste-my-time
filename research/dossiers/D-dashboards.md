# Research dossier D-dashboards (Layer 1, unvalidated)

**Research question.** How should director-level dashboards, KPI reports, business reviews and board papers be designed so a senior reader can grasp the situation and what needs attention, and what recent (2020-2026) evidence and practice matters? Covers dashboard research (Few, Sarikaya et al., Bach et al.), KPI design, variance commentary, board papers, and AI-reporting verification risk.

## Key findings

### D1. Dashboard Design Patterns

- **Source:** Benjamin Bach, Euan Freeman, Alfie Abdul-Rahman, Cagatay Turkay, Saiful Khan, Yulei Fan, Min Chen; IEEE Transactions on Visualization and Computer Graphics 29(1), 2023, 2023 (journal); arXiv v1 2022-05-02, v2 2022-08-24, <https://arxiv.org/abs/2205.00757>
- **Accessed this session:** yes | **Evidence type:** empirical-study | **Confidence:** high
- **Finding:** A systematic review of 144 dashboards identified eight groups of recurring design patterns. The patterns combine into dashboard genres (narrative, analytical, embedded). A two-week workshop with 23 participants of varied expertise, each working with their own data, tested how the patterns fit design processes. The abstract says concrete design guidance for dashboards is scarce.
- **Interpretation (agent):** The review supports a design checklist. It does not show that using the patterns improves decisions or comprehension.
- **Limitations:** Read from the arXiv abstract page only; the PDF body was not readable. Pattern names come from D2. Journal DOI 10.1109/TVCG.2022.3209448 came from search metadata and was not checked on IEEE. Workshop outcome measures are not in the abstract. Confidence is high for the review counts and genre concept; workshop generalisability is less certain.
- **Implication for the skill:** Choose the dashboard genre (narrative, analytical or embedded) before choosing layout, and build from named patterns rather than ad hoc layouts.

### D2. Dashboard Design Patterns: component and composition pattern catalogue

- **Source:** Bach et al. (companion website to D1), unknown, <https://dashboarddesignpatterns.github.io/patterns.html>
- **Accessed this session:** yes | **Evidence type:** other | **Confidence:** medium
- **Finding:** The authors' companion catalogue lists component patterns. Meta-information patterns: data source, disclaimer (assumptions and processing decisions, limitations), data description, update information (when data was last updated), annotations. Data-information patterns include derived values such as KPIs, and thresholds that label a value good, bad or neutral against objective cutoffs. Screenspace patterns: screenfit (dashboard fully visible without interaction) versus overflow, detail-on-demand, multiple page. Colour patterns include semantic colour, such as green and red for positive and negative results or traffic-light schemes.
- **Limitations:** Catalogue of available patterns; the page says the patterns aim to support creativity and streamline design. It does not claim the patterns improve comprehension. Not peer-reviewed separately from D1.
- **Implication for the skill:** Require source, update date, definitions and disclaimer on every KPI dashboard. Make thresholds explicit rather than implied by colour.

### D3. What Do We Talk About When We Talk About Dashboards?

- **Source:** Alper Sarikaya, Michael Correll, Lyn Bartram, Melanie Tory, Danyel Fisher (author list from a bibliographic record), 2018 (online 2018-08-16; IEEE InfoVis 2018, Berlin); IEEE TVCG 25(1), January 2019, <https://doi.org/10.1109/TVCG.2018.2864903>
- **Accessed this session:** no | **Evidence type:** meta-analysis-or-review | **Confidence:** medium
- **Finding:** Sarikaya et al. combined a literature review with an examination of dashboard examples and their documentation. They built a design space and identified major dashboard types, characterising dashboards by design goals, levels of interaction, and the practices around their use. The authors present the framework as a basis for future research on dashboard design, implementation and use.
- **Limitations:** Full text not read: the Tableau-hosted page and PDF returned 403. Abstract phrases come from search results. The request calls the venue IEEE VIS 2018; the paper was presented at InfoVis 2018 and published in TVCG. One catalogue lists Correll as a Tableau author rather than a main author, which is inconsistent with the other record.
- **Implication for the skill:** Classify each dashboard by design goal (for example monitoring, analysis or communication) and interaction level before design. The goal determines what appears on the first screen.

### D4. Bullet graph

- **Source:** Wikipedia contributors, citing Stephen Few (Perceptual Edge), unknown, <https://en.wikipedia.org/wiki/Bullet_graph>
- **Accessed this session:** yes | **Evidence type:** secondary-summary | **Confidence:** medium
- **Finding:** Few's bullet graph is described as a replacement for dashboard gauges and meters, which the Wikipedia article says typically show too little information, need too much space, and are cluttered with distracting decoration. Components: a featured measure (thick centre line), a comparative measure such as a target (thin line), and shaded qualitative bands. Qualitative ranges use varying intensities of a single hue, which helps colour-blind readers and limits colour on the dashboard. The article links Few's Bullet Graph Design Specification at Perceptual Edge.
- **Limitations:** Secondary. Few's specification PDF was not readable. Search snippets from a Telerik-hosted copy (dated October 2013 in the snippet, unverified) list five parts: label, quantitative scale, featured measure, comparative measures, and two to five qualitative ranges. Few's 2006 book Information Dashboard Design was not read.
- **Implication for the skill:** For KPI status, use a horizontal bar with a target marker and muted single-hue bands in place of dials, gauges or pie charts.

### D5. Bullet Graph Versus Gauges Graph: Evaluation Human Information Processing of Industrial Visualization Based on Eye-Tracking Methods

- **Source:** Lei Wu, Lingli Guo, Hao Fang, Lijun Mou; chapter in Advances in Usability, User Experience and Assistive Technology (Springer), 2019, <https://www.springerprofessional.de/en/bullet-graph-versus-gauges-graph-evaluation-human-information-pr/15890184>
- **Accessed this session:** yes | **Evidence type:** empirical-study | **Confidence:** low
- **Finding:** An eye-tracking experiment with 40 participants compared bullet graphs with gauge graphs for industrial visualisations. Factors were information style, information complexity and task complexity; dependent variables were time to first fixation and subjective feelings. The authors report that the bullet graph provides more efficient reading than gauge graphs, and that all three factors significantly affected time to first fixation (p < .05).
- **Interpretation (agent):** The vendor claim that bullet graphs are easier to interpret in less time (Altair guide, no named study) is consistent with this one study, but it is not independent evidence.
- **Limitations:** Abstract and metadata only. Time to first fixation measures attention and speed, not accuracy or understanding. Accuracy and completion time are not reported in the abstract. Single study in an industrial setting.
- **Implication for the skill:** Prefer bullet-style status bars over gauges where status must be read quickly. Do not claim accuracy gains from this evidence.

### D6. The Balanced Scorecard: Measures That Drive Performance

- **Source:** Robert S. Kaplan and David P. Norton; Harvard Business Review, 1992 (January-February), <https://archive.org/download/bscinharvardbusinessreview/BSC%20in%20Harvard%20Business%20Review.pdf>
- **Accessed this session:** no | **Evidence type:** other | **Confidence:** medium
- **Finding:** Kaplan and Norton proposed the Balanced Scorecard in HBR (January-February 1992, pp. 71-79). It adds customer, internal business process, and learning and growth measures to financial measures, so executives see both results and the drivers of future performance. Secondary descriptions say financial measures report results of actions already taken.
- **Limitations:** The archive copy is a scan with no text layer; the HBR page was not found in search results (a guessed hbr.org URL returned 404). Content is from search-result descriptions only. The statement about financial measures is paraphrased from a secondary description. Confidence is medium for existence and the four perspectives, low for detail.
- **Implication for the skill:** Pair lagging financial outcomes with leading operational measures on board and business-review pages, and label which is which (see D7).

### D7. The Amazon Weekly Business Review (WBR)

- **Source:** Cedric Chin (Commoncog), drawing on Colin Bryar; related book Bryar and Carr, Working Backwards (2021, per search metadata), unknown (a glossary cites 2024), <https://commoncog.com/the-amazon-weekly-business-review/>
- **Accessed this session:** yes | **Evidence type:** practitioner-guidance | **Confidence:** medium
- **Finding:** Commoncog's account of Amazon's Weekly Business Review (based on practice documented with Colin Bryar) describes: controllable input metrics (actions teams can take) versus output metrics (results such as revenue). Outputs are reported but not discussed; teams hit them by managing inputs. Metrics are rotated out when an input stops moving its output. Discussion centres on unusual variation or missed targets; owners explain causes or say they do not know yet, and the facilitator logs a follow-up. Owners must explain how each metric is instrumented. Standard format: a 6-12 graph (trailing six weeks plus trailing year by month, with the prior-year line faded). Targets appear only where they exist, shown as markers. Growth rates appear next to absolute values. The format stays fixed week to week.
- **Limitations:** Secondary account of one company's internal practice. The Bryar and Carr book was not read. The article reports 400 to 500 metrics reviewed weekly, which the skill should not copy as a target. The article's correction note conflicts with its body on deck order (see disagreements).
- **Implication for the skill:** Separate controllable inputs from outcomes. Keep the same format each period. Lead with exceptions. Record unresolved questions as owned follow-ups. Show targets only where they exist. Show rates beside absolute values.

### D8. Effects of workload, work complexity, and repeated alerts on alert fatigue in a clinical decision support system

- **Source:** Ancker, Edwards, Nosal, Hauser, Mauer, Kaushal; BMC Medical Informatics and Decision Making 17:36, 2017-04-10, <https://pmc.ncbi.nlm.nih.gov/articles/PMC5387195/>
- **Accessed this session:** yes | **Evidence type:** empirical-study | **Confidence:** medium
- **Finding:** A retrospective study of EHR data (January 2010 to June 2013) covering 112 primary-care clinicians and 1,266,325 clinical reminders (best-practice advisories) found: each additional reminder per encounter was associated with a 30% lower likelihood of acceptance (IRR 0.70, 95% CI 0.60-0.82); each five-point rise in the share of repeated reminders was associated with a 10% lower likelihood (IRR 0.90, 95% CI 0.86-0.95). The study found no evidence of an effect of workload per se. When a first reminder was overridden, a later repeat was overridden 87.9% of the time, versus 51.9% when the first was accepted. The authors recommend targeting within-patient repeats.
- **Limitations:** Observational study in one commercial EHR and one safety-net network. Alert severity was not available. Repeats were a proxy for uninformative alerts. Transfer to KPI dashboards is an inference, not a tested finding.
- **Implication for the skill:** KPI alerts should fire on a new exception, not on every refresh. Cap the number of simultaneous flags. Do not re-show the same unresolved flag unchanged. Track override or ignore rates.

### D9. Everything Is Under Control? How to Recognize the Watermelon Effect Before Your IT Project Sinks

- **Source:** Pragmatic Coders (sells audit and project-rescue services), 2026-01-27, <https://www.pragmaticcoders.com/blog/everything-is-under-control-how-to-recognize-the-watermelon-effect-before-your-it-project-s>
- **Accessed this session:** yes | **Evidence type:** practitioner-guidance | **Confidence:** low
- **Finding:** A January 2026 practitioner article defines watermelon reporting as status that looks healthy on the surface while problems stay hidden. Causes it lists: optimism bias, fear of blame where red means failure, career self-interest, vanity metrics, and underestimated final work. Mitigations: an explicit Definition of Done, default access to the underlying tools, rewarding early red reports, and independent audit. The article gives no RAG thresholds. Other practitioner sources (search snippets only) advise written definitions for each colour, automatic red triggers such as a missed due date, and a recovery plan with any red.
- **Limitations:** No prevalence or outcome data. Vendor article with a commercial interest. Focus is IT projects. The RAG-definition and automatic-trigger advice comes from non-accessed snippets.
- **Implication for the skill:** Define each RAG colour as a written rule on the card. Make some reds automatic, such as a missed milestone or a KPI below a stated floor. Require a recovery plan with any red.

### D10. Categorizing Variants of Goodhart's Law

- **Source:** David Manheim, Scott Garrabrant (arXiv, cs.AI), 2018-03-13 (v1); latest version v4 2019-02-24, <https://arxiv.org/abs/1803.04585>
- **Accessed this session:** yes | **Evidence type:** other | **Confidence:** high
- **Finding:** Manheim and Garrabrant give a taxonomy of four Goodhart mechanisms. Regressional: selecting the highest values of an imperfect proxy also selects measurement noise. Extremal: optimisation pushes the system into regimes where relationships seen earlier no longer hold. Causal: the intervention itself changes the causal structure, so the proxy stops tracking the goal. Adversarial: another actor acts to undermine the metric. The authors say these forms often occur together, but that defining them separately is useful.
- **Interpretation (agent):** Watermelon reporting looks like an adversarial or causal variant, where incentives change what gets reported. This mapping is my inference, not the authors' claim.
- **Limitations:** Conceptual taxonomy with no empirical measurement. High confidence for the taxonomy content; low for direct application to dashboards. No dashboard-specific evidence.
- **Implication for the skill:** For every target-bound KPI, name the proxy's known gaps and pair it with a guardrail metric that would catch gaming.

### D11. Budget-to-actual variance commentary that is consistent, fast and reviewable

- **Source:** FitGap (vendor guide); cross-checked against FanRuan, Wisemonk and Rework vendor pages, unknown, <https://us.fitgap.com/stack-guides/budget-to-actual-variance-commentary-that-is-consistent-fast-and-reviewable>
- **Accessed this session:** no | **Evidence type:** firm-publication | **Confidence:** low
- **Finding:** Practitioner guidance on variance commentary converges on: decompose a total variance into drivers (for example price versus volume) before writing; rank variances and comment only on those above a threshold, backed by evidence; collect structured inputs from owners (driver, magnitude, one-time versus recurring, action) before drafting; cover event, cause, implication and follow-up with an owner and date. Software can draft text, but an owner with operating knowledge must supply the causal explanation. One secondary summary says SEC MD&A guidance expects discussion beyond restating the statements, and attribution of material revenue changes to price, volume or new products (not verified against SEC text).
- **Limitations:** All vendor material; no independent standard. IBCS 2.0 is the most likely named standard for variance notation (its ISO 24896-aligned Notation part covers variance analyses per search snippet) but its variance rules were not read. SEC text not fetched.
- **Implication for the skill:** Variance commentary template: event, then cause, then so what (impact on margin, cash or target), then now what (action, owner, date). Show variance against target and against prior period. Comment only above a stated threshold.

### D12. In the boardroom, size matters

- **Source:** Board Intelligence with Cambridge Judge Business School (article by Megan Pantelides), unknown (survey year not stated; page last updated 2026-01-05 per page), <https://www.boardintelligence.com/blog/in-the-boardroom-size-matters>
- **Accessed this session:** yes | **Evidence type:** empirical-study | **Confidence:** low
- **Finding:** In a small survey (50 board members, 72% company secretaries; online survey plus nine interviews) run by Board Intelligence with Cambridge Judge Business School: 53% of respondents said their board pack had grown. Directors spend just under four hours on a pack, about 30% more than in 2011. The authors use a benchmark of about 30 pages per hour for careful reading (about 120 pages in four hours). Among packs that grew, 92% had more compliance and regulation reporting. The article sets no target length; it recommends defining the pack's purpose first and says less can mean more.
- **Limitations:** Sample of 50, dominated by company secretaries; vendor-authored; survey year not stated. The 30 pages per hour figure is an advisory benchmark, not a measurement.
- **Implication for the skill:** Budget a pack's reading time against directors' real capacity. Put the decision-relevant content in the first pages.

### D13. Board papers: annotated sample board paper (May 2020)

- **Source:** Australian Institute of Company Directors, 2020-05 (from file name; not verified in text), <https://www.aicd.com.au/content/dam/aicd/pdf/tools-resources/director-resources/board%20papers_may%202020_final_%20appendix_an%20annotated%20sample%20board%20paper.pdf>
- **Accessed this session:** no | **Evidence type:** practitioner-guidance | **Confidence:** medium
- **Finding:** The AICD annotated sample board paper requires every paper to be labelled For Decision, For Discussion or For Noting. Decision papers set out the exact draft resolution, worded so the board can adopt it without amendment. The executive summary is one paragraph of about four to five lines, stating purpose and whether the board is asked to approve or only note. Strategy and financial implications are each capped at about half a page. Complex detail goes into appendices. Recommendations compare alternatives where relevant and state the intended outcomes.
- **Limitations:** The PDF returned unreadable binary; the rules come from a search excerpt. It is a sample paper from one governance body, not a formal standard. IoD, CGI and NACD guidance was not found in one search.
- **Implication for the skill:** Board paper opening: type tag (decide, discuss or note), draft resolution for decisions, four-to-five-line summary, recommendation, appendices for detail.

### D14. Shorter and sharper board packs, please

- **Source:** Board Intelligence (vendor of a report-writing tool), unknown, <https://www.boardintelligence.com/blog/shorter-and-sharper-board-packs-please>
- **Accessed this session:** yes | **Evidence type:** firm-publication | **Confidence:** low
- **Finding:** Board Intelligence reports from its cumulative survey (over 1,000 directors, C-suite and governance professionals from nearly 700 organisations): fewer than half (48%) get value from board papers; 63% rate their packs weak or poor; 54% say key messages are hard to find; 62% say management information is too operational. The average pack is about 226 pages, up 30% since 2019. The page recommends a summary that shows key points up front.
- **Limitations:** Vendor publication with commercial interest. Survey years are mixed (2018 to 2023 data). The 84% headline appearing in a search result title was not found on this page. The 226-page figure conflicts with an unverified aggregator claim (24% of packs over 200 pages in 2025).
- **Implication for the skill:** Put key messages and the decision at the top of every board paper. Each section should be checked for whether it changes a decision.

### D15. Fabrication and errors in the bibliographic citations generated by ChatGPT

- **Source:** William H. Walters and Esther Isabelle Wilder; Scientific Reports 13:14045, 2023-09-07, <https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/>
- **Accessed this session:** yes | **Evidence type:** empirical-study | **Confidence:** high
- **Finding:** GPT-3.5 and GPT-4 each generated 42 short papers (84 total, 636 citations: 222 from GPT-3.5, 414 from GPT-4). Citations were checked against multiple databases. 55% of GPT-3.5 citations and 18% of GPT-4 citations were fabricated. Of real works, 43% of 101 (GPT-3.5) and 24% of 340 (GPT-4) had substantive errors. Numeric fields were the most common errors: volume, issue or page numbers were wrong in 34% of GPT-3.5 and 13% of GPT-4 article or chapter citations; publication years were wrong in 22% and 16%.
- **Limitations:** Models and prompts are from 2023 (papers generated in April 2023). Multidisciplinary topics only. High confidence in the reported counts; low for transfer to current models.
- **Implication for the skill:** Treat every AI citation as unverified until resolved to a DOI or publisher page. Check volume, issue, page and year fields specifically, since they are the most error-prone.

### D16. GPT-4o literature review citation accuracy (JMIR Mental Health, 2025)

- **Source:** JMIR Mental Health (authors not confirmed from snippet), 2025 (study conducted June 2025 per snippet), <https://mental.jmir.org/2025/1/e80371/PDF>
- **Accessed this session:** no | **Evidence type:** empirical-study | **Confidence:** low
- **Finding:** In a 2025 study of GPT-4o writing six mental-health literature reviews, 176 citations were generated; 35 (19.9%) were fabricated. Of the 141 real citations, 64 (45.4%) had errors, most often incorrect or invalid DOIs. Reported fabrication rates varied by topic (for example 4 of 68 for major depressive disorder versus 14 of 48 for body dysmorphic disorder, per the snippet).
- **Interpretation (agent):** Compared with D15, the 2025 fabrication share (19.9%) for one model is not clearly lower than GPT-4 in 2023 (18%), though the domains differ. No clear improvement is shown.
- **Limitations:** Figures from a search snippet; the fetch returned empty. Six reviews in one clinical domain. Small sample.
- **Implication for the skill:** Newer models still fabricate citations at double-digit rates in this test. Do not treat a newer model as safe for references.

### D17. From Single to Multi: How LLMs Hallucinate in Multi-Document Summarization

- **Source:** Catarina G Belem, Pouya Pezeshkpour, Hayate Iso, Seiji Maekawa, Nikita Bhutani, Estevam Hruschka; Findings of ACL NAACL 2025, pp. 5291-5324, 2025 (April 2025 per fetched page), <https://aclanthology.org/2025.findings-naacl.293/>
- **Accessed this session:** yes | **Evidence type:** empirical-study | **Confidence:** medium
- **Finding:** Across five LLMs on two multi-document summarisation benchmarks, the abstract reports that up to 75% of the content in LLM-generated summaries is hallucinated. Hallucinations are more likely toward the end of summaries. When asked to summarise topics absent from the source documents, GPT-3.5-turbo produced summaries about 79.45% of the time and GPT-4o about 44% of the time.
- **Limitations:** About multi-document summarisation, not numbers specifically. Models are dated relative to 2026. The arXiv abstract gives 79.35% where the ACL version gives 79.45%. The 75% is a per-benchmark upper figure, not an average across tasks.
- **Implication for the skill:** In AI-drafted summaries, check the closing sections first. Trace every summary sentence to a source passage.

### D18. Deloitte to partially refund Australian government for report with apparent AI-generated errors

- **Source:** Associated Press (syndicated); CFO Dive and City AM also cited, 2025-10-07, <https://www.news4jax.com/business/2025/10/07/deloitte-to-partially-refund-australian-government-for-report-with-apparent-ai-generated-errors/>
- **Accessed this session:** no | **Evidence type:** secondary-summary | **Confidence:** medium
- **Finding:** Deloitte Australia agreed to partly refund the Australian Department of Employment and Workplace Relations for a report (first posted July 2025) that included an invented quote attributed to a federal judge and citations to academic papers that do not exist. The revised version disclosed use of Azure OpenAI and removed the fabricated material; the department said core findings and recommendations were unchanged. Refund figures conflict: AP reported the final installment would be repaid, while CFO Dive cited a spokesperson saying over A$97,000 had been refunded on a contract of about A$440,000.
- **Limitations:** News coverage from search results; no primary government or Deloitte document read. Amounts disputed across outlets. Confidence is medium for the event and low for the amounts.
- **Implication for the skill:** Client-facing reports need a named human citation check and disclosure of AI use before release.

## Disagreements

- **Executive summary length:** AICD sample paper: one paragraph of about four to five lines (D13). Board Intelligence: a summary that shows key points up front, with no length given (D14). A university board template in search results caps decision requests at two pages with three to five summary points (secondary, not accessed). Working default: follow the AICD length and note the others. (D13, D14)
- **Amazon WBR deck order:** The Commoncog article body says decks run inputs first, then matching outputs, ending with financials. Its correction note says Amazon actually opens with financials and then reviews operations. Do not state a deck order as fact without the primary source. (D7)
- **Fabrication rates across model generations:** GPT-4 fabricated 18% of citations in the 2023 Walters and Wilder study (D15). GPT-4o fabricated 19.9% in a 2025 mental-health test (D16, snippet only). The domains differ, so the two cannot be compared directly, but neither shows a clear improvement. (D15, D16)
- **Board pack length:** Board Intelligence reports an average pack of about 226 pages (D14). An aggregator claims 24% of packs exceeded 200 pages in 2025 (unverified and not reconciled with the 226-page average). A separate Board Intelligence study reports 53% of packs grew (D12). These measure different things and cannot be reconciled from the sources read. (D12, D14)
- **Headline statistic in board-pack research:** A search result title cited 84% of directors wanting more focused packs. The fetched Board Intelligence page has no 84% figure; it reports 48% getting value from papers and 63% rating packs weak or poor (D14). Do not use the 84% figure. (D14)
- **Bullet graphs versus gauges: strength of evidence:** Altair's visualisation guide says research shows bullet graphs are easier to interpret in less time than radial gauges, without naming a study. The only named experiment (D5) measures time to first fixation with 40 participants and reports more efficient reading for bullet graphs. Direction is consistent, but the evidence base is one abstract-level study. (D4, D5)
- **Sarikaya et al. bibliographic record:** One catalogue lists Alper Sarikaya, Lyn Bartram, Melanie Tory and Danyel Fisher as authors, with Michael Correll credited as a Tableau author. Another lists five authors including Correll. The five-author list is used here. Verify on IEEE Xplore before citing. (D3)
- **Deloitte refund amount:** AP reports the final contract installment would be repaid, with the figure to be published. CFO Dive cites a spokesperson saying over A$97,000 was refunded from a contract of about A$440,000. Figures conflict and neither is primary-verified. (D18)

## Implementation recommendations

- [core] Before layout, write one sentence naming the audience, the decision or question, and the dashboard genre (monitoring, analysis or communication). (D1, D3). Design goals and genres are the main classification dimensions in the dashboard literature; the choice determines what must appear on the first screen.
- [core] Put exceptions (off target, changed, decision needed) in the top band. Compress routine items and move detail to drill-down or appendix. (D7, D2). Amazon's review is exception-driven, and thresholds are a named dashboard pattern for labelling values good, bad or neutral.
- [core] The first view should fit one screen without interaction (screenfit). Anything beyond it is detail-on-demand or a separate page. (D2). Screenfit is a named composition pattern. Few's single-screen principle is cited secondarily but was not read, and the concept is debated for mobile screens.
- [core] Every dashboard page shows data source, owner, KPI definitions, last-updated date, and a short disclaimer on assumptions and known limits. (D2). Meta-information patterns (source, disclaimer, description, update information) are the catalogue's explicit components.
- [core] Keep layout and format fixed across periods; change content, not structure. (D7). Amazon's WBR format is held constant so readers build intuition; the article says the same colours and graph format are used each week.
- [core] Use one muted hue for performance bands. Reserve red and green for status, and always pair colour with a word or symbol. (D2, D4). Single-hue bands support colour-blind readers; semantic colour is a named pattern; colour-only encoding fails accessibility.
- [core] For status reading, use horizontal bullet bars with a target marker instead of gauges, dials or pie charts. (D4, D5). Bullet graphs were designed to replace gauges (Few, via Wikipedia). One 40-participant eye-tracking study found more efficient reading (time to first fixation), with no accuracy result in the abstract.
- [core] Alerts fire on a new exception, not on every refresh. Cap simultaneous flags; do not re-show an unresolved flag unchanged; log overrides and ignores. (D8). In healthcare alerting, each extra reminder per encounter reduced acceptance by 30%, and repeats were overridden far more often. Transfer to KPIs is an inference.
- [core] KPI card fields: name; one-line definition; owner; source and as-of date; unit; polarity (higher is better, lower is better, or range); actual with period label. (D7, D10). Amazon's WBR requires owners to explain instrumentation and definitions; polarity is an inference from the metric-gaming literature and has no direct source.
- [core] Target field shows the target value and its source (plan, budget, regulatory, none). Where there is no target, print 'No target' explicitly rather than leaving it blank. (D7). Amazon's WBR shows targets only where they exist; not every metric has one.
- [core] Comparison: show the last six periods alongside the same periods last year (prior year faded). Show growth rates next to absolute values. (D7). Amazon's 6-12 graph; the article notes growth rates often matter more than absolute values.
- [core] Variance: show actual minus target and actual minus prior period, both absolute and percent. Label favourable or unfavourable from polarity, not from the sign of the number. (D11, D7). Variance practice requires explicit drivers and comparison bases; polarity logic follows from the metric-polarity issue. No primary source found for the polarity rule.
- [core] Status is a written rule on the card, for example: green when at or better than target; amber within a stated tolerance; red beyond tolerance or when a stated trigger fires (such as a missed milestone). Any red requires a recovery plan. The tolerance values must be set by the owning team. (D9). Watermelon reporting is driven by subjective RAG ratings and fear of red; written criteria and automatic triggers are the practitioner mitigation. No source gives numeric thresholds.
- [core] Commentary per flagged KPI: one-line cause, owner, next action and date. 'Not yet known' is acceptable only with a logged follow-up owner and date. (D7, D11). Amazon logs unresolved questions as follow-ups and asks owners to say when they do not know.
- [optional] Each target-bound KPI carries a paired guardrail metric that would reveal gaming or a shifted proxy. (D10). Goodhart mechanisms (regressional, causal, adversarial) show how targets corrupt proxies; the pairing is a mitigation inferred from that taxonomy.
- [core] Label each card as input (controllable action) or output (outcome). Outcome cards link to their driver cards and are not debated without them. (D7, D6). Amazon's WBR distinguishes controllable inputs from outputs, and outputs are reported but not discussed on their own.
- [core] Tag every board paper For Decision, For Discussion or For Noting. (D13). AICD sample requires the tag; it signals what the board must do.
- [core] Decision papers state the exact draft resolution near the top, worded for adoption without amendment. (D13). AICD sample requires the draft resolution up front on decision items.
- [core] Executive summary: one paragraph of about four to five lines covering purpose, the ask (approve or note), recommendation and next step. (D13, D14). AICD caps the summary at four to five lines; Board Intelligence says key points go first. The length is from one governance body, not a standard.
- [core] Cap strategy and financial implications at about half a page each; move complex detail to appendices. (D13). AICD sample guidance on issue sections and appendices.
- [core] Define the pack's purpose and the decisions it must support before adding content. Remove sections that change no decision. (D12, D14). Board Intelligence/Cambridge recommend purpose first; packs that did not grow reported more strategic content (small, self-selected sample).
- [optional] Budget reading time against directors' capacity (about 30 pages per hour as an advisory benchmark) and flag the pages that must be read for the decision. (D12). Reading-time benchmark from a small survey; use as a prompt to cut, not a validated limit.
- [core] Every figure in an AI-drafted document traces to a named source cell or document and date. Recalculate totals, variances and percentages in a spreadsheet or code, not in prose. (D15, D17). Numeric fields were the most error-prone elements of AI citations (D15). Numbers in prose are an inference from that and from summary hallucination (D17); no study measures numeric error rates in business reports.
- [core] Resolve every citation to a DOI or publisher page before use. Check volume, issue, page and year specifically. Drop any citation that cannot be resolved. (D15, D16). Fabrication rates were 18% to 55% for 2023 models and 19.9% for GPT-4o in 2025 (one small study); DOIs were the most common error in the 2025 study.
- [core] Check the closing sections of any AI-drafted summary first, and trace each summary sentence to a source passage. (D17). Hallucinations were more likely toward the end of summaries in a multi-document benchmark.
- [core] Name a human reviewer who signs off figures and citations, and disclose AI use in the document before release. (D18). The Deloitte case shows an invented quote and nonexistent references reached a government client; the revised version disclosed AI use.
- [core] Unverifiable figures and claims are marked unverified or removed, not restated from memory. (D15, D16, D18). Fabricated citations and invented quotes appear in AI output at documented rates; no safe default exists without checking.

## Open questions

- Kaplan and Norton (1992): full text not readable. The Balanced Scorecard claims in D6 come from secondary descriptions and need the article text to verify.
- Sarikaya et al.: full text not read (publisher page and PDF returned 403). The design-space dimensions and dashboard types are from abstract phrases in search results.
- Few's Bullet Graph Design Specification and 'Why Most Dashboards Fail' PDFs returned unreadable compressed binary. The component list, the monitoring sequence (overview, flagged areas, detail) and the single-screen definition need text versions from Perceptual Edge.
- AICD sample paper: PDF unreadable; rules are from a search excerpt. IoD, CGI and NACD board-paper guidance was not found in one search and needs targeted searches.
- No empirical study from 2020-2026 on executive dashboard comprehension, glanceability or time-to-insight was found. The nearest is IEEE VIS 2025 eye-tracking work on dashboard viewing behaviour (60 participants, 36 dashboards, per snippet): https://aa.ieeevis.org/year/2025/program/paper_3ba85378-08f5-4533-b7d1-a8734f3bf319.html. It measures viewing, not comprehension.
- Yigitbasioglu and Velcu (2012, International Journal of Accounting Information Systems 13(1), 41-59): abstract only. It states that dashboard effectiveness is poorly documented, especially which dashboard types suit which users or tasks: https://ideas.repec.org/a/eee/ijoais/v13y2012i1p41-59.html. Full text needed.
- IBCS 2.0 (aligned with ISO 24896; the page states approval on June 11, 2026): the variance-notation rules are in the full standard, which is a members' PDF. The variance display guidance in this dossier is therefore unverified.
- No measured error rate for LLM-generated numbers in business reports was found. FAITH (arXiv 2508.05201, ICAIF 2025) benchmarks tabular financial hallucinations on S&P 500 annual reports; its abstract gives no rates. Full text needed.
- Nature 2026 analysis (about 2.6% of 2025 computer-science conference papers with potentially hallucinated citations, up from 0.3% in 2024) was found only in reposted copies and is excluded.
- Kumar, Prince and Baker (2021, FIIB Business Review) reviewed 114 balanced-scorecard articles; the review's findings are in a search snippet only and are not used. Evidence on balanced scorecard effectiveness is mixed and conceptual-heavy.
- ICAEW guidance on identifying AI errors in financial models (June 2026): the fetched page returned site navigation only, so its checks are unverified.
- Watermelon reporting prevalence in governance or executive reporting has no quantitative source; the RAG-threshold advice is practitioner opinion.

## Sources attempted but not accessed

- <https://www.tableau.com/research/publications/what-do-we-talk-about-when-we-talk-about-dashboards>: Fetch returned 403. Bibliographic details and abstract phrases come from search results only.
- <https://tableau.com/sites/default/files/2023-01/DashboardsConspiracy_final.pdf>: Fetch returned 403. Not confirmed to be the Sarikaya et al. paper.
- <https://www.perceptualedge.com/articles/misc/Bullet_Graph_Design_Spec.pdf>: Fetched; returned compressed binary PDF with no readable text.
- <https://www.telerik.com/docs/default-source/blogs-docs/bullet_graph_design_spec-pdf>: Fetched; returned compressed binary PDF with no readable text. Component details are from a search snippet.
- <https://blogs.ischool.berkeley.edu/i247s13/files/2013/02/WhyMostDashboardsFail.pdf>: Fetched; returned compressed binary PDF with no readable text. Monitoring and failure-mode content is from a secondary review snippet.
- <https://archive.org/download/bscinharvardbusinessreview/BSC%20in%20Harvard%20Business%20Review.pdf>: Fetched; scanned pages with no text layer. The 1992 article's content is unverified.
- <https://hbr.org/>: No HBR URL for the 1992 article surfaced in search results. A guessed hbr.org article URL returned 404.
- <https://www.aicd.com.au/content/dam/aicd/pdf/tools-resources/director-resources/board%20papers_may%202020_final_%20appendix_an%20annotated%20sample%20board%20paper.pdf>: Fetched; returned unreadable binary PDF. Rules are from a search excerpt only (D13 accessed=false).
- <https://www.cgi.org.uk/about-us/press-office/news-releases/board-packs-are-too-long-and-backward-looking-to-be-properly-effective>: Fetch returned 404. CGI survey figures (74% and 85% saying packs are too long) come from a search snippet and are not used as findings.
- <https://www.azeusconvene.com/en-au/articles/board-papers>: Fetch returned 403.
- <https://www.icaew.com/insights/viewpoints-on-the-news/2026/jun-2026/how-to-identify-ai-errors-in-financial-models>: Fetched; the first 100,000 characters were site navigation with no guidance text.
- <https://mental.jmir.org/2025/1/e80371/PDF>: Fetch returned empty content (HTML and PDF variants). D16 figures come from a search snippet (accessed=false).
- <https://www.nature.com/>: Nature's April 2026 news feature on hallucinated citations was found only in reposted copies; not fetched from nature.com.
- <https://ibcs.com/standards/>: Fetched overview only: version 2.0, ISO 24896 alignment, approval date stated. Variance rules are in the full standard, which is a members' PDF.
- <https://ideas.repec.org/a/eee/ijoais/v13y2012i1p41-59.html>: Bibliographic and abstract record only; full text not read.
- <https://www.slideshare.net/slideshow/whatdowetalkaboutwhenwetalkaboutdashboards-1pdf/257903850>: Fetch returned a site error page.
- <https://aa.ieeevis.org/year/2025/program/paper_3ba85378-08f5-4533-b7d1-a8734f3bf319.html>: Search snippet only; not fetched.
