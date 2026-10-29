#!/usr/bin/env python3
"""Generate the input files used by the evaluation cases in ../../evals/.

All companies, people and figures are fictitious. Numbers are internally
consistent unless a deliberate flaw is documented in FLAWS below, because
several test cases check whether the skill notices and flags such flaws
instead of silently "fixing" or repeating them.

Usage: python3 tests/fixtures/build_fixtures.py   (from the repo root)
"""
from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / "evals"

# Deliberate flaws, documented so graders know what a careful reviewer should catch.
FLAWS = {
    "translate-pt-board-deck": [
        "Slide 2 says the quarter closed 2,1% below budget; the slide 3 table total gives -2,0% (48,7 vs 49,7). "
        "Likely rounding, but a careful translator flags it rather than silently changing either figure.",
        "Slide 5 footnote: September sell-out is estimated (IQVIA data only through August). The caveat must survive translation.",
    ],
    "incomplete-data-summary": [
        "North: no September row; October target blank.",
        "West: new region in 2026, so net_sales_py is blank for every month.",
        "South: October gross_margin_pct = 143.0 (impossible; data error).",
        "East: October net_sales blank (not loaded) although the target exists.",
    ],
    "dashboard-html-directors": [
        "dso_days, inventory_weeks and complaints are lower-is-better metrics (polarity trap for red/green logic).",
    ],
}


def _fmt_br(x: float, nd: int = 1) -> str:
    return f"{x:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _add_bullets(slide, left, top, width, height, lines, size=16):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
    return box


def _make_pie_3d(chart):
    """python-pptx cannot write 3D pies; convert a 2D pie in place (deliberate chartjunk for the weak deck)."""
    from pptx.oxml.ns import qn
    from lxml import etree

    cs = chart._chartSpace
    pie = cs.find(".//" + qn("c:pieChart"))
    pie.tag = qn("c:pie3DChart")
    for el in pie.findall(qn("c:firstSliceAng")):
        pie.remove(el)
    chart_el = cs.find(qn("c:chart"))
    view3d = etree.SubElement(chart_el, qn("c:view3D"))
    etree.SubElement(view3d, qn("c:rotX")).set("val", "30")
    etree.SubElement(view3d, qn("c:rotY")).set("val", "0")
    chart_el.remove(view3d)
    chart_el.insert(list(chart_el).index(chart_el.find(qn("c:plotArea"))), view3d)


def _title_slide(prs, title, subtitle):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    s.shapes.title.text = title
    s.placeholders[1].text = subtitle
    return s


def _content_slide(prs, title):
    s = prs.slides.add_slide(prs.slide_layouts[5])  # title only
    s.shapes.title.text = title
    return s


def _table(slide, rows, left, top, width, height, size=12):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), left, top, width, height)
    tbl = shape.table
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(size)
    return tbl


