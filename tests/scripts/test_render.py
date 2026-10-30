"""Tests for render.py. Rendering tests are skipped when LibreOffice / poppler / Node+Playwright are absent."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import _helpers as h
import render

HAVE_OFFICE = bool(shutil.which("soffice") or shutil.which("libreoffice")) and bool(shutil.which("pdftoppm"))


def _have_playwright() -> bool:
    node = shutil.which("node")
    if not node:
        return False
    try:
        env = render.node_env()
        return subprocess.run([node, "-e", "require('playwright')"], capture_output=True, env=env, timeout=60).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


HAVE_PLAYWRIGHT = _have_playwright()

CLIP_PAGE = """<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clip test</title></head><body>
<h1>Dashboard</h1>
<div id="clipped-card" class="card" style="width:200px;overflow:hidden;border:1px solid #ccc">
  <table style="width:600px"><tr><td>Scorecard column one</td><td>Scorecard column two</td><td>Scorecard column three</td></tr></table>
</div>
<div id="scroll-wrap" class="scroller" style="width:200px;overflow-x:auto;border:1px solid #ccc">
  <table style="width:600px"><tr><td>Scrolling table A</td><td>Scrolling table B</td><td>Scrolling table C</td></tr></table>
</div>
<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)">visually hidden label</span>
</body></html>"""

ERROR_PAGE = """<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Broken</title></head><body><h1>Hello</h1>
<script>console.error("deliberate console error");
setTimeout(function () { throw new Error("deliberate uncaught"); }, 20);
undefinedFunctionCall();</script>
<img src="missing-image.png" alt="missing"></body></html>"""

OVERFLOW_PAGE = """<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wide</title></head><body><div id="wide" style="width:900px;height:20px;background:#ccc">wide block</div></body></html>"""


SCROLL_PAGE = """<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Scroll test</title></head><body>
<h1>Scorecards</h1>
<div id="wide-wrap" class="tbl-wrap" style="width:600px;overflow-x:auto;border:1px solid #ccc">
  <table style="width:900px"><tr><td>Wide scorecard A</td><td>Wide scorecard B</td><td>Wide scorecard C</td></tr></table>
</div>
<div id="fits-wrap" class="tbl-wrap" style="width:600px;overflow-x:auto;border:1px solid #ccc">
  <table style="width:300px"><tr><td>Fitting scorecard</td></tr></table>
