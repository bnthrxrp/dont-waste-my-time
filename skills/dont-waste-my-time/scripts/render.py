#!/usr/bin/env python3
"""render.py - visual QA helper: turn a deck, document, sheet, PDF or web page into PNGs you can look at.

Usage
-----
    python3 render.py FILE [--out DIR] [--pages 1-5] [--json]

    FILE     .pptx .docx .xlsx (also .ppt .doc .xls .odp .odt .ods .rtf), .pdf, .html/.htm
    --out    output folder (default: a "render/" folder next to FILE)
    --pages  pages/slides to render for office files and PDFs, e.g. "3", "1-5", "1,3,7-9", "4-"
             (ignored for HTML, which is one long page)
    --json   machine-readable output

How each type is rendered
-------------------------
* pptx/docx/xlsx: LibreOffice (`soffice --headless --convert-to pdf`, using a throw-away user
  profile so concurrent runs do not fight over profile locks), then `pdftoppm -png -r 80`.
  The PDF is kept next to the PNGs. Files: <name>-<page>.png.
* pdf: `pdftoppm` directly.
* html: Node + Playwright (Chromium) loads the file via file:// at 1440x900 (desktop) and
  390x844 (mobile, with touch/mobile emulation so <meta viewport> is honoured) and takes
  full-page screenshots <name>-desktop.png and <name>-mobile.png. It also collects:
    - console errors, uncaught page errors, failed requests (including HTTP >= 400) and broken images
    - horizontal overflow of the page: document scrollWidth vs viewport width, with the widest
      offending elements
    - CONTAINER CLIPPING: elements whose content is wider/taller than the box while overflow is
      hidden/clip (content cut off inside a card or table wrapper, which a page-level overflow
      check misses). overflow auto/scroll is treated as intentional and not reported. Up to 20
      per viewport, with a selector-ish descriptor, the first 40 characters of text and the
      overflow in px. Ellipsis / line-clamp truncation is marked as such.
    - a missing <meta name="viewport">, which makes phones render the page at ~980px wide
  HTML static checks only see what the page does at load time plus a short settle delay.

Missing tools are reported exactly (which tool, what was skipped). Exit codes: 0 rendering
succeeded (console errors etc. are reported prominently but do not change the exit code);
1 rendering failed or usage/IO error. The tool requirements: soffice (LibreOffice) for office
files, pdftoppm (poppler-utils) for PNGs from PDFs, node + the playwright package + Chromium for HTML.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PNG_DPI = 80                       # legible on screen, small enough to look at many pages
SOFFICE_TIMEOUT_S = 240            # first LibreOffice start with a fresh profile is slow
PDFTOPPM_TIMEOUT_S = 300
NODE_TIMEOUT_S = 180
VIEWPORTS = [("desktop", 1440, 900, False), ("mobile", 390, 844, True)]   # name, width, height, mobile emulation
MAX_CLIPPED_REPORTED = 20          # per viewport
MAX_OFFENDERS_REPORTED = 8         # widest elements when the page overflows horizontally
PAGE_SETTLE_MS = 800               # let charts/animations finish after the load event
NAVIGATION_TIMEOUT_MS = 30_000
OVERFLOW_TOLERANCE_PX = 1          # sub-pixel layout rounding

OFFICE_EXTENSIONS = {".pptx", ".docx", ".xlsx", ".ppt", ".doc", ".xls", ".odp", ".odt", ".ods", ".rtf"}
HTML_EXTENSIONS = {".html", ".htm"}

# Runs inside Node. Written to a temp file at run time; results go to a JSON file (not stdout) so
# stray console output from Playwright can never corrupt them.
NODE_SCRIPT = r"""
const fs = require('fs');
const [fileUrl, outPrefix, resultPath, viewportsJson, settleMs, navTimeout, clipLimit, offenderLimit, tolerance] = process.argv.slice(2);
function finish(result, code) { fs.writeFileSync(resultPath, JSON.stringify(result)); process.exit(code); }
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e1) {
  try { ({ chromium } = require('playwright-core')); }
  catch (e2) { finish({ fatal: "node cannot resolve the 'playwright' package: " + String(e1.message).split('\n')[0] }, 3); }
}

