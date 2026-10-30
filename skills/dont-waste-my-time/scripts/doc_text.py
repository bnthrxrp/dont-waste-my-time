#!/usr/bin/env python3
"""doc_text.py - dump the text of a deck, document, sheet or page, with locations.

Shared extraction module for the other helper scripts (fluff_lint.py,
numbers_check.py) and a small CLI. One reader for every format means all the
checks see the same text and report locations the same way.

Usage
-----
    python3 doc_text.py FILE [--json] [--titles] [--include-masters]

    FILE      .pptx .docx .xlsx .csv .md .txt .html .htm
    --json    machine-readable output: {"file", "format", "units", "warnings"}
    --titles  (pptx only) print just the slide titles, one per line
    --include-masters  (pptx only) also read text on used layouts and the slide master

Text mode prints one block per unit as "[location] text"; multi-line texts
(bullets) are indented under the first line.

Python API
----------
    extract_units(path, include_masters=False) -> list[dict]
    extract_with_warnings(path, include_masters=False) -> (list[dict], list[str])
    slide_titles(path) -> [{"slide": 1, "title": "..."}, ...]   (pptx)
    detect_language(text) -> "pt" | "en"

Each unit is a dict:
    location  human-readable place, e.g. "slide 4 / title", "slide 3 / table r2c4",
              "slide 5 / chart", "slide 2 / notes", "paragraph 12", "Sheet1!B7",
              "row 9", "line 31", "html / h2 #4"
    kind      title | body | table | chart | notes | cell | line | heading | text
    text      the text (bullets joined with "\\n")
and optionally:
    slide             slide number (pptx)
    paragraphs        list of paragraph strings (pptx body/notes, bullets)
    line              1-based source line (md/txt)
    code              True for lines inside a markdown code fence
    formula           True for an xlsx cell holding a formula with no cached value
    comment, author   True/author for a docx review comment (reviewer chatter, not deliverable text)
    machine_spans     [[start, end], ...] character ranges of `text` whose numbers
                      are locale-neutral machine values (dot decimal, no grouping),
                      e.g. chart series values or numeric spreadsheet cells.
                      numbers_check uses this so a Portuguese deck's chart data
                      ("74.8") is not mistaken for a Portuguese-format number.

Notes
-----
* Charts are read from the chart XML (not python-pptx's plot API), so every
  chart type works, including 3-D pies that python-pptx cannot model.
* pptx also yields shape alt text ("slide N / alt": the descr/title of any shape, file-name
  alt text skipped). With --include-masters (off by default) it adds visible text on the
  layouts the deck uses ("layout <name>") and on the slide master ("master"), ignoring
  placeholder prompt text such as "Click to edit Master title style".
* docx also yields headers and footers ("header", "footer"), footnotes and endnotes
  ("footnote 3", numbered as Word shows them), comments ("comment 2", with the author) and
  text boxes ("textbox 1"). Parts a document does not have are skipped silently.
* HTML extraction is static: text created by JavaScript at runtime is not seen.
  Use render.py to look at the rendered page.
* Markdown/text files skip a leading YAML front matter block ("---" / "key: value" / "---"); line
  numbers still refer to the original file.
* Legacy .doc/.ppt/.xls are not supported; convert them with LibreOffice first.
* Exit codes: 0 ok, 1 usage/IO error (unreadable file, unsupported format,
  missing library).
"""
from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import re
import sys
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

SUPPORTED_EXTENSIONS = (".pptx", ".docx", ".xlsx", ".csv", ".md", ".txt", ".html", ".htm")

# Safety valves so a pasted data dump cannot produce millions of units.
MAX_XLSX_CELLS = 500_000
MAX_CSV_ROWS = 200_000
FRONT_MATTER_MAX_LINES = 200  # a front matter block longer than this is not front matter

Unit = dict[str, Any]


class MissingDependency(RuntimeError):
    """A required third-party library is not installed."""


class UnsupportedFormat(ValueError):
    """The file extension is not one of SUPPORTED_EXTENSIONS."""


def _require(module: str, pip_name: str):
    """Import lazily so unrelated formats work without every library installed."""
    try:
        return importlib.import_module(module)
    except ImportError as exc:
        raise MissingDependency(
            f"The '{module}' library is required for this file type. Install it with: pip install {pip_name}"
        ) from exc


def _unit(location: str, kind: str, text: str, **extra: Any) -> Unit:
    unit: Unit = {"location": location, "kind": kind, "text": text}
    unit.update(extra)
    return unit


def _clean(text: str) -> str:
    """Normalise whitespace oddities without touching line structure."""
    # \v is python-pptx's soft line break; NBSP/zero-width characters confuse
    # tokenisers downstream.
    text = text.replace("\v", " ").replace(" ", " ").replace("​", "")
    return text.strip()


def _read_text_file(path: Path) -> str:
    """Read UTF-8 (with or without BOM); fall back to cp1252 for Excel-exported CSVs."""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace")