</div>
<div id="tall-table-wrap" style="height:40px;overflow-y:auto"><table><tr><td>row</td></tr><tr><td>row</td></tr><tr><td>row</td></tr><tr><td>row</td></tr></table></div>
<div id="small-box" style="height:60px;overflow-y:auto"><div style="height:80px">20px of hidden height: noise</div></div>
<div id="big-box" style="height:60px;overflow-y:auto"><div style="height:200px">140px of hidden height</div></div>
</body></html>"""

BASELINE_DASHBOARD = Path("/home/user/dwmt-workspace/baseline/dashboard-html-directors/without_skill/work/commercial_dashboard.html")


class ParsePages(unittest.TestCase):
    def test_valid_specs(self):
        self.assertEqual(render.parse_pages(None), [])
        self.assertEqual(render.parse_pages("3"), [(3, 3)])
        self.assertEqual(render.parse_pages("1-5"), [(1, 5)])
        self.assertEqual(render.parse_pages("7-9,1,3"), [(1, 1), (3, 3), (7, 9)])
        self.assertEqual(render.parse_pages("4-"), [(4, None)])

    def test_invalid_specs(self):
        for bad in ("0", "a", "5-2", "1,,2", "-3"):
            with self.assertRaises(ValueError, msg=bad):
                render.parse_pages(bad)


@unittest.skipUnless(HAVE_OFFICE, "needs soffice and pdftoppm")
class OfficeRendering(unittest.TestCase):
    def test_weak_deck_renders_one_png_per_slide(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = h.run_script("render.py", h.WEAK_DECK, "--out", tmp, "--json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            self.assertEqual(len(data["images"]), 10)
            self.assertEqual(data["pages_total"], 10)
            for image in data["images"]:
                self.assertTrue(Path(image).is_file())
                self.assertTrue(Path(image).read_bytes().startswith(b"\x89PNG"))
                self.assertNotIn("\\", image)
            self.assertTrue(Path(data["pdf"]).is_file())

    def test_pages_option_limits_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = json.loads(h.run_script("render.py", h.WEAK_DECK, "--out", tmp, "--pages", "2-3,9-", "--json").stdout)
            self.assertEqual([Path(p).name[-6:] for p in data["images"]], ["02.png", "03.png", "09.png", "10.png"])

    def test_default_output_folder_is_render_next_to_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp) / "deck.pptx"
            shutil.copyfile(h.WEAK_DECK, deck)
            proc = h.run_script("render.py", deck, "--pages", "1")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue((Path(tmp) / "render" / "deck-01.png").is_file())

    def test_rerun_removes_stale_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            h.run_script("render.py", h.WEAK_DECK, "--out", tmp, "--pages", "1-4")
            h.run_script("render.py", h.WEAK_DECK, "--out", tmp, "--pages", "1-2")
            names = sorted(p.name for p in Path(tmp).glob("*.png"))
            self.assertEqual(names, ["q3_business_review-01.png", "q3_business_review-02.png"])

    def test_docx_and_xlsx_render(self):
        import docx
        with tempfile.TemporaryDirectory() as tmp:
            document = docx.Document()
            document.add_paragraph("Hello render")
            path = Path(tmp) / "d.docx"
            document.save(path)
            for source in (path, h.PRICING_XLSX):
                proc = h.run_script("render.py", source, "--out", tmp, "--json")
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertGreaterEqual(len(json.loads(proc.stdout)["images"]), 1)

    def test_pdf_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = json.loads(h.run_script("render.py", h.WEAK_DECK, "--out", tmp, "--json").stdout)
            out2 = Path(tmp) / "again"
            data = json.loads(h.run_script("render.py", first["pdf"], "--out", out2, "--pages", "1-2", "--json").stdout)
            self.assertEqual(len(data["images"]), 2)


class DegradesGracefully(unittest.TestCase):
    def run_without_tools(self, source):
        env = dict(os.environ, PATH=str(Path(tempfile.gettempdir()) / "no-such-bin-dir"))
        with tempfile.TemporaryDirectory() as tmp:
            return h.run_script("render.py", source, "--out", tmp, env=env)

    def test_missing_soffice_is_named_and_exit_1(self):
        proc = self.run_without_tools(h.WEAK_DECK)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("soffice", proc.stderr)
        self.assertIn("nothing was rendered", proc.stderr)

    def test_missing_node_is_named_and_exit_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "p.html"
            page.write_text(OVERFLOW_PAGE, encoding="utf-8")
            proc = self.run_without_tools(page)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("node", proc.stderr)

    def test_usage_errors_exit_1(self):
        self.assertEqual(h.run_script("render.py", "/nonexistent.pptx").returncode, 1)
        proc = h.run_script("render.py", h.WEAK_DECK, "--pages", "x")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("--pages", proc.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            odd = Path(tmp) / "x.xyz"
            odd.write_text("hi")
            self.assertEqual(h.run_script("render.py", odd).returncode, 1)


@unittest.skipUnless(HAVE_PLAYWRIGHT, "needs node with the playwright package and Chromium")
class HtmlRendering(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def render(self, html: str):
        page = self.tmp / "page.html"
        page.write_text(html, encoding="utf-8")
        proc = h.run_script("render.py", page, "--out", self.tmp / "out", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)  # problems never fail the run
        return json.loads(proc.stdout)

    def test_js_errors_are_reported_and_screenshots_taken(self):
        data = self.render(ERROR_PAGE)
        self.assertEqual(len(data["images"]), 2)
        self.assertTrue(all(Path(p).read_bytes().startswith(b"\x89PNG") for p in data["images"]))
        names = [Path(p).name for p in data["images"]]
        self.assertEqual(names, ["page-desktop.png", "page-mobile.png"])
        joined = "\n".join(data["problems"])
        self.assertIn("console error: deliberate console error", joined)
        self.assertIn("uncaught exception", joined)
        self.assertIn("deliberate uncaught", joined)
        self.assertIn("undefinedFunctionCall", joined)
        self.assertIn("missing-image.png", joined)            # failed request and broken image
        desktop, mobile = data["html"]
        self.assertEqual((desktop["name"], mobile["name"]), ("desktop", "mobile"))
        self.assertEqual((desktop["metrics"]["viewportWidth"], mobile["metrics"]["viewportWidth"]), (1440, 390))

    def test_text_output_leads_with_problems(self):
        page = self.tmp / "p.html"
        page.write_text(ERROR_PAGE, encoding="utf-8")
        out = h.run_script("render.py", page, "--out", self.tmp / "o").stdout
        self.assertIn("PROBLEMS FOUND", out)
        self.assertIn("deliberate console error", out)

    def test_clean_page_reports_no_problems(self):
        data = self.render("<!doctype html><html><head><meta name='viewport' content='width=device-width'>"
                           "<title>ok</title></head><body><h1>Fine</h1><p>Text</p></body></html>")
        self.assertEqual(data["problems"], [])
        self.assertEqual(data["html"][0]["metrics"]["horizontalOverflow"], False)

    def test_horizontal_overflow_detected_on_mobile_only(self):
        data = self.render(OVERFLOW_PAGE)
        desktop, mobile = (v["metrics"] for v in data["html"])
        self.assertFalse(desktop["horizontalOverflow"])
        self.assertTrue(mobile["horizontalOverflow"])
        self.assertGreaterEqual(mobile["scrollWidth"], 900)
        self.assertTrue(any("wide" in o["element"] for o in mobile["offenders"]))
        self.assertTrue(any("[mobile] horizontal overflow" in p for p in data["problems"]))

    def test_clipped_container_flagged_but_scroll_container_is_not(self):
        data = self.render(CLIP_PAGE)
        for viewport in data["html"]:
            clipped = viewport["metrics"]["clipped"]
            descriptors = [c["element"] for c in clipped]
            self.assertTrue(any(d.startswith("div#clipped-card.card") for d in descriptors), descriptors)
            card = next(c for c in clipped if c["element"].startswith("div#clipped-card"))
            self.assertGreater(card["overflowXpx"], 300)
            self.assertIn("Scorecard column one", card["element"])
            self.assertFalse(any("scroll-wrap" in d for d in descriptors), "overflow:auto is intentional")
            self.assertFalse(any("visually hidden" in d for d in descriptors), "1px sr-only boxes are skipped")
            self.assertFalse(viewport["metrics"]["horizontalOverflow"], "the page itself does not overflow")
        self.assertTrue(any("clipped content: div#clipped-card" in p for p in data["problems"]))

    def test_clipped_list_is_capped_at_20(self):
        boxes = "".join(f'<div style="width:50px;overflow:hidden;white-space:nowrap">item number {i} is quite long text</div>'
                        for i in range(30))
        data = self.render(f"<!doctype html><html><head><meta name='viewport' content='width=device-width'></head>"
                           f"<body>{boxes}</body></html>")
        metrics = data["html"][0]["metrics"]
        self.assertEqual(len(metrics["clipped"]), 20)
        self.assertEqual(metrics["clippedTotal"], 30)

    def test_scroll_needed_is_reported_for_desktop_only_and_is_informational(self):
        data = self.render(SCROLL_PAGE)  # render() asserts exit code 0
        desktop, mobile = data["html"]
        needed = [item["element"] for item in desktop["metrics"]["scrollNeeded"]]
        self.assertTrue(any(e.startswith("div#wide-wrap.tbl-wrap") and "Wide scorecard A" in e for e in needed), needed)
        wide = next(i for i in desktop["metrics"]["scrollNeeded"] if "wide-wrap" in i["element"])
        self.assertEqual(wide["hiddenXpx"], 300)
        self.assertFalse(any("fits-wrap" in e for e in needed), "a table that fits is not reported")
        self.assertTrue(any("tall-table-wrap" in e for e in needed), "vertical scroll in a table wrapper is reported")
        self.assertTrue(any("big-box" in e for e in needed), "more than 40px hidden vertically is reported")
        self.assertFalse(any("small-box" in e for e in needed), "20px of hidden height in a plain box is noise")
        self.assertEqual(mobile["metrics"]["scrollNeeded"], [], "sideways table scroll is normal on phones")
        self.assertEqual(mobile["metrics"]["scrollNeededTotal"], 0)
        self.assertEqual(data["problems"], [], "scroll-needed notes are informational, not problems")
        self.assertIn("3 containers need scrolling at desktop width to show all content", data["info"])

    def test_scroll_needed_summary_and_section_in_text_output(self):
        page = self.tmp / "s.html"
        page.write_text("<!doctype html><html><head><meta name='viewport' content='width=device-width'></head><body>"
                        "<div class='tbl-wrap' style='width:600px;overflow-x:auto'><table style='width:900px'>"
                        "<tr><td>Wide scorecard</td></tr></table></div></body></html>", encoding="utf-8")
        proc = h.run_script("render.py", page, "--out", self.tmp / "o")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("1 container needs horizontal scrolling at desktop width", proc.stdout)
        self.assertIn("Scroll needed to see content (desktop)", proc.stdout)
        self.assertIn("div.tbl-wrap", proc.stdout)
        self.assertIn("300px hidden horizontally", proc.stdout)
        self.assertNotIn("PROBLEMS FOUND", proc.stdout)

    def test_scroll_needed_list_is_capped_at_10(self):
        wraps = "".join("<div style='width:100px;overflow-x:auto'><div style='width:300px'>x</div></div>" for _ in range(14))
        data = self.render(f"<!doctype html><html><head><meta name='viewport' content='width=device-width'></head><body>{wraps}</body></html>")
        metrics = data["html"][0]["metrics"]
        self.assertEqual((len(metrics["scrollNeeded"]), metrics["scrollNeededTotal"]), (10, 14))

    @unittest.skipUnless(BASELINE_DASHBOARD.is_file(), "baseline dashboard not available")
    def test_baseline_dashboard_reports_the_channel_scorecard_wrapper(self):
        proc = h.run_script("render.py", BASELINE_DASHBOARD, "--out", self.tmp / "dash", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        desktop, mobile = data["html"]
        scorecard = [i for i in desktop["metrics"]["scrollNeeded"] if i["element"].startswith("div.tbl-wrap")
                     and "Channel" in i["element"] and "Net sales" in i["element"]]
        self.assertEqual(len(scorecard), 1, desktop["metrics"]["scrollNeeded"])
        self.assertGreater(scorecard[0]["hiddenXpx"], 0)
        self.assertEqual(mobile["metrics"]["scrollNeeded"], [])
        self.assertTrue(any("horizontal scrolling at desktop width" in note for note in data["info"]))

    def test_missing_viewport_meta_is_flagged_for_mobile(self):
        data = self.render("<!doctype html><html><head><title>x</title></head><body><p>hi</p></body></html>")
        self.assertTrue(any("no <meta name=\"viewport\">" in p for p in data["problems"]))


if __name__ == "__main__":
    unittest.main()