function measurePage(args) {
  const { clipLimit, offenderLimit, tol } = args;
  const de = document.documentElement, body = document.body;
  const vw = window.innerWidth;
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const describe = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    const cls = (typeof el.className === 'string' ? el.className : '').trim().split(/\s+/).filter(Boolean).slice(0, 2);
    if (cls.length) s += '.' + cls.join('.');
    const text = clean(el.innerText || el.textContent).slice(0, 40);
    return text ? s + ' "' + text + '"' : s;
  };
  const scrollWidth = Math.max(de.scrollWidth, body ? body.scrollWidth : 0);
  const result = {
    viewportWidth: vw,
    scrollWidth: scrollWidth,
    scrollHeight: Math.max(de.scrollHeight, body ? body.scrollHeight : 0),
    horizontalOverflow: scrollWidth > vw + tol,
    hasViewportMeta: !!document.querySelector('meta[name="viewport"]'),
    title: document.title,
    offenders: [], clipped: [], clippedTotal: 0, brokenImages: [],
  };

  const everything = [de].concat(body ? [body] : [], body ? Array.from(body.querySelectorAll('*')) : []);

  // Containers that cut their content off (overflow hidden/clip). auto/scroll scroll on purpose, so they pass.
  const clipped = [];
  for (const el of everything) {
    if (!(el instanceof HTMLElement)) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    // Skip collapsed or 1px boxes: visually-hidden labels and closed accordions clip by design.
    if (el.clientWidth <= 1 || el.clientHeight <= 1) continue;
    const hidesX = cs.overflowX === 'hidden' || cs.overflowX === 'clip';
    const hidesY = cs.overflowY === 'hidden' || cs.overflowY === 'clip';
    const x = hidesX ? el.scrollWidth - el.clientWidth : 0;
    const y = hidesY ? el.scrollHeight - el.clientHeight : 0;
    if (x > tol || y > tol) {
      const clamp = cs.webkitLineClamp && cs.webkitLineClamp !== 'none';
      clipped.push({
        element: describe(el),
        overflowXpx: x > tol ? x : 0,
        overflowYpx: y > tol ? y : 0,
        truncation: cs.textOverflow === 'ellipsis' ? 'text-overflow: ellipsis' : (clamp ? 'line-clamp' : ''),
      });
    }
  }
  clipped.sort((a, b) => Math.max(b.overflowXpx, b.overflowYpx) - Math.max(a.overflowXpx, a.overflowYpx));
  result.clippedTotal = clipped.length;
  result.clipped = clipped.slice(0, clipLimit);

  if (result.horizontalOverflow) {
    // Only elements that really push the page wider: not those inside a scrolling/clipping wrapper.
    const insideClipper = (el) => {
      for (let p = el.parentElement; p && p !== de && p !== body; p = p.parentElement) {
        const o = getComputedStyle(p).overflowX;
        if (o !== 'visible') return true;
      }
      return false;
    };
    const wide = [];
    for (const el of everything) {
      if (!(el instanceof HTMLElement) || el === de || el === body) continue;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.right <= vw + tol || insideClipper(el)) continue;
      wide.push({ element: describe(el), rightEdgePx: Math.round(r.right) });
    }
    wide.sort((a, b) => b.rightEdgePx - a.rightEdgePx);
    result.offenders = wide.slice(0, offenderLimit);
  }
  result.brokenImages = Array.from(document.images).filter((i) => i.complete && i.naturalWidth === 0 && i.src).map((i) => i.src).slice(0, 20);
  return result;
}

(async () => {
  let browser;
  try { browser = await chromium.launch(); }
  catch (e) { finish({ fatal: 'could not launch Chromium: ' + String(e.message).split('\n')[0] + " (try: npx playwright install chromium)" }, 4); }
  const viewports = JSON.parse(viewportsJson);
  const out = { viewports: [] };
  for (const vp of viewports) {
    const entry = { name: vp.name, width: vp.width, height: vp.height, consoleErrors: [], consoleWarnings: 0,
                    pageErrors: [], failedRequests: [], screenshot: null, metrics: null, error: null };
    try {
      const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: vp.mobile,
                                                  hasTouch: vp.mobile, deviceScaleFactor: 1 });
      const page = await context.newPage();
      page.on('console', (m) => {
        if (m.type() === 'error') entry.consoleErrors.push(m.text().slice(0, 300));
        else if (m.type() === 'warning') entry.consoleWarnings += 1;
      });
      page.on('pageerror', (e) => entry.pageErrors.push(String((e && e.stack) || e).split('\n').slice(0, 3).join(' | ').slice(0, 400)));
      page.on('requestfailed', (r) => entry.failedRequests.push({ url: r.url().slice(0, 200), failure: (r.failure() || {}).errorText || 'failed' }));
      page.on('response', (r) => { if (r.status() >= 400) entry.failedRequests.push({ url: r.url().slice(0, 200), failure: 'HTTP ' + r.status() }); });
      try { await page.goto(fileUrl, { waitUntil: 'load', timeout: Number(navTimeout) }); }
      catch (e) { entry.error = 'navigation: ' + String(e.message).split('\n')[0]; }
      await page.waitForTimeout(Number(settleMs));
      entry.metrics = await page.evaluate(measurePage, { clipLimit: Number(clipLimit), offenderLimit: Number(offenderLimit), tol: Number(tolerance) });
      const shot = outPrefix + '-' + vp.name + '.png';
      await page.screenshot({ path: shot, fullPage: true });
      entry.screenshot = shot;
      await context.close();
    } catch (e) { entry.error = String(e.message).split('\n')[0]; }
    out.viewports.push(entry);
  }
  await browser.close();
  finish(out, 0);
})().catch((e) => finish({ fatal: String(e && e.message || e).split('\n')[0] }, 5));
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class RenderError(Exception):
    """Rendering could not be completed; the message says what is missing or what failed."""