# ---------------------------------------------------------------------------
# Language detection (shared by fluff_lint and numbers_check)
# ---------------------------------------------------------------------------

# Function words that are frequent in one language and (nearly) absent in the
# other. Ambiguous short words (a, e, o, no, as, me) are deliberately left out.
PT_STOPWORDS = frozenset(
    """de da do das dos que não para com uma um os em na nas nos por mais foi são está ao aos se ou como mas
    pelo pela pelos pelas entre sobre até também já só seu sua seus suas ser tem têm foram será vs
    nosso nossa nossos nossas deve devem entre quando onde cada ainda sem mesmo""".split()
)
EN_STOPWORDS = frozenset(
    """the of and to in is that for it with as was on are by this be at from or an have not but which were
    has our we their its been will can than over year more all into each when where still without same""".split()
)
# English has no accented letters; their presence is strong evidence for Portuguese.
_PT_DIACRITICS = "ãõçáàâéêíóôú"
_DIACRITIC_WEIGHT = 0.5  # a diacritic is weaker evidence than a whole function word


def language_scores(text: str) -> tuple[float, float]:
    """Return (pt_score, en_score) for `text`."""
    words = re.findall(r"[^\W\d_]+", text.lower())
    pt = float(sum(1 for w in words if w in PT_STOPWORDS))
    en = float(sum(1 for w in words if w in EN_STOPWORDS))
    pt += _DIACRITIC_WEIGHT * sum(1 for ch in text.lower() if ch in _PT_DIACRITICS)
    return pt, en


def detect_language(text: str) -> str:
    """Return "pt" or "en". Defaults to "en" when there is no evidence."""
    pt, en = language_scores(text)
    return "pt" if pt > en else "en"


# ---------------------------------------------------------------------------
# PPTX
# ---------------------------------------------------------------------------

def _walk_shapes(shapes):
    """Yield leaf shapes, descending into groups, in shape-tree order."""
    for shape in shapes:
        try:
            is_group = shape.shape_type == 6  # MSO_SHAPE_TYPE.GROUP
        except NotImplementedError:
            is_group = False
        if is_group:
            yield from _walk_shapes(shape.shapes)
        else:
            yield shape


def _walk_all_shapes(shapes):
    """Yield every shape including the group containers themselves (alt text can sit on a group)."""
    for shape in shapes:
        yield shape
        try:
            is_group = shape.shape_type == 6
        except NotImplementedError:
            is_group = False
        if is_group:
            yield from _walk_all_shapes(shape.shapes)


# Alt text that is only a file name (python-pptx stores the image's file name when a picture is added)
# is tooling noise, not something a reader or a translator needs to see.
_FILENAME_ALT = re.compile(r"^[\w\- .()]+\.(?:png|jpe?g|gif|svg|bmp|emf|wmf|tiff?|webp)$", re.I)
_FOOTER_PLACEHOLDER = 15  # PP_PLACEHOLDER.FOOTER: the only placeholder type that carries real text on layouts


def _alt_text(shape) -> str:
    """Alt text from the descr/title attributes of the shape's p:cNvPr ("" when none)."""
    try:
        c_nv_pr = shape._element.xpath("./*[1]/p:cNvPr")
    except Exception:
        return ""
    if not c_nv_pr:
        return ""
    parts: list[str] = []
    for attribute in ("title", "descr"):
        value = _clean(c_nv_pr[0].get(attribute) or "")
        if value and not _FILENAME_ALT.match(value) and value not in parts:
            parts.append(value)
    return " - ".join(parts)


def _template_units(shapes, label: str) -> list[Unit]:
    """Visible text on a slide layout or master: everything except placeholder prompt text."""
    found: list[tuple[str, str]] = []
    for shape in _walk_shapes(shapes):
        if not getattr(shape, "has_text_frame", False) or not shape.has_text_frame:
            continue
        if shape.is_placeholder and shape.placeholder_format.type != _FOOTER_PLACEHOLDER:
            continue  # "Click to edit Master title style" and friends
        paragraphs = [_clean(p.text) for p in shape.text_frame.paragraphs]
        paragraphs = [p for p in paragraphs if p]
        if paragraphs:
            found.append(("\n".join(paragraphs), shape.name))
    units = []
    for index, (text, name) in enumerate(found, start=1):
        suffix = f" #{index}" if len(found) > 1 else ""
        units.append(_unit(f"{label}{suffix}", "text", text, shape=name))
    return units


