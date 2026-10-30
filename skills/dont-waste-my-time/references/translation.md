# Translation and localization

Read this for a full-file translation, a long multi-section text, or an adaptation for another market. The rule behind everything here: transfer meaning, intent, numbers and business context, not words. Never change a number, claim or conclusion. When something in the source looks wrong, flag it; don't fix it.

## Contents
- Modes
- Procedure for files
- Never
- Locale conventions: pt-BR, en-US, en-GB
- PT→EN business glossary
- False friends
- File-specific handling
- QA checklist
- Executive adaptation
- Final message
- Evidence notes

## Modes

| Mode | Use when | May change | Never changes |
|---|---|---|---|
| **Faithful** (default) | Any request to translate | Wording, word order, locale conventions (separators, dates, quarters, scale words) | Content, numbers, claims, conclusions, caveats, order, emphasis |
| **Executive adaptation** | The user asks to adapt or localize, or to make it read naturally for a named market or audience | Also sentence structure and length, idioms, formality, title style | Same as faithful |
| **Both** | The user asks, or a faithful rendering would read badly to the target audience | Faithful version first, adapted version second, each labeled | Same as faithful |

- **Quick translations** (a passage, email, title or single slide): translate at once in faithful mode, apply the locale conventions below without comment, check every figure against the source before replying, and add at most one note (an ambiguous term or a suspected source error). No termbase, no procedure.
- **Both, for files**: deliver two files only if asked. Otherwise deliver the faithful file and list up to three passages where an adaptation would read better, with the proposed wording.
- **Target variant**: use the one the user names. "English" with no variant means en-US unless the audience, company or user is British; "Portuguese" means pt-BR unless they are in Portugal. Say which variant you used.

## Procedure for files