# --------------------------------------------------------------------------
# 1. Portuguese board deck to translate
# --------------------------------------------------------------------------
def build_pt_deck(dest: Path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)

    s = _title_slide(prs, "Resultados Comerciais – 3º Trimestre de 2026",
                     "Diretoria Comercial Brasil | Vitalis Saúde | Outubro de 2026")
    s.notes_slide.notes_text_frame.text = (
        "Abrir agradecendo a presença do board global. Reforçar que o trimestre foi positivo em sell-out, "
        "mas que a margem precisa de atenção.")

    s = _content_slide(prs, "Destaques do trimestre")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5), [
        "Faturamento bruto de R$ 48,7 mi, +6,2% vs. 3T25 e 2,1% abaixo do orçado",
        "Sell-out cresceu 9,4% (IQVIA*), acima do mercado (+5,8%)",
        "Positivação de PDVs atingiu 71,3% (meta: 75,0%)",
        "Ruptura média de 8,6% nas redes regionais",
        "Margem de contribuição de 41,2% (-1,8 p.p. vs. 3T25) devido à maior verba promocional",
    ], size=20)

    s = _content_slide(prs, "Desempenho por canal")
    channels = [  # canal, realizado, orçado, vs 3T25 (%)
        ("Grandes redes", 21.4, 22.9, 3.1),
        ("Redes regionais", 12.8, 12.1, 11.2),
        ("Independentes", 9.6, 9.9, 4.9),
        ("Distribuidores", 4.9, 4.8, 8.8),
    ]
    rows = [["Canal", "Realizado (R$ mi)", "Orçado (R$ mi)", "Var. vs. orçado", "Var. vs. 3T25"]]
    for name, act, bud, yoy in channels:
        rows.append([name, _fmt_br(act), _fmt_br(bud), f"{'+' if act >= bud else ''}{_fmt_br((act / bud - 1) * 100)}%",
                     f"+{_fmt_br(yoy)}%"])
    ta, tb = sum(c[1] for c in channels), sum(c[2] for c in channels)
    rows.append(["Total", _fmt_br(ta), _fmt_br(tb), f"{_fmt_br((ta / tb - 1) * 100)}%", "+6,2%"])
    _table(s, rows, Inches(0.7), Inches(1.6), Inches(12), Inches(3.2), size=16)
    _add_bullets(s, Inches(0.7), Inches(5.2), Inches(12), Inches(1.2), [
        "Grandes redes abaixo do orçado por atraso na negociação do acordo anual com duas redes.",
    ], size=16)

    s = _content_slide(prs, "Positivação por região vs. meta")
    cd = CategoryChartData()
    cd.categories = ["Sudeste", "Sul", "Centro-Oeste", "Nordeste", "Norte"]
    cd.add_series("Positivação 3T26 (%)", (74.8, 72.1, 69.0, 66.4, 61.7))
    cd.add_series("Meta (%)", (75.0, 75.0, 75.0, 75.0, 75.0))
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.7), Inches(1.5), Inches(8), Inches(5), cd)
    gf.chart.has_legend = True
    gf.chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    _add_bullets(s, Inches(9), Inches(1.8), Inches(4), Inches(4), [
        "Nordeste e Norte concentram o gap de positivação.",
        "Plano de cobertura com distribuidor regional em andamento.",
    ], size=16)
    s.notes_slide.notes_text_frame.text = "Positivação = % dos PDVs da carteira com pelo menos uma compra no trimestre."

    s = _content_slide(prs, "Margem e verba promocional")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(4), [
        "Verba promocional subiu para 9,8% do faturamento bruto (3T25: 7,6%)",
        "Margem de contribuição: 41,2% vs. 43,0% no 3T25",
        "Ticket médio nas farmácias independentes caiu 4,3%",
        "Resultado do trimestre pressionado pela política de descontos no canal independente",
    ], size=20)
    _add_bullets(s, Inches(0.7), Inches(6.5), Inches(12), Inches(0.6), [
        "*Dados de sell-out IQVIA disponíveis até agosto/26; setembro estimado pela área de Inteligência de Mercado.",
    ], size=11)

    s = _content_slide(prs, "Próximos passos")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5), [
        "Renegociar acordos comerciais com 2 grandes redes até 15/11/2026",
        "Ampliar cobertura no Nordeste via distribuidor (meta: +600 PDVs até março/27)",
        "Revisar política de verba: teto de 8,5% do faturamento bruto no 4T26",
        "Decisão necessária: aprovar investimento de R$ 1,2 mi em trade marketing regional",
    ], size=20)
    prs.save(dest)


# --------------------------------------------------------------------------
# 2. Dense English commercial report
# --------------------------------------------------------------------------
REGIONS = [  # region, actual, budget, prior year ($M, YTD Sep 2026)
    ("Northeast", 78.4, 77.1, 74.2),
    ("Mid-Atlantic", 64.9, 66.8, 63.1),
    ("Southeast", 71.2, 70.5, 67.0),
    ("Midwest", 59.8, 62.4, 59.9),
    ("Southwest", 48.3, 49.0, 46.1),
    ("Mountain", 27.6, 28.9, 26.8),
    ("Pacific", 62.4, 63.3, 59.6),
]