def find_tool(*names: str) -> str | None:
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def parse_pages(spec: str | None) -> list[tuple[int, int | None]]:
    """"1,3,5-7,9-" -> [(1,1),(3,3),(5,7),(9,None)] (None = to the last page)."""
    if not spec:
        return []
    runs: list[tuple[int, int | None]] = []
    for part in spec.split(","):
        part = part.strip()
        match = re.fullmatch(r"(\d+)(?:(-)(\d*))?", part)
        if not match or int(match.group(1)) < 1:
            raise ValueError(f"invalid --pages value {part!r}; use e.g. 3, 1-5, 1,3,7-9 or 4-")
        first = int(match.group(1))
        if match.group(2):
            last = int(match.group(3)) if match.group(3) else None
            if last is not None and last < first:
                raise ValueError(f"invalid --pages range {part!r}: end before start")
        else:
            last = first
        runs.append((first, last))
    return sorted(runs, key=lambda r: r[0])


def run(cmd: list[str], timeout: int, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)


def clear_previous(out_dir: Path, stem: str) -> None:
    """Remove PNGs from an earlier run of the same file so stale pages never look current."""
    pattern = re.compile(rf"^{re.escape(stem)}-(?:\d+|desktop|mobile)\.png$")
    for path in out_dir.iterdir():
        if pattern.match(path.name):
            path.unlink()


def pdf_page_count(pdf: Path) -> int | None:
    pdfinfo = find_tool("pdfinfo")
    if not pdfinfo:
        return None
    try:
        output = run([pdfinfo, str(pdf)], 60).stdout
    except (subprocess.TimeoutExpired, OSError):
        return None
    match = re.search(r"^Pages:\s+(\d+)", output, re.M)
    return int(match.group(1)) if match else None


def pdf_to_pngs(pdf: Path, out_dir: Path, stem: str, runs: list[tuple[int, int | None]], result: dict) -> None:
    pdftoppm = find_tool("pdftoppm")
    if not pdftoppm:
        raise RenderError("pdftoppm (poppler-utils) is not installed: PNG rendering skipped"
                          + (f"; the PDF was kept at {pdf.resolve().as_posix()}" if pdf.parent == out_dir else ""))
    total = pdf_page_count(pdf)
    result["pages_total"] = total
    for first, last in runs or [(1, None)]:
        if total is not None and first > total:
            result["warnings"].append(f"page {first} requested but the document has only {total} page(s); skipped")
            continue
        cmd = [pdftoppm, "-png", "-r", str(PNG_DPI), "-f", str(first)]
        if last is not None:
            cmd += ["-l", str(min(last, total) if total else last)]
        cmd += [str(pdf), str(out_dir / stem)]
        proc = run(cmd, PDFTOPPM_TIMEOUT_S)
        if proc.returncode != 0:
            raise RenderError(f"pdftoppm failed: {proc.stderr.strip() or 'unknown error'}")
    pngs = sorted((p for p in out_dir.iterdir() if re.fullmatch(rf"{re.escape(stem)}-\d+\.png", p.name)),
                  key=lambda p: int(re.search(r"-(\d+)\.png$", p.name).group(1)))
    result["images"] = [p.resolve().as_posix() for p in pngs]