def _format_number_text(raw: str, number_format: str = "") -> str:
    """Render a numeric string from XML as a plain decimal (no exponent)."""
    try:
        value = Decimal(raw.strip())
    except Exception:
        return raw.strip()
    if "%" in number_format:
        # Chart/cell stores 0.052 but displays "5.2%"; report what a reader sees.
        decimals = len(re.sub(r"[^0#]", "", number_format.split(".", 1)[1].split(";")[0])) if "." in number_format else 0
        return f"{value * 100:.{decimals}f}%"
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _chart_points(parent, tag: str) -> list[str]:
    """Cached values of a c:cat / c:val / c:xVal / c:yVal child, in index order."""
    points = parent.xpath(f"{tag}//c:pt")
    ordered = sorted(points, key=lambda p: int(p.get("idx", "0")))
    return [(p.xpath("string(c:v)") or "").strip() for p in ordered]


def _chart_unit(chart_space, location: str, slide: int) -> Unit:
    """Build one unit from chart XML: title, axis titles, categories, series names, values."""
    lines: list[str] = []
    spans: list[list[int]] = []
    offset = 0

    def add(line: str, value_span: tuple[int, int] | None = None) -> None:
        nonlocal offset
        if value_span is not None:
            spans.append([offset + value_span[0], offset + value_span[1]])
        lines.append(line)
        offset += len(line) + 1  # +1 for the "\n" join

    title = " ".join(t.strip() for t in chart_space.xpath("c:chart/c:title//a:t/text()") if t.strip())
    if title:
        add(f"Title: {title}")
    for axis_title in chart_space.xpath("c:chart/c:plotArea/*/c:title"):
        axis_text = " ".join(t.strip() for t in axis_title.xpath(".//a:t/text()") if t.strip())
        if axis_text:
            add(f"Axis: {axis_text}")

    seen_categories: list[str] | None = None
    for ser in chart_space.xpath(".//c:ser"):
        name = " ".join(t.strip() for t in ser.xpath("c:tx//c:v/text()") if t.strip())
        cats = _chart_points(ser, "c:cat") or _chart_points(ser, "c:xVal")
        vals = _chart_points(ser, "c:val") or _chart_points(ser, "c:yVal")
        if cats and cats != seen_categories:
            add("Categories: " + " | ".join(cats))
            seen_categories = cats
        fmt = (ser.xpath("string(c:val//c:formatCode)") or ser.xpath("string(c:yVal//c:formatCode)") or "").strip()
        rendered = " | ".join(_format_number_text(v, fmt) for v in vals)
        prefix = f'Series "{name}": ' if name else "Series: "
        add(prefix + rendered, (len(prefix), len(prefix) + len(rendered)) if vals else None)
    text = "\n".join(lines)
    unit = _unit(location, "chart", text, slide=slide)
    if spans:
        unit["machine_spans"] = spans
    return unit


def _pptx_units(path: Path, warnings: list[str], options: dict[str, Any]) -> list[Unit]:
    pptx = _require("pptx", "python-pptx")
    prs = pptx.Presentation(str(path))
    units: list[Unit] = []

    for number, slide in enumerate(prs.slides, start=1):
        title_shape = None
        try:
            title_shape = slide.shapes.title
        except Exception:  # defensive: malformed placeholder trees
            title_shape = None
        if title_shape is not None and title_shape.has_text_frame:
            title_text = _clean(title_shape.text_frame.text)
            if title_text:
                units.append(_unit(f"slide {number} / title", "title", title_text, slide=number))

        text_shapes, tables, charts = [], [], []
        for shape in _walk_shapes(slide.shapes):
            if title_shape is not None and shape.shape_id == title_shape.shape_id:
                continue
            if getattr(shape, "has_chart", False) and shape.has_chart:
                charts.append(shape)
            elif getattr(shape, "has_table", False) and shape.has_table:
                tables.append(shape)
            elif shape.has_text_frame:
                if shape.is_placeholder and shape.placeholder_format.type == 13:  # SLIDE_NUMBER
                    continue
                text_shapes.append(shape)

        # Number the text frames/tables/charts only when a slide has several,
        # so the common case stays "slide 3 / body".
        for index, shape in enumerate(text_shapes, start=1):
            paragraphs = [_clean(p.text) for p in shape.text_frame.paragraphs]
            paragraphs = [p for p in paragraphs if p]
            if not paragraphs:
                continue
            suffix = f" {index}" if len(text_shapes) > 1 else ""
            units.append(_unit(f"slide {number} / body{suffix}", "body", "\n".join(paragraphs),
                               slide=number, paragraphs=paragraphs, shape=shape.name))

        for t_index, shape in enumerate(tables, start=1):
            prefix = f"table {t_index} " if len(tables) > 1 else "table "
            for r, row in enumerate(shape.table.rows, start=1):
                for c, cell in enumerate(row.cells, start=1):
                    if cell.is_spanned:  # continuation of a merged cell; text lives in the origin cell
                        continue
                    text = _clean(cell.text.replace("\n", " "))
                    if text:
                        units.append(_unit(f"slide {number} / {prefix}r{r}c{c}", "table", text, slide=number))

        for c_index, shape in enumerate(charts, start=1):
            suffix = f" {c_index}" if len(charts) > 1 else ""
            location = f"slide {number} / chart{suffix}"
            try:
                units.append(_chart_unit(shape.chart._chartSpace, location, number))
            except Exception as exc:  # unreadable chart part: say so rather than crash
                warnings.append(f"{location}: chart could not be parsed ({exc.__class__.__name__}: {exc})")
                units.append(_unit(location, "chart", "chart (unparsed)", slide=number))

        alts = [(shape, _alt_text(shape)) for shape in _walk_all_shapes(slide.shapes)]
        alts = [(shape, text) for shape, text in alts if text]
        for a_index, (shape, text) in enumerate(alts, start=1):
            suffix = f" {a_index}" if len(alts) > 1 else ""
            units.append(_unit(f"slide {number} / alt{suffix}", "text", text, slide=number, shape=shape.name))

        if slide.has_notes_slide:
            frame = slide.notes_slide.notes_text_frame
            if frame is not None:
                paragraphs = [_clean(p.text) for p in frame.paragraphs]
                paragraphs = [p for p in paragraphs if p]
                if paragraphs:
                    units.append(_unit(f"slide {number} / notes", "notes", "\n".join(paragraphs),
                                       slide=number, paragraphs=paragraphs))

    if options.get("include_masters"):
        # Only layouts that slides actually use: a template ships dozens of unused ones.
        used_layouts: dict[str, Any] = {}
        for slide in prs.slides:
            used_layouts.setdefault(slide.slide_layout.name, slide.slide_layout)
        for name, layout in used_layouts.items():
            units += _template_units(layout.shapes, f"layout {name}")
        units += _template_units(prs.slide_master.shapes, "master")
    return units