def build_dense_report(dest: Path):
    ta = sum(r[1] for r in REGIONS)
    tb = sum(r[2] for r in REGIONS)
    tp = sum(r[3] for r in REGIONS)
    lines = []
    w = lines.append
    w("# Northwind Consumer Health — Commercial Performance Report")
    w("## Period: January–September 2026 (YTD) | Prepared by Commercial Excellence | Version 3 (final)")
    w("")
    w("### 1. Introduction")
    w("In today's rapidly evolving and highly competitive consumer health landscape, it is more important than ever "
      "to keep a close eye on our commercial performance. This report aims to provide a comprehensive and holistic "
      "overview of all relevant aspects of our commercial results for the year to date, leveraging the full breadth of "
      "data available to the Commercial Excellence team. As in previous editions, the report covers market context, "
      "regional performance, price and volume dynamics, channel inventory, promotions, portfolio, customer service and "
      "outlook. We would like to thank all teams for their continued dedication and hard work, which has been "
      "instrumental in navigating a challenging environment.")
    w("")
    w("### 2. Market context")
    w("The US OTC market grew 3.9% in value and 0.6% in units over the period (scanner data, all outlets combined). "
      "Inflation in the category remained elevated, with average shelf prices up 3.3%. Private label continued to gain "
      "share, reaching 24.8% of category value (+1.1 points year over year). Cold and flu incidence was in line with the "
      "five-year average. Digestive health was the weakest segment (-2.4% value). Pain relief grew 5.1%. E-commerce now "
      "represents 17.2% of category value versus 15.0% a year ago. Our overall value share was 11.4%, down 0.3 points.")
    w("")
    w("### 3. Net sales by region (USD millions, YTD September)")
    w("")
    w("| Region | Actual | Budget | Prior year | Var. vs budget | Var. vs PY |")
    w("|---|---:|---:|---:|---:|---:|")
    for name, a, b, p in REGIONS:
        w(f"| {name} | {a:.1f} | {b:.1f} | {p:.1f} | {(a / b - 1) * 100:+.1f}% | {(a / p - 1) * 100:+.1f}% |")
    w(f"| **Total** | **{ta:.1f}** | **{tb:.1f}** | **{tp:.1f}** | **{(ta / tb - 1) * 100:+.1f}%** | **{(ta / tp - 1) * 100:+.1f}%** |")
    w("")
    w("Northeast delivered the strongest performance, exceeding budget, helped by a strong pain relief season and the "
      "expansion of shelf space at two regional pharmacy chains. Mid-Atlantic was slightly below budget. Southeast was "
      "ahead of budget. The Midwest was below budget and broadly flat year over year; the region was affected by a number "
      "of factors, including weather, competitive activity and, from May, the delisting of Digestia at MegaMart Midwest "
      "(approximately $3.1M of annualized net sales). Southwest was slightly below budget. Mountain was below budget. "
      "Pacific was slightly below budget but grew year over year.")
    w("")
    w("### 4. Price, volume and mix")
    w("Year-over-year net sales growth of +4.0% breaks down as follows: price +6.8%, volume -3.1%, mix +0.5% "
      "(multiplicative decomposition). The budget assumed price +4.5% and volume +1.5%. The list price increase of "
      "February 2026 was fully implemented across all customers by April. Volume declines were concentrated in "
      "Digestia and Brevex value packs, where private label price gaps widened to 38% and 31% respectively.")
    w("")
    w("### 5. Sell-in and sell-out")
    w("Sell-in (our shipments to customers, net sales value) grew +4.0% year over year. Sell-out (consumer offtake at "
      "retail, scanner data, value) grew +0.7% over the same period. Trade inventory at our top 20 customers rose from "
      "5.2 weeks of supply in December 2025 to 6.8 weeks in September 2026, against a customer-agreed range of 4 to 6 "
      "weeks. Average weekly sell-out at these customers was $7.9M in Q3. Several customers have signaled that they "
      "intend to bring inventory back within the agreed range before year-end.")
    w("")
    w("### 6. Trade promotions")
    w("Trade spend reached $58.4M YTD versus $49.5M in the prior year (+18.0%), equal to 14.1% of gross sales "
      "(prior year: 12.4%). Of the 11 national promotions run this year, 3 delivered an ROI below 1.0 (incremental gross "
      "profit divided by promotion cost). The average ROI across all national promotions was 0.82 versus 1.07 in the "
      "prior year. The two largest promotions by spend (Brevex BOGO in January and Relivia 30% off in June) had ROIs of "
      "0.61 and 0.74.")
    w("")
    w("### 7. Portfolio")
    w("| Brand | Category | YTD net sales ($M) | Var. vs PY | Comment |")
    w("|---|---|---:|---:|---|")
    w("| Relivia | Pain relief | 168.3 | +9.2% | Strong season, shelf gains |")
    w("| Brevex | Cold & flu | 121.7 | +3.4% | Value packs under pressure |")
    w("| Digestia | Digestive | 84.7 | -12.1% | Private label gap, MegaMart delisting |")
    w("| Somnis (launch Mar-26) | Sleep | 6.1 | n/a | 38% of launch target ($16.0M) |")
    w("| Other | Various | 31.8 | +1.0% | |")
    w("")
    w("Somnis distribution reached 41% ACV versus a plan of 70% by September; repeat purchase rate among triers is 34%, "
      "in line with the category benchmark used in the launch plan.")
    w("")
    w("### 8. Customer service")
    w("On-time-in-full (OTIF) averaged 91.2% YTD against a 95.0% target (prior year: 94.1%). The main driver was a "
      "packaging supplier issue at the Columbus plant between April and July. Customer compliance fines totaled $1.9M "
      "YTD (prior year: $0.6M).")
    w("")
    w("### 9. Outlook")
    w("The current full-year forecast is $548M of net sales versus a budget of $556M (98.6%), assuming that Q4 sell-in "
      "continues at the run-rate of Q3. The forecast does not include any impact from customer inventory reductions.")
    w("")
    w("### 10. Conclusion")
    w("Overall, the year to date shows a solid performance in a challenging environment, with growth versus prior year, "
      "a strong Relivia season and good regional momentum in the Northeast and Southeast. The team remains committed to "
      "delivering the full-year plan.")
    w("")
    w("### Appendix A. Top SKUs (YTD net sales, $M)")
    w("| SKU | Brand | Net sales | Var. vs PY |")
    w("|---|---|---:|---:|")
    skus = [("Relivia 24ct", "Relivia", 41.2, 8.1), ("Relivia 100ct", "Relivia", 38.9, 12.4), ("Relivia Gel 2oz", "Relivia", 22.7, 6.0),
            ("Brevex Night 12ct", "Brevex", 29.4, 5.2), ("Brevex Day 24ct", "Brevex", 27.8, 4.1), ("Brevex Value 48ct", "Brevex", 18.3, -6.7),
            ("Digestia Chew 32ct", "Digestia", 24.1, -9.8), ("Digestia Liquid 8oz", "Digestia", 19.6, -14.2), ("Digestia Value 96ct", "Digestia", 15.2, -17.5),
            ("Somnis 30ct", "Somnis", 4.4, None), ("Somnis Gummies 60ct", "Somnis", 1.7, None)]
    for sku, brand, ns, v in skus:
        w(f"| {sku} | {brand} | {ns:.1f} | {'n/a' if v is None else f'{v:+.1f}%'} |")
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# 3. Data dictionary for dashboard spec
# --------------------------------------------------------------------------
def build_data_dictionary(dest: Path):
    dest.write_text("""# Available data — Brazil Consumer Health commercial team

| Source | Content | Grain | Refresh | Latency | Notes |
|---|---|---|---|---|---|
| ERP (SAP) | Sell-in: gross sales, discounts, net sales, units | SKU x customer x day | Daily | D+1 | Customers = chains, distributors, independents served directly |
| IQVIA | Sell-out: value and units at pharmacy level | SKU x channel x region x month | Monthly | ~4 weeks after month end | Covers ~82% of the pharmacy universe; independents projected |
| CRM (Salesforce) | Visits, coverage (positivação = outlets with >= 1 purchase in period), call plan compliance | Rep x outlet x visit | Daily | D+1 | Outlet master has ~18% duplicates under cleanup |
| Retail audit (vendor) | Out-of-stock (ruptura) on shelf | SKU x store, sample of 400 stores | Biweekly | 1 week | Sample skewed to large chains in Southeast |
| Price scan (vendor) | Shelf price vs. competitors | SKU x store sample | Weekly | 1 week | 120 SKUs monitored |
| Finance (BPC) | Trade spend / promotional budget, contribution margin | Brand x channel x month | Monthly | Close + 6 working days | Budget and forecast available |

Targets exist for net sales, coverage (75%) and trade spend (cap 8.5% of gross sales). No formal target for OOS; the team uses 5% informally.
""", encoding="utf-8")


