# Synthesis: evidence base and operating rules for the "dont-waste-my-time" skill

Layer-2 synthesis of five dossier + validation pairs (A-strategy, B-dataviz, C-storytelling, D-dashboards, E-translation). Written 2026-10-30. Purpose: give the skill author a validated, deduplicated rule set for executive-grade materials (board decks, director dashboards, management reviews, strategic memos, research-driven recommendations, PT<->EN translation/adaptation, improvement of existing materials), governed by two aims: do not waste the decision-maker's time, do not waste the user's time.

## 0. Conventions used in this document

**Finding ids.** Every reference is an id from the inputs: dossier findings A1-A16, B1-B17, C1-C17, D1-D18, E1-E18; validator gap fills AV1-AV4, BV1-BV4, CV1-CV4, DV1-DV4, EV1-EV4; and one validator check id, `IMPL-palette-contrast` (stream B). Rule ids (CORE-n, WRIT-n, STORY-n, VIZ-n, DASH-n, RES-n, XLAT-n, QA-n), principle ids (P1-P15), contradiction ids (RC-n resolved, PC-n preserved) and asset ids (S1-S13) are local to this document.

**Strength labels** (copied from the validators, never raised; where rules were merged the lowest strength of the merged parts is shown unless stated):

| Label | Meaning here |
|---|---|
| strong | Normative standard, or validator-rated strong on verified primary sources |
| moderate | Convergent but observational, crowd-sourced, small, or extrapolated from a neighbouring setting |
| weak | Single small or developer-run study, secondary source, or inference from a different domain |
| practitioner-consensus | Convention or guidance with no outcome evidence; kept because it is cheap and checkable |

**Placement tags** on rules: `[core]` = short form in SKILL.md; `[ref:<name>]` = reference file loaded on demand; `[opt:<name>]` = optional module loaded only when requested or in use. File names are proposed in section 5.

**Integrity rules applied.** (1) No strength upgrades. (2) Claims the validators marked contradicted, unsupported, outdated or source-inaccessible appear only in sections 6 (Exclusions) and 7 (Needs verification), apart from brief mentions in section 4 that name a rejected reading in order to explain a resolution. (3) Where a validator corrected a dossier (for example B1, B4, C17, E12, E14), the corrected form is used. (4) Where a rule is Claude's own policy rather than a finding (for example "wrong number = Critical"), it says so. (5) Dates are reported as the inputs give them; several sources are dated 2026 and the current date is 2026-10-30.

---

## 1. Evidence base at a glance

Only sources the validator verified or partially supported, or that the researcher accessed and the validator did not contradict, are listed. Sources the validator could not access and the researcher did not read (A14, the vendor part of D11, C-disagreement-wpm, the ISO page for E1 status) are not listed here; see section 7. "Gap fill" means the validator supplied the source.

### 1.1 Stream A: strategy and decision quality

| Ids | Source | Date | Evidence type | Validator verdict | Status |
|---|---|---|---|---|---|
| A1-A4 | Kahneman, Lovallo, Sibony, "Before You Make That Big Decision" (HBR) | 2011-06 | practitioner guidance | verified | Usable. Checklist is meant for reviewers independent of the proposers; no outcome data; not for routine rubber-stamp decisions |
| A5, AV1 | Lovallo & Sibony, "The case for behavioral strategy" (McKinsey Quarterly), cited in HBR | 2010-03 | survey of 1,048 decisions, self-reported, correlational | A5 verified; AV1 gap fill | Motivation only. HBR wording is "up to seven percentage points"; not a causal effect size |
| A6 | Klein, "Performing a Project Premortem" (HBR) | 2007-09 | practitioner guidance, three anecdotes | method verified; the 30% figure partially supported | Method usable (weak). The 30% figure is Klein's second-hand report; do not quote |
| A7 | Eisenhardt, AMJ 32(3) | 1989 | inductive study, 8 firms, one industry | verified (abstract-level) | Usable with weak generalisation |
| A8 | Nutt, AME 13(4) | 1999 | observational, 356 decisions | verified (full text, Table 4) | Usable. "Failure" means not sustained or fully used after two years |
| A9 | Dean & Sharfman, AMJ 39(2) | 1996 | field study, 52 decisions | partially supported (abstract-level) | Low. Not a basis for any rule |
| A10 | Spetzler, CBS interview | 2009-05 | expert opinion | verified | Usable as a self-check; interview-level |
| A11, AV2 | Bain, Cochemé & Mottura; Rogers & Blenko via Bain | 2026-10-07; 2006-01 | firm publications | A11 verified; AV2 gap fill (summarising fetch) | The two Bain pieces disagree on whether "Agree" can veto; see RC-8 |
| A12 | MECE (Wikipedia) | undated | secondary | verified | Critiques are conceptual; underlying sources unchecked |
| A13 | Stratrix, pyramid principle | undated | vendor practitioner page | verified | No effect evidence; pricing example is hypothetical |
| A15 | Schoemaker, MIT SMR | 1995-01 | expert opinion plus one experiment (n=68) | verified (PDF) | Weak. Range widening not shown to improve calibration |
| A16 | Pareto principle (Wikipedia) | undated | secondary | verified | Low weight |
| AV3 | Flyvbjerg, Project Management Journal 37(3) | 2006 | large-sample forecast data, public infrastructure | gap fill | Transfer to corporate forecasts is by analogy |
| AV4 | Farkas on Alley et al. (informal critique) | 2010 | critique | gap fill | Sentence headlines: modest, confounded gains; scope to read-ahead decks |

### 1.2 Stream B: data visualization

| Ids | Source | Date | Evidence type | Validator verdict | Status |
|---|---|---|---|---|---|
| B1 | Heer & Bostock, CHI | 2010-04 | crowd replication of Cleveland & McGill | partially supported | Safe claim only: position on a common scale is best; area is worse than position and angle; angle was not shown worse than length |
| B2 | Correll, Bertini, Franconeri, CHI | 2020-01 | crowd experiments (Prolific, small n) | verified | Truncated bars exaggerate effects; authors resist a blanket "always zero" |
| B3 | Datawrapper academy | 2021-03-23 | vendor guidance | verified | Bars and columns at zero; lines, dots, ranges may be non-zero |
| B4, BV4 | Datawrapper dual-axis blog; Datawrapper reversal post | 2018-05-08 (edit 2026-07); 2026-07-23 | vendor guidance | B4 outdated (description accurate, evidence base weaker than implied); BV4 gap fill | Conservative default only; see RC-6 |
| B5 | Skau & Kosara, EuroVis | 2016 | crowd experiment, two-segment stimuli | verified | Angle-only pies least accurate; donut equals pie; variant warnings are reasoned, not tested |
| B6 | Bateman et al., CHI | 2010-04 | experiment, n=20 | verified | Tiny sample, one designer's style; no stance either way |
| B7 | Borkin et al., TVCG | 2013 | memorability study, 2,070 charts | verified (page-level) | Memorability is not comprehension |
| B8 | Kong, Liu, Karahalios, CHI | 2018-04 | experiments, about 100 per experiment, controversial topics | verified | Title slant shifts perceived message |
| B9 | Kim, Setlur, Agrawala, CHI | 2021-01 | crowd experiments, line charts only | verified | Caption adopted only if the feature is also visually prominent |
| B10 | Ajani et al., TVCG | 2021 | within-subject, 24 undergraduates, 10-second views | verified | Declutter raises professionalism ratings; focus raises memory and clarity |
| B11 | Franconeri et al., PSPI 22(3) | 2021-12 | review | verified (abstract-level) | Full text unread |
| B12 | Correll & Gleicher, TVCG 20(12) | 2014-08 | survey of 46 papers plus crowd experiments | verified | Unlabeled error bars common; containment bias |
| B13, BV3, DV1 | W3C WCAG 1.4.11, 1.4.3, 1.4.1 | updated 2025-2026 | standard | verified / gap fill | Applying web criteria to slides and print is an extension: say "WCAG-aligned" |
| B14 | Wilke ch. 19; Okabe & Ito | undated | book | partially supported | Palette and hex values verified; prevalence must be a range |
| B15 | Lapajne (AFP Exchange); IBCS / ISO 24896 | 2015-11; ISO 2026-06-11 | firm publication, standard | partially supported | Standard text paywalled; scenario encodings unverified |
| B16 | Javed et al.; Ondov et al. | 2010-10; 2018 | experiments (n=16 for Javed) | verified | Task- and span-dependent; no series-count threshold |
| B17 | Munzner lecture slides | undated | expert opinion | partially supported | Principles confirmed; channel-ranking figure is an image |
| IMPL-palette-contrast | Validator recomputation of Okabe-Ito contrast on white | 2026-10 | computation (WCAG formula) | verified | Re-run in this synthesis: values match (section 8, S11) |
| BV1 | Witt, Meta-Psychology 3 | 2019 | five small experiments (n 9-20) | gap fill | Too-wide and too-narrow ranges both bias; no business formula |
| BV2 | Kale, Kay, Hullman, TVCG | 2020 | crowd experiments | gap fill | A visible point estimate leads readers to discount the range |

### 1.3 Stream C: storytelling, writing, presentation

| Ids | Source | Date | Evidence type | Validator verdict | Status |
|---|---|---|---|---|---|
| C1 | Rogers & Lasky-Fink book excerpt (49 vs 127 words) | undated | field experiment, reported without statistics | verified | Directional prior only; one context |
| C2 | Harvard Gazette interview with Rogers | 2023-10 | interview | partially supported | Weak. Emphasis claim rests on unreported experiments |
| C3, CV1 | Excerpt (83% added words); Adams et al., Nature 592:258-261 | excerpt undated; 2021-04-08 | experiments | C3 verified; CV1 gap fill | CV1 is the primary source; an explicit cue to subtract raises subtraction |
| C4, C5 | Amazon 2017 shareholder letter; Callahan essay | 2018-04; 2018-05 | firm self-description; consultant essay | verified | Practice documented; no outcome data; 2004 email wording unverified |
| C6, CV3 | Tufte on CAIB; CAIB Report Vol. 1 ch. 7-8 | 2003-08 | expert opinion; primary report | verified | Single, multi-causal case; Board relies on Tufte's slide analysis |
| C7 | Garner, Alley et al., IJEE 29(6) | 2013 (conference 2011) | developer-run experiment, 110 students, deliberately weak control slides | partially supported | Weak |
| C8 | Alley et al., Tech Comm 53(2) | 2006-05 | classroom trial; article text unread | partially supported | Weak; confounds unresolved |
| C9 | Adesope & Nesbit; Yue, Bjork, Bjork | 2012; 2013 | meta-analysis; experiments | verified (abstract-level) | Lab learning, college students |
| C10, C11 | Noetel et al.; Sundararajan & Adesope | 2022 (online 2021); 2020-09 | meta-meta-analysis; meta-analysis | partially supported | Learning outcomes only; ranking and moderator claims not used |
| C12 | Koetsenruijter et al., JMIR Med Inform | 2022 | pilot, n=35 | verified | Not used as a rule (stretched beyond what it tested) |
| C13 | Gao & Corter, CogSci | 2020 (inferred) | abstract-level experiment | verified | Sentence-level, weak |
| C14 | digital.gov plain-language guidance | undated | official guidance | verified | Guidance, not effect evidence |
| C15 | ISO 24495-1:2023 | 2023-06 | standard | partially supported | Four-principle rubric only; standard text unread |
| C16, CV4 | AR 25-50 (BLUF); Britt & Larson | 2020-10 edition; 2003-05 | doctrine; sentence-level experiments | C16 partially supported; CV4 gap fill (abstract-level) | Default structure, not a measured document-level benefit |
| C17 | Minto, Pyramid Principle (secondary) | 1985 (1987 per other source) | expert opinion | partially supported | Structure only; the "2-3 supporting arguments" limit is unsupported |
| CV2 | Morkes & Nielsen, NN/g | 1997 | experiment, n=51, web task | gap fill | Concise and scannable beat promotional; dated, web-only |

### 1.4 Stream D: dashboards, KPIs, board materials, AI verification

| Ids | Source | Date | Evidence type | Validator verdict | Status |
|---|---|---|---|---|---|
| D1, D2 | Bach et al., Dashboard Design Patterns (TVCG 29(1)) and catalogue | 2023 (arXiv 2022) | review of 144 dashboards plus 23-person workshop | verified | Patterns not shown to improve comprehension |
| D3 | Sarikaya et al., TVCG 25(1) | 2019 (online 2018-08-16) | review | verified (abstract-level) | Five-author list resolved |
| D4 | Bullet graph (Wikipedia, citing Few) | undated | secondary | partially supported | The pie-chart extension in the dossier is not supported |
| D5 | Wu et al., eye-tracking | 2019 | experiment, n=40 | verified | Time to first fixation only; no accuracy result |
| D6 | Kaplan & Norton, Balanced Scorecard (HBR) | 1992-01 | concept | partially supported | Concept only; paywalled |
| D7 | Commoncog on Amazon WBR | 2024-07-02 (updated 2026-06-14; correction 2025-01-24) | practitioner account | verified | One company; deck order contradicts itself |
| D8 | Ancker et al., BMC MIDM 17:36 | 2017-04-10 | observational, 112 clinicians, 1.27M alerts | verified; transfer to KPIs partially supported | Heuristic only for dashboards |
| D9 | Pragmatic Coders, watermelon reporting | 2026-01-27 | vendor article | verified | Weak. Written-RAG-definition advice was not in the article |
| D10 | Manheim & Garrabrant | 2018-03 (v4 2019-02) | conceptual taxonomy | verified | No dashboard evidence |
| D11 (SEC part), DV2 | 17 CFR 229.303 (Item 303) | current CFR | regulation | verified | Anchor for driver-based variance explanation; applies to SEC filers |
| D12 | Board Intelligence / Cambridge, "size matters" | undated (page updated 2026-01-05) | vendor survey, n=50 | verified | Low |
| D13 | AICD annotated sample board paper | 2020-05 | practitioner guidance | verified | One governance body; richer than the dossier reported |
| D14 | Board Intelligence, "shorter and sharper" | undated (data 2020-2023) | vendor survey | verified | Low; mean pack length is skewed |
| D15, D16 | Walters & Wilder, Sci Rep 13:14045; Linardon et al., JMIR Ment Health (via release) | 2023-09-07; 2025-11 | empirical citation audits | verified | Rates depend on model vintage and topic familiarity |
| D17 | Belem et al., NAACL Findings | 2025 | benchmark study | partially supported | Position effect usable; "75%" is not |
| D18 | AP report on Deloitte Australia | 2025-10-07 | news | partially supported | Event usable as a caution; refund amounts unresolved |
| DV3 | Few, "Dashboard Confusion" | 2004-03-17 | expert definition | gap fill | Single-screen definition applies to monitoring dashboards |
| DV4 | FinanceBench (arXiv 2311.11944) | 2023-11-20 | benchmark, abstract page | gap fill | 2023 models, question answering, not report drafting |

### 1.5 Stream E: translation and localization

| Ids | Source | Date | Evidence type | Validator verdict | Status |
|---|---|---|---|---|---|
| E1 | ISO 17100:2015 | 2015-05 | standard | partially supported (headings and definitions via preview) | Structural model only; the standard excludes raw MT plus post-editing |
| E2, E3 | MQM typology and scoring models | current site | community standard | verified (mapping of error types to severities is Claude policy) | Multipliers 0/1/5/25 are non-normative |
| E4-E6 | WMT24 Findings | 2024-11 | shared-task evaluation | verified | No English-Portuguese pair |
| E7 | Tang et al., ICASSP | 2025-01-09 | benchmark, Chinese-English, small open-source LLMs | verified (abstract) | Risk evidence, not a Portuguese or frontier-model result |
| E8 | Kocmi & Federmann, GEMBA-MQM | 2023-10-21 | method paper | verified | System ranking, not document sign-off |
| E9 | Skorobogat, Prabhu, Bethge | 2026-04-14 | benchmark correlation | verified | Low; full paper is more cautious than its abstract |
| E10 | W3C text size in translation (IBM table) | undated | practitioner guidance | verified | Direction only |
| E11 | Portuguese expansion figures (13%-30%) | undated | secondary | partially supported | Spread corroborated; no primary measurement |
| E12, E13, EV1 | CLDR pt, en, pt-PT | current (CLDR 47 runtime-checked) | standard | verified (E12 "bi" interpretation partially supported and superseded by EV1) | Reference for formats and scale words |
| E14-E16, EV3 | CPC 47, CPC 26 (R1), CPC 00 (R2) | consolidated Rev. 14; CPC 00 dated 2019-12-13 | accounting standards (Portuguese text) | E14, E15 verified; E16 partially supported; EV3 gap fill | English equivalents are inferred from IFRS/IAS; the dossier's glossary implication for "faturamento" was corrected by EV2 |
| E17 | IFRS Foundation, PT Integrated Reporting Framework | 2024-05-02 | firm publication | verified | Marginal; says nothing on terminology |
| E18 | Globalization Partners | 2021-12-01 | vendor | verified | Low authority |
| EV2 | Migalhas de Peso, faturamento / receita bruta | 2018-12-12 (updated 2019-10-04) | law-firm article | gap fill | Single source for Brazilian usage |
| EV4 | Microsoft pt-BR localization style guide | 2024-02-09 | vendor style guide | gap fill | Product-localization context, applied by analogy |