def render_office(path: Path, out_dir: Path, runs: list[tuple[int, int | None]], result: dict) -> None:
    soffice = find_tool("soffice", "libreoffice")
    if not soffice:
        raise RenderError(f"soffice (LibreOffice) is not installed: cannot render {path.suffix} files; nothing was rendered")
    profile = Path(tempfile.mkdtemp(prefix="dmwt-lo-profile-"))
    scratch = Path(tempfile.mkdtemp(prefix="dmwt-lo-out-"))
    try:
        cmd = [soffice, f"-env:UserInstallation={profile.resolve().as_uri()}", "--headless", "--norestore",
               "--convert-to", "pdf", "--outdir", str(scratch), str(path.resolve())]
        try:
            proc = run(cmd, SOFFICE_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            raise RenderError(f"LibreOffice did not finish within {SOFFICE_TIMEOUT_S}s converting {path.name}")
        produced = scratch / f"{path.stem}.pdf"
        if proc.returncode != 0 or not produced.exists():
            detail = (proc.stderr or proc.stdout).strip().splitlines()
            raise RenderError(f"LibreOffice could not convert {path.name} to PDF"
                              + (f": {detail[-1]}" if detail else " (no output produced; is the file corrupt?)"))
        pdf = out_dir / f"{path.stem}.pdf"
        shutil.copyfile(produced, pdf)
        result["pdf"] = pdf.resolve().as_posix()
    finally:
        shutil.rmtree(profile, ignore_errors=True)
        shutil.rmtree(scratch, ignore_errors=True)
    pdf_to_pngs(pdf, out_dir, path.stem, runs, result)


def node_env() -> dict:
    """Make `require('playwright')` resolvable: keep NODE_PATH and add the global module folder."""
    env = dict(os.environ)
    npm = find_tool("npm")
    if npm:
        try:
            root = run([npm, "root", "-g"], 30).stdout.strip()
        except (subprocess.TimeoutExpired, OSError):
            root = ""
        if root:
            env["NODE_PATH"] = os.pathsep.join(p for p in (env.get("NODE_PATH", ""), root) if p)
    return env


def render_html(path: Path, out_dir: Path, result: dict) -> None:
    node = find_tool("node")
    if not node:
        raise RenderError("node is not installed: HTML rendering needs Node.js with the playwright package; nothing was rendered")
    with tempfile.TemporaryDirectory(prefix="dmwt-render-") as tmp:
        script = Path(tmp) / "render_html.js"
        results_file = Path(tmp) / "result.json"
        script.write_text(NODE_SCRIPT, encoding="utf-8")
        viewports = [{"name": n, "width": w, "height": h, "mobile": m} for n, w, h, m in VIEWPORTS]
        cmd = [node, str(script), path.resolve().as_uri(), str(out_dir / path.stem), str(results_file),
               json.dumps(viewports), str(PAGE_SETTLE_MS), str(NAVIGATION_TIMEOUT_MS), str(MAX_CLIPPED_REPORTED),
               str(MAX_OFFENDERS_REPORTED), str(OVERFLOW_TOLERANCE_PX)]
        try:
            proc = run(cmd, NODE_TIMEOUT_S, env=node_env())
        except subprocess.TimeoutExpired:
            raise RenderError(f"the browser did not finish within {NODE_TIMEOUT_S}s")
        if not results_file.exists():
            detail = (proc.stderr or proc.stdout).strip().splitlines()
            raise RenderError("node failed before producing results" + (f": {detail[-1]}" if detail else ""))
        data = json.loads(results_file.read_text(encoding="utf-8"))
    if data.get("fatal"):
        raise RenderError(data["fatal"])
    result["html"] = data["viewports"]
    result["images"] = [Path(v["screenshot"]).resolve().as_posix() for v in data["viewports"] if v.get("screenshot")]
    for v in data["viewports"]:
        if v.get("error"):
            result["warnings"].append(f"{v['name']}: {v['error']}")


def collect_problems(result: dict) -> list[str]:
    """Flatten everything worth a human's attention into one list."""
    problems: list[str] = []
    for v in result.get("html") or []:
        name = v["name"]
        for message in v["consoleErrors"]:
            problems.append(f"[{name}] console error: {message}")
        for message in v["pageErrors"]:
            problems.append(f"[{name}] uncaught exception: {message}")
        for req in v["failedRequests"]:
            problems.append(f"[{name}] failed request: {req['url']} ({req['failure']})")
        metrics = v.get("metrics")
        if not metrics:
            continue
        if metrics["horizontalOverflow"]:
            offenders = "; ".join(f"{o['element']} (right edge {o['rightEdgePx']}px)" for o in metrics["offenders"][:3])
            problems.append(f"[{name}] horizontal overflow: page is {metrics['scrollWidth']}px wide in a "
                            f"{metrics['viewportWidth']}px viewport" + (f"; widest: {offenders}" if offenders else ""))
        for clip in metrics["clipped"]:
            amounts = []
            if clip["overflowXpx"]:
                amounts.append(f"{clip['overflowXpx']}px horizontally")
            if clip["overflowYpx"]:
                amounts.append(f"{clip['overflowYpx']}px vertically")
            note = f" [{clip['truncation']}]" if clip["truncation"] else ""
            problems.append(f"[{name}] clipped content: {clip['element']} hides {' and '.join(amounts)}{note}")
        if metrics["clippedTotal"] > len(metrics["clipped"]):
            problems.append(f"[{name}] ... and {metrics['clippedTotal'] - len(metrics['clipped'])} more clipped element(s)")
        for src in metrics["brokenImages"]:
            problems.append(f"[{name}] broken image: {src}")
        if name == "mobile" and not metrics["hasViewportMeta"]:
            problems.append('[mobile] no <meta name="viewport">: phones will render this page at ~980px and shrink it')
    return problems


def render_file(path: Path, out_dir: Path, pages: str | None) -> dict:
    runs = parse_pages(pages)
    suffix = path.suffix.lower()
    result: dict = {"input": path.resolve().as_posix(), "type": suffix.lstrip("."), "out_dir": out_dir.resolve().as_posix(),
                    "images": [], "pdf": None, "pages_total": None, "warnings": [], "problems": [], "html": None}
    out_dir.mkdir(parents=True, exist_ok=True)
    clear_previous(out_dir, path.stem)
    if suffix in OFFICE_EXTENSIONS:
        render_office(path, out_dir, runs, result)
    elif suffix == ".pdf":
        pdf_to_pngs(path, out_dir, path.stem, runs, result)
        result["pdf"] = path.resolve().as_posix()
    elif suffix in HTML_EXTENSIONS:
        if pages:
            result["warnings"].append("--pages ignored for HTML (rendered as one full-page screenshot per viewport)")
        render_html(path, out_dir, result)
    else:
        raise RenderError(f"unsupported file type {suffix or '(none)'}; supported: "
                          f"{', '.join(sorted(OFFICE_EXTENSIONS | HTML_EXTENSIONS | {'.pdf'}))}")
    if not result["images"]:
        raise RenderError("rendering produced no images")
    result["problems"] = collect_problems(result)
    return result


def render_text(result: dict) -> str:
    lines = [f"render.py: {result['input']}", f"  output folder: {result['out_dir']}"]
    if result["pdf"]:
        lines.append(f"  pdf: {result['pdf']}" + (f" ({result['pages_total']} pages)" if result["pages_total"] else ""))
    lines.append(f"  {len(result['images'])} image(s):")
    lines += [f"    {p}" for p in result["images"]]
    if result["problems"]:
        lines += ["", f"PROBLEMS FOUND ({len(result['problems'])}) - fix these before delivering:"]
        lines += [f"  - {p}" for p in result["problems"]]
    elif result["html"]:
        lines += ["", "No console errors, uncaught exceptions, failed requests, overflow or clipped containers detected."]
    for v in result["html"] or []:
        m = v.get("metrics")
        if m:
            lines.append(f"  {v['name']} ({v['width']}x{v['height']}): document {m['scrollWidth']}px wide / viewport "
                         f"{m['viewportWidth']}px, {m['scrollHeight']}px tall; {v['consoleWarnings']} console warning(s)")
    for warning in result["warnings"]:
        lines.append(f"warning: {warning}")
    lines.append("")
    lines.append("Open the images and look at them: this script cannot judge layout quality, only mechanics.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="render.py",
        description="Render a pptx/docx/xlsx/pdf/html file to PNGs for visual QA; for HTML also report console errors, "
                    "uncaught exceptions, failed requests, horizontal overflow and clipped containers at 1440 and 390 px.",
        epilog="Exit codes: 0 rendered (problems are reported but do not fail the run), 1 rendering failed or usage/IO error.",
    )
    parser.add_argument("file", help="file to render")
    parser.add_argument("--out", help="output folder (default: render/ next to the file)")
    parser.add_argument("--pages", help="pages/slides for office files and PDFs, e.g. 1-5 or 1,3,7-9")
    parser.add_argument("--json", action="store_true", help="machine-readable JSON output")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.is_file():
        print(f"render.py: no such file: {path.as_posix()}", file=sys.stderr)
        return 1
    out_dir = Path(args.out) if args.out else path.resolve().parent / "render"
    try:
        result = render_file(path, out_dir, args.pages)
    except ValueError as exc:
        print(f"render.py: {exc}", file=sys.stderr)
        return 1
    except RenderError as exc:
        print(f"render.py: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"render.py: I/O error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render_text(result))
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.stdout.flush()
    except BrokenPipeError:
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        exit_code = 0
    sys.exit(exit_code)