# --------------------------------------------------------------------------
# 5. Weak English deck to improve
# --------------------------------------------------------------------------
def build_weak_deck(dest: Path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    _title_slide(prs, "Q3 Business Review", "Specialty Ingredients Division | Prepared by the Commercial Team")

    s = _content_slide(prs, "Agenda")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5),
                 ["Background", "Sales Overview", "Market Data", "Regional Performance", "Customer Feedback", "Challenges", "Next Steps"], 20)

    s = _content_slide(prs, "Background")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5), [
        "The Specialty Ingredients Division was created in 2014 through the merger of two business units and today serves "
        "food, beverage and nutrition customers in 31 countries from three plants. The division has a long history of "
        "innovation and customer intimacy, and the team continues to work hard to deliver value to our customers in a "
        "dynamic and challenging market environment. The market for specialty ingredients is large and growing, and we "
        "believe the division is well positioned to capture opportunities going forward.",
    ], 16)

    s = _content_slide(prs, "Sales Overview")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5.5), [
        "Revenue was $86.2M in Q3", "This compares to $84.9M in Q2", "Q3 last year revenue was $88.7M",
        "Gross margin was 23.4%", "Gross margin last year was 27.9%", "Volume was 41,300 tonnes (Q3 last year: 40,100 tonnes)",
        "Pricing was broadly stable", "Raw material costs increased", "Mix was slightly negative", "EMEA was weaker",
    ], 18)

    s = _content_slide(prs, "Market Data")
    cd = CategoryChartData()
    regions = ["North America", "EMEA", "LATAM", "China", "SE Asia", "India", "Japan/Korea", "Oceania"]
    cd.categories = regions
    cd.add_series("Q3 revenue ($M)", (31.4, 22.8, 9.7, 7.9, 5.6, 4.1, 3.2, 1.5))
    gf = s.shapes.add_chart(XL_CHART_TYPE.PIE, Inches(0.7), Inches(1.5), Inches(7.5), Inches(5.5), cd)
    gf.chart.has_legend = True
    gf.chart.legend.position = XL_LEGEND_POSITION.RIGHT
    _make_pie_3d(gf.chart)
    _add_bullets(s, Inches(8.5), Inches(2), Inches(4.3), Inches(4), [
        "Market grew 3% in Q3", "North America is our biggest region", "Competition remains intense",
        "The market is large and growing (see Background)",
    ], 16)

    s = _content_slide(prs, "Regional Performance")
    rows = [["Region", "Rev Q3 ($M)", "Rev Q3 PY", "GM% Q3", "GM% PY", "Vol (kt)", "Vol PY (kt)"],
            ["North America", "31.4", "31.0", "25.1%", "28.4%", "15.2", "14.6"],
            ["EMEA", "22.8", "25.6", "19.8%", "26.0%", "10.9", "11.1"],
            ["LATAM", "9.7", "9.5", "22.3%", "27.7%", "4.6", "4.4"],
            ["China", "7.9", "8.1", "24.9%", "28.8%", "3.9", "3.8"],
            ["SE Asia", "5.6", "5.4", "26.2%", "29.5%", "2.7", "2.5"],
            ["India", "4.1", "3.9", "24.0%", "27.1%", "2.0", "1.9"],
            ["Japan/Korea", "3.2", "3.6", "27.5%", "31.2%", "1.4", "1.3"],
            ["Oceania", "1.5", "1.6", "21.0%", "25.9%", "0.6", "0.5"]]
    _table(s, rows, Inches(0.5), Inches(1.5), Inches(12.3), Inches(4.8), size=13)

    s = _content_slide(prs, "Customer Feedback")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5), [
        "\"Service levels have improved since Q2\" — key account, North America",
        "\"Your prices are higher than Competitor X in EMEA\" — distributor, Germany",
        "\"We value the technical support\" — global beverage customer",
        "NPS was 41 (Q2: 38)",
    ], 18)

    s = _content_slide(prs, "Challenges")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5), [
        "Raw material costs up 14% year over year; price increases only partly passed through (+2%)",
        "Private-label supply contract with Brandt Foods priced below cost since Q1 (loses ~$1.4M per year at current volumes)",
        "Plant 2 utilization at 64%",
        "Competitor X price cuts in EMEA",
    ], 18)

    s = _content_slide(prs, "Next Steps")
    _add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5), [
        "Continue monitoring the market", "Review pricing", "Improve internal communication",
        "Consider options for the Brandt contract (exit frees 6,800 t of Plant 2 capacity; 90-day notice must be given by Dec 31 to avoid automatic renewal for 2027)",
        "Follow up with customers",
    ], 18)

    s = _content_slide(prs, "Thank You — Questions?")
    prs.save(dest)