### 1.6 Stream quality (from the validators)

| Stream | Dossier quality (1-5) | Claim checks verified | Checks with problems (partial, outdated, contradicted, inaccessible) | Main weakness |
|---|---|---|---|---|
| A-strategy | 4 | 14 of 17 | 3 | Process-over-analysis evidence is observational; slide-structure rules rest on practitioner pages |
| B-dataviz | 3.5 | 13 of 18 | 5 | B1 overstated; B4 evidence base thinner than presented; no evidence for distributions, scatter, sorting |
| C-storytelling | 3.5 | 9 of 18 | 9 | Many findings abstract-level; no executive-reader or document-level tests |
| D-dashboards | 4 | 14 of 20 | 6 | No 2020-2026 dashboard comprehension study; several rules are inferences |
| E-translation | 3.5 | 16 of 24 | 8 | No Portuguese or frontier-model evidence for numeric errors; glossary English side inferred |

---

## 2. Universal operating principles

Fifteen principles that should govern every deliverable. Each lists load-bearing finding ids, the overall strength (the weakest load-bearing part unless stated), and the rules that implement it.

**P1. Lead with the answer and the ask.** The first screen says what is recommended and what decision is requested, by whom and by when; informational items say whether action is required. Refs: [A11, AV2, A13, AV4, C16, C17, CV4, D13, D14]. Strength: practitioner-consensus; only sentence-level experiments support claim-before-reason (CV4) and no document-level test exists. Rules: CORE-1.

**P2. Match effort to the stakes.** Full decision machinery (alternatives, forecasts, downside, owners) only for consequential, irreversible or recurring decisions; routine items get a short decision statement. Refs: [A4, A1]. Strength: practitioner-consensus. Rules: CORE-2.

**P3. Subtract on purpose.** Cut every sentence, idea and request that would not change the reader's decision or action; writers default to adding, so deletion needs an explicit pass and a visible cut list. Refs: [C1, C2, C3, CV1, CV2]. Strength: moderate for cutting, weak for the one-ask rule. Rules: CORE-3, CORE-13, WRIT-9.

**P4. Show real alternatives and what the recommendation gives up.** At least one or two genuine options on the same criteria, with reasons for rejection; no strawmen. Refs: [A2, A7, A8, AV1]. Strength: moderate (observational). Rules: CORE-4.

**P5. Every number carries provenance, units and a computation trail.** Source and as-of date, reported vs calculated vs assumed, unit, period and scope; arithmetic done by tools, not prose. Refs: [A1, D2, D7, D15, D17, DV4, B8, B12, E3, E7]. Strength: practitioner-consensus (provenance), moderate (compute by tool). Rules: CORE-5, CORE-6, XLAT-6.

**P6. Never fabricate sources, process, causes or inputs.** No citation, quote or statistic that was not opened; no invented consultation, dissent, pilot, cause, target, tolerance or owner; use "unverified", "cause not provided" or "No target". Refs: [D15, D16, D18, A1, A2, D7, D9, D17, DV2]. Strength: strong for citations, practitioner-consensus for process and inputs. Rules: CORE-7, CORE-8, RES-9, RES-10.

**P7. Put uncertainty, risk and caveats where the decision is made.** In full sentences, in the main body, next to the recommendation, with a number or range; downside as a named failure scenario, not a decorative table. Refs: [A2, A3, A6, C6, CV3, B12, BV2]. Strength: moderate (CAIB is one multi-causal case). Rules: CORE-9, RES-3, RES-4, VIZ-15.

**P8. Titles are claims and each exhibit makes one point.** Full-sentence, neutral, quantified headings; one comparison per exhibit; the most prominent visual element is the one the title names. Refs: [A13, AV4, C7, C8, B8, B9, B10, B11]. Strength: weak for claim-form headings, moderate for neutral quantified exhibit titles and prominence. Rules: CORE-11, STORY-3, VIZ-7, VIZ-8, VIZ-10.

**P9. Draw honestly.** Encodings match the question; bars start at zero; non-zero ranges are labeled and justified; comparable charts share ranges; one meaning per colour in a document. Refs: [B1, B2, B3, BV1, B5, B12, B15]. Strength: strong for bar baselines and for avoiding angle-only or area-coded primary quantities; practitioner-consensus for the rest. Rules: VIZ-1 to VIZ-6, VIZ-18.

**P10. Never rely on colour alone; keep contrast.** Every status, category or variance has a word, sign, symbol or pattern as well; marks at least 3:1, chart text at least 4.5:1. Refs: [B13, BV3, B14, DV1]. Strength: strong (standard; applied to slides and print by extension). Rules: VIZ-12, VIZ-13, VIZ-14.

**P11. Declare the job and mode before layout, then put attention first.** Name audience, decision and form (read-ahead vs presented; monitoring vs analytic vs narrative; faithful translation vs adaptation); open with exceptions; keep the format stable across periods. Refs: [D1, D3, DV3, D7, D2, C7, C8, C9, E18]. Strength: practitioner-consensus. Rules: CORE-10, CORE-12, STORY-1, DASH-1, DASH-2, XLAT-16.

**P12. Make status, ownership and next steps explicit and rule-based.** One named decider, one recommender, stated blocking power for sign-off parties, written status rules, an owner and date on every action or red flag. Refs: [A11, AV2, A6, D9, D7, D13, DV2]. Strength: practitioner-consensus to weak. Rules: RES-5, RES-6, DASH-3, DASH-4, WRIT-10.

**P13. Transformations must be auditable.** Translating, condensing, restyling or localising must preserve content and numbers, reconcile counts and figures before delivery, and tell the user what changed, what was removed and what was queried. Refs: [CV1, C3, E1, E3, E5, E6, E18]. Strength: moderate. Rules: CORE-13, XLAT-1, XLAT-6, XLAT-11, XLAT-12, XLAT-16, XLAT-17.

**P14. Self-review is a floor, not independent review.** Run the pre-delivery gate and the weakest-link check; advise independent human review for high-stakes items; treat automatic scores, LLM judges and back-translation as triage only. Refs: [A1, A10, E6, E8, E9, D17, D18]. Strength: practitioner-consensus; no tested support for the compromise itself. Rules: QA-1, QA-4, QA-6, QA-7, XLAT-14, XLAT-15.