def slide_titles(path: str | Path) -> list[dict[str, Any]]:
    """Return [{"slide": n, "title": str}] for every slide of a .pptx ("" when a slide has no title)."""
    path = Path(path)
    if path.suffix.lower() != ".pptx":
        raise UnsupportedFormat("slide_titles() only supports .pptx files")
    units, _ = extract_with_warnings(path)
    pptx = _require("pptx", "python-pptx")
    count = len(pptx.Presentation(str(path)).slides)
    titles = {u["slide"]: u["text"] for u in units if u["kind"] == "title"}
    return [{"slide": n, "title": titles.get(n, "")} for n in range(1, count + 1)]


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------

def _docx_table_units(table, label: str, units: list[Unit]) -> None:
    for r, row in enumerate(table.rows, start=1):
        seen_cells = set()
        for c, cell in enumerate(row.cells, start=1):
            if id(cell._tc) in seen_cells:  # horizontally merged cells repeat the same _tc
                continue
            seen_cells.add(id(cell._tc))
            location = f"{label} r{r}c{c}"
            text = _clean(" ".join(p.text for p in cell.paragraphs))
            if text:
                units.append(_unit(location, "table", text))
            for n, nested in enumerate(cell.tables, start=1):
                _docx_table_units(nested, f"{location} / table {n}", units)


def _docx_units(path: Path, warnings: list[str], options: dict[str, Any]) -> list[Unit]:
    docx = _require("docx", "python-docx")
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    document = docx.Document(str(path))
    units: list[Unit] = []
    body = document.element.body
    state = {"para": 0, "table": 0}

    def walk(parent) -> None:
        for child in parent.iterchildren():
            tag = child.tag.rsplit("}", 1)[-1]
            if tag == "p":
                state["para"] += 1
                paragraph = Paragraph(child, document)
                text = _clean(paragraph.text)
                if not text:
                    continue
                try:
                    style = (paragraph.style.name or "") if paragraph.style is not None else ""
                except Exception:
                    style = ""
                if style.lower().startswith("heading"):
                    kind = "heading"
                elif style.lower() == "title":
                    kind = "title"
                else:
                    kind = "body"
                units.append(_unit(f"paragraph {state['para']}", kind, text, style=style))
            elif tag == "tbl":
                state["table"] += 1
                _docx_table_units(Table(child, document), f"table {state['table']}", units)
            elif tag == "sdt":  # content control: its children live in w:sdtContent
                for content in child.iterchildren():
                    if content.tag.rsplit("}", 1)[-1] == "sdtContent":
                        walk(content)

    walk(body)

    units += _docx_package_units(path, warnings)
    return units


# Parts python-docx does not model (footnotes, endnotes, comments) or models awkwardly (headers/footers in
# all variants, text boxes) are read straight from the zip with the standard library. A part that is
# absent or unparseable is skipped silently: most documents have none of them.
_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"
_PAGE_NUMBER_ONLY = re.compile(r"^\d{1,3}$")  # a PAGE field's cached result, not content


