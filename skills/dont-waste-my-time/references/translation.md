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

- **Quick translations** (a passage, email, title or single slide): translate at once in faithful mode, apply the locale conventions below without comment, and add at most one note (an ambiguous term or a suspected source error). No termbase, no procedure.
- **Both, for files**: deliver two files only if asked. Otherwise deliver the faithful file and list up to three passages where an adaptation would read better, with the proposed wording.
- **Target variant**: use the one the user names. "English" with no variant means en-US unless the audience, company or user is British; "Portuguese" means pt-BR unless they are in Portugal. Say which variant you used.

## Procedure for files

1. **Inventory** the text: `python3 ${CLAUDE_SKILL_DIR}/scripts/doc_text.py <file>`. The dump can miss alt text, slide master and layout text, docx footnotes, endnotes, comments and text boxes, SmartArt, and text inside images: check those in the file. Text inside an image can't be replaced; list it in the final message.
2. **Read for meaning** before translating: audience, purpose and key message; terms of art and any definitions given in notes or footnotes; ambiguous terms; apparent source errors (totals that don't add up, a figure that differs between pages, a footnote marker on the wrong item or with no footnote).
3. **Build a termbase** for this document: 5-20 recurring or ambiguous terms, one target term each, with the reason. Start from the glossary below, but prefer the organization's own established terms when the material, an earlier version or the user shows them. Resolve each ambiguity once, from context, and apply it everywhere, including notes and charts.
4. **Translate in place**: work on a copy, keep the original untouched, and replace text inside the existing structure so formatting, layout, animations and links survive. Never rebuild the file from extracted text.
5. **Fit to layout** (see File-specific handling), then **verify** with the QA checklist, then write the final message.

## Never

- Change a number, claim, conclusion, hedge or emphasis. "Deve crescer" is "is expected to grow", not "will grow"; "recuou" is "declined", not "plunged".
- Silently correct a source error. Translate what is there and flag it with its location: "Slide 3 says margin fell 1.5 pp; the slide 6 table gives -1.3 pp. Kept both as in the source; please confirm."
- Drop, merge or move a caveat, footnote, source line or footnote marker. A marker attached to the wrong item stays where the source put it, and you flag it.
- Translate proper names, brands, product names, legal entity names (Ltda., S.A.), code, formulas, cell references, file paths, URLs or tickers. Translate department names and job titles descriptively (Diretoria Financeira → Finance Division), or use the organization's official English form.
- Convert currencies without an explicit rate and date from the user or the source. Keep values in their currency; add a converted figure only when asked, labeled with rate, date and source.
- Round or rescale differently from the source: 12,5 becomes 12.5, not 13 or 12.50. A unit change is allowed only when exact and needed by the reader (R$ 12.500 mil → R$12.5M).

## Locale conventions: pt-BR, en-US, en-GB

| Item | pt-BR | en-US | en-GB | Rule |
|---|---|---|---|---|
| Decimal and thousands | 1.234,5 | 1,234.5 | 1,234.5 | Swap both. "12,5" left in English reads as 125 or as a list. |
| Currency | R$ 12,5 mi | R$12.5M or BRL 12.5M | R$12.5m or BRL 12.5m | Keep the currency. Use BRL wherever "$" could be read as US dollars. No space after a symbol in English. |
| Unit headers | R$ mil; R$ mi; R$ MM | BRL thousands (R$ '000); BRL millions | same as en-US | "R$ mil" means thousands of reais, not millions. |
| Scale words | mil = thousand; mi, milhão, milhões = million; bi, bilhão = billion (10⁹) | K, M, B, or thousand, million, billion | k, m, bn, or thousand, million, billion | Brazil uses the short scale. Portugal uses the long scale: bilião = 10¹², mil milhões = 10⁹. "MM" usually means million, but "M" means thousand in some finance usage: check against a total before converting. |
| Percent | 6,2% | 6.2% | 6.2% | No space before %. |
| Percentage points | p.p. | pp in decks and tables; percentage points in prose | same | Never "%" for a change in a rate, and avoid "ppt". 1 pp = 100 bps. |
| Dates | 30/04/2027; 30 de abril de 2027 | Apr 30, 2027 | 30 Apr 2027 | Write the month as a word in English: 05/06 is a different day in the US and the UK. Months are lowercase in Portuguese, capitalized in English ("abr/27" → Apr 2027). |
| Periods | 2T27, 2º trimestre de 2027; 1S27; acumulado do ano | Q2 2027 or 2Q27; H1 2027; YTD | Q2 2027; H1 2027; YTD | One form throughout the file. "vs. 2T26" → "vs. Q2 2026" (year over year). |
| Negatives | -2,0%; -R$ 1,5 mi | -2.0%; -R$1.5M, or (1.5) in financial tables | same as en-US | Keep the source's sign style unless the target template uses parentheses. Never lose a sign. |
| Versus | x or vs. ("Realizado x Orçado") | vs. | vs. | "x" means versus here, not "times". |
| Titles | Sentence case | Title case or sentence case: follow the template | Sentence case | One style for every title in the file. |

## PT→EN business glossary

Basis: **std [X]** = supported by source [X] in Evidence notes (for [L], the Portuguese term and its place in the accounts; the English rendering is common practice). **practice** = practitioner usage, unverified. The organization's established terms beat this table.

| Portuguese | English | Notes and ambiguity | Basis |
|---|---|---|---|
| receita | revenue | Not "receipts" (cash in). | std [C] |
| faturamento bruto; receita bruta | gross sales, gross revenue | Ambiguous. Brazilian gross figures usually include taxes on sales and come before returns, discounts and rebates; "faturamento" can also mean invoicing (billings). Choose from context; if the definition matters and the file doesn't give it, flag it. | std [L] (receita bruta) |
| faturamento líquido; receita líquida | net sales, net revenue | After deductions: returns, discounts, rebates, taxes on sales. | std [L] (receita líquida) |
| deduções; abatimentos; bonificação | deductions; rebates, allowances; free goods | "Bonificação" in trade usually means free product, not a bonus. | std [L], except bonificação |
| CPV / CMV | cost of goods sold (COGS) | Custo dos produtos / das mercadorias vendidos. | practice |
| lucro bruto; margem bruta | gross profit; gross margin | Margin is % of net revenue unless the source says otherwise. | std [L] (lucro bruto) |
| margem de contribuição | contribution margin | Keep the source's base (gross or net revenue). | practice |
| EBITDA; LAJIDA | EBITDA | "EBITDA ajustado" = adjusted EBITDA: keep the adjustment note with it. | practice |
| lucro líquido; prejuízo | net income (US), net profit or profit for the period (UK); loss | | std [L] |
| resultado | profit, earnings, results or performance | Ambiguous. "Demonstração do resultado" = income statement; "resultado do trimestre" may mean profit, EBITDA or overall results; "resultado financeiro" = net finance income/costs. Resolve from context; if you can't, write "results" and flag it. | std [L] |
| orçado; orçamento | budget | "Abaixo do orçado" = below budget. | practice |
| realizado | actual(s) | "Realizado x Orçado" = Actual vs. Budget. Never "realized". | practice |
| meta | target | | practice |
| previsto; projeção; forecast | forecast, projection | "Previsto" can mean the budget or a re-forecast: check which before choosing. | practice |
| acumulado do ano; acumulado 12 meses | year-to-date (YTD); last twelve months (LTM) | | practice |
| mesmo período do ano anterior | same period last year, prior-year period | A comparison against it is year over year (YoY). | practice |
| regime de competência; regime de caixa | accrual basis; cash basis | | practice |
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
| atualmente | currently | actually (= na verdade) |
| realizar; realizado | carry out, hold, achieve; actual (in tables) | realize, except "realizar ganhos" = realize gains |
| assistir (a) | attend, watch | assist (= apoiar, ajudar) |
| rentabilidade | profitability, or return (name it: ROI, ROE, margin) | "rentability" |
| performance; desempenho | performance, or better, the measure itself (sales, margin) | a vague "performance" where a number exists |
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
- Length: PT→EN usually gets shorter, EN→PT longer. When text overflows, shorten the wording first; then shrink by at most 2 pt, never below 14 pt body and 10 pt chart labels and source lines (or the source's own size, if smaller). No text may overflow or overlap.
- Set the run language to the target (e.g. en-US) so spell-check doesn't underline every word.
- Render source and target with `python3 ${CLAUDE_SKILL_DIR}/scripts/render.py <file>` and compare each pair of slides.

**docx**: translate inside the existing runs and keep styles (don't rename them; names like "Título 1" are internal). Cover headers and footers in every section (including first-page and even-page variants), footnotes, endnotes, text boxes, captions and tables. Translate comments only if the document will be shared with them; otherwise leave them and say so. Translate the cached table-of-contents text too, or old headings remain until fields are updated. If the source has tracked changes, ask whether to translate the accepted version. Set the document language to the target.

**xlsx**: translate labels only (titles, headers, row labels, notes, comments, chart text). Keep formulas, cell references, defined names, number formats and the sheet names formulas use, unless asked; the file stores function names in English whatever the user's Excel language. Text that works as a key (lookup values, SUMIF criteria, validation lists, pivot sources) breaks formulas when translated: leave it, or change it everywhere and recalculate. After saving, check there are no new `#N/A`, `#REF!` or `#VALUE!` errors.

**html**: set `<html lang="en-US">` (or `en-GB`, `pt-BR`); translate `<title>`, meta description, `alt`, `title`, `aria-label`, `placeholder` and button text. Change locale arguments in scripts (`toLocaleString('pt-BR')`, `Intl.NumberFormat('pt-BR')`) to the target, and render: text built by JavaScript doesn't appear in a static dump.

**markdown**: keep syntax, code blocks, inline code, link URLs and front-matter keys. When headings change, update in-document anchor links.

## QA checklist

- [ ] `python3 ${CLAUDE_SKILL_DIR}/scripts/numbers_check.py compare <source> <target>` shows zero unexplained differences. Each difference is a deliberate locale conversion (decimal comma, p.p. → pp, a date written out) or a defect to fix; a number missing from the target can mean dropped content.
- [ ] Terminology matches the termbase everywhere, including notes, charts, footers and alt text.
- [ ] No leftovers. PT→EN: `python3 ${CLAUDE_SKILL_DIR}/scripts/doc_text.py <target> | grep -nE '[çãõáâêéíóú]|\b(de|da|do|das|dos|para|com|não|pelo|pela|mi)\b|p\.p\.'`; the only hits left should be proper names. Then check the places the dump misses (step 1 of the procedure). EN→PT: read the dump for English the audience wouldn't use.
- [ ] Same number of slides, pages or sections, tables, charts, notes, caveats, source lines and footnote markers (`*`, `†`, `¹`) as the source, each on the same item.
- [ ] Conventions consistent: in an English file, no "12,5", "p.p.", "mi" or "2T27" left; one date format and one period format.
- [ ] Rendered target fits: no overflow, clipping, overlap or awkward wrapping; compared with the source render.
- [ ] Ambiguity log complete: every term decision and flagged source issue, with its location.

## Executive adaptation

Adapt these for the target audience:
- **Sentence length and structure**: split long Portuguese chains of subordinate clauses; prefer verbs to nominalizations ("realização da renegociação dos contratos" → "renegotiate the contracts") and the active voice.
- **Idioms and register**: replace formulas such as "Prezados", "Segue em anexo" or "Fico à disposição" with natural target-language equivalents, or drop them. EN→PT: use the more formal Brazilian executive register and keep the English loanwords the organization already uses.
- **Conventions**: title style, number and date formats, job titles (use the person's official title if known; never promote or demote a role).

Never adapt the claims, numbers, conclusions, caveats, emphasis or the argument's structure unless asked. Hedges keep their strength: "pode" = may or could; "deve" = should or is expected to. Turning topic titles into takeaway titles, cutting or reordering content, or adding a recommendation is improving the material, not translating it: do it only when asked, and list what you changed.

## Final message

Keep it to this:

```
Translated file: <path> (faithful, en-US)
Term decisions: <up to five non-obvious ones, e.g. positivação → "active-outlet rate" (defined at first use)>
Source issues, kept as in the source: <location + what conflicts>
Please confirm: <only what would change the file, e.g. whether "faturamento" here includes taxes>
```

Leave out any line with nothing to report. Don't list what you translated or narrate the process.

## Evidence notes

Sources accessed while drafting this file. The locale table rests on [U], [W] and [G]; the glossary's Basis column points to [L] and [C].
- **[U]** Unicode CLDR 47 locale data for pt-BR, en-US and en-GB, read through the Babel 2.18.0 Python library: separators; currency patterns (R$ 1.234,50 vs R$1,234.50; parentheses for accounting negatives in en-US and en-GB); compact forms (12,5 mi, 1,2 bi, 3,5 mil vs 12.5M, 1.2B, 3.5K); dates (30/04/2027, Apr 30, 2027, 30 Apr 2027; lowercase months in pt-BR); quarters (T2 vs Q2).
- **[L]** Lei nº 6.404/1976 (Lei das S.A.), consolidated text, Câmara dos Deputados, https://www2.camara.leg.br/legin/fed/lei/1970-1979/lei-6404-15-dezembro-1976-368447-normaatualizada-pl.html: art. 130 (ata), art. 138 (management by the conselho de administração and the diretoria; the conselho deliberates collegially; only diretores represent the company), art. 187 (income statement: receita bruta, deduções, abatimentos, impostos, receita líquida, custo, lucro bruto, resultado, lucro líquido).
- **[C]** CPC 47, Receita de Contrato com Cliente, "Correlação às Normas Internacionais de Contabilidade – IFRS 15", CVM, https://conteudo.cvm.gov.br/cvm_institucional/export/sites/cvm/menu/regulados/normascontabeis/cpc/CPC_47_Rev_14.pdf; and IFRS Foundation, IFRS 15 Revenue from Contracts with Customers, https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/.
- **[W]** Wikipedia (secondary): "Long and short scales" (Brazilian bilhão = 10⁹; European Portuguese long scale) and "Basis point" (1 bp = 0.01 percentage point).
- **[G]** GOV.UK A to Z style guide (UK government, not business): sentence case for titles; dates as "4 June 2017"; million and billion spelled out in money. UK business writing commonly uses m and bn (practice).
