"""Tests for doc_text.py: extraction from the real fixtures plus small synthetic files."""
import json
import tempfile
import unittest
from pathlib import Path

import _helpers as h
import doc_text


def by_location(units):
    return {u["location"]: u for u in units}


class FixtureExtraction(unittest.TestCase):
    def test_weak_deck_titles_and_filler_slides(self):
        titles = doc_text.slide_titles(h.WEAK_DECK)
        self.assertEqual(len(titles), 10)
        self.assertEqual(titles[0], {"slide": 1, "title": "Q3 Business Review"})
        self.assertEqual([t["title"] for t in titles[1:4]], ["Agenda", "Background", "Sales Overview"])
        self.assertEqual(titles[-1]["title"], "Thank You — Questions?")

    def test_weak_deck_3d_pie_chart_does_not_crash_and_is_read_from_xml(self):
        units, warnings = doc_text.extract_with_warnings(h.WEAK_DECK)
        chart = by_location(units)["slide 5 / chart"]
        self.assertEqual(chart["kind"], "chart")
        for expected in ("North America", "Oceania", "Q3 revenue ($M)", "31.4", "1.5"):
            self.assertIn(expected, chart["text"])
        self.assertNotIn("unparsed", chart["text"])
        self.assertEqual(warnings, [])

    def test_chart_values_are_flagged_as_machine_numbers(self):
        chart = by_location(doc_text.extract_units(h.WEAK_DECK))["slide 5 / chart"]
        spans = chart["machine_spans"]
        self.assertTrue(spans)
        start, end = spans[0]
        self.assertEqual(chart["text"][start:end], "31.4 | 22.8 | 9.7 | 7.9 | 5.6 | 4.1 | 3.2 | 1.5")

    def test_weak_deck_table_bullets_and_kinds(self):
        units = by_location(doc_text.extract_units(h.WEAK_DECK))
        self.assertEqual(units["slide 6 / table r1c2"]["text"], "Rev Q3 ($M)")
        self.assertEqual(units["slide 6 / table r3c2"]["text"], "22.8")
        self.assertEqual(units["slide 6 / table r3c2"]["kind"], "table")
        body = units["slide 4 / body"]
        self.assertEqual(body["kind"], "body")
        self.assertEqual(len(body["paragraphs"]), 10)
        self.assertEqual(body["text"].split("\n")[0], "Revenue was $86.2M in Q3")
        self.assertEqual(units["slide 4 / title"]["kind"], "title")

    def test_pt_deck_chart_table_and_notes(self):
        units = by_location(doc_text.extract_units(h.PT_DECK))
        self.assertEqual(units["slide 3 / table r2c2"]["text"], "21,4")
        self.assertEqual(units["slide 3 / table r6c1"]["text"], "Total")
        chart = units["slide 4 / chart"]["text"]
        self.assertIn("Categories: Sudeste | Sul | Centro-Oeste | Nordeste | Norte", chart)
        self.assertIn('Series "Positivação 3T26 (%)": 74.8 | 72.1 | 69 | 66.4 | 61.7', chart)
        self.assertEqual(units["slide 1 / notes"]["kind"], "notes")
        self.assertIn("board global", units["slide 1 / notes"]["text"])
        self.assertIn("Positivação = % dos PDVs", units["slide 4 / notes"]["text"])
        self.assertIn("IQVIA", units["slide 5 / body 2"]["text"])  # slide 5 has two text boxes

    def test_markdown_keeps_table_rows_and_headings(self):
        units = doc_text.extract_units(h.REPORT_MD)
        locs = by_location(units)
        self.assertEqual(locs["line 4"]["kind"], "heading")
        self.assertEqual(locs["line 4"]["text"], "1. Introduction")
        row = locs["line 14"]
        self.assertEqual(row["kind"], "line")
        self.assertTrue(row["text"].startswith("| Northeast | 78.4 |"))
        self.assertFalse(any(set(u["text"]) <= set("|-: ") for u in units), "table separator rows are noise")

    def test_xlsx_cells_with_numbers(self):
        units = by_location(doc_text.extract_units(h.PRICING_XLSX))
        self.assertEqual(units["SKUs!A1"]["text"], "sku")
        self.assertEqual(units["SKUs!A2"]["text"], "REL-24")
        self.assertEqual(units["SKUs!D2"]["text"], "8.99")
        self.assertEqual(units["SKUs!G2"]["text"], "-0.6")
        self.assertEqual(units["SKUs!D2"]["machine_spans"], [[0, 4]])
        self.assertIn("Assumptions!B2", units)
        self.assertEqual(units["Assumptions!B2"]["text"], "5.5%")
        self.assertNotIn("machine_spans", units["Assumptions!B2"])  # text cell, not a numeric one

    def test_csv_fixture_rows(self):
        units = doc_text.extract_units(h.KPI_CSV)
        self.assertEqual(units[0]["location"], "row 1")
        self.assertTrue(units[0]["text"].startswith("month | channel | net_sales_musd"))
        self.assertTrue(units[1]["text"].startswith("2026-01 | Retail chains | 22.26"))