def _xml_para_text(paragraph) -> str:
    """Text of one w:p: runs, tabs and breaks; not text boxes (read separately) or deleted text."""
    pieces: list[str] = []

    def visit(node) -> None:
        for child in node:
            if child.tag in (_W + "txbxContent", _MC_FALLBACK):
                continue
            if child.tag == _W + "t":
                pieces.append(child.text or "")
            elif child.tag in (_W + "tab", _W + "br", _W + "cr"):
                pieces.append(" ")
            else:
                visit(child)

    visit(paragraph)
    return _clean(re.sub(r"\s+", " ", "".join(pieces)))


def _xml_paragraphs(root) -> list[str]:
    """Non-empty paragraph texts under `root` in document order, skipping text-box content and mc:Fallback copies."""
    found: list[str] = []

    def visit(node) -> None:
        for child in node:
            if child.tag in (_W + "txbxContent", _MC_FALLBACK):
                continue
            if child.tag == _W + "p":
                text = _xml_para_text(child)
                if text:
                    found.append(text)
            else:
                visit(child)

    visit(root)
    return found


def _xml_textboxes(root) -> list[str]:
    """One text per text box. Word writes each box twice (DrawingML + VML fallback); only the first is read."""
    boxes: list[str] = []

    def visit(node) -> None:
        for child in node:
            if child.tag == _MC_FALLBACK:
                continue
            if child.tag == _W + "txbxContent":
                text = "\n".join(_xml_paragraphs(child))
                if text:
                    boxes.append(text)
                visit(child)  # a text box nested in a text box
            else:
                visit(child)

    visit(root)
    return boxes


def _reference_order(root, tag: str) -> dict[str, int]:
    """Map w:id -> 1-based position of its first reference in the body (what Word numbers the note as)."""
    order: dict[str, int] = {}

    def visit(node) -> None:
        for child in node:
            if child.tag == _MC_FALLBACK:
                continue
            if child.tag == _W + tag:
                order.setdefault(child.get(_W + "id", ""), len(order) + 1)
            visit(child)

    visit(root)
    return order


def _docx_package_units(path: Path, warnings: list[str]) -> list[Unit]:
    import zipfile
    from xml.etree import ElementTree

    units: list[Unit] = []

    def read(archive, name: str):
        try:
            return ElementTree.fromstring(archive.read(name))
        except (KeyError, ElementTree.ParseError):
            return None

    try:
        archive = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        return units
    with archive:
        names = set(archive.namelist())
        document = read(archive, "word/document.xml")

        for label in ("header", "footer"):
            distinct: list[str] = []
            boxes: list[str] = []
            for name in sorted(n for n in names if re.fullmatch(rf"word/{label}\d*\.xml", n)):
                root = read(archive, name)
                if root is None:
                    continue
                text = "\n".join(_xml_paragraphs(root))
                if text and not _PAGE_NUMBER_ONLY.match(text) and text not in distinct:
                    distinct.append(text)
                boxes += [box for box in _xml_textboxes(root) if box not in boxes]
            for index, text in enumerate(distinct, start=1):
                units.append(_unit(label if len(distinct) == 1 else f"{label} {index}", "text", text))
            for box in boxes:
                units.append(_unit(f"{label} textbox", "text", box))

        for part, tag, element, label, kind in (
            ("word/footnotes.xml", "footnoteReference", "footnote", "footnote", "notes"),
            ("word/endnotes.xml", "endnoteReference", "endnote", "endnote", "notes"),
            ("word/comments.xml", "commentReference", "comment", "comment", "text"),
        ):
            root = read(archive, part)
            if root is None:
                continue
            order = _reference_order(document, tag) if document is not None else {}
            entries = []
            for index, node in enumerate(root.iter(_W + element)):
                if node.get(_W + "type") in ("separator", "continuationSeparator", "continuationNotice"):
                    continue
                text = "\n".join(_xml_paragraphs(node))
                if text:
                    entries.append((order.get(node.get(_W + "id", ""), 10**6 + index), node, text))
            for rank, (_, node, text) in enumerate(sorted(entries, key=lambda e: e[0]), start=1):
                extra = {"comment": True, "author": node.get(_W + "author") or ""} if element == "comment" else {}
                units.append(_unit(f"{label} {rank}", kind, text, **extra))

        if document is not None:
            for number, box in enumerate(_xml_textboxes(document), start=1):
                units.append(_unit(f"textbox {number}", "text", box))
    return units


# ---------------------------------------------------------------------------
# XLSX
# ---------------------------------------------------------------------------

def _quote_sheet(name: str) -> str:
    """Excel quotes sheet names that are not plain identifiers."""
    return name if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", name) else "'" + name.replace("'", "''") + "'"


def _cell_text(value: Any, number_format: str) -> tuple[str, bool]:
    """Return (text, is_machine_numeric) for a cell value."""
    import datetime as dt

    if isinstance(value, bool):
        return ("TRUE" if value else "FALSE"), False
    if isinstance(value, (int, float)):
        return _format_number_text(repr(value) if isinstance(value, float) else str(value), number_format or ""), True
    if isinstance(value, dt.datetime):
        if value.time() == dt.time(0, 0):
            return value.date().isoformat(), True
        return value.isoformat(sep=" ", timespec="minutes"), True
    if isinstance(value, dt.date):
        return value.isoformat(), True
    return _clean(str(value)), False