# --------------------------------------------------------------------------
# 7. Monthly KPI CSV for the HTML dashboard
# --------------------------------------------------------------------------
def build_monthly_kpis(dest: Path):
    months = [f"2026-{m:02d}" for m in range(1, 10)]
    channels = {  # base net sales $M per month, growth drift
        "Retail chains": (21.0, 0.012), "Independent pharmacies": (9.4, -0.004), "E-commerce": (5.1, 0.031)}
    rows = []
    for i, m in enumerate(months):
        for ch, (base, drift) in channels.items():
            ns = round(base * (1 + drift) ** i * (1.06 if m in ("2026-01", "2026-02") and ch == "Retail chains" else 1.0), 2)
            bud = round(base * (1.01) ** i * 1.02, 2)
            py = round(base * (0.985) ** i * 0.97, 2)
            gm = round({"Retail chains": 41.5, "Independent pharmacies": 46.0, "E-commerce": 38.2}[ch] - 0.18 * i, 1)
            gmb = {"Retail chains": 42.0, "Independent pharmacies": 46.5, "E-commerce": 39.0}[ch]
            otif = round({"Retail chains": 93.5, "Independent pharmacies": 95.2, "E-commerce": 97.1}[ch] - (2.4 if m in ("2026-05", "2026-06", "2026-07") else 0), 1)
            dso = round({"Retail chains": 52, "Independent pharmacies": 38, "E-commerce": 21}[ch] + 0.9 * i, 1)
            inv = round({"Retail chains": 5.1, "Independent pharmacies": 3.2, "E-commerce": 2.4}[ch] + 0.17 * i, 2)
            compl = {"Retail chains": 14, "Independent pharmacies": 9, "E-commerce": 22}[ch] + (i % 3) + (6 if m == "2026-06" else 0)
            rows.append({"month": m, "channel": ch, "net_sales_musd": ns, "net_sales_budget_musd": bud, "net_sales_py_musd": py,
                         "gross_margin_pct": gm, "gross_margin_budget_pct": gmb, "otif_pct": otif, "otif_target_pct": 95.0,
                         "dso_days": dso, "dso_target_days": {"Retail chains": 50, "Independent pharmacies": 40, "E-commerce": 25}[ch],
                         "inventory_weeks": inv, "customer_complaints": compl})
    with dest.open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)