1. **Inventory** the text: `python3 ${CLAUDE_SKILL_DIR}/scripts/doc_text.py <file>`. The dump can miss alt text, slide master and layout text, docx footnotes, endnotes, comments and text boxes, SmartArt, and text inside images: check those in the file. Text inside an image can't be replaced; list it in the final message.
2. **Read for meaning** before translating: audience, purpose and key message; terms of art and any definitions given in notes or footnotes; ambiguous terms. Foot the totals and recompute the stated % changes once: that is how source errors surface (a figure that differs between pages, a total that doesn't add up, a footnote marker on the wrong item).
3. **Build a termbase** for this document: 5-20 recurring or ambiguous terms, one target term each, with its basis (the organization's own documents, a CPC/IFRS text, or practitioner usage). Start from the glossary below, but the organization's established terms win. Resolve each ambiguity once, from context, and apply it everywhere, including notes and charts.
4. **Resolve scale and units** before converting any figure: the unit header that governs it, the scale word, the currency, percent vs percentage points (Locale conventions).
5. **Translate in place**: work on a copy, keep the original untouched, and replace text inside the existing structure so formatting, layout, animations and links survive. Never rebuild the file from extracted text.
6. **Fit to layout** (File-specific handling).
7. **Revise**: compare source and target segment by segment, slide by slide or paragraph by paragraph, in a separate pass after translating. For High-stakes material (board pack, investors, regulator, auditor, contract, external publication), run this pass in a fresh context or subagent if available. Never describe it as independent or human revision.
8. **Verify** with the QA checklist, then write the final message.

## Never

- Change a number, claim, conclusion, hedge or emphasis. "Deve crescer" is "is expected to grow", not "will grow"; "recuou" is "declined", not "plunged".
- Silently correct a source error. Translate what is there, choose the most defensible reading, and flag it with its location: "Slide 3 says margin fell 1.5 pp; the slide 6 table gives -1.3 pp. Kept both as in the source; please confirm."
- Drop, merge or move a caveat, footnote, source line or footnote marker. A marker attached to the wrong item stays where the source put it, and you flag it.
- Put anything but the translation into the deliverable: no preface ("Here is the translation"), translator's notes, explanations or code fences. Notes go in the final message.
- Translate proper names, brands, product names, code, formulas, cell references, file paths, URLs or tickers. Keep Brazilian legal forms, taxes, regulators and registries (Ltda., S.A., ICMS, PIS/COFINS, CVM, B3, CNPJ) and add a short English gloss on first use for non-Brazilian readers. Translate department names and job titles descriptively (Diretoria Financeira → Finance Division), or use the organization's official English form.
- Convert currencies without an explicit rate and date from the user or the source. R$ is BRL; US$ is USD. If asked to convert, keep the original amount beside the converted one, with rate, date and source.
- Round or rescale differently from the source: 12,5 becomes 12.5, not 13 or 12.50. A unit change is allowed only when exact and needed by the reader (R$ 12.500 mil → R$12.5M).

## Locale conventions: pt-BR, en-US, en-GB

| Item | pt-BR | en-US | en-GB | Rule |
|---|---|---|---|---|
| Decimal and thousands | 1.234,5 | 1,234.5 | 1,234.5 | Swap both. "12,5" left in English reads as 125 or as a list. |
| Currency | R$ 12,5 mi; US$ 3,0 mi | R$12.5M or BRL 12.5M; $3.0M | R$12.5m or BRL 12.5m; US$3.0m | Keep the currency. In English text that mentions both, write BRL and USD, never a bare "$". No space after a symbol in English. In pt-BR, a non-breaking space binds symbol and scale to the number (R$ 12,5 mi, 3 p.p.). |
| Unit headers | R$ mil; Em milhões de R$; R$ MM | BRL thousands (R$ '000); BRL millions | same as en-US | A unit header governs every figure under it: translate it, never drop it. "R$ mil" means thousands of reais, not millions. |
| Scale words | mil = thousand; mi, milhão = million; bi, bilhão = billion (10⁹); tri, trilhão = trillion | K, M, B, T, or the words | k, m, bn, or the words | Brazil uses the short scale. In Portugal, bilião = 10¹² and mil milhões = 10⁹, and usage varies: fix the magnitude from context, flag it, and never write "bilião" in pt-BR. "MM" usually means million, but "M" means thousand in some finance usage: with a bare M or MM, infer from magnitude, state the reading and flag it. |
| Percent | 6,2% | 6.2% | 6.2% | No space before %. |
| Percentage points | p.p. | pp in decks and tables; percentage points in prose | same | Never "%" for a change in a rate, and avoid "ppt". 1 pp = 100 bps. |
| Dates | 30/04/2027; 30 de abril de 2027 | Apr 30, 2027 | 30 Apr 2027 | Write the month as a word in English, or ISO 2027-04-30 in tables: 05/06 is a different day in the US and the UK, and day-first order doesn't tell you the variant. Months are lowercase in Portuguese, capitalized in English ("abr/27" → Apr 2027). |
| Time | 14:30 | 2:30 PM | 14:30 | |
| Periods | 2T27, 2º trimestre de 2027; 1S27; acumulado do ano | Q2 2027 or 2Q27; H1 2027; YTD | Q2 2027; H1 2027; YTD | One form throughout the file. "vs. 2T26" → "vs. Q2 2026" (year over year). |
| Negatives | -2,0%; -R$ 1,5 mi | -2.0%; -R$1.5M, or (1.5) in financial tables | same as en-US | Keep the source's sign style unless the target template uses parentheses. Never lose a sign. |
| Versus | x or vs. ("Realizado x Orçado") | vs. | vs. | "x" means versus here, not "times". |
| Titles | Sentence case | Title case or sentence case: follow the template | Sentence case | One style for every title in the file. |

## PT→EN business glossary

Basis: **std [X]** = the Portuguese term is supported by source [X] in Evidence notes; the English rendering is common practice or IFRS correspondence, not read from IFRS text, unless the note says it is printed. **practice** = practitioner usage, unverified. The organization's established terms beat this table.

| Portuguese | English | Notes and ambiguity | Basis |
|---|---|---|---|
| receita | revenue | Not "receipts" (cash in). | std [C] |
| faturamento; faturamento bruto; receita bruta | gross revenue, gross sales | In management and tax usage, faturamento is the gross top line (≈ receita bruta), before deductions for returns, discounts, rebates and taxes on sales. Not IFRS "revenue" unless the source says it is net, and not "invoicing". If gross vs net is unclear, write "gross revenue (faturamento)" on first use and flag it; check whether taxes on sales are included before comparing it with a net figure. | std [L], [EV2] |
| faturamento (the act); ciclo de faturamento; faturar e manter | invoicing, billing; billing cycle; bill-and-hold | Use "invoicing" or "billings" only for issuing invoices, or for billings the source distinguishes from recognized revenue. | std [C] (bill-and-hold printed) |
| faturamento líquido; receita líquida; receita operacional líquida | net revenue, net sales | After deductions; the figure comparable to IFRS revenue. | std [L] (receita líquida) |
| deduções; abatimentos; bonificação | deductions; rebates, allowances; free goods | "Bonificação" in trade usually means free product, not a bonus. | std [L], except bonificação |
| CPV / CMV | cost of goods sold (COGS) | Custo dos produtos / das mercadorias vendidos. | practice |
| lucro bruto; margem bruta | gross profit; gross margin | Margin is % of net revenue unless the source says otherwise. | std [L] (lucro bruto) |
| margem de contribuição | contribution margin | Keep the source's base (gross or net revenue). | practice |
| EBITDA; LAJIDA | EBITDA | "EBITDA ajustado" = adjusted EBITDA: keep the adjustment note with it. | practice |
| lucro líquido; prejuízo | net income (US), net profit (UK); loss | CPC 26 lets entities label the period result "lucro líquido": check whether a figure is the statutory total. One English term per concept per document. | std [L], [E15] |
| resultado | depends on the line it labels | Never "result". Resultado do período or resultado líquido = profit or loss for the period (statutory) or net income (management); resultado operacional = operating income; resultado financeiro = net finance result; demonstração do resultado = income statement. Narrative "resultado do trimestre" = results or earnings; flag it if a figure depends on the reading. | std [L], [E15] |
| patrimônio líquido; balanço patrimonial; ativo / passivo circulante | equity; balance sheet (statement of financial position in IFRS statements); current assets / liabilities | | std [E15] |
| regime de competência; regime de caixa | accrual basis; cash basis | | std [E15] (competência); practice |
| orçado; orçamento | budget | "Abaixo do orçado" = below budget. | practice |
| realizado | actual(s) | "Realizado x Orçado" = Actual vs. Budget. Never "realized". | practice |
| meta | target | | practice |
| previsto; projeção; forecast | forecast, projection | "Previsto" can mean the budget or a re-forecast: check which before choosing. | practice |
| acumulado do ano; acumulado 12 meses | year-to-date (YTD); last twelve months (LTM) | | practice |
| mesmo período do ano anterior | same period last year, prior-year period | A comparison against it is year over year (YoY). | practice |
| caixa; geração de caixa | cash; cash generation | Don't upgrade to "free cash flow" unless the source defines it so. | practice |
| inadimplência | delinquency, overdue receivables | "Default" claims non-payment, which is stronger; keep the source's days-overdue definition. | practice |
| PDD (provisão para devedores duvidosos) | allowance for doubtful accounts; expected credit loss allowance (IFRS 9) | Use the company's label if its English reports exist. | practice |
| PMR; PMP; PME (prazo médio de recebimento / pagamento / estocagem) | DSO; DPO; DIO (days sales / payables / inventory outstanding) | | practice |
| giro de estoque | inventory turnover | Times per period, not days. | practice |
| cobertura de estoque | inventory cover, days of inventory | Usually days or weeks of forecast sales. | practice |
| ruptura | out-of-stock (OOS) rate, stockout | Keep the base: % of SKUs, stores or store-days. | practice |
| positivação | active-outlet rate; numeric distribution | Brazilian term: share (or count) of outlets in the customer base that bought at least once in the period. No exact English equivalent: on first use write "active-outlet rate (positivação)" or follow the source's definition. Never "positivity". | practice |
| PDV (ponto de venda) | outlet, store, point of sale | "POS" can be read as the till; prefer "outlet" or "store". | practice |
| ticket médio | average ticket, average order value | Average order value for B2B orders; average ticket or basket for retail. | practice |
| mix; efeito mix | mix; mix effect | | practice |
| sell-in; sell-out | sell-in; sell-out | Keep. Sell-in: company to trade customer; sell-out: trade customer to shopper. | practice |
| verba; verba promocional | budget, funds; trade spend, promotional spend | "Verba" alone is any allocated budget. | practice |
| trade marketing | trade marketing | Keep. | practice |
| grandes redes; redes regionais; independentes | key accounts or large chains; regional chains; independent stores (pharmacies, etc.) | Not "large networks". | practice |
| distribuidor; atacadista | distributor; wholesaler | | practice |
| representante (comercial) | sales agent, sales representative | Often an independent agent, not an employee: keep the distinction when it matters. | practice |
| carteira (de clientes); carteira de pedidos | customer base, account portfolio; order book, backlog | | practice |
| share; participação de mercado | market share | "Share de gôndola" = share of shelf. | practice |
| cobertura (comercial) | coverage | Outlets served as a share of the outlet universe. | practice |
| conselho de administração | board of directors | "Conselho consultivo" = advisory board; "conselho fiscal" = fiscal council (keep the term, add a short gloss). | std [L] |
| diretoria; diretor | executive board, executive officers; director or officer (often VP level) | Never "board of directors". A named area ("Diretoria Financeira") is the finance division or finance leadership. "Diretor-presidente" = CEO. | std [L] |
| comitê executivo | executive committee | | practice |
| pauta | agenda | Portuguese "agenda" means calendar or schedule. | practice |
| deliberação; deliberar | resolution, decision; resolve, decide | Not "deliberation", which is the discussion. | std [L] |
| ata | minutes | "Lavrar a ata" = draw up the minutes. | std [L] |
| AGO; AGE (assembleia geral) | AGM; EGM (annual / extraordinary general meeting) | A shareholders' meeting, not a board meeting. | practice |

## False friends

| Portuguese | Means | Not |
|---|---|---|
| eventualmente | occasionally, possibly, if needed | eventually (= por fim, finalmente) |
| pretender | intend, plan | pretend |
| atual; atualmente | current; currently | actual; actually (= na verdade) |
| realizar; realizado | carry out, hold, achieve; actual (in tables) | realize, except "realizar ganhos" = realize gains |
| assistir (a) | attend, watch | assist (= apoiar, ajudar) |
| rentabilidade | profitability, or return (name it: ROI, ROE, margin) | "rentability" |
| performance; desempenho | performance, or better, the measure itself (sales, margin) | a vague "performance" where a number exists |
| aplicação (financeira) | investment | application |
| exercício | fiscal year (financial year in the UK) | exercise |
| balanço | balance sheet, or the annual financial statements | balance |
| ações | shares, or actions and initiatives: check context | |
| data; dados | date; data | |
| deve | should, is expected to, or must, depending on context | always "must" |
| colaboradores | employees, staff | collaborators |

## File-specific handling

**pptx**
- Replace text run by run so bold, color and size stay on the equivalent words. When word order changes, put the emphasized words in the emphasized run and empty the surplus runs. Never assign `text_frame.text`: it discards run formatting.
- Cover everything the reader or presenter sees: titles, bodies, tables, grouped shapes, SmartArt, speaker notes, alt text (`descr`), hyperlink display text, and layout or master text that shows on slides (footers, confidentiality labels).
- Charts: translate the title, axis titles, categories and series names in the chart XML caches **and** the embedded workbook, so "Edit data" doesn't bring Portuguese back. If you use `chart.replace_data()`, pass the original number format and re-check labels and colors. Leave chart values and number formats alone: they are locale-neutral and display correctly. Numbers typed as text ("R$ 12,5 mi", "-1,5 p.p.") do need conversion.
- Length: PT→EN usually gets shorter, EN→PT longer, and short labels (KPI tiles, table headers, axis labels, buttons) change most. When text overflows, shorten the wording first; then shrink by at most 2 pt, never below 14 pt body and 10 pt chart labels and source lines (or the source's own size, if smaller). No text may overflow or overlap.
- Set the run language to the target (e.g. en-US) so spell-check doesn't underline every word.
- Render source and target with `python3 ${CLAUDE_SKILL_DIR}/scripts/render.py <file>` and compare each pair of slides.

**docx**: translate inside the existing runs and keep styles (don't rename them; names like "Título 1" are internal). Cover headers and footers in every section (including first-page and even-page variants), footnotes, endnotes, text boxes, captions and tables. Translate comments only if the document will be shared with them; otherwise leave them and say so. Translate the cached table-of-contents text too, or old headings remain until fields are updated. If the source has tracked changes, ask whether to translate the accepted version. Set the document language to the target.

**xlsx**: translate labels only (titles, headers, row labels, notes, comments, chart text). Keep formulas, cell references, defined names, number formats and the sheet names formulas use, unless asked; the file stores function names in English whatever the user's Excel language. Text that works as a key (lookup values, SUMIF criteria, validation lists, pivot sources) breaks formulas when translated: leave it, or change it everywhere and recalculate. After saving, check there are no new `#N/A`, `#REF!` or `#VALUE!` errors.

**html**: set `<html lang="en-US">` (or `en-GB`, `pt-BR`); translate `<title>`, meta description, `alt`, `title`, `aria-label`, `placeholder` and button text. Generate numbers and dates with `Intl.NumberFormat` / `toLocaleString` in the target locale, not string concatenation, and render: text built by JavaScript doesn't appear in a static dump.

**markdown**: keep syntax, code blocks, inline code, link URLs and front-matter keys. When headings change, update in-document anchor links.

## QA checklist

- [ ] `python3 ${CLAUDE_SKILL_DIR}/scripts/numbers_check.py compare <source> <target>` shows zero unexplained differences. Each difference is a deliberate locale conversion (decimal comma, p.p. → pp, a date written out) or a defect to fix; a number missing from the target can mean dropped content. Numbers in images, which the script can't read, get a manual check.
- [ ] Terminology matches the termbase everywhere, including notes, charts, footers and alt text.
- [ ] No leftovers. PT→EN: `python3 ${CLAUDE_SKILL_DIR}/scripts/doc_text.py <target> | grep -nE '[çãõáâêéíóú]|\b(de|da|do|das|dos|para|com|não|pelo|pela|mi)\b|p\.p\.'`; the only hits left should be proper names. Then check the places the dump misses (step 1 of the procedure). EN→PT: read the dump for English the audience wouldn't use. Either way, search for prefaces, notes or explanations that slipped into the file.
- [ ] Same number of slides, pages or sections, tables, rows, charts, notes, caveats, source lines and footnote markers (`*`, `†`, `¹`) as the source, each on the same item.
- [ ] Conventions consistent: in an English file, no "12,5", "p.p.", "mi" or "2T27" left; one date format and one period format.
- [ ] Rendered target fits: no overflow, clipping, overlap or awkward wrapping; compared with the source render.
- [ ] Ambiguity log complete: every term decision and flagged source issue, with its location.

**Severity gate** (this skill's policy, using MQM's severity names). Critical: any changed number, currency, unit, scale, date, period or sign; a caveat or qualifier dropped, added or softened; a preface, note or refusal inside the deliverable. Major: a term or false friend that changes meaning; a missing slide, bullet, row or footnote marker; clipped or overflowing text. Minor: fluency and style. Deliver only with zero open Critical findings; fix Major ones or list them in the final message.

Report only the checks you actually ran. A back-translation, a self-rating or a metric score is not evidence of fidelity; use back-translation at most to triage headline claims and key figures.

## Executive adaptation

Adapt these for the target audience:
- **Sentence length and structure**: split long Portuguese chains of subordinate clauses; prefer verbs to nominalizations ("realização da renegociação dos contratos" → "renegotiate the contracts") and the active voice. Avoid calques: word-for-word renderings read stiff.
- **Idioms and register**: replace formulas such as "Prezados", "Segue em anexo" or "Fico à disposição" with natural target-language equivalents, or drop them. EN→PT: use the more formal Brazilian executive register and keep the English loanwords the organization already uses. Keep one register and one form of address throughout.
- **Conventions**: title style, number and date formats, job titles (use the person's official title if known; never promote or demote a role).

Never adapt the claims, numbers, conclusions, caveats, emphasis or the argument's structure unless asked. Hedges keep their strength: "pode" = may or could; "deve" = should or is expected to. Turning topic titles into takeaway titles, cutting or reordering content, or adding a recommendation is improving the material, not translating it: do it only when asked, and list what you changed.

## Final message

Keep it to this:

```
Translated file: <path> (faithful, en-US)
Term decisions: <up to five judgment calls, e.g. positivação → "active-outlet rate" (defined at first use)>
Source issues, kept as in the source: <location + what conflicts>
Please confirm: <only what would change the file, e.g. whether "faturamento" here is gross or net>
Human check: <High-stakes only: recommend a bilingual review and name the 3-5 figures or terms to check first>
```

Leave out any line with nothing to report. Don't list what you translated or narrate the process.

## Evidence notes

Sources the drafter accessed ([U], [L], [C], [W], [G]) and validated research-stream entries (E and EV ids). The locale table rests on [U], [E12]/[EV1], [EV4], [W] and [G]; the glossary's Basis column cites [L], [C], [E15] and [EV2].
- **[U]** Unicode CLDR 47 locale data for pt-BR, en-US, en-GB and pt-PT, read through the Babel 2.18.0 Python library: separators; currency patterns (R$ 1.234,50 vs R$1,234.50; US$ in pt-BR and en-GB, $ in en-US; accounting negatives in parentheses in en-US and en-GB); compact forms (12,5 mi, 1,5 bi vs 12.5M, 1.5B; pt-PT 1,5 mil milhões); dates; times (14:30 vs 2:30 PM); quarters (T2 vs Q2).
- **[E12], [E13], [EV1]** CLDR JSON for pt, pt-PT and en, checked by the validator: non-breaking space in pt currency and compact patterns; pt-PT 10⁹ = mil milhões, 10¹² = bilião. Microsoft's pt-PT style guide conflicts ("16 biliões" for 16 billion); unresolved, hence "flag it".
- **[EV4]** Microsoft, Portuguese (Brazil) Localization Style Guide: non-breaking space between a number and its unit or currency; avoid word-for-word translation. Product-UI guidance, applied here by analogy.
- **[L]** Lei nº 6.404/1976 (Lei das S.A.), consolidated text, Câmara dos Deputados, https://www2.camara.leg.br/legin/fed/lei/1970-1979/lei-6404-15-dezembro-1976-368447-normaatualizada-pl.html: art. 130 (ata), art. 138 (management by the conselho de administração and the diretoria; the conselho deliberates collegially; only diretores represent the company), art. 187 (income statement: receita bruta less deduções, abatimentos and impostos = receita líquida; custo; lucro bruto; resultado; lucro ou prejuízo líquido).
- **[C], [E14]** CPC 47, Receita de Contrato com Cliente, "Correlação às Normas Internacionais de Contabilidade – IFRS 15", CVM, https://conteudo.cvm.gov.br/cvm_institucional/export/sites/cvm/menu/regulados/normascontabeis/cpc/CPC_47_Rev_14.pdf: "receita" throughout; "faturamento" only for invoicing; prints "faturar e manter (bill-and-hold)". IFRS Foundation, IFRS 15 Revenue from Contracts with Customers, https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/.
- **[EV2]** Migalhas de Peso, "Faturamento, receita bruta e receita" (law-firm article, 2018, updated 2019): tax law and court rulings tie faturamento to sales of goods and services and equate it with receita bruta (Lei 9.718/1998, Lei 12.973/2014, STF RE 390.840). Secondary, and no single settled definition, hence "resolve from context".
- **[E15], [EV3]** CPC 26 (R1), Apresentação das Demonstrações Contábeis, CVM consolidated Rev. 14, checked by the validator: items 7-8 (resultado do período; "lucro líquido" allowed as its label), items 27-28 (regime de competência), items 51-53 (presentation currency and rounding level shown in headings). English equivalents are inferred from IFRS correspondence.
- **[E3]** MQM Council, "The MQM Scoring Models" (themqm.org): a Critical error makes content unfit for purpose or risks serious financial harm, and in many systems one Critical error fails the text; severity multipliers are not normative. MQM doesn't map error types to severities: the severity gate here is this skill's policy.
- **[E1]** ISO 17100:2015, partially supported (clause headings and definitions via a preview; normative text not read): revision is a bilingual examination of target against source by a second person. Its scope excludes raw machine translation plus post-editing, so the revision step here borrows the structure, not a compliance claim.
- **[E5], [E6], [E9]** Kocmi et al., Findings of WMT24 (2024; no English-Portuguese pair): LLM outputs sometimes add explanations or refuse; human evaluation should be the final judge. Skorobogat et al. (2026): a correct round trip doesn't imply a correct intermediate translation.
- **[E10]** W3C Internationalization, "Text size in translation" (old, generic IBM UI guidance): short strings expand most. The Portuguese expansion percentages found in the research disagree and are not used.
- **[W]** Wikipedia (secondary): "Long and short scales" (Brazilian bilhão = 10⁹) and "Basis point" (1 bp = 0.01 percentage point).
- **[G]** GOV.UK A to Z style guide (UK government, not business): sentence case for titles; dates as "4 June 2017"; million and billion spelled out in money. UK business writing commonly uses m and bn (practice).