def _xlsx_units(path: Path, warnings: list[str], options: dict[str, Any]) -> list[Unit]:
    openpyxl = _require("openpyxl", "openpyxl")
    units: list[Unit] = []

    # Formulas without a cached result (files written by libraries, never opened
    # in Excel) read as None in data_only mode; find them so they are not silently lost.
    formulas: dict[tuple[str, str], str] = {}
    wb_f = openpyxl.load_workbook(str(path), read_only=True, data_only=False)
    try:
        for ws in wb_f.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and cell.value.startswith("="):
                        formulas[(ws.title, cell.coordinate)] = cell.value
    finally:
        wb_f.close()

    wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
    count = 0
    try:
        for ws in wb.worksheets:
            ws.reset_dimensions()  # some writers leave a wrong <dimension>; scan the real extent
            for row in ws.iter_rows():
                for cell in row:
                    value = cell.value
                    coordinate = getattr(cell, "coordinate", None)
                    if coordinate is None:
                        continue
                    location = f"{_quote_sheet(ws.title)}!{coordinate}"
                    if value is None:
                        if (ws.title, coordinate) in formulas:
                            units.append(_unit(location, "cell", formulas[(ws.title, coordinate)], formula=True))
                        continue
                    text, machine = _cell_text(value, getattr(cell, "number_format", "") or "")
                    if not text:
                        continue
                    unit = _unit(location, "cell", text)
                    if machine:
                        unit["machine_spans"] = [[0, len(text)]]
                    units.append(unit)
                    count += 1
                    if count >= MAX_XLSX_CELLS:
                        warnings.append(f"stopped after {MAX_XLSX_CELLS} cells; the rest of the workbook was not read")
                        return units
    finally:
        wb.close()
    uncached = sum(1 for u in units if u.get("formula"))
    if uncached:
        warnings.append(f"{uncached} formula cell(s) have no cached value (file never recalculated); formula text shown")
    return units


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

def _csv_units(path: Path, warnings: list[str], options: dict[str, Any]) -> list[Unit]:
    text = _read_text_file(path)
    sample = text[:8192]
    try:
        # Restrict candidates: PT-BR exports usually use ';', which the default sniffer set handles poorly.
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    units: list[Unit] = []
    reader = csv.reader(text.splitlines(), dialect)
    for number, row in enumerate(reader, start=1):
        cells = [_clean(c) for c in row]
        if not any(cells):
            continue
        units.append(_unit(f"row {number}", "line", " | ".join(cells), cells=cells))
        if number >= MAX_CSV_ROWS:
            warnings.append(f"stopped after {MAX_CSV_ROWS} rows; the rest of the file was not read")
            break
    return units


# ---------------------------------------------------------------------------
# Markdown / plain text
# ---------------------------------------------------------------------------

_MD_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
_MD_TABLE_SEPARATOR = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
_MD_RULE = re.compile(r"^\s*([-*_=])\1{2,}\s*$")
_MD_FENCE = re.compile(r"^\s*(```|~~~)")


def _front_matter_end(lines: list[str]) -> int:
    """Number of leading lines taken by a YAML front matter block ("---" ... "---"), or 0 if there is none.

    The block must look like YAML (first line after the opening rule is "key: ..."), so a document that merely
    starts with a horizontal rule is not swallowed.
    """
    if not lines or lines[0].strip() != "---":
        return 0
    if len(lines) < 3 or not re.match(r"^[\w.-]+\s*:", lines[1]):
        return 0
    for index in range(2, min(len(lines), FRONT_MATTER_MAX_LINES)):
        if lines[index].strip() in ("---", "..."):
            return index + 1
    return 0


def _markdown_units(path: Path, warnings: list[str], options: dict[str, Any]) -> list[Unit]:
    units: list[Unit] = []
    in_code = False
    lines = _read_text_file(path).splitlines()
    skip = _front_matter_end(lines)  # metadata such as "max_turns: 30" is not document content
    for number, raw in enumerate(lines, start=1):
        if number <= skip:
            continue
        line = raw.rstrip()
        if _MD_FENCE.match(line):
            in_code = not in_code
            continue
        if not line.strip():
            continue
        if in_code:
            units.append(_unit(f"line {number}", "line", line.strip(), line=number, code=True))
            continue
        if _MD_RULE.match(line) or (_MD_TABLE_SEPARATOR.match(line) and "-" in line):
            continue
        heading = _MD_HEADING.match(line)
        if heading:
            units.append(_unit(f"line {number}", "heading", heading.group(2), line=number, level=len(heading.group(1))))
        else:
            units.append(_unit(f"line {number}", "line", line.strip(), line=number))
    return units


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