# --------------------------------------------------------------------------
# 8. Incomplete regional KPI CSV
# --------------------------------------------------------------------------
def build_incomplete_csv(dest: Path):
    rows = [
        # region, month, net_sales, target, net_sales_py, gm, otif
        ("Central", "2026-08", 14.2, 14.0, 13.5, 38.1, 95.4), ("Central", "2026-09", 14.9, 14.5, 13.9, 38.4, 96.0), ("Central", "2026-10", 15.3, 15.0, 14.6, 37.9, 95.1),
        ("East", "2026-08", 18.7, 19.5, 18.1, 35.2, 92.3), ("East", "2026-09", 19.1, 19.8, 18.4, 35.0, 91.8), ("East", "2026-10", None, 20.1, 18.9, None, None),
        ("North", "2026-08", 9.8, 10.2, 9.9, 33.7, 94.0), ("North", "2026-10", 10.1, None, 10.4, 33.1, 93.2),
        ("South", "2026-08", 12.4, 12.0, 11.6, 36.8, 96.5), ("South", "2026-09", 12.9, 12.4, 11.9, 36.5, 96.9), ("South", "2026-10", 13.6, 12.8, 12.2, 143.0, 97.2),
        ("West", "2026-08", 6.1, 6.5, None, 31.2, 90.4), ("West", "2026-09", 6.6, 6.8, None, 31.9, 91.1), ("West", "2026-10", 7.2, 7.0, None, 32.4, 92.0),
    ]
    with dest.open("w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["region", "month", "net_sales_musd", "target_musd", "net_sales_py_musd", "gross_margin_pct", "otif_pct"])
        for r in rows:
            wr.writerow(["" if v is None else v for v in r])


# --------------------------------------------------------------------------
# 9-11. Pricing workbook for the briefing cases
# --------------------------------------------------------------------------
def build_pricing_xlsx(dest: Path):
    wb = Workbook()
    ws = wb.active
    ws.title = "SKUs"
    ws.append(["sku", "brand", "category", "list_price_2026_usd", "proposed_increase_2027_pct", "units_2026_k",
               "est_price_elasticity", "price_index_vs_main_competitor", "private_label_gap_pct"])
    data = [
        ("REL-24", "Relivia", "Pain relief", 8.99, 5.0, 4620, -0.6, 104, 34),
        ("REL-100", "Relivia", "Pain relief", 17.49, 6.0, 2210, -0.7, 101, 36),
        ("REL-GEL", "Relivia", "Pain relief", 11.29, 4.0, 2010, -0.5, 97, 28),
        ("BRE-N12", "Brevex", "Cold & flu", 9.79, 4.5, 3000, -0.8, 106, 31),
        ("BRE-D24", "Brevex", "Cold & flu", 12.49, 4.5, 2230, -0.9, 108, 33),
        ("BRE-V48", "Brevex", "Cold & flu", 15.99, 3.0, 1140, -1.4, 112, 41),
        ("DIG-C32", "Digestia", "Digestive", 10.99, 0.0, 2190, -1.6, 115, 38),
        ("DIG-L8", "Digestia", "Digestive", 9.49, 0.0, 2070, -1.5, 113, 37),
        ("DIG-V96", "Digestia", "Digestive", 19.99, -3.0, 760, -1.9, 118, 45),
        ("SOM-30", "Somnis", "Sleep", 14.99, 0.0, 290, -1.1, 99, None),
    ]
    for row in data:
        ws.append(list(row))
    a = wb.create_sheet("Assumptions")
    a.append(["assumption", "value", "source"])
    a.append(["COGS inflation 2027", "5.5%", "Procurement outlook, Sep 2026"])
    a.append(["Category price inflation 2027 (expected)", "3.0%", "Market intelligence estimate"])
    a.append(["Elasticity estimates", "Econometric model on 2022-2026 scanner data", "Revenue management team; confidence interval +/-0.3"])
    a.append(["Retailer acceptance risk", "Two top-5 chains historically delay increases above 5% by ~8 weeks", "Key account managers"])
    wb.save(dest)


def main():
    out = {
        "translate-pt-board-deck": ("apresentacao_resultados_3T26.pptx", build_pt_deck),
        "dense-report-to-narrative": ("commercial_performance_report_sep2026.md", build_dense_report),
        "director-dashboard-spec": ("available_data.md", build_data_dictionary),
        "improve-weak-deck": ("q3_business_review.pptx", build_weak_deck),
        "dashboard-html-directors": ("monthly_kpis.csv", build_monthly_kpis),
        "incomplete-data-summary": ("regional_kpis_oct2026.csv", build_incomplete_csv),
        "briefing-answers-all": ("pricing_2027.xlsx", build_pricing_xlsx),
        "briefing-audience-only": ("pricing_2027.xlsx", build_pricing_xlsx),
        "briefing-use-defaults": ("pricing_2027.xlsx", build_pricing_xlsx),
    }
    for case, (fname, fn) in out.items():
        d = EVALS / case / "files"
        d.mkdir(parents=True, exist_ok=True)
        fn(d / fname)
        print(f"wrote {d / fname}")


if __name__ == "__main__":
    main()