class SyntheticFiles(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_pptx_group_shapes_are_walked_recursively(self):
        from pptx import Presentation
        from pptx.util import Inches
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.title.text = "Grouped content"
        group = slide.shapes.add_group_shape()
        group.shapes.add_textbox(Inches(1), Inches(2), Inches(3), Inches(1)).text_frame.text = "Inside the group"
        nested = group.shapes.add_group_shape()
        nested.shapes.add_textbox(Inches(1), Inches(3), Inches(3), Inches(1)).text_frame.text = "Nested group text"
        path = self.tmp / "g.pptx"
        prs.save(path)
        text = " ".join(u["text"] for u in doc_text.extract_units(path))
        self.assertIn("Inside the group", text)
        self.assertIn("Nested group text", text)

    def test_docx_paragraphs_headings_and_tables(self):
        import docx
        document = docx.Document()
        document.add_heading("Report title", 0)
        document.add_heading("Section", 1)
        document.add_paragraph("Normal paragraph with 5.2% growth.")
        table = document.add_table(rows=2, cols=3)
        for c, label in enumerate("ABC"):
            table.cell(0, c).text = label
        table.cell(1, 0).text = "1"
        table.cell(1, 1).merge(table.cell(1, 2)).text = "merged"
        path = self.tmp / "d.docx"
        document.save(path)
        units = by_location(doc_text.extract_units(path))
        self.assertEqual((units["paragraph 1"]["kind"], units["paragraph 2"]["kind"], units["paragraph 3"]["kind"]),
                         ("title", "heading", "body"))
        self.assertEqual(units["table 1 r2c2"]["text"], "merged")
        self.assertNotIn("table 1 r2c3", units)  # merged cell is reported once

    def test_html_visible_text_only_with_attributes(self):
        html = self.tmp / "p.html"
        html.write_text(
            "<!doctype html><html><head><title>Q3 &amp; Results</title><style>.x{color:red}</style>"
            "<script>var secret='HIDDEN_SCRIPT_TEXT';</script></head><body>"
            "<h1>Revenue grew <em>6.2%</em></h1><p>Para <a title=\"Source: IQVIA\" href=#>link</a> text"
            "<div hidden>HIDDEN_ATTR</div><div style=\"display:none\">HIDDEN_STYLE</div>"
            "<button aria-label=\"Close dialog\">X</button><noscript>NOSCRIPT_TEXT</noscript>"
            "<table><tr><th>Region</th><th>Rev</th></tr><tr><td>NA</td><td>31,4</td></tr></table></body></html>",
            encoding="utf-8")
        units = doc_text.extract_units(html)
        joined = " | ".join(u["text"] for u in units)
        for hidden in ("HIDDEN_SCRIPT_TEXT", "HIDDEN_ATTR", "HIDDEN_STYLE", "NOSCRIPT_TEXT", "color:red"):
            self.assertNotIn(hidden, joined)
        locs = by_location(units)
        self.assertEqual(locs["html / title"]["text"], "Q3 & Results")
        heading = next(u for u in units if u["kind"] == "heading")
        self.assertEqual(heading["text"], "Revenue grew 6.2%")
        self.assertIn("Source: IQVIA", joined)
        self.assertIn("Close dialog", joined)
        self.assertEqual(locs["html / table 1 r2c2"]["text"], "31,4")
        order = [u["text"] for u in units]
        self.assertLess(order.index("Revenue grew 6.2%"), order.index("Close dialog"))

    def test_csv_semicolon_delimiter_and_cp1252_encoding(self):
        path = self.tmp / "br.csv"
        path.write_bytes("mês;valor\njaneiro;1.234,5\n".encode("cp1252"))
        units = doc_text.extract_units(path)
        self.assertEqual(units[0]["text"], "mês | valor")
        self.assertEqual(units[1]["text"], "janeiro | 1.234,5")

    def test_language_detection(self):
        self.assertEqual(doc_text.detect_language("O faturamento cresceu em relação ao ano anterior e a margem caiu"), "pt")
        self.assertEqual(doc_text.detect_language("Revenue grew compared with the prior year and margin fell"), "en")
        self.assertEqual(doc_text.detect_language(""), "en")


class Cli(unittest.TestCase):
    def test_text_output_format(self):
        proc = h.run_script("doc_text.py", h.WEAK_DECK)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("[slide 4 / title] Sales Overview", proc.stdout)
        self.assertIn("[slide 4 / body] Revenue was $86.2M in Q3\n    This compares to $84.9M in Q2", proc.stdout)

    def test_json_output_is_valid(self):
        proc = h.run_script("doc_text.py", h.PT_DECK, "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["format"], "pptx")
        self.assertTrue(all({"location", "kind", "text"} <= set(u) for u in data["units"]))

    def test_titles_flag(self):
        proc = h.run_script("doc_text.py", h.WEAK_DECK, "--titles")
        self.assertEqual(proc.stdout.splitlines()[1], "2. Agenda")

    def test_errors_exit_1(self):
        self.assertEqual(h.run_script("doc_text.py", "/nonexistent/file.pptx").returncode, 1)
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "x.pdf"
            bad.write_bytes(b"%PDF")
            proc = h.run_script("doc_text.py", bad)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("Unsupported", proc.stderr)

    def test_help_documents_usage(self):
        proc = h.run_script("doc_text.py", "--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--json", proc.stdout)


if __name__ == "__main__":
    unittest.main()