_VOID_TAGS = frozenset("area base br col embed hr img input link meta param source track wbr".split())
_SKIP_TAGS = frozenset({"script", "style", "noscript", "template"})
# Elements that start a new visual block of text; inline tags (span, a, b, ...) are merged into their block.
_BLOCK_TAGS = frozenset(
    """address article aside blockquote body button caption dd details dialog div dl dt fieldset figcaption figure
    footer form h1 h2 h3 h4 h5 h6 header hr label legend li main nav ol optgroup option p pre section select
    summary table tbody td tfoot th thead title tr ul textarea""".split()
)
_HEADING_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
_ATTRIBUTE_TEXT = ("aria-label", "title", "alt")
_HIDDEN_STYLE = re.compile(r"display\s*:\s*none|visibility\s*:\s*hidden", re.I)


# Start tags that implicitly close an open <p> (HTML optional-end-tag rules); lets sloppy
# markup such as "<p>one<p>two" keep sensible block boundaries.
_CLOSES_PARAGRAPH = frozenset(
    """address article aside blockquote div dl fieldset footer form h1 h2 h3 h4 h5 h6 header hr main nav ol p pre
    section table ul""".split()
)


class _HtmlTextParser(HTMLParser):
    """Collects visible text in document order, one unit per block element."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.units: list[Unit] = []
        self._stack: list[dict[str, Any]] = []
        self._buffer: list[str] = []
        self._owner: dict[str, Any] | None = None
        self._pending_attrs: list[tuple[str, str, str]] = []
        self._tables: list[dict[str, int]] = []
        self._table_count = 0
        self._counter = 0

    # -- helpers ---------------------------------------------------------
    def _hidden(self) -> bool:
        return any(entry["hidden"] for entry in self._stack)

    def _in(self, tag: str) -> bool:
        return any(entry["tag"] == tag for entry in self._stack)

    def _nearest_block(self) -> str:
        for entry in reversed(self._stack):
            if entry["tag"] in _BLOCK_TAGS:
                return entry["tag"]
        return "body"

    def _close_to(self, names: set[str] | frozenset[str], stop: set[str] | frozenset[str]) -> None:
        """Implicitly end the nearest open element in `names`, not looking past any element in `stop`."""
        for index in range(len(self._stack) - 1, -1, -1):
            tag = self._stack[index]["tag"]
            if tag in names:
                del self._stack[index:]
                return
            if tag in stop:
                return

    def _emit(self, location_prefix: str, kind: str, text: str, label: str | None = None) -> None:
        self._counter += 1
        self.units.append(_unit(label or f"html / {location_prefix} #{self._counter}", kind, text))

    def _flush_pending_attrs(self) -> None:
        for tag, attr, value in self._pending_attrs:
            self._emit(f"{tag}[{attr}]", "text", value)
        self._pending_attrs = []

    def _flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self._buffer)).strip()
        owner = self._owner
        self._buffer, self._owner = [], None
        if text and owner:
            tag = owner["tag"]
            if owner.get("cell"):
                table_no, r, c = owner["cell"]
                self.units.append(_unit(f"html / table {table_no} r{r}c{c}", "table", text))
            elif tag == "title" and owner.get("svg"):
                self._emit("svg-title", "text", text)
            elif tag == "title":
                self.units.append(_unit("html / title", "title", text))
            elif tag in _HEADING_TAGS:
                self._emit(tag, "heading", text)
            else:
                self._emit(tag, "text", text)
        self._flush_pending_attrs()

    # -- parser callbacks --------------------------------------------------
    def handle_starttag(self, tag: str, attrs) -> None:
        attributes = {k: (v or "") for k, v in attrs}
        hidden = tag in _SKIP_TAGS or "hidden" in attributes or bool(_HIDDEN_STYLE.search(attributes.get("style", "")))

        if tag == "li":
            self._close_to({"li"}, {"ul", "ol"})
        elif tag in ("td", "th"):
            self._close_to({"td", "th"}, {"tr", "table"})
        elif tag == "tr":
            self._close_to({"tr"}, {"table"})
        if tag in _CLOSES_PARAGRAPH:
            self._close_to({"p"}, {"td", "th", "li", "table", "div", "section", "article"})
        if tag in _BLOCK_TAGS:
            self._flush()

        cell = None
        if tag == "table":
            self._table_count += 1
            self._tables.append({"no": self._table_count, "row": 0, "col": 0})
        elif tag == "tr" and self._tables:
            self._tables[-1]["row"] += 1
            self._tables[-1]["col"] = 0
        elif tag in ("td", "th") and self._tables:
            table = self._tables[-1]
            cell = (table["no"], table["row"], table["col"] + 1)
            span = attributes.get("colspan", "1")
            table["col"] += int(span) if span.isdigit() and int(span) > 0 else 1

        if not (hidden or self._hidden()):
            display_tag = "svg-title" if tag == "title" and self._in("svg") else tag
            for attr in _ATTRIBUTE_TEXT:
                value = re.sub(r"\s+", " ", attributes.get(attr, "")).strip()
                if value:
                    self._pending_attrs.append((display_tag, attr, value))
            if tag in _BLOCK_TAGS:  # block boundary just flushed: emit attribute text in document order
                self._flush_pending_attrs()
        if tag == "br":
            self._buffer.append(" ")
        if tag not in _VOID_TAGS:
            self._stack.append({"tag": tag, "hidden": hidden, "cell": cell})

    def handle_startendtag(self, tag: str, attrs) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in _VOID_TAGS and self._stack and self._stack[-1]["tag"] == tag:
            self._stack.pop()

    def handle_endtag(self, tag: str) -> None:
        if tag in _VOID_TAGS:
            return
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index]["tag"] == tag:
                if tag in _BLOCK_TAGS:
                    self._flush()
                del self._stack[index:]
                break
        if tag == "table" and self._tables:
            self._tables.pop()

    def handle_data(self, data: str) -> None:
        if self._hidden() or not data:
            return
        if self._owner is None and data.strip():
            cell = next((e["cell"] for e in reversed(self._stack) if e["cell"]), None)
            self._owner = {"tag": self._nearest_block(), "cell": cell, "svg": self._in("svg")}
        self._buffer.append(data)

    def close(self) -> None:
        super().close()
        self._flush()


def _html_units(path: Path, warnings: list[str], options: dict[str, Any]) -> list[Unit]:
    parser = _HtmlTextParser()
    parser.feed(_read_text_file(path))
    parser.close()
    return parser.units


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_READERS = {
    ".pptx": ("pptx", _pptx_units),
    ".docx": ("docx", _docx_units),
    ".xlsx": ("xlsx", _xlsx_units),
    ".csv": ("csv", _csv_units),
    ".md": ("markdown", _markdown_units),
    ".txt": ("text", _markdown_units),
    ".html": ("html", _html_units),
    ".htm": ("html", _html_units),
}


def file_format(path: str | Path) -> str:
    """Short format name for a path ("pptx", "docx", ...), or raise UnsupportedFormat."""
    suffix = Path(path).suffix.lower()
    if suffix not in _READERS:
        raise UnsupportedFormat(
            f"Unsupported file type '{suffix or '(none)'}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}. "
            "Convert legacy .doc/.ppt/.xls or PDF files first."
        )
    return _READERS[suffix][0]


def extract_with_warnings(path: str | Path, include_masters: bool = False) -> tuple[list[Unit], list[str]]:
    """Extract text units and any non-fatal warnings (e.g. an unparseable chart).

    include_masters: (pptx only) also return text on the layouts the deck uses and on the slide master.
    """
    path = Path(path)
    file_format(path)  # validates the extension
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    warnings: list[str] = []
    units = _READERS[path.suffix.lower()][1](path, warnings, {"include_masters": include_masters})
    return units, warnings


def extract_units(path: str | Path, include_masters: bool = False) -> list[Unit]:
    """Extract text units from a supported file. See the module docstring for the unit schema."""
    return extract_with_warnings(path, include_masters)[0]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _format_unit(unit: Unit) -> str:
    lines = unit["text"].split("\n")
    return f"[{unit['location']}] " + "\n    ".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="doc_text.py",
        description="Dump the text of a .pptx/.docx/.xlsx/.csv/.md/.txt/.html file with human-readable locations.",
    )
    parser.add_argument("file", help="file to read")
    parser.add_argument("--json", action="store_true", help="machine-readable JSON output")
    parser.add_argument("--titles", action="store_true", help="(pptx only) print only the slide titles")
    parser.add_argument("--include-masters", action="store_true",
                        help="(pptx only) also read text on the used slide layouts and the slide master")
    args = parser.parse_args(argv)
    path = Path(args.file)

    try:
        if args.titles:
            titles = slide_titles(path)
            if args.json:
                print(json.dumps({"file": path.as_posix(), "titles": titles}, ensure_ascii=False, indent=2))
            else:
                for item in titles:
                    print(f"{item['slide']}. {item['title'] or '(no title)'}")
            return 0
        units, warnings = extract_with_warnings(path, args.include_masters)
    except (FileNotFoundError, UnsupportedFormat, MissingDependency) as exc:
        print(f"doc_text: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # corrupt or password-protected files raise assorted library errors
        print(f"doc_text: could not read {path.as_posix()}: {exc.__class__.__name__}: {exc}", file=sys.stderr)
        return 1

    if args.json:
        payload = {"file": path.as_posix(), "format": file_format(path), "units": units, "warnings": warnings}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for unit in units:
            print(_format_unit(unit))
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.stdout.flush()
    except BrokenPipeError:
        # The reader closed the pipe early (e.g. `| head`); exit quietly instead of dumping a traceback.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        exit_code = 0
    sys.exit(exit_code)