**P15. State research at its true strength.** Never quote headline effect sizes without definition, source and limitation; label each justification as standard, experiment, practitioner convention or Claude policy. Refs: [A5, AV1, A6, A15, A8, C10, C11, D17, B1, B4, B6, B10, B14]. Strength: strong (the don't-overclaim rules were validator-rated strong). Rules: RES-11, QA-5.

---

## 3. Operational rules by domain

Each rule is imperative and testable. Format: id, placement tag, rule, then Evidence, Strength, Scope. Overlapping rules from different streams were merged under one id; a "Merged" or "Note" remark records the reasoning where the sources conflicted. Cross-references in the form RC-n and PC-n point to section 4.

### 3.1 Core (applies to most deliverables)

- **CORE-1** `[core]` Open every decision-oriented deliverable (memo, email, deck, report, board paper) with the answer and the ask in the first one or two sentences: the recommended action, then the decision requested as verb + object + amount or scope + who decides + by when, and label the item Decision, Discussion or Information. For a purely informational item, open with the main finding and say whether any action is required. Test: a reader who stops after the first screen can say what is asked, of whom, by when. *Evidence:* A13, A11, AV2, AV4, C16, C17, CV4, C13, D13, D14. *Strength:* practitioner-consensus. *Scope:* context: decision-oriented deliverables for readers who know the topic; not raw-data dashboards or reference appendices. If the answer cannot be read without context, put at most three situation sentences first (WRIT-4).
- **CORE-2** `[core]` Classify the decision before writing. Consequential means irreversible or costly to reverse, material spend or headcount, cross-unit impact, or a recurring decision type; it gets the alternatives, forecast, downside and ownership rules (CORE-4, RES-2 to RES-6). Routine means a short decision statement: the ask, the reason, one alternative or the status quo, the main risk (S5). If stakes are unclear, write the short form and offer to expand. *Evidence:* A4, A1. *Strength:* practitioner-consensus. *Scope:* universal across recommendation deliverables. Note: the source gives no numeric stakes threshold, so the criteria are the validator's working definition, not a finding.
- **CORE-3** `[core]` Cut every sentence, idea and request that would not change the reader's decision or action. Set no word target and cite no quantified benefit of shortness. Detail needed for audit or compliance moves to an appendix instead of being deleted. *Evidence:* C1, C2, CV2, CV1. *Strength:* moderate. *Scope:* universal executive default; overridden when the user asks for a comprehensive technical or compliance document.
- **CORE-4** `[core]` For consequential decisions, show the recommended option beside at least one or two genuine alternatives (include "do nothing / status quo" when it is a real option). Compare all options on the same three to five criteria stated up front; give each alternative's pros, cons and why it was not chosen; state what the recommendation costs or gives up. If only one option is credible, say why. Never include an option nobody would choose just to flatter the recommendation. *Evidence:* A2, A8, A7, AV1. *Strength:* moderate (observational convergence; Eisenhardt covers eight firms). *Scope:* consequential decisions.
- **CORE-5** `[core]` Give every figure-bearing page, table and chart a source line and as-of date, define any non-obvious term once, and state unit, period and scope; for indexed or adjusted series state the base period or method. Tag every decision-driving number as reported (source, date), calculated (from what) or assumed (whose assumption, why). Never present an assumption, an estimate or a remembered figure as a sourced fact, and flag any figure you could not verify. Test: each headline number has a source line, a calculation note or an "assumption" tag. *Evidence:* A1, D2, D7, B12, B8. *Strength:* practitioner-consensus. *Scope:* universal for deliverables with numbers. Merged: provenance (stream A), source and as-of date (stream D), metric, unit, period and source on every exhibit (stream B).
- **CORE-6** `[core]` Compute totals, variances, percentages, percentage changes and growth rates with code or a spreadsheet tool when one is available, show the basis (what is compared with what, which period), and reconcile each total to its source before delivery. Do not do multi-step arithmetic in prose. *Evidence:* D15, D17, DV4. *Strength:* moderate. *Scope:* any deliverable with computed numbers. Note: this is a risk-control inference; no study measures numeric error rates in generated business reports (DV4 is a 2023 question-answering benchmark; D15 concerns citation fields).
- **CORE-7** `[core]` Do not include a citation, quote, statistic, regulation or named source that you did not open and check in this session. Mark anything unverifiable "unverified" in the text, or remove it; never restate it from memory. *Evidence:* D15, D16, D18. *Strength:* strong. *Scope:* universal.
- **CORE-8** `[core]` Do not invent process, causes or inputs. Never state that stakeholders were consulted, that dissent was heard, that options were compared, or that something was piloted or validated unless the user supplied that fact. Do not explain why a number moved unless the cause is in the user's inputs or in a source you opened; otherwise write "cause not provided", or label the explanation a hypothesis and list it as an open question for the metric owner. Never invent targets, tolerances, owners or thresholds; print "No target" or "[to be confirmed by <role>]". End a consequential recommendation with a one-to-three-line Basis note listing only the sources used, the key assumptions, and what is unverified or not yet reviewed by anyone independent. *Evidence:* A1, A2, D7, D9, D17, D18, D11 (convention; unchecked). *Strength:* practitioner-consensus. *Scope:* universal. Merged: the dossier's "how this was produced" note was replaced by the Basis note because a model-written process narrative can fabricate the dissent a reviewer would rely on (RC-18).
- **CORE-9** `[core]` Put the recommendation's main risk, key assumption and uncertainty in full sentences in the main body, next to the recommendation, with a number or range where one exists. Do not leave them only in footnotes, speaker notes, appendix or sub-bullets. *Evidence:* C6, CV3. *Strength:* moderate (one case; the CAIB account is organisational and multi-causal, so cite it as a caution). *Scope:* any recommendation or forecast a decision depends on.
- **CORE-10** `[core]` Put what needs attention first. In the opening band list only items that are off target, materially changed, or need a decision, ranked, and state the selection criterion; compress on-track items into one line or move them to an appendix. *Evidence:* D7, D2, DV3. *Strength:* practitioner-consensus. *Scope:* dashboards, business reviews, KPI and status reports, and the status section of longer documents.
- **CORE-11** `[core]` In a deliverable that executives will read or present, write every content-slide title and section heading as a full-sentence claim that the content beneath proves (subject, verb, so-what). Test: read only the headings in order; they must carry the recommendation and its supporting arguments, and each must survive "so what?". Topic labels ("Pricing review", "Background") fail. When converting a deck to answer-first, rewrite the supporting headings too, not only the front slide. *Evidence:* A13, AV4, C7, C8. *Strength:* weak. *Scope:* context: strongest for pre-read decks, memos and reports; allow descriptive labels for appendix, data tables and reference pages; in presenter-led talks keep claim titles to about two lines or let the speaker state the claim (RC-4).
- **CORE-12** `[core]` Before choosing layout, write one line naming the audience, the decision or question, and the form: read-ahead or presented deck (STORY-1); monitoring, analytical or narrative dashboard (DASH-1); faithful translation or adaptation (XLAT-16). Tell the user the choice in the build note. *Evidence:* D1, D3, DV3, C7, C8, C9, E18. *Strength:* practitioner-consensus. *Scope:* universal.
- **CORE-13** `[core]` When improving existing material, build a cut list before rewriting: for every section, slide, paragraph or bullet record keep, cut or merge with a one-line reason, run an explicit pass that asks what can be removed, and give the user the list of what was removed or changed. Tasks whose brief is to expand are exempt. *Evidence:* CV1, C3. *Strength:* moderate. *Scope:* improve, rewrite, condense and self-review of long drafts. Note: in CV1 the remedy that worked was an explicit cue to subtract (for example 21% to 48% in one test and 41% to 61% in another). The 83% figure comes from the book excerpt (C3); CV1 is the peer-reviewed primary source of the add-bias effect, and the exact mapping of the 83% to a CV1 study is unverified (section 7.4).

### 3.2 Writing

- **WRIT-1** `[ref:writing]` Run a plain-language sentence pass on English prose: named actor as subject; active voice (passive only when the actor is unknown or irrelevant); present tense by default; turn hidden verbs (-ment, -tion, -sion, -ance endings, or make/take/have/give plus a noun) back into verbs. Do not transfer English hidden-verb patterns mechanically to Portuguese. *Evidence:* C14, CV3. *Strength:* practitioner-consensus (official guidance; no comprehension-effect data). *Scope:* context: English business prose.
- **WRIT-2** `[core]` Put the decisive number in the headline or first sentence, never only at the bottom. Replace vague quantifiers (significant, substantial, major, improved) with the figure and its comparison base. Use "significant" only for statistical significance. Write units and number formats consistently. *Evidence:* CV3. *Strength:* practitioner-consensus (case-based: the CAIB slide buried the key number, used "significant" five times in different senses and mixed units). *Scope:* universal for quantitative claims, including dashboard commentary.
- **WRIT-3** `[ref:writing]` Structure an argument as one governing recommendation, then supporting arguments grouped logically (same kind, in a stated order such as time, structure or importance, with no overlaps or gaps), then evidence under each. Do not impose a fixed count of supporting arguments; regroup if the list keeps growing. *Evidence:* C17, A13. *Strength:* practitioner-consensus. *Scope:* context: memos, reports and deck storylines for decisions; not reference documents or chronological records (logs, incident timelines). Merged: the validator's "about three supports" default was dropped because the 2-3 limit is unsupported (RC-16, section 6).
- **WRIT-4** `[ref:writing]` Use an SCQA opener (situation, complication, implied question, answer) only when the reader lacks context or the recommendation is surprising or contested. Keep it to three sentences or fewer with the answer last; skip it for informed readers. *Evidence:* C17. *Strength:* practitioner-consensus. *Scope:* context: memos, emails and first slides for audiences needing context.
- **WRIT-5** `[ref:writing]` For documents longer than about one page, add claim-style headings, one idea per paragraph, lists for parallel items, and an opening paragraph saying what the document contains and where the recommendation is. Skip the navigation paragraph for one-page notes. *Evidence:* CV2, C2. *Strength:* weak. *Scope:* documents read by time-pressed readers on screen or paper. The one-page threshold is a default, not tested (RC-3).
- **WRIT-6** `[ref:writing]` Use at most one emphasis device per section (for example bold only), reserved for the decision, a key number or a deadline; do not stack bold, underline and highlight; do not bold whole sentences. *Evidence:* C2. *Strength:* weak (the authors' claim from an interview). *Scope:* emails, memos, reports. Chart colour emphasis is governed by VIZ-8.
- **WRIT-7** `[ref:writing]` Replace promotional adjectives and unsupported superlatives ("world-class", "game-changing", "significant opportunity") with the fact or number that supports them. *Evidence:* CV2. *Strength:* weak (only the subjective-satisfaction gain was significant). *Scope:* executive memos, decks and reports; sales or marketing material may keep persuasive language when the user asks.
- **WRIT-8** `[ref:writing]` When a quantity changes, write the starting value before the ending value in the same sentence ("from 12% to 9%") and state period and base. Headline claims may lead with the result if the from-to appears in the same sentence or the first line below. *Evidence:* C13. *Strength:* weak (abstract-level, sentence-level). *Scope:* prose describing change.
- **WRIT-9** `[ref:writing]` State exactly one primary request per message or section. Put other requests under a separate label ("Also needed") or in a second message, each with an owner and a date. *Evidence:* C1, C2. *Strength:* weak (the authors' claim plus one field experiment without statistics). *Scope:* context: emails, memos and updates; not a limit on the number of decisions in a long board paper, where each decision gets its own labeled section.
- **WRIT-10** `[ref:writing]` Write variance commentary as event, cause (supplied), so-what (effect on margin, cash or target), and next action with owner and date. Comment only on variances above a materiality threshold supplied by the user; do not restate table numbers line by line; "not yet known" is acceptable only with a named follow-up owner and date. *Evidence:* DV2, D7, D11 (convention; unchecked). *Strength:* practitioner-consensus. *Scope:* variance narratives in reports and business reviews. Note: DV2 is a regulatory anchor for SEC filers (explain, do not merely repeat the numbers; attribute material revenue changes to price, volume or new products), not a requirement for internal documents.

### 3.3 Storytelling and presentations

- **STORY-1** `[ref:presentations]` Declare the deck mode before building. Presented mode: sparse slides, narration in speaker notes. Read-ahead mode: each slide must be understandable without a speaker (claim title, evidence, and one to three lines stating the so-what). Do not ship a sparse presented-style deck as a read-ahead. *Evidence:* C7, C8, C9, AV4. *Strength:* practitioner-consensus (the slide-design experiments test narrated slides; Farkas notes the speaker's role is ignored). *Scope:* all decks; state the mode in the build note.
- **STORY-2** `[ref:presentations]` Write the storyline first: a numbered list of claim sentences that will become the titles. Check that reading them top to bottom delivers the recommendation without the body and that every body element supports exactly one title. *Evidence:* C7, C17, A13. *Strength:* practitioner-consensus (no accessed empirical evidence on storyline-first). *Scope:* decks and multi-section memos of more than a few slides or pages.
- **STORY-3** `[ref:presentations]` One message per slide. If the title needs "and" to join two independent claims, split the slide. A summary or agenda slide may carry several items if its title states one claim about them. *Evidence:* C7, C8. *Strength:* practitioner-consensus (Farkas supports that sentence titles focus attention on one idea; no study tests one-message-per-slide). *Scope:* slides.
- **STORY-4** `[ref:presentations]` In a presented deck, on-slide text is a claim title plus evidence (chart, table or number) with short labels. Do not paste the speaker script or the memo's paragraphs onto slides; narration goes in speaker notes. *Evidence:* C9, C10. *Strength:* moderate (lab learning studies with students, extrapolated to decks). *Scope:* narrated or presented slides; not read-ahead decks, where text must stand alone (STORY-1).
- **STORY-5** `[ref:presentations]` Keep bullets short, parallel and at most two levels deep. Any statement containing a cause, condition, comparison or caveat is a full sentence, not a nested bullet or fragment. *Evidence:* C6, CV3, C8. *Strength:* weak. *Scope:* decks and memos; plain parallel lists (steps, options, owners) stay as bullets. Reasoning: the CAIB slide used six levels for content that was eleven simple sentences, but Farkas finds brief well-phrased bullets harmless, so the rule covers reasoning and risk content only (RC-21).
- **STORY-6** `[ref:presentations]` Remove decorative images, anecdotes and tangential facts that do not bear on the decision, unless the stated purpose is engagement. Do not quote effect sizes for this. *Evidence:* C11, C10. *Strength:* weak (learning-study meta-analysis from a secondary summary; moderators conflict). *Scope:* decision decks and memos; keynotes, training and storytelling-led talks are exempt.
- **STORY-7** `[ref:presentations]` Keep the main body to what the decision needs. Put backup, methods and long tables in an appendix with a pointer from the main text. Never place a caveat that changes the recommendation only in the appendix. *Evidence:* CV3. *Strength:* practitioner-consensus (no accessed evidence on appendix use). *Scope:* decks and reports for executives; not documents whose purpose is full documentation.
- **STORY-8** `[opt:narrative-memo]` For a complex, multi-factor decision, offer a narrative memo of about six pages in full-sentence prose that ranks and connects the arguments, with slides reserved for data exhibits. Describe this as Amazon's documented practice (2017 shareholder letter), not as proof of better decisions. *Evidence:* C4, C5. *Strength:* practitioner-consensus. *Scope:* strategy and investment decisions with trade-offs; not routine updates (RC-17).

### 3.4 Data visualization

- **VIZ-1** `[core]` Start the value axis of every bar or column chart at zero. Never truncate it and never use an axis break. When the differences that matter are small relative to the values, print the delta (absolute and percent) on the chart or switch to a dot, line or difference chart with a labeled axis range. *Evidence:* B2, B3, BV1. *Strength:* strong. *Scope:* bar and column charts and any filled mark whose length encodes value, including stacked baselines. Note: the authors of B2 resist a blanket "always zero"; the rule rests on the length-encoding logic plus convention, and BV1 shows too-wide ranges also mislead, which is why the fix for small deltas is a different encoding or an explicit number, not a truncated bar (RC-5).
- **VIZ-2** `[ref:dataviz]` On line, dot and range charts, a non-zero axis is allowed only when change or difference is the message. Print the axis start and end values; state the actual change as a number in the title or an annotation; never choose a range that makes a decision-relevant change look larger or smaller than its business size; use identical axis ranges for charts the reader is meant to compare, across panels and across slides. *Evidence:* B2, B3, BV1. *Strength:* moderate. *Scope:* line, dot and range charts. Witt's SD-based range is not transferable to business KPIs.
- **VIZ-3** `[ref:dataviz]` To compare magnitudes across categories, use bars or dots on one shared axis or baseline with direct value labels. Do not encode the primary quantity by area (bubbles, treemap size), volume or 3D, or angle (pie, donut, radial bars) when a common-baseline bar can carry it; if such a form is used for layout reasons, print every value. When justifying: position on a common scale was the most accurate encoding in the Cleveland-McGill replication and area was worse than position and angle; do not claim angle is worse than length. *Evidence:* B1, B5, B17. *Strength:* strong. *Scope:* any exhibit whose question is "which is bigger, by how much". Note: B1 was only partially supported and B17 only partially supported; the rule is worded to the safe claim.
- **VIZ-4** `[ref:dataviz]` Sort categorical bars by value (descending, or by the ranked metric) unless the categories have an inherent order such as time, funnel stage, size band or hierarchy; place "Other" or "Not specified" last. *Evidence:* B1. *Strength:* practitioner-consensus (no experiment in the dossier tests sorting). *Scope:* ranking and comparison bars with nominal categories.
- **VIZ-5** `[ref:dataviz]` Show composition as sorted bars or one 100% stacked bar with labeled percentages. Use a pie or donut only for two or three slices that sum to a stated whole, each labeled with its value. Do not use exploded, varying-radius, icon-shaped, nested or 3D pies, and never let angle alone carry a share. Do not claim a donut is more or less accurate than a pie. *Evidence:* B5, B1. *Strength:* moderate. *Scope:* part-to-whole exhibits. The two-to-three slice limit is a heuristic; "never" for the variants is a conservative choice (B5 reasons about them and says exploded pies may be fine for some tasks).
- **VIZ-6** `[ref:dataviz]` Default to no dual y-axes. Use two aligned panels sharing the x-axis, or index both series to 100 at a stated base period with endpoint labels. Allow a dual axis only when the reader's question is timing or co-movement of two series in different units; then label each axis with units, colour-match each axis to its series, label the series directly, and do not use it to imply correlation or for a single measure. *Evidence:* B4, BV4. *Strength:* practitioner-consensus. *Scope:* charts with two series in different units; general executive audiences (RC-6).
- **VIZ-7** `[ref:dataviz]` Give every explanatory exhibit a title that states the finding as metric + direction + magnitude + comparison base ("Gross margin fell 2.1 pp vs plan in Q3"), without evaluative or loaded words (alarming, disappointing, healthy). Descriptive titles are allowed only in appendix or exploratory exhibits. Test: would a reader who disagrees with the conclusion still read the same claim from title and chart? If the title would read differently under the opposing frame, rewrite it. *Evidence:* B8, B9, B10, B11. *Strength:* moderate. *Scope:* exhibits in decks, memos and dashboard headlines that carry a claim. Note: the ban on evaluative adjectives extends B8, which manipulated frames and slants, not adjectives as such (RC-1, PC-4).
- **VIZ-8** `[ref:dataviz]` Make the element named in the title the most visually prominent element (accent colour, annotation, direct label) and mute the rest in grey. If the claim concerns a low-prominence feature, restructure or highlight the chart; do not rely on a title or caption to override a more dominant pattern. *Evidence:* B9, B10. *Strength:* moderate. *Scope:* explanatory exhibits, especially line charts.
- **VIZ-9** `[ref:dataviz]` Default explanatory format: remove 3D, shadows, heavy borders and dense gridlines; grey for context plus one accent colour (no more than two meaningful colours unless categories require more); one annotation at the key point; label end points, maxima, minima and highlighted values rather than every point of a dense series; with about 12 bars or fewer, label every bar and drop the value axis (practitioner convention). Do not say decluttering improves comprehension. *Evidence:* B10, B11, B7. *Strength:* moderate. *Scope:* explanatory exhibits for executives; not exploratory analysis, where gridlines and all-value labels may help (PC-2).
- **VIZ-10** `[ref:dataviz]` Limit each exhibit to one comparison and one message, visible at first glance in the title or a direct label; if a slide or panel needs two comparisons, split it. Use familiar chart forms (bar, line, table, and finance-standard forms such as waterfall and bullet where the audience uses them); add a one-line "how to read" note for any less familiar form; do not choose novel chart types for memorability. *Evidence:* B11, B7, B12. *Strength:* moderate. *Scope:* executive decks and dashboards; mixed or senior audiences.
- **VIZ-11** `[ref:dataviz]` Label series and categories directly on the chart instead of in a separate legend whenever there is room. Beyond about eight categories do not rely on colour to distinguish them: use direct labels, group the tail into "Other", or use small multiples. *Evidence:* B14, B10, B17. *Strength:* practitioner-consensus (eight from Wilke; Munzner's slides give 6-12). *Scope:* charts with more than one series or category.
- **VIZ-12** `[core]` Never let colour be the only carrier of a category, status, sign or variance. Pair every red/amber/green or red/green mark with a word, +/- sign, arrow, icon or pattern, and reserve red and green for status. Test: the exhibit still reads correctly in grayscale and under a red-green colour-vision-deficiency simulation. When citing prevalence write "roughly 5-8% of men and 0.4-0.5% of women, depending on ancestry". *Evidence:* B13, B14, DV1. *Strength:* strong. *Scope:* all visual deliverables including slides, PDFs and print.
- **VIZ-13** `[ref:dataviz]` Contrast thresholds: every mark a reader needs (bar, line, segment, marker) at least 3:1 against its adjacent background; chart text (axis labels, data labels, annotations, footnotes) at least 4.5:1, or 3:1 if 18 pt or larger (14 pt bold). Muted context greys must pass: #949494 on white is 3.03:1 (passes narrowly), #BFBFBF is 1.84:1 (fails), #767676 is 4.54:1 (suits text). Exceptions: decorative gridlines, and marks whose values are printed as text that itself passes 4.5:1. Call this "WCAG-aligned", not "compliant". *Evidence:* B13, BV3, IMPL-palette-contrast. *Strength:* strong. *Scope:* all chart deliverables, applied by extension from web to slides and print.
- **VIZ-14** `[ref:dataviz]` If no brand palette is given, use Okabe-Ito for categorical colour with at most eight categories (S11). On white, do not use yellow (1.32:1), orange (2.25:1) or sky blue (2.31:1) as the only colour of a thin line, small marker or text; prefer blue (5.19), vermilion (3.87), bluish green (3.42), reddish purple (3.06, borderline; 2.81 on #F5F5F5, so it fails on light-grey fills) or black. If a brand palette is supplied, keep it and run VIZ-12 and VIZ-13 against it. *Evidence:* B14, B13, IMPL-palette-contrast. *Strength:* moderate. *Scope:* categorical series colours when no brand or template palette governs. Note: blue next to vermilion has only 1.34:1 contrast, so adjacency contrast is not guaranteed by the palette.
- **VIZ-15** `[ref:dataviz]` Whenever a number is an estimate, forecast, survey result or model output, show or state its range beside the point estimate (low/base/high scenarios or an interval) and say what the range means in the label or footnote (95% CI, +/-1 SD, min-max, scenario spread). Do not leave error bars or bands unlabeled; do not present a forecast as a single line without a range. *Evidence:* B12, BV2. *Strength:* moderate. *Scope:* estimates, forecasts and projections; not audited actuals.
- **VIZ-16** `[ref:dataviz]` Do not use bars with whiskers as the only display when readers must compare estimates or judge how likely values are. Use a point with its interval, a range table or labeled scenario bands. Do not use gradient or violin plots in executive materials unless the audience asks. *Evidence:* B12. *Strength:* weak (the dot-and-interval substitution is an extrapolation: B12 tested gradient and violin plots and notes the cultural cost of non-standard encodings). *Scope:* inferential comparisons of estimates; not plain-count bars.
- **VIZ-17** `[ref:dataviz]` For two series with similar values, overlay them in one panel. Overlay lines only up to about four series (heuristic) and only when values are close; with more series or a wide value range, use small multiples with identical axis ranges and a shared x-axis. *Evidence:* B16. *Strength:* moderate. *Scope:* multi-series time series and pairwise comparison (PC-3). Animation in Ondov et al. does not transfer to static documents.
- **VIZ-18** `[ref:dataviz]` Within one document a colour, fill or pattern keeps one meaning in every chart: actual, plan, prior year and forecast each keep one encoding throughout, and a scenario colour is not reused for an unrelated series. *Evidence:* B15, B11. *Strength:* practitioner-consensus (the IBCS "unify" idea; no controlled test). *Scope:* multi-slide or multi-page deliverables with recurring series.
- **VIZ-19** `[opt:ibcs-notation]` Apply IBCS-style scenario and variance notation only if the user or company uses IBCS or asks for it. Then show actual, prior year, plan and forecast with one fixed encoding each (the commonly documented convention is actual solid dark, prior year grey, plan outlined, forecast hatched, but vendors disagree on black versus dark grey for actual), show variances in both absolute and relative terms with sign, and mark favourability with a sign or word as well as colour, since a cost overrun is a positive number with an unfavourable effect. Check any specific encoding against the current IBCS 2.0 or ISO 24896 text before presenting it as required. *Evidence:* B15, B13. *Strength:* practitioner-consensus. *Scope:* finance or controlling reports where IBCS is in use or requested (RC-15).

### 3.5 Dashboards, KPIs and board papers

- **DASH-1** `[ref:dashboards]` For a monitoring dashboard or one-page KPI summary, make the first view fully readable on one screen or page without scrolling or interaction, and put everything else behind drill-down or in an appendix. Analytical or narrative multi-page formats are acceptable only if page one stands alone. *Evidence:* DV3, D2. *Strength:* practitioner-consensus. *Scope:* monitoring dashboards and one-page summaries; not analytical tools. The single-screen rule is contested for mobile and wall displays (RC-9).
- **DASH-2** `[ref:dashboards]` Keep layout, chart types, colours and metric order identical from period to period in a recurring pack; change content, not structure. If structure must change, say so at the top. *Evidence:* D7. *Strength:* practitioner-consensus (one company's practice; the source calls the constraint "not hard"). *Scope:* recurring dashboards and business reviews.
- **DASH-3** `[ref:dashboards]` Give each KPI the same minimum fields (S2): name, one-line definition, owner, source and as-of date, unit, polarity (higher is better, lower is better, or in range), actual with period label, target with its source or the words "No target", comparison basis, variance, status rule; add a one-line commentary for flagged KPIs. Every dashboard page also shows data source, owner, KPI definitions, last-updated date and a short note on assumptions and known limits. *Evidence:* D7, D2, D10. *Strength:* practitioner-consensus (catalogue-level for meta-information; polarity and the exact field list are design inferences, not tested). *Scope:* KPI dashboards and scorecards.
- **DASH-4** `[ref:dashboards]` Define each status colour as a written rule on the page (for example "green: at or better than target; amber: within the stated tolerance; red: beyond tolerance or a stated trigger"); make some reds automatic through a stated trigger such as a missed milestone; attach an action, owner and date to every red. Tolerance values come from the owning team; do not invent them (S3). *Evidence:* D9, D2. *Strength:* weak (one vendor article plus catalogue; no numeric thresholds exist in any source; the written-definition, automatic-red and recovery-plan advice was not found in the D9 article itself, so it is a practitioner convention). *Scope:* status-colour reporting (project, programme, KPI).
- **DASH-5** `[ref:dashboards]` Show qualitative performance ranges as bands of one muted hue at different intensities, and keep saturated colour for the status or exception being flagged. *Evidence:* D4. *Strength:* practitioner-consensus (Wikipedia citing Few; secondary). *Scope:* KPI-versus-range displays.
- **DASH-6** `[ref:dashboards]` Show status against target as a horizontal bar with a target marker (bullet-graph style) instead of a gauge or dial. If asked to justify: it is more compact and was read more efficiently (time to first fixation) in one 40-participant eye-tracking study; do not claim better accuracy or comprehension, and do not extend the claim to pie charts. *Evidence:* D4, D5. *Strength:* weak. *Scope:* KPI status displays.
- **DASH-7** `[ref:dashboards]` Flag only new or worsened exceptions. Do not repeat an unchanged flag every period at full prominence: move it to a "carried over" line with age and owner, and state how many flags are shown and how they are ranked. *Evidence:* D8. *Strength:* weak (healthcare alert-fatigue data; transfer to KPI flags is an inference; no cap value is evidenced, so state a cap rather than copying a number). *Scope:* recurring dashboards, alerts and exception lists (PC-6).
- **DASH-8** `[ref:dashboards]` Show variance against target and against the prior period, absolute and percent, and label it favourable or unfavourable from the KPI's polarity, not from the sign of the number. When a material total moves, decompose it into drivers (price, volume, mix) before commenting. *Evidence:* DV2, D11 (convention; unchecked). *Strength:* practitioner-consensus. *Scope:* financial and operational variance reporting. Polarity labelling follows from the definition and has no direct source.
- **DASH-9** `[ref:dashboards]` In operational reviews, label each metric as an input (controllable action) or an output (result), link every output to its driver inputs, and discuss outputs only through those drivers. Show recent trend with the same period last year visually de-emphasised, and put growth rates beside absolute values where rates matter. *Evidence:* D7, D6. *Strength:* practitioner-consensus (one company's practice through a secondary account; D6 is used as a concept only). *Scope:* recurring operational reviews with identifiable driver metrics; not every financial board pack. Do not state the Amazon WBR deck order (PC-7).
- **DASH-10** `[opt:kpi-guardrails]` When a KPI has a target tied to incentives or team goals, name its known gaps as a proxy and pair it with a guardrail metric that would reveal gaming or a drifting proxy. *Evidence:* D10. *Strength:* weak (a mitigation inferred from a conceptual taxonomy). *Scope:* incentive-linked or target-bound KPIs, not every metric. Keep the taxonomy labels out of executive documents.
- **DASH-11** `[opt:board-paper]` For a decision paper, put the exact draft resolution near the top, worded so the board can adopt it without amendment. *Evidence:* D13. *Strength:* practitioner-consensus. *Scope:* board and committee decision papers.
- **DASH-12** `[opt:board-paper]` Keep the executive summary to one paragraph of about four to five lines stating purpose and whether approval or noting is sought, then give the recommendation in its own section of no more than one page, including alternatives considered and intended outcomes. *Evidence:* D13, D14. *Strength:* practitioner-consensus (one governance body's sample). *Scope:* board papers in the AICD style. For non-board memos, CORE-1 applies (RC-10).
- **DASH-13** `[opt:board-paper]` Cap strategy, financial, risk and any other implications sections at about half a page each and background at about one page; put business cases, calculations and criteria in appendices and keep the financial section to key points. *Evidence:* D13. *Strength:* practitioner-consensus. *Scope:* board papers.
- **DASH-14** `[opt:board-paper]` Before adding content to a pack, state its purpose and the decisions it supports; remove or demote to an appendix or a "for noting" bundle any section that changes no decision or discussion, especially routine compliance and operational reporting. *Evidence:* D12, D14. *Strength:* weak (vendor surveys; small or mixed samples). *Scope:* board and committee packs. Do not set page-count or reading-speed targets (PC-8, section 6).

### 3.6 Research and evidence standards (including recommendation quality)

- **RES-1** `[ref:research-evidence]` State the lead answer early, then say what evidence would change it and what you checked that could have disproved it, with the result. If the data conflicts with what the requester expects, headline the conflict. Do not collapse to one option early to save time: narrow depth of analysis, not breadth of options. *Evidence:* A2, A7. *Strength:* practitioner-consensus (hypothesis-first as a default practice is unverified, see A14 in section 7; pairing it with disconfirmation is a synthesis with no outcome test, RC-2). *Scope:* research-driven recommendations and analyses.
- **RES-2** `[ref:research-evidence]` Anchor each base-case forecast (timeline, cost, revenue, adoption) to at least one comparable reference: benchmark, comparable past projects or launches, or a historical hit rate. Name the reference class and show the gap between it and the internal estimate. If no comparison data exists, label the figure "inside-view estimate, not benchmarked" and give a range. *Evidence:* A3, AV3. *Strength:* moderate (large-sample infrastructure data; transfer to corporate forecasts is by analogy). *Scope:* consequential decisions resting on forecasts.
- **RES-3** `[ref:research-evidence]` Give the downside case as a named failure scenario, not a symmetric percentage haircut: what has to happen, where the case comes from (data, analogy or assumption), the quantified impact, an early-warning signal, and one line on how competitors or counterparties would likely respond. *Evidence:* A3. *Strength:* practitioner-consensus (the authors' own assertion). *Scope:* consequential decisions.
- **RES-4** `[ref:research-evidence]` For consequential decisions with an execution plan, add three to five failure causes written as if the plan has already failed. Each must be specific to this plan (a named dependency, date, owner or number) and carry an early signal, a mitigation and an owner (or "owner needed"). Generic risks ("market volatility", "resource constraints") do not count. Label the list as a draft for the team to run a real independent premortem. *Evidence:* A6, A3, A2. *Strength:* weak (three anecdotes; an LLM-written premortem lacks the independent dissent that is the method's point). *Scope:* consequential decisions only.
- **RES-5** `[ref:research-evidence]` When ownership of the decision is unclear or three or more parties are involved, name one recommender, exactly one decider, anyone whose sign-off is required, who carries it out (with a start date) and who is only consulted. For every sign-off party state whether they can block the decision and what happens if they object. Use plain labels; use RAPID letters only if the audience already uses RAPID. *Evidence:* A11, AV2. *Strength:* practitioner-consensus. *Scope:* cross-functional or multi-owner decisions (RC-8).
- **RES-6** `[ref:research-evidence]` For decisions that need other people to change what they do, include a short implementation path: who must act, what they need to agree to, the first step in the next 30 days, and whether implementers have been involved; if they have not, or you do not know, say so instead of implying alignment. *Evidence:* A8. *Strength:* moderate (observational; success defined as sustained use). *Scope:* change and implementation decisions.
- **RES-7** `[ref:research-evidence]` State a concentration claim ("top 5 customers = 70% of margin") only after computing it from the supplied data. Show the cumulative share, name the remaining tail (count and share), and flag small items that are growing or carry risk. Never assert "80/20" as a generic fact. *Evidence:* A16. *Strength:* weak. *Scope:* prioritisation and portfolio analyses.
- **RES-8** `[opt:scenarios]` Use scenarios only when one or two external uncertainties dominate the outcome and cannot be forecast. Present two to four scenarios built by varying several uncertainties together, label them "plausible" rather than "probable", show how the recommendation performs in each, and state the trigger for changing course ("if X by date, then Y"). Do not assign probabilities unless the user supplies them. *Evidence:* A15. *Strength:* weak. *Scope:* high-uncertainty strategic choices.
- **RES-9** `[ref:research-evidence]` Resolve every citation to a DOI or publisher page and check that title, authors, year, volume, issue and pages match the record; check DOIs themselves; drop any citation that cannot be resolved. *Evidence:* D15, D16. *Strength:* strong. *Scope:* research-driven recommendations and any document with references.
- **RES-10** `[ref:research-evidence]` For niche, regional or recent topics (local regulation, small companies, new standards) assume higher fabrication risk: use only sources fetched in the session and state when no source was found. *Evidence:* D16. *Strength:* moderate (one study, one model; fabrication ran about 6% in the best-documented condition versus 28-29% in the less familiar ones). *Scope:* research on specialised, local or less-documented topics.
- **RES-11** `[ref:research-evidence]` Do not cite these as established in a deliverable: "reducing bias adds up to 7 pp of ROI" or "process matters 6x more than analysis"; "prospective hindsight improves identification of failure reasons by 30%"; "scenario planning widens confidence ranges by 50%"; "half of all decisions fail"; "up to 75% of LLM summaries is hallucinated"; learning-study effect sizes (g = -0.33 and similar) as effects on executive decisions; Westinghouse reading shares, "page ten has a 90% chance of going unseen", "8x faster innovation", 15 or 20 words per minute of slide text; the 2004 Bezos email wording or "Bezos banned PowerPoint" as verbatim fact. If the user asks for one, give source, year, definition and limitation (self-reported correlational survey; second-hand citation; one n=68 study; failure defined as not sustained or fully used after two years; peak on one benchmark under a non-standard definition). *Evidence:* A5, AV1, A6, A15, A8, C10, C11, D17, C4, C5. *Strength:* strong. *Scope:* universal when quoting research. See S10 for replacement wording.

### 3.7 Translation and localization (PT<->EN focus)

- **XLAT-1** `[core]` When the task has source text in one language and requests output in another (PT<->EN), or converts Portuguese or English figures, load ref:translation and do not deliver until a source-versus-target number table (every numeral, currency, unit, scale word, date and period label) has been reconciled, even for one slide or a short summary. *Evidence:* E3, E5, E6, E7. *Strength:* moderate. *Scope:* any deliverable built from a source in another language or translated by Claude.
- **XLAT-2** `[core]` In any Portuguese-language deliverable use pt-BR formatting throughout one document: decimal comma and thousands point (1.234.567,89); currency symbol first with a non-breaking space (R$ 1.234,56; US$ 1.234,50 for dollars); percent without a space (12,5%); compact forms mil, mi, bi, tri (R$ 2,3 mi; R$ 1,5 bi) and milhão/milhões, bilhão/bilhões in prose; 24-hour time (14:30). In HTML or JavaScript generate numbers with Intl.NumberFormat('pt-BR', ...) instead of string concatenation. *Evidence:* E12, EV1, EV4. *Strength:* strong. *Scope:* any deliverable written in Brazilian Portuguese.
- **XLAT-3** `[ref:translation]` Never write an all-numeric date in an English or bilingual deliverable where day and month can be swapped (day 12 or lower). Write "29 Oct 2026" or "29 de outubro de 2026", or ISO 2026-10-29 inside tables. Do not mix day-first and month-first in one document; day-first does not identify the English variant, because en-GB is also day-first. *Evidence:* E12, E13. *Strength:* strong. *Scope:* English or bilingual deliverables; dashboards and reports shared across BR and US/UK readers.
- **XLAT-4** `[ref:translation]` Run translation as an ordered procedure and record it in the handoff note: (1) term register; (2) source number table; (3) translate section by section, preserving slide, table and bullet structure; (4) self-check against the register and number table; (5) a separate revision pass comparing source and target segment by segment (fresh context or sub-agent where available), tagging each finding with an MQM dimension and Minor, Major or Critical; (6) target-language read-through for the stated audience; (7) number, entity and layout checks; (8) re-run 5-7 on changed segments. Never describe step 5 as independent human revision. *Evidence:* E1, E2, E3, E4. *Strength:* moderate. *Scope:* executive PT<->EN materials of more than a few lines. Note: ISO 17100 excludes raw MT plus post-editing, so this is an adapted analogy, and a model revising its own output is weaker than a second human.
- **XLAT-5** `[ref:translation]` Before translating, write a term register listing each finance or KPI term, acronym, entity name, period label and unit convention with the chosen target term and its basis (client document, CPC/IFRS text, or "practitioner"). Freeze it for the document, use one target term per source term, and show practitioner or judgment-based entries to the user in the handoff note. *Evidence:* E1, E14, E15, E16, E17. *Strength:* practitioner-consensus. *Scope:* finance, KPI and reporting documents; any document longer than about one page.
- **XLAT-6** `[ref:translation]` Extract every numeral, percent, currency, unit, scale word, date, period label and sign convention from source and target into a table (S7). Normalise both sides to canonical values (R$ 2,3 mi = 2,300,000 BRL = BRL 2.3M), recompute every total, subtotal, percentage and percentage change in the target, and include numbers in charts, images, speaker notes, alt text and footnotes. Any mismatch, or any figure silently rounded, added or dropped, is Critical and blocks delivery. *Evidence:* E3, E7, E12, E13. *Strength:* moderate (the Critical classification is Claude policy; E7 is Chinese-English with small open-source models). *Scope:* every translated document containing numbers.
- **XLAT-7** `[ref:translation]` Resolve scale and unit before translating each figure: mil = thousand, mi/milhão = million, bi/bilhão = billion (10^9), tri/trilhão = trillion; English K, M, B, T. Treat table-level unit headers ("R$ mil", "Em milhões de R$", "US$ MM") as applying to every figure in that table and carry them into the translation. When a source uses a bare "M" or "MM", or has no unit header, infer from magnitude, state the reading and add a query. Distinguish percent from percentage points ("p.p.") and keep period labels equivalent (acumulado no ano = YTD; 1T26 = Q1 2026; exercício = fiscal year). *Evidence:* E7, E12, E13, EV1, EV3. *Strength:* moderate (CLDR fixes the word-to-power mapping; CPC 26 items 51-53 show statements declare scale and rounding in headings; the M/MM and 1T26 conventions are practitioner usage). *Scope:* any numeric content moving between Portuguese and English.
- **XLAT-8** `[ref:translation]` Treat R$ as BRL and $ or US$ as USD. Never convert currency unless asked. If asked, state the rate, its date and its source in the document and keep the original amount beside the converted one. In English text about Brazil where both currencies appear, write R$/BRL and US$/USD explicitly rather than a bare "$". *Evidence:* E12, E13, EV1. *Strength:* moderate (the conversion-disclosure policy is practitioner practice). *Scope:* any deliverable with more than one currency, or BRL amounts for non-Brazilian readers.
- **XLAT-9** `[ref:translation]` State the target variant once in the handoff note: pt-BR (never pt-PT unless requested) and en-US unless the user names en-GB or another variant. If the source is pt-PT or contains "bilião/biliões", "mil milhões", "Bi", or space-grouped numbers with the currency symbol after the number, do not carry it over: in pt-PT "bilião" is 10^12 and "mil milhões" is 10^9. Determine the magnitude from context, write the pt-BR or English word explicitly, and flag it in the queries. Never write "bilião" in pt-BR output. *Evidence:* E13, EV1. *Strength:* moderate (CLDR pt-PT and Microsoft's pt-PT guide disagree on "bilião", so the safe rule is to verify magnitude; RC-14). *Scope:* sources or reviewers that may use European Portuguese.
- **XLAT-10** `[ref:translation]` When converting a figure between locales, change separators, scale words, currency-symbol placement and date order in one operation and verify against the number table (pt-BR "1.234,56" -> en-US "1,234.56"; "R$ 2,3 mi" -> "R$2.3M" or "BRL 2.3 million"; "US$ 1.234,50" -> "$1,234.50"). En-US reference: comma thousands, point decimal, symbol first with no space, 12.5%, K/M/B/T, 12-hour time with am/pm (S9). *Evidence:* E12, E13. *Strength:* strong. *Scope:* any PT<->EN figure conversion.
- **XLAT-11** `[ref:translation]` Tag every review finding with an MQM dimension (Accuracy, Terminology, Linguistic conventions, Style, Locale conventions, Audience appropriateness, Design and markup) and a severity. Critical: any changed number, currency, unit or scale, date, period or sign; an omitted, added or softened caveat, risk or qualifier that changes a decision; wrapper text or a refusal in the deliverable. Major: a financial term that changes meaning, a false friend, a missing slide, bullet, row or footnote, clipped or overflowing text, a US-only reference left unexplained. Minor: fluency, grammar, style. Deliver only with zero open Critical findings and report the Major and Minor counts. Do not compute MQM penalty scores. *Evidence:* E2, E3, E4, E5. *Strength:* moderate (the dimensions and severity definitions are published; assigning wrong numbers to Critical is Claude policy, because MQM maps no error type to a severity). *Scope:* review of any translated executive document.
- **XLAT-12** `[ref:translation]` Before review, count slides or pages, headings, paragraphs, bullets, table rows and columns, footnotes and chart series in source and target, and resolve every difference unless an adaptation was requested. Do not merge, split, reorder, shorten or "improve" content inside a translation. *Evidence:* E2, E3, E5. *Strength:* moderate. *Scope:* faithful translations of decks, memos and reports.
- **XLAT-13** `[ref:translation]` The translated file contains only the translated deliverable: no preface ("Here is the translation"), no explanations, apologies, refusals, translator notes or markdown fences. Notes go in the handoff note. Before delivery, search the output for such phrases and for leftover source-language sentences other than approved untranslated terms. *Evidence:* E5. *Strength:* moderate (2024 behaviour under organiser prompts; prevalence not quantified). *Scope:* any file or slide text from a translation pass.
- **XLAT-14** `[ref:translation]` Never cite BLEU or COMET scores, an LLM-judge score, a self-rating or a back-translation as evidence of fidelity, in the deliverable or the handoff note. State the checks actually run and what was not checked. Back-translation is allowed only as a triage pass on headline claims and key figures, in a separate pass, and a clean back-translation does not clear a segment. *Evidence:* E6, E8, E9. *Strength:* moderate. *Scope:* all translation QA claims (RC-12).
- **XLAT-15** `[ref:translation]` End every translation with a handoff note of at most ten lines: variant and register, mode (faithful or adaptation), checks run, counts of Minor and Major findings fixed, open queries, and the five to ten highest-risk items for a human to spot-check (key figures, defined terms, caveats). Recommend bilingual human review when the document is for a board, regulator, auditor, contract, investor or external publication. *Evidence:* E1, E6, E8. *Strength:* practitioner-consensus. *Scope:* all translation deliverables.
- **XLAT-16** `[ref:translation]` Default to a faithful translation: same structure, nothing added, nothing dropped. Produce an executive adaptation (shorter, reordered, re-explained) only when asked or when the audience clearly differs; label it "Adaptation" in the header and list what was cut or reordered. Never present an adaptation as a translation and never shorten inside a "translate" request. *Evidence:* E18, E5. *Strength:* practitioner-consensus (the labeling rule is the skill's own design; glossaries blur the boundaries). *Scope:* translation requests where source and target audiences differ.
- **XLAT-17** `[ref:translation]` When the source is ambiguous or looks wrong (totals that do not foot, inconsistent units, an undefined acronym, "faturamento" without gross or net), translate what is written, choose the most defensible reading, and list the issue and the choice in a queries block. Never silently correct source numbers or terms. *Evidence:* E1, E5. *Strength:* practitioner-consensus (supported by ISO snippets rather than the normative text). *Scope:* all translations.
- **XLAT-18** `[ref:translation]` Keep Brazil-specific institutions, taxes, registries and legal forms in the original on first use with a short English gloss (ICMS, state tax on circulation of goods and services; PIS/COFINS, federal revenue-based contributions; CVM, securities regulator; CPC; Ltda.; S.A.; CNPJ). Do not translate brand, product or legal-entity names. When adapting English text for Brazilian readers, flag US-only programs, regulations and GAAP-only terms instead of translating them literally. *Evidence:* E2, E14, E15. *Strength:* practitioner-consensus (MQM lists audience appropriateness as a dimension; the gloss list is practitioner knowledge). *Scope:* PT->EN for non-Brazilian readers; EN->PT for Brazilian readers.
- **XLAT-19** `[ref:translation]` Translate "faturamento" by context, not by a fixed equivalent. Management and tax usage (faturamento bruto, faturamento do mês, meta de faturamento) becomes "gross revenue" or "gross sales"; keep "net revenue" for receita líquida and receita operacional líquida; use "invoicing" or "billing" only for the act or process of issuing invoices (ciclo de faturamento; faturar e manter = bill-and-hold) or for billings the source distinguishes from recognised receita. When unclear, write "gross revenue (faturamento)" on first use and add a query. Do not equate faturamento with IFRS "revenue" unless the source says it is net of deductions. *Evidence:* E14, EV2. *Strength:* moderate (the business-usage side rests on one law-firm article plus search results). *Scope:* PT->EN revenue lines in reports, decks and dashboards (RC-13).
- **XLAT-20** `[ref:translation]` Do not translate a bare "resultado" as "result". Decide from the line it labels: resultado do período or resultado líquido -> "profit or loss for the period" (statutory) or "net income" (management); resultado operacional -> "operating income" or "operating result"; resultado financeiro -> "net finance result". CPC 26 item 8 allows "lucro líquido" as a label for the period result, so check whether a figure is the statutory total before choosing. Use one English term per concept per document. *Evidence:* E15. *Strength:* moderate (the operating and finance mappings are standard usage; English terms not read from IFRS text). *Scope:* P&L and financial-statement lines (PC-11).
- **XLAT-21** `[ref:translation]` Use the seed glossary (S8) for PT->EN accounting terms. Portuguese terms come from CPC 47, 26 and 00; English equivalents are inferred from IFRS/IAS correspondence and must be checked before being quoted. Tag every term outside CPC/IFRS (orçado, realizado, previsto, ticket médio, inadimplência, positivação, sell-in/sell-out) as "practitioner" in the register and surface it to the user. *Evidence:* E14, E15, E16. *Strength:* moderate. *Scope:* accounting and financial-reporting vocabulary.
- **XLAT-22** `[ref:translation]` For EN->PT in fixed layouts (slides, KPI tiles, table headers, axis labels, buttons), allow at least 30% extra width on short labels, enable wrapping or auto-fit, and render the result to check every container for clipping, overlap and misalignment; clipped or overlapping text is a Major finding. For PT->EN, re-check labels where abbreviations or acronyms expand. *Evidence:* E10, E11. *Strength:* weak (the Portuguese figures range 13%-30% and none is a primary measurement; the render test is more reliable than any percentage). *Scope:* fixed-size layouts translated from English into Portuguese (PC-10).
- **XLAT-23** `[ref:translation]` Bind currency symbols and units to their numbers with non-breaking spaces (U+00A0): "R$ 1.234,56", "2,3 mi", "12 p.p.", "US$ 4 mi", so a figure never splits across lines. Put no space before %. *Evidence:* EV4, E12. *Strength:* moderate (Microsoft's pt-BR guide and CLDR; percent spacing in Brazilian formal norms is unverified). *Scope:* Portuguese text in decks, reports and dashboards.
- **XLAT-24** `[ref:translation]` Translate meaning, not words: keep action titles and headlines as conclusions (verb + number + implication) in natural target phrasing and avoid calques. Scan for false friends: atual/atualmente = current/currently, not actual; eventualmente = possibly, not eventually; realizar = carry out, not realize; pretender = intend, not pretend; "aplicação" in finance = investment. Choose one address form and one register per document and keep it. *Evidence:* E2, EV4. *Strength:* practitioner-consensus (MQM lists false friends under Mistranslation; the list and the single-register rule are practitioner knowledge). *Scope:* all translated prose, especially titles and summaries.

### 3.8 Quality assurance

- **QA-1** `[core]` Before delivering any executive deliverable, run the pre-delivery gate (S12): answer and ask on the first screen; headings read as the argument; every number sourced, dated and reconciled; no unopened citation, invented cause or invented input; risks in the body; no colour-only meaning and contrast passed; bars at zero; units, period and scope stated; the user told what was changed, removed or left unverified. *Evidence:* A1, C6, CV3, D15, D16, D18, B2, B13, CV1, E3. *Strength:* practitioner-consensus (a roll-up of other rules; adds no new evidence). *Scope:* universal.
- **QA-2** `[ref:qa-checklists]` Before delivering or improving any chart, run this audit and fix or flag each failure: (1) bar axis starts at zero; (2) no dual y-axis without justification; (3) no 3D, angle-only or area-coded primary quantity; (4) title states the finding with a number and comparison base in neutral wording; (5) the highlighted element is the one the title names; (6) no meaning by colour alone; (7) marks at least 3:1 and text at least 4.5:1 contrast; (8) uncertainty labeled with what it represents; (9) unit, period, source and as-of date present; (10) consistent encodings across the document. *Evidence:* B2, B3, B4, B5, B8, B9, B12, B13, BV3. *Strength:* moderate (a roll-up; adds no new evidence). *Scope:* reviewing or improving existing materials.
- **QA-3** `[ref:qa-checklists]` Check every grouping (issue-tree branches, slide categories, driver lists) before finalising: items are the same kind, overlaps are intentional, nothing important for the question is missing, and every item is relevant to the question. Allow overlapping groups where real redundancy exists and say so. Do not print "MECE" on slides or sections. *Evidence:* A12, A13. *Strength:* practitioner-consensus (the critiques are conceptual: MECE tests distinctness and coverage, not relevance). *Scope:* any structured analysis.
- **QA-4** `[ref:qa-checklists]` Before sending a consequential recommendation, run a silent weakest-link check on six elements: right problem and frame, objectives or criteria, alternatives, information and uncertainty, reasoning, and commitment to a next step with an owner. Fix the weakest element first (for example restate the question in the opening lines, or add an owner and date). Do not print the checklist. For high-stakes items advise the user that an independent reviewer should apply the HBR-style challenge questions, because the authors hold that people cannot reliably see their own biases and Claude's self-check is a minimum, not a substitute. *Evidence:* A10, A1. *Strength:* practitioner-consensus (interview-level; the compromise has no tested support, RC-11). *Scope:* consequential recommendations.
- **QA-5** `[ref:qa-checklists]` When justifying chart choices in a deliverable or speaker script, cite only what the evidence supports. Do not write: "pie charts are always bad", "angle is the least accurate way to read charts", "donuts are better than pies", "dual axes are banned", "decluttering improves comprehension", "embellishment hurts accuracy", "8% of all men are colourblind". Label thresholds such as three pie slices, four overlaid series and twelve labeled bars as heuristics. *Evidence:* B1, B4, B5, B6, B10, B14. *Strength:* strong. *Scope:* any rationale, note or script that cites research on charts.
- **QA-6** `[ref:qa-checklists]` Before releasing an AI-drafted summary of source documents, trace each summary sentence to a source passage, checking the final third first, and delete or flag sentences without support. Do not quote a hallucination percentage for summaries. *Evidence:* D17. *Strength:* weak (the position effect and absent-topic summaries are usable; the "75%" headline is not). *Scope:* summaries of multiple or long source documents.
- **QA-7** `[ref:qa-checklists]` For client-facing, board or regulatory deliverables, end the draft with a pre-release checklist: figures reconciled to source, citations resolved, a named human reviewer for figures and citations, and a question to the user whether the client, contract or employer requires disclosure of AI use. Do not decide disclosure on the user's behalf. *Evidence:* D18, D15, D16. *Strength:* moderate (the Deloitte case supports verifying before release; it does not establish disclosure as best practice, so disclosure is raised as a question). *Scope:* client-facing, board and regulated deliverables.
- **QA-8** `[ref:qa-checklists]` In the final read-through ask four questions based on ISO 24495-1: Is every element relevant to this reader's decision? Can the reader find the answer and each argument quickly? Is it understandable on first read? Can the reader act on it, with owner and date? *Evidence:* C15. *Strength:* practitioner-consensus (standard text unread; secondary sources agree on the four principles; make no compliance claim). *Scope:* any final review of an executive deliverable.

---

## 4. Contradictions

### 4.1 Resolved (with the resolution and why)

- **RC-1 Neutral titles versus claim or action titles** [B8, B10, A13, C7, AV4]. B8: title slant shapes the message viewers take, and viewers assume charts are neutral. B10 and the practitioner sources want a headline that states the pattern. *Resolution:* write titles as quantified factual claims (metric, direction, magnitude, comparison base) with no evaluative adjectives (VIZ-7, CORE-11). *Why:* a quantified factual headline supplies the "focus" headline of B10 while removing the slant that B8 manipulated. Residual: some B10 participants said focused graphs "seemed to have an agenda" (PC-4).
- **RC-2 Hypothesis-first versus the single-hypothesis trap** [A2, A7; A14 unverified]. *Resolution:* state the lead answer early and pair it with an explicit disconfirmation step (RES-1). *Why:* A2 warns that people generate one hypothesis and look only for support; A7 shows breadth and speed are compatible. Hypothesis-first as a default practice rests on A14, which neither researcher nor validator could read, and no study tests the pairing.
- **RC-3 Cut versus add structure** [C1, C2]. *Resolution:* every added element must earn its place; a navigation paragraph only beyond about one page (CORE-3, WRIT-5). *Why:* the authors concede there is no right amount to cut; structure serves navigation, not extra content.
- **RC-4 Sentence headlines versus live delivery** [AV4, C7, C8]. *Resolution:* scope by deck mode: claim titles for read-ahead decks and memos; in presenter-led talks keep them to about two lines or let the speaker state the claim (CORE-11, STORY-1). *Why:* the supporting studies are developer-run with deliberately weak controls and ignore the speaker's role, but the critic still sees a good case for sentence titles, and the measured gains are modest.
- **RC-5 Zero baseline for bars versus range bias in both directions** [B2, B3, BV1]. *Resolution:* bars stay at zero; small deltas get an explicit number or a dot or line chart with a labeled range; lines may be non-zero when change is the message, with range printed and delta quoted (VIZ-1, VIZ-2). *Why:* B2's authors resist a blanket zero rule and BV1 (n 9-20 per experiment) shows full-range axes make effects look small; the zero rule for bars rests on the length-encoding logic plus convention, so the fix is a different encoding, not a truncated bar.
- **RC-6 Dual axes** [B4, BV4]. *Resolution:* default to no dual axes, with named exceptions (VIZ-6). *Why:* the empirical base cited for a ban (Isenberg et al. 2011) tested focus-plus-context charts, not two-measure dual axes, and Datawrapper reversed its product position in July 2026 while keeping its concern for general audiences. The rule is practitioner opinion, not a finding.
- **RC-7 Mechanism of pie reading** [B1, B5, B17]. *Resolution:* keep the practical conclusion (label values, prefer bars) and assert no mechanism (VIZ-3, VIZ-5, QA-5). *Why:* Heer & Bostock did not find angle worse than length; Skau & Kosara find angle the least important cue and report that readers use arc length.
- **RC-8 Can "Agree" veto in RAPID?** [A11, AV2]. *Resolution:* use plain role labels and state each sign-off party's blocking power and escalation path in the document (RES-5). *Why:* Bain's 2006 article describes a limited veto with a duty to offer an alternative or escalate; Bain's 2026 article says no veto and escalation to the decider; third-party summaries differ again.
- **RC-9 One screen versus multiple pages** [DV3, D2, D3, D1]. *Resolution:* by genre: a monitoring view fits one screen; analytical or narrative formats are acceptable if page one stands alone (DASH-1). *Why:* Few's definition is single-screen monitoring; Bach et al. and Sarikaya et al. treat multi-page as a legitimate pattern; the single-screen rule is contested on mobile and wall displays. No empirical test exists.
- **RC-10 Where the recommendation sits relative to the summary** [D13, D14, A13, C16]. *Resolution:* board papers in the AICD style carry a four-to-five-line summary of purpose and ask, with the recommendation in its own section; every other senior-reader document opens with the answer and the ask (CORE-1, DASH-12). *Why:* they are different document types and no evidence compares the two layouts.
- **RC-11 Self-review versus independent review** [A1, A10]. *Resolution:* run the silent weakest-link check and advise independent review for high-stakes items (QA-4). *Why:* the HBR authors say people cannot see their own biases and Claude can only self-check; the compromise has no tested support.
- **RC-12 Automatic or LLM judges versus a human final judge** [E6, E8, E9]. *Resolution:* scores, LLM judges and back-translation are triage only; a human signs off; Claude states what was not checked (XLAT-14, XLAT-15). *Why:* the WMT24 metric leader was not the human-ranking leader; GEMBA-MQM is a black-box method validated for system ranking; E9 validates model-level rankings and itself warns that a correct round trip does not imply a correct intermediate translation.
- **RC-13 "Faturamento"** [E14, EV2]. *Resolution:* translate by context; management and tax usage means gross revenue or gross sales; "invoicing" only for the act of issuing invoices; the real trap is gross versus net (XLAT-19). *Why:* CPC 47 uses the word for the invoicing event in its bill-and-hold text, but Brazilian tax law and business usage equate faturamento with receita bruta (EV2). The dossier's fixed "invoicing, never revenue" reading was contradicted by EV2 and is not used.
- **RC-14 pt-PT versus pt-BR scale words** [E13, EV1]. *Resolution:* target pt-BR; verify the magnitude whenever a source or reviewer may be European Portuguese; never write "bilião" in pt-BR (XLAT-9). *Why:* CLDR pt-PT gives bilião = 10^12 and mil milhões = 10^9, while Microsoft's pt-PT guide renders 16,000,000,000 as "16 biliões"; pt-BR bilhão is 10^9.
- **RC-15 IBCS green/red variance versus colour-alone rule** [B13, B15]. *Resolution:* keep favourability marking but add a sign or word (VIZ-19, VIZ-12). *Why:* WCAG 1.4.1 requires another cue; the IBCS primary text was not read for its colour-vision handling.
- **RC-16 Fixed count of supporting arguments** [C17, A12, A13]. *Resolution:* keep the logical-grouping constraint (same kind, stated order, no overlap or gap) and drop any numeric limit (WRIT-3). *Why:* nothing read supports "2-3 arguments"; the stated constraint is logical grouping, and the MECE critique adds that relevance is a separate test.
- **RC-17 Memo length** [C4, C5]. *Resolution:* cite the six-page narrative memos documented in the 2017 letter and do not cite a four-page figure (STORY-8). *Why:* the 2004 email was not read.
- **RC-18 Process transparency versus fabrication risk** [A1, A2, D18]. *Resolution:* replace the dossier's "how this was produced" note with a Basis note limited to facts the user supplied (CORE-8). *Why:* the HBR argument is that process should be reviewed, but a model-written process narrative can invent the consultation and dissent a reviewer would rely on.
- **RC-19 Answer-first versus readers who need background** [C16, C17, CV4]. *Resolution:* answer first; add at most three situation sentences when the reader lacks context or the answer is surprising (WRIT-4). *Why:* CV4 supports claim-before-reason at argument level; nothing tests readers who need background.
- **RC-20 Decluttering alone versus decluttering plus focus** [B10]. *Resolution:* decluttering raises perceived professionalism; adding focus (highlight colour, pattern-describing headline, annotation) raises memory and clarity (VIZ-9, QA-5). *Why:* the validator read the full paper (24 undergraduates, 10-second views); the looser Kellogg description is superseded.
- **RC-21 Bullets: Tufte versus Farkas** [C6, C8, CV3]. *Resolution:* keep bullets for short parallel items; put reasoning, conditions and risk in sentences (STORY-5). *Why:* the CAIB evidence concerns buried risk and six-level hierarchy; Farkas finds brief well-phrased bullets harmless.
- **RC-22 Colour-vision-deficiency prevalence** [B14]. *Resolution:* state a range by ancestry, not a single figure (VIZ-12). *Why:* Wilke gives about 8% of males and 0.5% of females; the validator's check of Birch (2012) gives about 8% of European-ancestry men and 0.4% of women, and 4-6.5% of Chinese and Japanese men.

### 4.2 Preserved (guidance for case-by-case handling)

- **PC-1 Breadth versus focus** [A7, A8, A16]. Eisenhardt and Nutt favour more alternatives and wider search; the 80/20 heuristic and "stop when more analysis would not change the decision" favour focus; no evidence says where to stop. *Guidance:* offer breadth of options (two or three on the same criteria, CORE-4) and depth only where the decision is sensitive; say which analysis was not done; when the user is short of time, use the short form (CORE-2).
- **PC-2 Embellishment versus declutter** [B6, B7, B10]. Bateman (n=20) found no accuracy cost and better recall after two to three weeks; Ajani found declutter helps professionalism ratings only; prior declutter literature "has not converged". *Guidance:* take no stance on whether imagery helps; keep imagery out of the analytical exhibit and never let it replace labels or axes; if the user asks for a decorative style, comply while holding CORE-5, VIZ-12 and VIZ-13, and do not argue from the research in either direction.
- **PC-3 Overlay versus small multiples** [B16]. Task- and span-dependent; no series-count threshold exists. *Guidance:* use the four-series figure only as a labeled heuristic; if the intended comparison is not findable at a glance in the first layout, switch layout.
- **PC-4 Neutral titles versus "seems to have an agenda"** [B8, B10]. *Guidance:* keep exhibit titles factual; put the recommendation in the slide's own claim line or the recommendation section rather than in evaluative chart titles; when the user wants a more persuasive headline, comply but keep the number and the comparison base.
- **PC-5 Size of the process effect** [A5, AV1]. Process explains 53% of variance versus 8% for analysis, but the ROI gap is 6.9 pp for process versus 5.3 pp for analysis, all self-reported. *Guidance:* do not quote; if asked, give both with the limitation.
- **PC-6 Alert-fatigue transfer to KPI flags** [D8]. Healthcare data; no executive-dashboard test; no evidenced cap. *Guidance:* treat as a design heuristic; state the cap chosen and why; ask the user how many flags the reader can act on.
- **PC-7 Amazon WBR deck order** [D7]. The source's body and its own correction disagree. *Guidance:* never state a deck order as Amazon's; the user's own cadence governs.
- **PC-8 Board-pack length** [D12, D14]. A 226-page mean, a median near 200 and 40% under 100 pages cannot be reconciled. *Guidance:* give no page targets; prune by purpose and by which pages the decision needs (DASH-14).
- **PC-9 Citation fabrication across model generations** [D15, D16]. 18% (GPT-4, 2023) and 19.9% (GPT-4o, 2025) are not comparable; topic familiarity moved one model from about 6% to 29%. *Guidance:* make no claim that newer models are safer or no safer; apply CORE-7 uniformly and raise the risk for niche topics (RES-10).
- **PC-10 Portuguese text expansion** [E10, E11]. 13%, 15-25%, 20-30% and about 30% are all secondary. *Guidance:* start from 30% headroom for short labels, then render and measure on the user's real labels (XLAT-22).
- **PC-11 "Resultado" versus "lucro líquido"** [E15]. CPC 26 item 8 allows the second as a label for the first. *Guidance:* decide at line level; ask or add a query when a statutory total and a management measure could be confused (XLAT-20).
- **PC-12 On-screen text divergence** [C9]. Verbatim duplication hurts and some divergence helps, but the optimum is unknown. *Guidance:* avoid copying the script or memo onto slides; the mode choice in STORY-1 sidesteps the question.
- **PC-13 Summary boxes** [C12]. The pilot showed attention without a reading-time or helpfulness gain, and its authors also concluded it helped judge the methods quickly. *Guidance:* claim neither benefit nor harm; open with a prose answer (CORE-1); use a box only when a template requires it or the user asks, never in place of the prose.
- **PC-14 Size of the signaling effect** [C10]. d = .38, r = 0.17 and "among the largest" are unreconciled. *Guidance:* use signaling (clear headings, highlights) as a design idea only; quote no number.
- **PC-15 Tool versus thinking in poor slides** [C6]. *Guidance:* take the narrow position that placement, hierarchy and vague wording can hide risk; do not assert that slide software is inherently defective.
- **PC-16 Whether back-translation detects numeric or omission errors** [E9]. *Guidance:* triage only, in a separate pass, never clearing a segment (XLAT-14).
- **PC-17 Deloitte refund amounts and disclosure norms** [D18]. *Guidance:* do not cite amounts; use the case only for the verify-before-release lesson; ask the user about disclosure (QA-7).
- **PC-18 ISO 17100 revision status** [E1]. *Guidance:* do not cite the standard as current or as a compliance basis; use it as a structural model only.

---

## 5. Placement map

### 5.1 Principles for placement

- SKILL.md carries only what applies to most deliverables, in one or two lines per rule, plus a routing table. Long wording, tests, thresholds and examples live in reference files loaded on demand.
- A rule that is `[core]` here keeps its full wording in section 3; SKILL.md carries the short form and, where a reference file exists for the domain, a pointer to it.
- Optional modules load only when the user asks for the artifact type or the context says it is in use (board paper, IBCS, scenarios, narrative memo, KPI guardrails).
- Evidence strength and scope travel with each rule into the reference files; SKILL.md omits ids but keeps the "unverified" flags.
- Rule tags map to files as follows: `ref:writing` = `references/writing.md`; `ref:presentations` = `references/presentations.md`; `ref:dataviz` = `references/dataviz.md`; `ref:dashboards` = `references/dashboards-kpis.md`; `ref:research-evidence` = `references/research-evidence.md`; `ref:translation` = `references/translation-pt-en.md`; `ref:qa-checklists` = `references/qa-checklists.md`; `opt:<name>` = `references/modules/<name>.md`.
- If SKILL.md must shrink further, demote in this order: WRIT-2 to ref:writing, CORE-13 to ref:qa-checklists, XLAT-2 to ref:translation (leaving the XLAT-1 pointer), CORE-12 to a one-line routing hint.

### 5.2 SKILL.md contents (proposed)

1. Purpose in two lines (do not waste the decision-maker's time; do not waste the user's time).
2. The 15 principles (P1-P15) as one line each, without ids or strengths.
3. The 19 core rules (below), short forms.
4. Routing table (below).
5. Build-note and handoff convention: after producing a deliverable, tell the user in a few lines the mode chosen, the stakes classification, what was cut or changed (CORE-13), what is unverified (CORE-8) and, for translation, the queries (XLAT-15).
6. Composition notes (5.6).

**Core rules (19):** CORE-1 to CORE-13, WRIT-2, VIZ-1, VIZ-12, XLAT-1, XLAT-2, QA-1.

**Routing table**

| Task | Load |
|---|---|
| Board deck or presentation | ref:presentations, ref:dataviz, ref:writing; opt:board-paper for a board paper; opt:narrative-memo for a complex decision memo |
| Director dashboard or HTML dashboard screen | ref:dashboards, ref:dataviz; opt:ibcs-notation if IBCS is used; opt:kpi-guardrails for incentive-linked KPIs |
| Management or business review | ref:dashboards, ref:writing (variance commentary), ref:research-evidence |
| Strategic memo or executive summary | ref:writing, ref:research-evidence; opt:scenarios if uncertainty dominates |
| Research-driven recommendation | ref:research-evidence, ref:writing, ref:qa-checklists |
| PT<->EN translation or adaptation | ref:translation, ref:qa-checklists; ref:dataviz if charts are involved |
| Improve an existing deliverable | ref:qa-checklists plus the reference for the artifact type |
| Any chart | ref:dataviz |

### 5.3 Reference files (proposed names)

| File | Purpose | Rules | Count |
|---|---|---|---|
| `references/writing.md` | Sentence- and document-level writing, variance commentary | WRIT-1, WRIT-3 to WRIT-10 | 9 |
| `references/presentations.md` | Deck mode, storyline, slide text, appendix discipline | STORY-1 to STORY-7 | 7 |
| `references/dataviz.md` | Chart selection, axes, titles, colour and contrast, uncertainty | VIZ-2 to VIZ-11, VIZ-13 to VIZ-18 | 16 |
| `references/dashboards-kpis.md` | Dashboard genre and first view, KPI cards, status rules, flags, variance display | DASH-1 to DASH-9 | 9 |
| `references/research-evidence.md` | Recommendation quality (alternatives support, forecasts, downside, premortem, roles), citation standards, true-strength quoting | RES-1 to RES-7, RES-9 to RES-11 | 10 |
| `references/translation-pt-en.md` | PT<->EN procedure, numbers, locale, glossary use, layout, review and handoff | XLAT-3 to XLAT-24 | 22 |
| `references/qa-checklists.md` | Chart audit, grouping check, weakest-link check, claims watchlist, summary tracing, pre-release checklist | QA-2 to QA-8 | 7 |

### 5.4 Optional modules

| File | Loaded when | Rules | Count |
|---|---|---|---|
| `references/modules/board-paper.md` | A board or committee paper is requested | DASH-11 to DASH-14 | 4 |
| `references/modules/ibcs-notation.md` | The user or company uses IBCS or asks for it | VIZ-19 | 1 |
| `references/modules/scenarios.md` | One or two external uncertainties dominate the decision | RES-8 | 1 |
| `references/modules/narrative-memo.md` | A complex multi-factor decision merits a narrative memo | STORY-8 | 1 |
| `references/modules/kpi-guardrails.md` | KPIs are tied to incentives or team targets | DASH-10 | 1 |

Core: 19 rules. Reference files: 80 rules. Optional modules: 8 rules. Total: 107 rules.

### 5.5 Seed assets (proposed files)

| Asset | File |
|---|---|
| S1 Chart-selection table | `assets/chart-selection-table.md` |
| S2 KPI-card spec | `assets/kpi-card-spec.md` |
| S3 Status-rule template | `assets/status-rule-template.md` |
| S4 Board-paper cover sheet | `assets/board-paper-cover-sheet.md` |
| S5 Decision statement and recommendation skeleton | `assets/decision-and-recommendation-templates.md` |
| S6 Variance-commentary template | `assets/variance-commentary-template.md` |
| S7 Number-fidelity table | `assets/number-fidelity-table.md` |
| S8 PT->EN business glossary | `assets/glossary-pt-en.md` |
| S9 Locale format cheat sheet | `assets/locale-format-cheatsheet.md` |
| S10 Overclaim watchlist | `assets/overclaim-watchlist.md` |
| S11 Okabe-Ito palette with contrast | `assets/okabe-ito-contrast.md` |
| S12 Pre-delivery gate | `assets/pre-delivery-gate.md` |
| S13 Translation QA checklist | `assets/translation-qa-checklist.md` |

### 5.6 Composition with other skills (design guidance, not derived from the inputs)

- **pptx:** this skill decides storyline, titles, mode, numbers and what to cut; the pptx skill handles file mechanics. Hand it claim titles, speaker-note text (presented mode), the contrast and colour-alone rules, and ask for a render so XLAT-22 and VIZ-13 can be checked.
- **frontend:** for HTML dashboards hand over the KPI-card fields (S2), the written status rules (S3), the first-view rule (DASH-1) and locale formatting through `Intl.NumberFormat` (XLAT-2).
- **data-analysis and xlsx:** CORE-6 requires computation by tool; this skill requires the result to be reconciled and tagged reported, calculated or assumed (CORE-5) before it enters a deliverable.
- **Any skill that produces a file:** the pre-delivery gate (QA-1) runs on the output, not on the plan.

---

## 6. Exclusions

Concepts deliberately left out of the skill, with the reason. Items in 6.1 are claims the validators found contradicted, unsupported, outdated or corrected; they are carried here only so nobody reintroduces them.

### 6.1 Claims rejected or corrected as stated

- **"Faturamento" always means invoicing and is never revenue** (the dossier's glossary rule, E14). Contradicted by EV2: Brazilian tax and business usage equate faturamento with receita bruta. Replaced by XLAT-19.
- **The dossier's reading of "bi" versus "bilhão" as a trillion trap** (E12 interpretation). Muddled; superseded by EV1 (the trap is European Portuguese "bilião" = 10^12 and the mil/mi/M confusion).
- **"Length next, then angle and area" as the Heer & Bostock ranking** (B1). The paper says angle was not shown worse than length. Only position best, area worse than position and angle is retained.
- **The empirical basis for a dual-axis ban** (B4). The cited study tested focus-plus-context charts, and the vendor reversed its product stance (BV4). Kept only as a conservative default (VIZ-6).
- **"The paper reports added error for exploded, varying-radius, icon and nested pies"** (B5 rationale). The paper reasons about them and does not test them.
- **The middle of the Munzner channel ranking** (B17, B1). The ranking figure is an image and was not text-verified.
- **Klein's 30% figure** (A6). Second-hand; the original abstract reports little influence of temporal perspective.
- **The A1 interpretation that the HBR checklist works as author self-review.** Runs against the article's premise that review must be independent of the proposers.
- **Treating Bain 2026 as the sole RAPID definition** (A11). Bain's own 2006 article says Agree can carry a limited veto (AV2).
- **A fixed "2-3 supporting arguments" or rule of three** (C17). Not supported by anything read.
- **"Coherence and verbal redundancy have robust but not top-tier support"** (C10). Not in the abstract the validator saw.
- **15 versus 20 words per minute of on-slide text, 28 pt headlines, 18-24 pt body** (C stream, `C-disagreement-wpm`). Source inaccessible; values conflict.
- **Westinghouse reading shares, "page ten has a 90% chance of going unseen", "8x faster innovation"** (C and D streams). Second-hand, undated, no primary source.
- **"84% of directors want more focused packs"** (D14). Not on the fetched page.
- **"Up to 75% of LLM summaries is hallucinated"** (D17). A peak on one benchmark under a non-standard definition.
- **"Bullet graphs improve accuracy or comprehension" and any pie-chart ban attributed to the dashboard stream** (D4, D5). One abstract-level study of time to first fixation; pies are not covered.
- **The Deloitte refund figures** (D18). Conflicting and unverified.
- **Kaplan and Norton's 1992 perspective names as "learning and growth"** (D6). The 1992 article used "innovation and learning"; the later label is anachronistic.
- **Written RAG definitions, automatic reds and recovery plans as findings of the D9 article** (D9). Not in the article; retained only as a practitioner convention (DASH-4).
- **Statistics seen only in search snippets:** Lo et al. 2022 (28.6% axis choice), Pandey et al. percentages, Eells 1926 self-reports (B stream, B3, B4, B5).
- **Expansion buckets and Portuguese percentages as hard numbers** (E10, E11). Old, generic, inconsistent.
- **E7's error rates as a Portuguese or frontier-model result.** The evidence is Chinese-English with small open-source models.

### 6.2 Concepts excluded by design

**Strategy and decisions (A)**
- Printing the 12 HBR questions or Spetzler's six elements inside deliverables: review aids, not reader content (A1, A10). Kept as silent checks (QA-4).
- Quoting the McKinsey seven-point ROI figure, "process 6x analysis", Klein's 30%, Schoemaker's 50% or Nutt's "half fail" as headline evidence (A5, AV1, A6, A15, A8). Allowed only under RES-11.
- Mandatory or visible MECE, including printing the label on slides or sections (A12). Kept as an internal check (QA-3).
- RAPID letters or RAPID as a required structure (A11, AV2).
- "80/20" as a law or default split (A16).
- Scenario planning as a default step or the ten-step process (A15). Optional module only.
- A full "how this was produced" narrative (A1). Replaced by the Basis note.
- Premortem or full alternatives treatment for routine decisions (A4).
- Eisenhardt-style "use more information" as a general rule (A7): abstract-level, eight firms, information type unstated.
- Dean & Sharfman (1996) as supporting evidence (A9).
- Pyramid-principle jargon (governing thought, SCQ) and ghost-deck or storyline-first as named methods in output (A13, C17). The practice is retained without the vocabulary.
- Issue-tree depth limits or fixed branch counts (no evidence).

**Data visualization (B)**
- Munzner's expressiveness/effectiveness vocabulary and the full channel taxonomy (B17).
- Full IBCS SUCCESS framework, hatching and notation as a default (B15). Optional module only.
- Gradient and violin plots for executive uncertainty displays (B12).
- Memorability-driven choice of unusual chart types (B7).
- Embellishment or imagery as a recall aid (B6): n=20, one designer's style, authors cautious.
- Witt's SD-based axis range as a business rule (BV1).
- Donut hole size and donut-versus-pie debates (B5).
- Claims that decluttering improves trustworthiness or comprehension (B10).
- A blanket "8% of men are colourblind" (B14).
- Heer & Bostock Experiments 2 and 3 (B1): not read.

**Storytelling and writing (C)**
- Quoting effect sizes (49 versus 127 words, 4.8% versus 2.7%; g values; 124% usability) in deliverables (C1, C11, CV2).
- A rule against highlighted summary boxes (C12): the pilot tested a methods-section box on students.
- Tufte-style absolutism: ban slides or bullets (C6).
- Mandatory visual evidence on every slide or a mandatory assertion-evidence template (C7, C8).
- Claiming memos or BLUF improve decision quality (C4, C16).
- The 2004 Bezos email wording, "banned PowerPoint" anecdote, four-page versus 20-page comparison (C5).
- The full Mayer/Noetel principle list (segmenting, pre-training, modality) (C10): per-principle effects not accessed.
- ISO 24495-1 as a compliance or certification claim (C15).
- Oppenheimer-style "simple words raise perceived intelligence" as a rule: read via press release only.

**Dashboards and board materials (D)**
- The Balanced Scorecard four-perspective frame as a required structure (D6).
- Copying Amazon WBR scale or mechanics: 400-500 metrics, 60-90 minute meeting, the 6-12 graph as mandated layout, deck order (D7).
- Page-count and reading-speed targets for board packs: 30 pages per hour, 226-page average, 120 pages in four hours (D12, D14).
- Mandatory use of Bach et al.'s pattern names or genre names as output vocabulary (D1, D2).
- Goodhart taxonomy labels and "watermelon reporting" as terms in executive documents (D9, D10).
- Numeric RAG tolerances (for example plus or minus 5%) and fixed caps on KPIs or flags (D9, D8): no source provides them.
- Emotive and other colour patterns from the catalogue (D2).
- Nature 2026 hallucinated-citation percentages, ICAEW AI-error guidance, Kumar et al. 2021: not read.

**Translation and localization (E)**
- Full MQM numeric scoring: multipliers, weights, per-1,000-word normalisation (E3).
- WMT24 Error Span Annotation protocol and 0-100 scores (E4).
- BLEU, COMET, chrF and GEMBA-style scoring pipelines as sign-off (E6, E8).
- Round-trip translation as a score and LMArena correlations (E9).
- ISO 17100 certification, translator qualification and project-management requirements; quoting ISO in deliverables (E1).
- Transcreation as a separate service tier (E18).
- MQM Neutral severity and the Untranslated subtype (E2, E3).
- Exhaustive pt-BR versus pt-PT vocabulary lists and the "passivo corrente is European" claim (E15 disagreement).
- Microsoft "voice" guidance (informal tone) (EV4): product UI voice, not executive register.
- The IFRS Integrated Reporting Framework translation as a glossary source (E17).
- WMT24 system rankings (E5).
- Practitioner jargon (positivação, ticket médio, giro de estoque, sell-in/sell-out) as rules rather than tagged glossary entries.
- Metric/imperial and fiscal-calendar conversions: no evidence and rarely relevant.

---

## 7. Needs verification

Claude must not present any item below as established. When one is relevant, write "unverified" and give the basis, or omit it. Items without a finding id come from the validators' own needs-verification lists and are marked "(validator list)".

### 7.1 Cross-stream gaps

- No document-level experiment compares answer-first with chronological order for decision-makers; the nearest evidence is sentence- and argument-level (C13, CV4, C16).
- No evidence on director-level reading behaviour, executive comprehension of claim headlines or decision-ask wording, or whether executive summaries improve decisions (A13, AV4, C12).
- No evidence on Brazilian corporate norms for answer-first, claim titles or the other presentation structures (C stream, validator list).
- No outcome evidence that the 12-question checklist, premortems, MECE, issue trees or driver trees improve decisions (A1, A6, A12).
- No 2020-2026 dashboard comprehension study was filled in; the Hjelle et al. (2024, Information & Management, reported 524 participants) experiment is the best candidate and its abstract could not be read (validator list, stream D).

### 7.2 Stream A

- Dean & Sharfman (1996) effect direction and size (A9). Mitchell, Russo & Pennington (1989): what produced the 30% figure (A6). Veinott, Klein & Wiggins (2010) premortem experiment (validator list).
- Alley et al. (2006) primary paper: sample, controls and whether the headline change was confounded (AV4, C8).
- McKinsey "bulletproof problem solving" page and hence hypothesis-first as default practice (A14, HTTP 503 twice). Minto's own materials (A13, C17).
- Eisenhardt (1989) full text: meaning of "more information" and whether alternatives run in parallel (A7). Nutt sampling (a secondary source says decisions were chosen by the organisations) (A8).
- Whether Bain's 2026 no-veto wording is a deliberate change from 2006 (A11, AV2).
- Whether outside-view uplifts hold for corporate, non-infrastructure forecasts; Lovallo, Clarke & Camerer (2012) is a candidate (AV3).
- van Gelder (2010) and Chevallier (2016) at source (A12). Spetzler, Winter & Meyer (2016) wording (A10).

### 7.3 Stream B

- Cleveland & McGill (1984) original ranking, especially angle versus length (B1, B17). Pandey et al. (CHI 2015) primary results (B3). Franconeri et al. (2021) full text (B11).
- IBCS 2.0 and ISO 24896 primary text: scenario encodings, zero-baseline rule, variance colour rules, accessibility handling (B15).
- No evidence gathered for stacked bars, sorting, legends versus direct labels, tables versus charts, distributions, scatter plots, sequential and diverging palettes, small-multiples thresholds, or charts per slide (validator list). Any default in these areas must be marked unverified.
- All numeric thresholds (two to three pie slices, about four overlaid series, about twelve labeled bars, eight colours) are heuristics; only the eight-colour limit has a practitioner source (B5, B14, B16).
- Kale et al. (2020) effect sizes and whether a point estimate beside a range helps or harms business forecasts (BV2). Borkin et al. full paper (B7). Ajani supplementary statistics (B10). Isenberg et al. (2011) venue (B4).
- Whether WCAG thresholds should be applied to projected slides and printed greyscale (B13, BV3).
- Brazilian colour-vision-deficiency prevalence (B14).

### 7.4 Stream C

- Rogers & Lasky-Fink primary experiments, including the 49-versus-127-word sample split and statistics and the emphasis experiments (C1, C2).
- Nature SI mapping of the 83% figure (C3, CV1).
- Garner & Alley (2013) statistics and the p below .01 claim, which appears only on the developers' site (C7).
- Noetel et al. per-principle effect sizes (C10); Sundararajan & Adesope study count, student count and moderators (C11); signaling magnitudes (C10).
- ISO 24495-1 text and scope (C15); AR 25-50 current text and what the 2024 administrative revision changed (C16).
- Britt & Larson (2003) full text; Kieras 1978/1980 (CV4).
- The 2004 Bezos email and the Working Backwards book (C5).
- Whether the concise and scannable gains in CV2 transfer beyond a 1997 web task.

### 7.5 Stream D

- Kaplan & Norton (1992) full text: perspective names and the lagging-financial wording (D6). Sarikaya et al. design-space dimensions (D3). Few's Bullet Graph specification, "Why Most Dashboards Fail" and the 2007 follow-up (D4, DV3).
- Variance display notation in IBCS 2.0 (B15, D11 context). Vendor variance-commentary guidance (FitGap, FanRuan, Wisemonk, Rework) was never read (D11).
- JMIR Mental Health 2025 raw counts and prompt-specificity result (D16). Whether current frontier models still show citation fabrication and the position-of-hallucination effect (D15, D16, D17).
- Board guidance from FRC, IoD, CGI, NACD and the IBGC code (validator list; D13 context). Board Intelligence survey year (D12). Yigitbasioglu & Velcu (2012) full text (validator list).
- Evidence for any cap on KPIs or flags shown to executives (D8). The Amazon WBR deck order (D7). The Deloitte refund figure (D18).

### 7.6 Stream E

- English equivalents of CPC terms against the English IFRS and IAS text (E14, E15, E16).
- Lei 6.404/76 art. 187 income-statement structure and Lei 9.718/98 art. 3 as amended by Lei 12.973/2014 (EV2).
- ISO 17100:2015 normative clauses 5.3.3-5.3.6, the query obligation and current revision status (E1).
- Whether frontier LLMs make large-unit number errors on Portuguese business text; no study found, so consider an internal test of 10-20 figures (E7).
- Practitioner conventions without a source: bare "M" versus "MM" versus "mil", "R$ mil" as thousands, 1T26 versus Q1 2026, p.p. usage (XLAT-7).
- The practitioner glossary entries (orçado, realizado, previsto, ticket médio, inadimplência, positivação, sell-in/sell-out, regime de caixa) (E14 dossier rule).
- Percent-sign spacing in Brazilian formal norms (ABNT/IBGE) versus CLDR (E12).
- CVM Deliberação 835/2019 and the 13 December 2019 date for CPC 00 (R2) (E16).
- Measured Brazilian Portuguese expansion rates for slides and dashboards (E11).
- Whether an ABNT adoption of ISO 17100 exists (validator list). The MQM scoring formula and whether "Untranslated" exists in the full typology (E2, E3).
- Whether CLDR "pt" is pt-BR is inferred from the locale structure (E12).

---

## 8. Seed assets

Concrete artifacts the evidence supports. Each states its basis and strength; anything that is Claude's design rather than a finding is marked "design". Placeholders in square brackets must be filled from the user's inputs, never invented.

### S1. Chart-selection table

Basis: VIZ-1 to VIZ-18. Strength per row.

| Reader's question | Default form | Axis and baseline | Labels and order | Avoid | Rules, ids, strength |
|---|---|---|---|---|---|
| Which is bigger, and by how much (categories) | Bars or dots on one shared axis | Bars: zero baseline. Dots: non-zero allowed | Direct value labels; sort by value; "Other" last | Area, volume, 3D or angle for the primary quantity | VIZ-1, VIZ-3, VIZ-4; B1, B2, B5; strong (sorting: practitioner-consensus) |
| How did it change over time | Line | Non-zero allowed only when the change is the message; print axis start and end; quote the delta in the title | Label end points and the key point; one accent series | A range that inflates or shrinks the business-relevant change | VIZ-2; B2, B3, BV1; moderate |
| Part of a whole | Sorted bars or one 100% stacked bar; pie or donut only for two or three labeled slices | Zero baseline | Percent labels | Exploded, varying-radius, icon, nested or 3D pies; angle alone | VIZ-5; B5; moderate |
| Actual versus target, plan or prior year | Bullet-style bar with a target marker, or paired bars or lines in one panel | Bars at zero | Variance absolute and percent with sign; favourability by polarity, in a word as well as colour | Gauges and dials | DASH-6, DASH-8; D4, D5, DV2; weak and practitioner-consensus |
| Two series, different units | Two aligned panels sharing x, or both indexed to 100 | Per panel | Endpoint labels; base period stated | Dual axis by default | VIZ-6; B4, BV4; practitioner-consensus |
| Two series, similar values | Overlay in one panel | Shared | Direct labels | | VIZ-17; B16; moderate |
| Many series (more than about four) or a wide range | Small multiples, identical axis ranges, shared x | Identical per panel | Panel titles as claims where possible | One crowded overlay | VIZ-17; B16; moderate (threshold is a heuristic) |
| Estimate, forecast, survey result | Point with labeled interval, range table or labeled scenario bands | Per chart type | State what the range means | Unlabeled error bars; bars with whiskers as the only display | VIZ-15, VIZ-16; B12, BV2; moderate, weak |
| Ranking | Sorted bars | Zero | Value labels | | VIZ-4; B1; practitioner-consensus |
| Variance decomposition (price, volume, mix) | Table with driver rows, or a waterfall where the audience uses it | | Sign and favourability marked | Unfamiliar forms without a how-to-read line | VIZ-10, DASH-8; B11, DV2; practitioner-consensus (waterfall is not evidence-tested) |
| KPI status at a glance | KPI card (S2) with a bullet-style bar | | Word plus symbol plus colour | Gauges | DASH-3, DASH-6; D4, D5; weak |
| Exact values needed | Table | | | | Practitioner convention; not tested (section 7.3) |
| Distributions, relationships (histogram, box plot, scatter) | No evidence gathered in this synthesis; use standard forms and mark the default unverified | | | | Section 7.3 |

### S2. KPI-card spec

Basis: DASH-3, DASH-4, DASH-8, DASH-9; D2, D7, D9, DV2, DV1. Strength: practitioner-consensus. The field list is a design synthesis; polarity and the exact set are design inferences.

| Field | Required | Rule |
|---|---|---|
| Name | yes | The metric name. The claim belongs in the commentary line or the exhibit title |
| Definition | yes | One line; define non-obvious terms once |
| Owner | yes | Named role or person; "[to be confirmed by <role>]" if not supplied |
| Type | operational reviews | Input (controllable action) or output (result); outputs link to their driver inputs |
| Source and as-of date | yes | On the card or in the page footer |
| Unit and scale | yes | For example "R$ mil", "%", "p.p." |
| Polarity | yes | Higher is better, lower is better, or in range (design) |
| Actual | yes | With the period label |
| Target | yes | Value and source (plan, budget, regulatory), or the words "No target" |
| Comparison | yes | Prior period and same period last year (de-emphasised); growth rate beside the absolute value where rates matter |
| Variance | yes | Against target and against prior period; absolute and percent; favourable or unfavourable from polarity, not sign |
| Status | yes | Word plus symbol plus colour; never colour alone |
| Status rule | yes | Written on the page (S3); tolerances supplied by the owning team |
| Range | estimates and forecasts | Low, base, high or an interval, and what it means |
| Commentary | flagged KPIs | Cause (supplied, else "cause not provided"), owner, next action, date |
| Guardrail metric | incentive-linked KPIs | Optional (DASH-10) |
| Trend | optional | Recent periods plus the same periods last year, faded; the 6-12 layout of one company is not a mandated format |

### S3. Status-rule template

Basis: DASH-4; D9, D2. Strength: weak (practitioner convention). Thresholds are placeholders; do not invent them.

```
Status rule for [KPI]   Owner: [role]   Tolerances confirmed by: [role, date]
Green : at or better than target
Amber : within [tolerance supplied by owner] of target
Red   : beyond [tolerance] OR [stated trigger, for example milestone missed, floor breached]
Every Red carries: action | owner | date | recovery plan
Carried over (unchanged since last period): flag | age | owner
Display: word + symbol + colour
```

### S4. Board-paper cover sheet

Basis: D13 (AICD annotated sample, May 2020), validator-verified from the PDF text; D14, D12 for pruning. Strength: practitioner-consensus (one governance body's sample, not a standard). Items marked "skill" are additions, not AICD content.

| Block | Content | Cap or note |
|---|---|---|
| Header | Title, meeting, date, author or sponsor | Generic header |
| Paper type | For Decision, For Discussion or For Noting | Required tag |
| Draft resolution | Decision papers only; worded for adoption without amendment | Near the top |
| Executive summary | Purpose, and whether the board is asked to approve or only note | One paragraph, about four to five lines. The AICD summary does not itself contain the recommendation |
| Recommendation | Recommended course, alternatives considered where relevant, intended outcomes | Own section, no more than one page |
| Background | Context the board needs | About one page |
| Implications | Strategy, financial, risk, and any other | Each no more than half a page; financial: key points only |
| Governance and compliance | As applicable | Section in the sample |
| Management responsibility | Who is accountable for execution | Section in the sample |
| Appendices | Business case, calculations, criteria, detail | Detail goes here, not in the body |
| Basis note (skill) | Sources used, key assumptions, what is unverified or not independently reviewed | One to three lines (CORE-8) |
| Purpose check (skill) | The decision(s) this pack supports; sections that change no decision moved to appendix or a "for noting" bundle | DASH-14; weak |

### S5. Decision statement and recommendation skeleton

Basis: CORE-1, CORE-2, CORE-4, RES-1 to RES-6, CORE-8. Strength: practitioner-consensus overall; individual components carry the strengths given in section 3.

**Routine decision (short form)**

```
Decision requested : [verb] [object] [amount or scope] - [who decides] - by [date]
Why                : [1-2 sentences with the decisive number and its comparison base]
Alternative        : [one option, or the status quo, and why it is not recommended]
Main risk          : [one sentence, with a number or range]
Basis              : [sources used; assumptions; unverified items]
```

**Consequential decision (full form)**

1. Answer and ask (CORE-1), labeled Decision, Discussion or Information.
2. Situation, only if the reader needs context: three sentences at most, answer last (WRIT-4).
3. Options compared on the same three to five criteria: recommended option, one or two genuine alternatives, status quo if real; pros, cons, why not chosen; what the recommendation gives up (CORE-4).
4. Evidence for the lead answer, what would change it, and what disconfirming checks were run with their results (RES-1).
5. Forecast basis: reference class versus the internal estimate, or "inside-view estimate, not benchmarked" with a range (RES-2).
6. Downside as a named failure scenario with source, impact, early signal and competitor response (RES-3).
7. Draft premortem: three to five plan-specific causes with early signal, mitigation and owner; labeled as a draft for the team to run independently (RES-4).
8. Roles: one recommender, one decider, sign-off parties with blocking power stated, who performs, who is consulted (RES-5).
9. Implementation path: who must act, first step in 30 days, whether implementers were involved (RES-6).
10. Basis note (CORE-8). Appendix for detail.

### S6. Variance-commentary template

Basis: WRIT-10, DASH-8; DV2, D7. Strength: practitioner-consensus. The materiality threshold and the cause must come from the user.

```
Driver decomposition (when the total is material): price | volume | mix | other  -> amounts
Event   : [metric] was [actual] vs [target] ([abs], [%]) and vs [prior period] ([abs], [%]); [favourable/unfavourable]
Cause   : [supplied by the owner] | "cause not provided" (open question for [owner])
So what : [effect on margin, cash or target, with number]
Now what: [action] - [owner] - [date]
Comment only where |variance| exceeds [threshold supplied by the user]
```

### S7. Number-fidelity table

Basis: XLAT-1, XLAT-6, XLAT-7; E3, E7, E12, E13. Strength: moderate (the Critical classification is Claude policy).

| # | Location | Source text | Source canonical value | Target text | Target canonical value | Match | Note |
|---|---|---|---|---|---|---|---|
| 1 | Slide 3, KPI tile | R$ 2,3 mi | 2,300,000 BRL | BRL 2.3M | 2,300,000 BRL | yes | Scale word mi = million |
| 2 | | | | | | | |

Rows are required for every numeral, percent, currency, unit, scale word, date, period label and sign convention, including charts, images, speaker notes, alt text and footnotes. Totals, subtotals and percentage changes are recomputed in the target. Any mismatch is Critical.

### S8. PT->EN business glossary

Basis codes: "CPC" entries have the Portuguese term verified in the cited CPC text (E14, E15, E16); English equivalents are inferred from IFRS/IAS correspondence and not read from IFRS text, so check before quoting. "CLDR" entries come from Unicode data (E12, E13, EV1). Everything marked "practitioner usage" has no primary source here and must be listed as such in the term register (XLAT-5, XLAT-21).

| Portuguese | English | Source or basis | Note |
|---|---|---|---|
| receita | revenue | CPC 47 App. A defines "Receita" (E14); English inferred from IFRS 15 | |
| receita de contrato com cliente | revenue from contracts with customers | CPC 47 title (E14); English inferred | |
| preço da transação | transaction price | CPC 47 App. A (E14); English inferred | |
| obrigação de performance | performance obligation | CPC 47 App. A (E14); English inferred | |
| ativo de contrato / passivo de contrato | contract asset / contract liability | CPC 47 App. A (E14); English inferred | |
| contraprestação | consideration | CPC 47 per the dossier (E14); the Portuguese term was not individually re-checked; English inferred | |
| faturar e manter | bill-and-hold | CPC 47 App. B (E14) | |
| faturamento | gross revenue or gross sales (management and tax usage); invoicing or billing (the act) | E14, EV2 | Decide by context (XLAT-19); gross versus net is the trap |
| receita bruta | gross revenue | EV2 | |
| receita líquida | net revenue | Practitioner usage; the Lei 6.404/76 art. 187 structure was seen only in a search snippet (EV2) | |
| resultado do período | profit or loss for the period | CPC 26 item 7 (E15); English inferred from IAS 1 | |
| resultado líquido do período | profit or loss for the period; net income (management) | CPC 26 items 88-89 (E15) | |
| lucro líquido | net income or net profit | CPC 26 item 8 allows it as a label for "resultado" (E15) | Check whether the figure is the statutory total |
| resultado operacional | operating income or operating result | Practitioner usage | |
| resultado financeiro | net finance result | Practitioner usage | |
| patrimônio líquido | equity | CPC 26 (E15); English inferred | |
| capital próprio | equity or owners' capital | CPC 26 gloss (E15) | |
| balanço patrimonial | statement of financial position (balance sheet in management text) | CPC 26 table of contents (E15); English inferred | |
| demonstração do resultado | statement of profit or loss | CPC 26 (E15); English inferred | |
| ativo circulante / passivo circulante | current assets / current liabilities | CPC 26 (E15); English inferred | |
| regime de competência | accrual basis | CPC 00 (R2) para 1.17 (E16); English inferred | The validator found CPC 26 items 27-28 a cleaner primary source |
| regime de caixa | cash basis | Practitioner usage; not verified in the fetched text | |
| mil / mi / bi / tri | thousand / million / billion / trillion | CLDR pt compact forms (E12, EV1) | bi = 10^9; tri = 10^12 |
| milhão / bilhão / trilhão | million / billion / trillion | CLDR pt long forms (E12) | |
| mil milhões (pt-PT) | billion (10^9) | CLDR pt-PT (EV1) | |
| bilião (pt-PT) | trillion (10^12) | CLDR pt-PT (EV1) | Microsoft's pt-PT guide conflicts; verify magnitude (XLAT-9) |
| R$ / US$ | BRL / USD | CLDR (E12, E13, EV1) | Never convert silently |
| p.p. | percentage points | Practitioner usage | Distinguish from % |
| acumulado do ano | year to date (YTD) | Practitioner usage | |
| 1T26 | Q1 2026 | Practitioner usage | |
| exercício | fiscal year | Practitioner usage | |
| orçado / realizado / meta | budget / actual / target | Practitioner usage | |
| previsto | forecast or planned figure | Practitioner usage | Decide by context |
| lucro bruto | gross profit | Practitioner usage | |
| margem de contribuição | contribution margin | Practitioner usage | |
| rentabilidade | profitability or return | Practitioner usage | Decide by context |
| inadimplência | delinquency or default rate | Practitioner usage | |
| ticket médio | average ticket or average order value | Practitioner usage | Define once |
| positivação | active customers in the period | Practitioner usage | Sales jargon; define once |
| sell-in / sell-out | shipments to the channel / sales to end consumers | Practitioner usage | Often left in English in Brazilian decks |
| giro de estoque | inventory turnover | Practitioner usage | |
| ICMS, PIS/COFINS, CVM, CNPJ, Ltda., S.A. | Keep the original; add a short gloss on first use | Practitioner usage (XLAT-18) | The CPC name "Comitê de Pronunciamentos Contábeis" appears in E14 |
| atual, atualmente | current, currently (not "actual") | Practitioner usage | False friend |
| eventualmente | possibly (not "eventually") | Practitioner usage | False friend |
| realizar | carry out (not "realize") | Practitioner usage | False friend |
| pretender | intend (not "pretend") | Practitioner usage | False friend |
| aplicação (finance) | investment | Practitioner usage | |

### S9. Locale format cheat sheet

Basis: E12, E13, EV1, EV4. Strength: strong (Unicode CLDR data; examples runtime-checked by the validator on CLDR 47). A dash means the inputs do not cover the item.

| Item | pt-BR (CLDR "pt") | en-US | pt-PT |
|---|---|---|---|
| Decimal separator | , | . | , |
| Group separator | . | , | non-breaking space (minimum grouping digits 2) |
| Number example | 1.234.567,89 | 1,234,567.89 | - |
| Currency pattern | R$ 1.234,56 (non-breaking space after the symbol) | $1,234.56; BRL in en-US prints as R$1,234.56 | #,##0.00 followed by the symbol |
| Percent | 12,5% | 12.5% | #,##0% pattern |
| Compact (short) | mil, mi, bi, tri | K, M, B, T | M (10^6), mM (10^9), Bi (10^12) |
| Long scale words | milhão, bilhão, trilhão | million, billion, trillion | milhão, mil milhões, bilião |
| Short date | dd/MM/y | M/d/yy (en-GB: dd/MM/y) | - |
| Long date | 29 de outubro de 2026 | October 29, 2026 | - |
| Time | HH:mm | h:mm am/pm | - |
| Currency codes | R$ = BRL; US$ = USD | $ = USD; R$ = BRL | - |

Verified runtime examples (pt-BR): "R$ 1.234.567,89", "2,3 mi", "1,5 bi", "12,5%", "29 de outubro de 2026". In executive text avoid all-numeric dates (XLAT-3).

### S10. Overclaim watchlist

Basis: RES-11, QA-5. Strength: strong. The left column lists statements Claude must not make; they appear here only as prohibitions and are not findings (see sections 6 and 7 for why). Use the right-hand wording only when asked, with the limitation attached.

| Do not say | Say instead, only if asked | Ids |
|---|---|---|
| "Reducing bias adds 7 points of ROI" or "process matters six times more than analysis" | In a self-reported survey of 1,048 decisions, higher process quality went with higher ROI (bottom to top quartile: +6.9 pp; analysis: +5.3 pp); correlational | A5, AV1 |
| "Premortems improve identification of failure reasons by 30%" | Klein cites a 1989 study for 30%; the original abstract does not support that figure; do not quote | A6 |
| "Scenario planning widens confidence ranges by 50%" | One experiment with 68 students saw ranges widen about 50%; calibration was not shown to improve | A15 |
| "Half of all decisions fail" | In 356 decisions, tactics prone to failure appeared in two of three; "failure" meant not sustained or fully used after two years | A8 |
| "Pie charts are always bad"; "angle is the least accurate way to read charts"; "donuts are better than pies" | Position on a common scale was the most accurate encoding; angle-only pies were least accurate; donut equalled pie in a two-segment test | B1, B5 |
| "Dual axes are banned" | Default to no dual axis, with named exceptions; the evidence is thin | B4, BV4 |
| "Decluttering improves comprehension" | Decluttering raised professionalism ratings; adding focus raised memory and clarity | B10 |
| "Embellishment hurts accuracy" | One small test (n=20) found no accuracy cost and better recall after two to three weeks | B6 |
| "8% of all men are colourblind" | Roughly 5-8% of men and 0.4-0.5% of women, depending on ancestry | B14 |
| "Assertion-evidence slides improve retention by X%" | Gains were modest and confounded in developer-run studies; quote no number | C7, C8, AV4 |
| "Shorter emails get 4.8% instead of 2.7% responses" as a benchmark | One field experiment, no statistics reported; directional only | C1 |
| "Bezos banned PowerPoint" (with the 2004 email text) | Amazon's 2017 shareholder letter documents narrative six-page memos | C4, C5 |
| "Memos or BLUF improve decisions" | A documented practice or doctrine; no outcome data | C4, C16 |
| "Up to 75% of LLM summaries is hallucinated" | Do not quote; hallucination was measured as non-matching insights on one benchmark | D17 |
| "Bullet graphs are more accurate than gauges" | Read more efficiently (time to first fixation) in one 40-person study | D5 |
| "RAPID's Agree has / has no veto" | State the blocking power of each sign-off party in the document | A11, AV2 |
| "84% of directors want more focused packs" | Not on the source page; do not use | D14 |
| "Back-translation proves the translation is faithful" | A triage pass only | E9 |

### S11. Okabe-Ito palette with contrast

Basis: hex values from Wilke (B14); thresholds from WCAG (B13); contrast ratios against white were recomputed by the validator (`IMPL-palette-contrast`) and re-computed in this synthesis with the WCAG relative-luminance formula; the values match. Ratios on #F5F5F5 for blue, vermilion, bluish green and reddish purple are the validator's; those for orange, sky blue, yellow and black were computed here.

| Colour | Hex | Contrast on white | Contrast on #F5F5F5 | Use |
|---|---|---|---|---|
| Black | #000000 | 21.0 | 19.26 | Text, key series |
| Blue | #0072B2 | 5.19 | 4.76 | Preferred series colour |
| Vermilion | #D55E00 | 3.87 | 3.55 | Preferred second series or accent |
| Bluish green | #009E73 | 3.42 | 3.14 | Passes 3:1 marks on white; borderline on light grey |
| Reddish purple | #CC79A7 | 3.06 | 2.81 | Borderline on white; fails on light-grey fills |
| Sky blue | #56B4E9 | 2.31 | 2.12 | Fill only; not a thin line, small marker or text on white |
| Orange | #E69F00 | 2.25 | 2.07 | Fill only; not a thin line, small marker or text on white |
| Yellow | #F0E442 | 1.32 | 1.21 | Fill behind dark text only |

Adjacent marks need their own contrast: blue next to vermilion is 1.34:1 (validator), so separate them with a gap, outline or direct labels. Context greys on white: #949494 = 3.03, #BFBFBF = 1.84 (fails), #767676 = 4.54 (suits text).

### S12. Pre-delivery gate

Basis: QA-1 (a roll-up; adds no new evidence). Run on the output file, not the plan.

1. The first screen states the answer and the ask, labeled Decision, Discussion or Information (CORE-1).
2. The stakes were classified and the depth matches (CORE-2).
3. Every remaining sentence, request and slide changes a decision; one primary request per message (CORE-3, WRIT-9).
4. Consequential: genuine alternatives on the same criteria, with what the recommendation gives up (CORE-4).
5. Each number has a source and date, or a calculation note, or an "assumption" tag; unit, period and scope are stated (CORE-5).
6. Arithmetic was done by tool and totals reconcile to source (CORE-6).
7. No citation, quote or statistic was left unopened; unverifiable items are marked or removed (CORE-7).
8. No invented process, cause, target, tolerance or owner; Basis note present for consequential items (CORE-8).
9. Main risk, assumption and uncertainty are in the body, in sentences, with a number or range (CORE-9, VIZ-15).
10. Status documents lead with exceptions and state the selection criterion (CORE-10).
11. Reading the headings alone gives the argument (CORE-11).
12. The mode is declared and matched (CORE-12, STORY-1, DASH-1).
13. Charts: bars at zero; no 3D, area or angle for the primary quantity; titles carry a number and a comparison base; the highlighted element matches the title; no meaning by colour alone; contrast passes (VIZ-1, VIZ-12, QA-2).
14. PT<->EN: number table reconciled, locale formats correct, handoff note written (XLAT-1, XLAT-2, XLAT-15).
15. The user was told what changed, what was removed, what is unverified and what needs human review (CORE-13, QA-4, QA-7).

### S13. Translation QA checklist

Basis: XLAT-1 to XLAT-24; E2, E3, E5, E7, E12, E13. Strength: moderate (severity mapping is Claude policy; the dimensions come from MQM). Fail on any open Critical.

| Step | Check | Dimension | Severity if failed |
|---|---|---|---|
| 1 Setup | Variant stated (pt-BR, en-US unless named); mode stated (faithful or adaptation); term register written and frozen | Terminology | Major |
| 2 Numbers | Every numeral, percent, currency, unit, scale word, date, period label and sign matches after normalisation (S7); totals and percentage changes recomputed | Accuracy | Critical |
| 3 Numbers | Scale words resolved (mil, mi, bi, tri; K, M, B, T); table-level unit headers carried; pt-PT magnitudes verified; percent versus p.p. | Accuracy | Critical |
| 4 Numbers | Currency kept (R$ = BRL; US$ = USD); no silent conversion; any conversion shows rate, date and source | Accuracy, Locale conventions | Critical |
| 5 Content | Nothing omitted, added or softened; caveats, risks and qualifiers intact | Accuracy (Omission, Addition) | Critical when a decision changes, otherwise Major |
| 6 Structure | Counts match: slides or pages, headings, paragraphs, bullets, table rows and columns, footnotes, chart series | Accuracy, Design and markup | Major |
| 7 Terms | One target term per source term; false friends scanned; faturamento and resultado decided by context | Terminology, Accuracy (Mistranslation) | Major |
| 8 Output | No preface, explanation, refusal or fence; no leftover source-language sentences | Accuracy | Critical |
| 9 Locale | Separators, scale words, currency placement, date order converted together; no ambiguous numeric dates; non-breaking spaces bind units | Locale conventions | Major (Critical if a figure changes meaning) |
| 10 Audience | Brazil-specific institutions glossed; US-only references flagged; one register and address form | Audience appropriateness, Style | Major / Minor |
| 11 Layout | Rendered and checked for clipping, overlap and misalignment (30% headroom for short labels) | Design and markup | Major |
| 12 Source issues | Anything ambiguous or wrong in the source listed in the queries block, not silently fixed | Accuracy | Major |
| 13 Handoff | At most ten lines: variant, mode, checks run, Minor and Major counts fixed, open queries, five to ten highest-risk items; recommend bilingual human review for board, regulator, auditor, contract, investor or external use | | |
