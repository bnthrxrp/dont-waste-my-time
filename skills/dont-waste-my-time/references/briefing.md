# Briefing, profiles and length budgets

Read this after deciding a brief is needed (SKILL.md section 2), or once a brief is set and you need its profile and budget.

## Contents
- Fallback questionnaire (English and Portuguese)
- Structured question tool mapping
- Handling answers (with examples)
- Production profiles A-E and how they combine
- Length budgets
- Production brief template
- Standing defaults
- Extending the profiles

## Fallback questionnaire

Use this when no structured question tool is available. Send it as one message, then stop and wait. Include only the questions whose answers are unknown and material; renumber what remains. Put what is already known on an "Already clear" line so the user sees you listened. Mark the default with `*` (for Objective and Deliverable, the default is your inference from the request).

```
Before I build this, a few quick choices. Reply with numbers (e.g. "2, 4, 3, 2"), your own words, or "defaults".

Already clear: board deck on 2027 pricing; data in pricing_2027.xlsx.

1. Audience: 1) CEO/Board  2) C-suite/VPs  3) Directors/Heads*  4) Senior managers  5) Managers/coordinators  6) Analysts/specialists  7) Mixed  8) Other
2. Style (combine freely, e.g. "1+4"): 1) Executive & objective  2) Analytical & evidence-driven  3) Strategic & conceptual  4) Financial & performance  5) Operational & action-oriented  6) Balanced*
3. Objective: 1) Inform  2) Persuade  3) Get a decision/approval*  4) Diagnose  5) Recommend action  6) Explore
4. Detail: 1) Ultra-concise  2) Executive standard*  3) Deep analytical
5. Anything fixed? Language, template/brand, slide limit, deadline, must-use data, confidential items.

* = what I'll use if you skip it.
```

Portuguese version, for users writing in Portuguese:

```
Antes de montar, algumas escolhas rápidas. Responda com números (ex.: "2, 4, 3, 2"), com suas palavras, ou "padrão".

Já está claro: apresentação para o board sobre preços 2027; dados em pricing_2027.xlsx.

1. Público: 1) CEO/Conselho  2) C-level/VPs  3) Diretores/Heads*  4) Gerentes seniores  5) Gerentes/coordenadores  6) Analistas/especialistas  7) Misto  8) Outro
2. Estilo (pode combinar, ex.: "1+4"): 1) Executivo e objetivo  2) Analítico e baseado em evidências  3) Estratégico e conceitual  4) Financeiro e de performance  5) Operacional e orientado a ação  6) Equilibrado*
3. Objetivo: 1) Informar  2) Convencer  3) Obter decisão/aprovação*  4) Diagnosticar  5) Recomendar ações  6) Explorar
4. Nível de detalhe: 1) Ultra-conciso  2) Padrão executivo*  3) Analítico aprofundado
5. Alguma restrição? Idioma, template/marca, limite de slides, prazo, dados obrigatórios, informações confidenciais.

* = o que vou usar se você não responder.
```

Keep it to these lines. No preamble about why you are asking and no explanation of each option.

## Structured question tool mapping

When a tool such as `AskUserQuestion` is available, use it instead of the text questionnaire. It typically allows up to 4 questions with 2-4 options each, plus a free-text "Other".

- Choose the 4 options most plausible **for this request**, not always the same four. Put the default first and append "(Recommended)".
- Audience usually covers: Directors/Heads (Recommended), CEO/Board, C-suite/VPs, Managers & specialists. Mixed or other audiences go through "Other".
- Style: set `multiSelect: true`, because styles combine.
- Detail: Executive standard (Recommended), Ultra-concise, Deep analytical.
- Spend the fourth slot on the most material unknown: Objective if ambiguous, otherwise the most important constraint (format, length, language).
- Headers of 12 characters or fewer: "Audience", "Style", "Objective", "Detail", "Format".
- Each question must stand on its own, because the user may see only the dialog.

## Handling answers

| User reply | What to do |
|---|---|
| All answers ("2, 4, 3, 2, max 10 slides") | Confirm in one line and start. No more questions. |
| Only some answers ("it's for the directors") | Apply defaults to the rest, say so in the confirmation line, start. Don't ask the remaining questions again. |
| "Defaults", "whatever you think", "just do it" | Use the defaults and your inferences, confirm in one line, start. |
| Natural language ("CFO, wants numbers, keep it short") | Map it: audience 2, style 4, detail 1. Confirm and start. |
| A new constraint later in the conversation | Apply it without re-briefing. |
| A critical gap remains (e.g. no data for a business case) | One targeted question, phrased so it's easy to answer, or proceed with marked placeholders if the user said so. |

Confirmation format: `Audience: C-suite | Style: Financial | Objective: Approval | Detail: Executive standard | Max 10 slides, English, .pptx`. Add "(defaults)" after any value you inferred.

## Production profiles

The audience sets the base profile; style, objective and detail adjust it. Explicit user instructions override everything here.

| Profile | Use for | Lead with | Emphasize | Keep out of the main body |
|---|---|---|---|---|
| **A. Board / CEO** | Audience 1, and audience 2 when the purpose is a decision | The answer or decision required, and its materiality | Enterprise value, material risks, strategic trade-offs, financial implications, what is being asked of them | Operational detail that doesn't change the decision (put it in the appendix) |
| **B. Director / Head** | Audience 3-4, and audience 2 for performance reviews | Business performance and its implications | Target vs actual, variance and drivers, risks, priorities, cross-functional impact, resource allocation | Both abstraction without numbers and analyst-level data dumps |
| **C. Analytical leadership** | Audience 6, or Style 2 at any level | The conclusion, then the supporting analysis | Calculation logic, definitions, comparisons, assumptions, methodological limits; charts that explain drivers | Technical detail that doesn't serve the conclusion (keep it available in an appendix) |
| **D. Operational management** | Audience 5, or Style 5 at any level | Exceptions and what must happen next | Causes, owners, deadlines, interventions, controllable vs uncontrollable drivers, priority by impact and urgency | Strategy discussion with no action attached |
| **E. Persuasive business case** | Objective 2 or 3 when money, headcount or a commitment is requested | The ask and why it pays off | Problem and its materiality, the proposal, quantified benefits and costs where evidence allows, risks, assumptions, alternatives, the decision requested | Advocacy without evidence; hiding the downside |

**How they combine.** Audience sets altitude and length. Style adds a lens: analytical overlays C, financial adds the P&L/cash/return view, strategic adds market, positioning and long-term options, operational overlays D, executive tightens toward A's brevity. Objective sets structure and ending:

| Objective | Structure | Ends with |
|---|---|---|
| Inform | Status → what changed → exceptions → outlook | What to watch, and when the next update comes |
| Persuade / decision | Ask → why → evidence → options and trade-offs → risks | The decision requested, with a deadline |
| Diagnose | What happened → why (drivers, root cause) → so what | Actions with owners |
| Recommend action | Recommendation → rationale → options compared → plan | Next steps, owners, dates |
| Explore | Question → what we know → what we don't → options | How to resolve the unknowns |
| Translate / adapt | The source's own structure | Flagged ambiguities |
| Improve existing | The source's purpose, sharpened | A change log |

Mixed audience: write for the most senior decision-maker, then add just enough context (definitions, a short "how to read this", an appendix) for the others.

## Length budgets

These are defaults, not quotas. The user's constraints win, and shorter is better whenever nothing material is lost. Reading speed for business prose is roughly 200-250 words per minute, so "a 3-minute read" means about 600 words at most.

| Deliverable | Ultra-concise | Executive standard (default) | Deep analytical |
|---|---|---|---|
| Email / message | ≤ 80 words | ≤ 150 words | ≤ 300 words |
| Memo / executive summary | ≤ 200 words | About one page: ≤ 450 words, plus an optional appendix | 2-5 pages, opening with a summary of ≤ 250 words |
| Report / business review | 1 page | Summary ≤ 250 words + body ≤ 3 pages + appendix | Summary + full analysis + method and data notes |
| Board paper | Cover sheet + 1 page | Cover sheet + ≤ 4 pages + appendices | As required, with a 1-page cover sheet |
| Deck | 3-5 slides | 6-12 main slides + appendix | 12-20 main slides + appendix |
| Dashboard | 3-5 headline KPIs on one screen | 5-9 headline KPIs + drivers + exceptions | Headline view + drill-down pages + data-quality notes |
| Research brief | ≤ 300 words + sources | 1-2 pages + sources | Full report + evidence table |
| BI/build specification | Not applicable: as long as the builders need, but lead with the purpose, decisions and headline KPIs on page 1. | | |

## Production brief template

Keep this internal unless showing it helps the user:

```
Audience:        Directors (Profile B) | secondary: finance analysts
Style:           Executive + financial lens
Objective:       Decision: approve 2027 price increases
Deliverable:     .pptx, English, ≤ 10 slides + appendix
Detail:          Executive standard
Key message:     "Raise 2027 prices 4.1% on average: +$X margin, volume risk contained to Digestia"
Decision sought: Approve the plan by Nov 30 so price letters go out Jan 1
Evidence needed: price × volume × elasticity per SKU (workbook); competitor index; COGS inflation
Constraints:     Company template not provided → clean default design
Assumptions:     Elasticities from the workbook (±0.3); no competitor response modeled
```

## Standing defaults

Users can set persistent defaults in CLAUDE.md, memory or project instructions, for example:

```
dont-waste-my-time defaults: audience=Board/CEO; style=financial+executive; detail=ultra-concise; language=pt-BR; deck format=pptx; template=assets/brand.potx
```

When defaults like these exist, treat those questions as answered, and list them in the "Already clear" line or the confirmation line.

## Extending the profiles

To add a profile (for example "Investors" or "Regulators"), add a row to the profiles table with the same five columns, map it to an audience or objective, and give it an objective structure if it needs a distinct ending. Keep the questionnaire unchanged unless the new profile needs a new audience option.
