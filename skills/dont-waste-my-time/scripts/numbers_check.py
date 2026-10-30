#!/usr/bin/env python3
"""numbers_check.py - numeric fidelity and traceability checks for executive deliverables.

Two subcommands, both built on the same locale-aware number reader:

  compare SOURCE TARGET   for translations/adaptations: did every number survive, unchanged?
  trace DELIVERABLE --sources SRC [SRC ...]
                          for "no invented numbers": which numbers in the deliverable appear
                          in no source file?

Usage
-----
    python3 numbers_check.py compare SOURCE TARGET [--source-locale pt|en] [--target-locale pt|en]
                                                   [--json] [--strict]
    python3 numbers_check.py trace DELIVERABLE --sources SRC [SRC ...] [--include-years]
                                                   [--deliverable-locale pt|en] [--source-locale pt|en]
                                                   [--json] [--strict]

Files may be anything doc_text.py reads (.pptx .docx .xlsx .csv .md .txt .html).
Exit codes: 0 ran fine (even if discrepancies were found); 1 usage/IO error;
2 only with --strict when discrepancies / untraced numbers exist (1 wins if both).

What counts as "the same number"
--------------------------------
Every token is normalised to (kind, value, unit, currency) before comparing:
  * Locale: pt-BR "1.234,5" and en "1,234.5" are both 1234.5. Unambiguous shapes are
    parsed as written; ambiguous ones ("1.234" / "1,234": thousands or decimals?) follow the
    document's locale, detected from the unambiguous numbers in it and from stopwords.
    Override with --source-locale / --target-locale / --deliverable-locale.
  * Scale words are part of the value: mil, mi, milhão/milhões, bi, bilhão/bilhões, tri;
    k, thousand, M, MM, mn, million, B, bn, billion. "R$ 48,7 mi" == "R$48.7M" == "BRL 48.7 million".
  * Currency: R$/BRL/reais, US$/$/USD/dollars, EUR/euros, GBP/pounds are normalised.
  * Percentages ("%", "por cento"), percentage points ("p.p.", "pp", "pontos percentuais",
    "percentage points", generic "points") and basis points ("bps", 100 bps = 1 pp).
  * Dates: dd/mm/yyyy (pt) vs mm/dd/yyyy (en), "Nov 15, 2026", "15 Nov 2026", ISO,
    "15 de novembro de 2026", "março/27", "agosto/26" -> ISO date or year-month.
  * Quarters: "3T25", "3º trimestre de 2025", "Q3 2025", "3Q25", "Q3'25" -> 2025-Q3.
  * Signs: "+6,2%" equals "6.2%"; a positive vs negative difference is reported.
  * Rounding: values match when they agree to the coarser of the two precisions
    (|a - b| <= half a unit of the less precise number): 48.7M matches 48,683,000.

Ignored on purpose: list/step numbering at line start ("1.", "2)"), "slide/page/table/figure N"
references, numbers inside URLs and e-mail addresses, alphanumeric identifiers (REL-24, B2B, 3PL).
Parenthesised negatives "(1.234)" are NOT read as negative.

compare reports: (a) source numbers missing from the target (with a hint when the target
has a different number at the same location, i.e. a likely edit), (b) target numbers absent
from the source, (c) locations whose number counts differ, (d) numbers that matched only
after ignoring a sign, currency or unit difference (these are real differences worth a look),
plus notes when the target uses the wrong locale format for its language.

trace reports every deliverable number that matches no source number, grouped by location.
Such numbers are either derived calculations (the deliverable must label them as derived
and show the basis) or fabrications (remove or source them). Differences and ratios of
source numbers (e.g. -2.8% computed from 86.2 and 88.7) will legitimately appear as
untraced: verify them, do not delete them. When an untraced number can be reproduced from
two other numbers in the same sentence/row, the report says how (possible basis).
By default bare years, year-month dates and quarter labels are ignored (--include-years
to check them too); full dates are always checked.
"""
from __future__ import annotations

import argparse
import bisect
import calendar
import json
import os
import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import doc_text  # noqa: E402  (shared extraction; must follow the sys.path tweak)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SNIPPET_RADIUS = 45          # characters of context shown on each side of a number
MIN_DOC_WORDS_FOR_FORMAT_NOTE = 20   # below this, language detection is too weak to call a format "wrong"
MAX_FORMAT_NOTES = 5         # examples listed per format note
LOCATION_OVERLAP_MIN = 0.5   # per-location counts are only meaningful if half the locations line up
YEAR_RANGE = (1900, 2100)    # four-digit integers in this range are treated as years
BPS_PER_PP = 100             # 1 percentage point = 100 basis points
SCALE_SHIFTS = (3, 6, 9)     # trace: a table in "$M" vs prose in "$" differs by 10^3, 10^6 or 10^9
PLAUSIBLE_YEARS = (1900, 2100)

# Hyphen-minus is the only sign we model; fold the look-alikes (length-preserving so offsets hold).
_CHAR_FOLD = str.maketrans({
    "−": "-", "‒": "-", "–": "-",          # minus, figure dash, en dash
    " ": " ", " ": " ", " ": " ", "​": " ",
    "’": "'", "‘": "'",
})

# scale multipliers. Single-letter scales are case-sensitive for M/B (lower-case m is metres, b is bytes/bits)
_SCALE_PATTERN = (
    r"(?:(?i:trilh[ãa]o|trilh[õo]es|trillion|tri)"
    r"|(?i:bilh[ãa]o|bilh[õo]es|billion|bn|bi)|B"
    r"|(?i:milh[ãa]o|milh[õo]es|million|mil|mn|mi)|MM|M"
    r"|(?i:thousand)|[kK])"
)
_SCALE_VALUE = {  # key = lower-case text, except where case matters (handled in _scale_multiplier)
    "tri": 10**12, "trilhão": 10**12, "trilhao": 10**12, "trilhões": 10**12, "trilhoes": 10**12, "trillion": 10**12,
    "bi": 10**9, "bn": 10**9, "bilhão": 10**9, "bilhao": 10**9, "bilhões": 10**9, "bilhoes": 10**9, "billion": 10**9,
    "mi": 10**6, "mn": 10**6, "milhão": 10**6, "milhao": 10**6, "milhões": 10**6, "milhoes": 10**6, "million": 10**6,
    "mil": 10**3, "thousand": 10**3, "k": 10**3,
}
_SINGLE_LETTER_SCALES = frozenset({"k", "K", "B", "M", "MM"})


def _scale_multiplier(text: str) -> int:
    if text in ("M", "MM"):
        return 10**6
    if text == "B":
        return 10**9
    return _SCALE_VALUE[text.lower()]


_CURRENCY_CODES = {
    "r$": "BRL", "brl": "BRL", "real": "BRL", "reais": "BRL",
    "us$": "USD", "u$s": "USD", "$": "USD", "usd": "USD", "dólar": "USD", "dolar": "USD", "dólares": "USD",
    "dolares": "USD", "dollar": "USD", "dollars": "USD",
    "€": "EUR", "eur": "EUR", "euro": "EUR", "euros": "EUR",
    "£": "GBP", "gbp": "GBP", "libra": "GBP", "libras": "GBP", "pound": "GBP", "pounds": "GBP",
}

_MONTH_FULL = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
    "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
}
_MONTH_ABBR = {
    "jan": 1, "feb": 2, "fev": 2, "mar": 3, "apr": 4, "abr": 4, "may": 5, "mai": 5, "jun": 6, "jul": 7,
    "aug": 8, "ago": 8, "sept": 9, "sep": 9, "set": 9, "oct": 10, "out": 10, "nov": 11, "dec": 12, "dez": 12,
}
# Abbreviations that are also ordinary words ("3 out of 5", "set 15 goals") need a period or a year to count.
_AMBIGUOUS_ABBR = frozenset({"mar", "set", "out"})
_MONTH_RE = (
    "(?:" + "|".join(sorted(_MONTH_FULL, key=len, reverse=True)) + "|"
    + "|".join(sorted(_MONTH_ABBR, key=len, reverse=True)) + ")"
)

_ORDINAL_WORDS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "primeiro": 1, "segundo": 2, "terceiro": 3,
                  "quarto": 4, "1st": 1, "2nd": 2, "3rd": 3, "4th": 4}

# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------

_URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.I)
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
# "slide 4", "página 3-5", "Table 2", "Figura 1": numbers that point at the document, not at business data.
_REFERENCE_RE = re.compile(
    r"(?i)\b(?:slides?|l[âa]minas?|p[áa]ginas?|pages?|p[áa]g\.?|pp?\.(?=\s*\d)|tables?|tabelas?|figures?|figuras?|"
    r"fig\.|gr[áa]ficos?|exhibits?|sections?|se[çc][ãa]o|se[çc][õo]es|chapters?|cap[íi]tulos?|appendix|"
    r"ap[êe]ndice|anexo|step|passo|etapa)\s*#?\s*\d+(?:\.\d+)*(?:\s*[-,&]\s*\d+(?:\.\d+)*)*"
)
# Outline numbering at the start of a line: "1. Intro", "2) Next", "### 3. Market", "4.2 Pricing".
_LIST_NUMBER_RE = re.compile(
    r"(?m)^[ \t]*(?:#{1,6}[ \t]+)?(?:[-*+•][ \t]+)?"
    r"(?P<num>\(?\d{1,3}[.)][ \t]+(?=\S)|\d{1,2}(?:\.\d{1,2})+\.?[ \t]+(?=[A-ZÀ-Ý]))"
)

_CORE_RE = re.compile(r"(?<![\w])\d+(?:[.,]\d+)*")
# Matched against the text just before a number and anchored at its end, so a sign is always adjacent to the digits.
_PREFIX_RE = re.compile(
    r"(?P<s1>[+\-±])?(?:(?P<cur>R\$|US\$|U\$S|\$|€|£|BRL|USD|EUR|GBP)\s?)?(?P<s2>[+\-±])?$"
)
_UNIT_SUFFIX_RE = re.compile(
    rf"""(?P<scale>\s?{_SCALE_PATTERN}(?![^\W\d_]))?
    (?:
        (?P<pct>\s?%|\s?(?i:por\s?cento|per\s?cent|percent|pct)\b)
      | (?P<bps>\s?(?i:bps|bp|basis\s+points?|pontos?[-\s]base)\b)
      | (?P<pp>\s?(?i:p\.\s?p\.?|pp\b|pontos?\s+percentuais?|ponto\s+percentual|percentage\s+points?|
                  percent\s+points?|pts\b|points?\b(?!\s+of\s+sale)|pontos?\b(?!\s+de\s+venda)))
      | (?P<mult>[x×](?![^\W\d_]))
      | (?P<cur>\s?(?:de\s+)?(?i:reais|real|d[óo]lares?|dollars?|euros?|libras?|pounds?|BRL|USD|EUR|GBP)\b)
    )?""",
    re.X,
)
# Letters glued to a number that are a unit of measure, not part of an identifier like "3PL" or "2FA".
_GLUED_UNIT_RE = re.compile(r"(?i:kg|kt|km|cm|mm|ml|mg|gb|mb|tb|hrs?|min|wks?|[gltshdwm])(?![^\W\d_])")
_ORDINAL_SUFFIX_RE = re.compile(r"(?:[ºª°]|(?i:st|nd|rd|th)(?![^\W\d_]))")

_TIME_RE = re.compile(r"(?<![\w:.])([01]?\d|2[0-3]):([0-5]\d)(?::[0-5]\d)?(?![\w:])")
_FY_RE = re.compile(r"(?<![\w])FY\s?['’]?(\d{4}|\d{2})(?![\w])", re.I)

# Quarters. 2-digit years after a space are ambiguous ("Q3 25 customers"), so they need a separator.
_QUARTER_PATTERNS: list[tuple[re.Pattern, Callable[[re.Match], tuple[int, int | None]]]] = []


def _year4(text: str | None) -> int | None:
    if not text:
        return None
    text = text.strip("'’ ")
    return int(text) if len(text) == 4 else 2000 + int(text)


def _add_quarter(pattern: str, flags: int, builder: Callable[[re.Match], tuple[int, int | None]]) -> None:
    _QUARTER_PATTERNS.append((re.compile(pattern, flags), builder))


_add_quarter(r"(?<![\w])([1-4])\s?T\s?['’]?(\d{4}|\d{2})(?![\w])", 0, lambda m: (int(m[1]), _year4(m[2])))        # 3T25
_add_quarter(r"(?<![\w])([1-4])\s?Q\s?['’]?(\d{4}|\d{2})(?![\w])", 0, lambda m: (int(m[1]), _year4(m[2])))        # 3Q25
_add_quarter(r"(?<![\w])Q\s?([1-4])\s?[-/'’]\s?(\d{4}|\d{2})(?![\w])", re.I, lambda m: (int(m[1]), _year4(m[2])))  # Q3'25 Q3-26
_add_quarter(r"(?<![\w])Q\s?([1-4])\s+(?:FY\s?)?(\d{4})(?![\w])", re.I, lambda m: (int(m[1]), _year4(m[2])))     # Q3 2025
_add_quarter(r"(?<![\w])([1-4])\s?[ºª°]\s*(?:trimestre|trim\b\.?)(?:\s+(?:de\s+|do\s+)?(\d{4}))?", re.I,
             lambda m: (int(m[1]), _year4(m[2])))                                                                  # 3º trimestre de 2025
_add_quarter(r"(?<![\w])(first|second|third|fourth|1st|2nd|3rd|4th)\s+quarter(?:\s+(?:of\s+)?(\d{4}))?", re.I,
             lambda m: (_ORDINAL_WORDS[m[1].lower()], _year4(m[2])))
_add_quarter(r"(?<![\w])(primeiro|segundo|terceiro|quarto)\s+trimestre(?:\s+(?:de\s+|do\s+)?(\d{4}))?", re.I,
             lambda m: (_ORDINAL_WORDS[m[1].lower()], _year4(m[2])))
_add_quarter(r"(?<![\w.,])Q([1-4])(?![\w])", re.I, lambda m: (int(m[1]), None))                                  # bare Q3
_add_quarter(r"(?<![\w.,])([1-4])T(?![\w])", 0, lambda m: (int(m[1]), None))                                      # bare 3T

_DATE_ISO = re.compile(r"(?<![\w.])(?P<y>\d{4})[-/.](?P<m>\d{1,2})[-/.](?P<d>\d{1,2})(?![\w])")
_DATE_NUMERIC = re.compile(r"(?<![\w.,])(?P<a>\d{1,2})(?P<sep>[/.\-])(?P<b>\d{1,2})(?P=sep)(?P<y>\d{4}|\d{2})(?![\w])")
_DATE_MONTH_YEAR_NUM = re.compile(r"(?<![\w./])(?P<m>\d{1,2})/(?P<y>\d{4})(?![\w/])")
_YEAR_AFTER_MONTH = r"(?:\s*(?:de\s+|of\s+)?,?\s*(?P<y4>\d{4})|\s*[/\-'’]\s*(?P<y2>\d{2}|\d{4}))"
_DATE_DMY_WORDS = re.compile(
    rf"(?<![\w])(?P<d>\d{{1,2}})(?:st|nd|rd|th|º|°)?[\s./\-]*(?:de\s+|of\s+)?(?P<mon>{_MONTH_RE})(?P<dot>\.)?"
    rf"(?:{_YEAR_AFTER_MONTH})?(?![\w])", re.I)
_DATE_MDY_WORDS = re.compile(
    rf"(?<![\w])(?P<mon>{_MONTH_RE})(?P<dot>\.)?\s*(?P<d>\d{{1,2}})(?:st|nd|rd|th)?(?![\d\w])"
    rf"(?:\s*,?\s*(?P<y4>\d{{4}})|\s*[/\-'’]\s*(?P<y2>\d{{2}}))?", re.I)
_DATE_MONTH_YEAR_WORDS = re.compile(
    rf"(?<![\w])(?P<mon>{_MONTH_RE})(?P<dot>\.)?(?:{_YEAR_AFTER_MONTH})(?![\w])", re.I)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Token:
    kind: str                       # number | date | quarter | fy | time | ordinal
    value: Decimal | str            # Decimal for numbers/ordinals, normalised string otherwise
    step: Decimal                   # precision of a number (0 for non-numeric kinds)
    unit: str = ""                  # "" | "%" | "pp" | "x"
    currency: str = ""              # "" | BRL | USD | EUR | GBP
    raw: str = ""
    location: str = ""
    snippet: str = ""
    style: str | None = None        # "pt"/"en" when the written shape proves a locale (e.g. 1.234,5)
    unit_index: int = 0
    scope: str = ""                 # row/paragraph key used to find a possible basis for derived numbers
    start: int = 0

    @property
    def is_numeric(self) -> bool:
        return self.kind in ("number", "ordinal")

    @property
    def number(self) -> Decimal:
        return self.value if isinstance(self.value, Decimal) else Decimal(0)

    def norm(self) -> str:
        """Canonical text such as 'BRL 48700000', '-1.8 pp', '2026-Q3'."""
        if not self.is_numeric:
            return str(self.value)
        text = _plain(self.number)
        if self.unit == "%":
            text += "%"
        elif self.unit == "pp":
            text += " pp"
        elif self.unit == "x":
            text += "x"
        return f"{self.currency} {text}" if self.currency else text

    def key(self) -> tuple:
        """Strict identity: everything except the (tolerant) numeric value."""
        return (self.kind, self.unit, self.currency, "" if self.is_numeric else self.value)

    def to_dict(self) -> dict:
        data = {"location": self.location, "raw": self.raw, "kind": self.kind, "normalized": self.norm(),
                "snippet": self.snippet}
        return data


def _plain(value: Decimal) -> str:
    text = format(value.normalize(), "f") if value else "0"
    return text


# ---------------------------------------------------------------------------
# Number parsing
# ---------------------------------------------------------------------------

@dataclass
class ParsedNumber:
    value: Decimal
    decimals: int
    style: str | None   # "pt" | "en" when the shape alone proves the locale


def _valid_groups(text: str, sep: str) -> bool:
    parts = text.split(sep)
    return 1 <= len(parts[0]) <= 3 and all(len(p) == 3 for p in parts[1:])


def parse_number(raw: str, locale: str, machine: bool = False) -> ParsedNumber | None:
    """Parse a digit string that may contain '.' and ',' separators, or None if its shape is invalid.

    `locale` only matters for the genuinely ambiguous shape: a single separator followed by
    exactly three digits ("1.234" / "1,234").
    """
    if machine or not re.search(r"[.,]", raw):
        try:
            value = Decimal(raw)
        except InvalidOperation:
            return None
        return ParsedNumber(value, len(raw.split(".")[1]) if "." in raw else 0, None)

    has_dot, has_comma = "." in raw, "," in raw
    if has_dot and has_comma:
        decimal_sep = "." if raw.rfind(".") > raw.rfind(",") else ","
        group_sep = "," if decimal_sep == "." else "."
        if raw.count(decimal_sep) != 1:
            return None
        int_part, frac = raw.rsplit(decimal_sep, 1)
        if not _valid_groups(int_part, group_sep):
            return None
        return ParsedNumber(Decimal(int_part.replace(group_sep, "") + "." + frac), len(frac),
                            "pt" if decimal_sep == "," else "en")

    sep = "." if has_dot else ","
    parts = raw.split(sep)
    if len(parts) > 2:  # 1.234.567 or 1,234,567: only thousands separators can repeat
        if not _valid_groups(raw, sep):
            return None
        return ParsedNumber(Decimal("".join(parts)), 0, "pt" if sep == "." else "en")
    int_part, frac = parts
    if len(frac) == 3 and 1 <= len(int_part) <= 3 and int_part != "0":
        grouped = (sep == "." and locale == "pt") or (sep == "," and locale == "en")
        if grouped:
            return ParsedNumber(Decimal(int_part + frac), 0, None)
        return ParsedNumber(Decimal(int_part + "." + frac), 3, None)
    return ParsedNumber(Decimal(int_part + "." + frac), len(frac), "pt" if sep == "," else "en")


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

def _in_spans(spans: list[tuple[int, int]], start: int, end: int) -> bool:
    return any(start < e and end > s for s, e in spans)


def _in_machine(spans: list[list[int]] | None, start: int) -> bool:
    return bool(spans) and any(s <= start < e for s, e in spans)


def _month_number(name: str, has_period: bool, has_year: bool) -> int | None:
    key = name.lower()
    if key in _MONTH_FULL:
        return _MONTH_FULL[key]
    if key in _AMBIGUOUS_ABBR and not (has_period or has_year):
        return None
    return _MONTH_ABBR.get(key)


def _valid_day(year: int | None, month: int, day: int) -> bool:
    if not 1 <= day <= 31:
        return False
    return day <= calendar.monthrange(year if year else 2024, month)[1]  # 2024: leap year, so Feb 29 is allowed


def _date_value(year: int | None, month: int, day: int | None) -> str:
    if year is None:
        return f"--{month:02d}-{day:02d}"
    return f"{year:04d}-{month:02d}" + (f"-{day:02d}" if day is not None else "")


def _plausible_year(year: int | None) -> bool:
    return year is None or PLAUSIBLE_YEARS[0] <= year <= PLAUSIBLE_YEARS[1]


def _find_dates(text: str, locale: str, free: Callable[[int, int], bool]) -> list[tuple[int, int, str]]:
    """Return (start, end, normalised) for dates. `free` says whether a span is still unclaimed."""
    found: list[tuple[int, int, str]] = []

    def add(m: re.Match, value: str) -> None:
        found.append((m.start(), m.end(), value))

    for m in _DATE_ISO.finditer(text):
        y, mo, d = int(m["y"]), int(m["m"]), int(m["d"])
        if free(m.start(), m.end()) and 1 <= mo <= 12 and _plausible_year(y) and _valid_day(y, mo, d):
            add(m, _date_value(y, mo, d))

    for m in _DATE_NUMERIC.finditer(text):
        if not free(m.start(), m.end()) or _in_spans([(s, e) for s, e, _ in found], m.start(), m.end()):
            continue
        a, b, ystr, sep = int(m["a"]), int(m["b"]), m["y"], m["sep"]
        if len(ystr) == 2 and sep != "/":
            continue  # "1.2.26" or "3-4-25" are more likely versions/ranges than dates
        year = _year4(ystr)
        if not _plausible_year(year):
            continue
        # dd/mm vs mm/dd: values above 12 settle it; otherwise the document locale decides.
        if a > 12 and b <= 12:
            day, month = a, b
        elif b > 12 and a <= 12:
            day, month = b, a
        elif sep in ".-" or locale == "pt":
            day, month = a, b
        else:
            month, day = a, b
        if 1 <= month <= 12 and _valid_day(year, month, day):
            add(m, _date_value(year, month, day))

    taken = lambda s, e: not free(s, e) or _in_spans([(a, b) for a, b, _ in found], s, e)  # noqa: E731

    for m in _DATE_MONTH_YEAR_NUM.finditer(text):
        month, year = int(m["m"]), int(m["y"])
        if not taken(m.start(), m.end()) and 1 <= month <= 12 and _plausible_year(year):
            add(m, _date_value(year, month, None))

    for m in _DATE_DMY_WORDS.finditer(text):
        year = _year4(m["y4"] or m["y2"])
        month = _month_number(m["mon"], bool(m["dot"]), year is not None)
        day = int(m["d"])
        if month and not taken(m.start(), m.end()) and _plausible_year(year) and _valid_day(year, month, day):
            add(m, _date_value(year, month, day))

    for m in _DATE_MDY_WORDS.finditer(text):
        year = _year4(m["y4"] or m["y2"])
        month = _month_number(m["mon"], bool(m["dot"]), year is not None)
        day = int(m["d"])
        if month and not taken(m.start(), m.end()) and _plausible_year(year) and _valid_day(year, month, day):
            add(m, _date_value(year, month, day))

    for m in _DATE_MONTH_YEAR_WORDS.finditer(text):
        year = _year4(m["y4"] or m["y2"])
        month = _month_number(m["mon"], bool(m["dot"]), True)
        if month and year and not taken(m.start(), m.end()) and _plausible_year(year):
            add(m, _date_value(year, month, None))
    return found


def tokenize(text: str, locale: str, machine_spans: list[list[int]] | None = None,
             location: str = "", unit_index: int = 0) -> list[Token]:
    """Extract normalised numeric tokens from one text unit."""
    text = text.translate(_CHAR_FOLD)
    blocked: list[tuple[int, int]] = []
    for pattern in (_URL_RE, _EMAIL_RE, _REFERENCE_RE):
        blocked += [(m.start(), m.end()) for m in pattern.finditer(text)]
    blocked += [(m.start("num"), m.end("num")) for m in _LIST_NUMBER_RE.finditer(text)]
    claimed: list[tuple[int, int]] = list(blocked)
    tokens: list[Token] = []

    def free(start: int, end: int) -> bool:
        return not _in_spans(claimed, start, end)

    def snippet(start: int, end: int) -> str:
        lo, hi = max(0, start - SNIPPET_RADIUS), min(len(text), end + SNIPPET_RADIUS)
        body = re.sub(r"\s+", " ", text[lo:hi].replace("\n", " / ")).strip()
        return ("…" if lo > 0 else "") + body + ("…" if hi < len(text) else "")

    def emit(kind: str, value, start: int, end: int, step: Decimal = Decimal(0), unit: str = "",
             currency: str = "", style: str | None = None) -> None:
        claimed.append((start, end))
        tokens.append(Token(kind, value, step, unit, currency, text[start:end].strip(), location,
                            snippet(start, end), style, unit_index, start=start))

    # 1. quarters (before dates and numbers so "3T25" and "Q3 2025" are not split)
    for pattern, build in _QUARTER_PATTERNS:
        for m in pattern.finditer(text):
            if free(m.start(), m.end()):
                quarter, year = build(m)
                if _plausible_year(year):
                    emit("quarter", f"{year}-Q{quarter}" if year else f"Q{quarter}", m.start(), m.end())

    # 2. fiscal years, dates, times
    for m in _FY_RE.finditer(text):
        if free(m.start(), m.end()):
            emit("fy", str(_year4(m[1])), m.start(), m.end())
    for start, end, value in sorted(_find_dates(text, locale, free)):
        if free(start, end):
            emit("date", value, start, end)
    for m in _TIME_RE.finditer(text):
        if free(m.start(), m.end()):
            emit("time", f"{int(m[1]):02d}:{m[2]}", m.start(), m.end())

    # 3. plain numbers with their sign, currency, scale and unit
    for m in _CORE_RE.finditer(text):
        start, end = m.start(), m.end()
        if not free(start, end):
            continue
        machine = _in_machine(machine_spans, start)
        parsed = parse_number(m.group(0), locale, machine)
        if parsed is None:  # malformed grouping, e.g. "1,2,3": fall back to the individual digit runs
            for piece in re.finditer(r"\d+", m.group(0)):
                if free(start + piece.start(), start + piece.end()):
                    emit("number", Decimal(piece.group(0)), start + piece.start(), start + piece.end(), Decimal(1))
            continue

        window_start = max(0, start - 8)
        prefix = _PREFIX_RE.search(text[window_start:start])
        sign, currency, prefix_start = "", "", start
        if prefix and (prefix["s1"] or prefix["cur"] or prefix["s2"]):
            prefix_start = window_start + prefix.start()
            before = text[prefix_start - 1] if prefix_start > 0 else ""
            raw_sign = prefix["s1"] or prefix["s2"] or ""
            if prefix["cur"]:
                code = prefix["cur"]
                if code.isalpha() and before.isalnum():  # "XUSD 5": not a currency code
                    prefix_start, code = window_start + prefix.start("cur") + len(code), ""
                currency = _CURRENCY_CODES.get(code.lower(), "") if code else ""
            if raw_sign:
                if before.isalpha():
                    continue              # "REL-24", "COVID-19": identifier, not a signed number
                if not before.isalnum():  # after a digit it is a range ("4-6"), not a sign
                    sign = "-" if raw_sign == "-" else ""
                elif not currency:
                    prefix_start = start

        suffix = _UNIT_SUFFIX_RE.match(text, end)
        scale_mult, unit, step_factor = 1, "", Decimal(1)
        suffix_end = end
        if suffix and suffix.end() > end:
            suffix_end = suffix.end()
            scale_text = (suffix["scale"] or "").strip()
            if scale_text in _SINGLE_LETTER_SCALES and (suffix["scale"] or "").startswith(" ") and not currency:
                # "Plant 2 B" / "5 M" with no currency is too likely to be a label; ignore the letter.
                scale_text, suffix_end = "", end
                suffix = None
            if scale_text:
                scale_mult = _scale_multiplier(scale_text)
            if suffix is not None:
                if suffix["pct"]:
                    unit = "%"
                elif suffix["pp"]:
                    unit = "pp"
                elif suffix["bps"]:
                    unit, step_factor = "pp", Decimal(1) / BPS_PER_PP
                elif suffix["mult"]:
                    unit = "x"
                elif suffix["cur"] and not currency:
                    currency = _CURRENCY_CODES.get(re.sub(r"^\s?(?:de\s+)?", "", suffix["cur"], flags=re.I).lower().strip(), "")
        if suffix_end == end:
            glued = text[end:end + 1]
            ordinal = _ORDINAL_SUFFIX_RE.match(text, end)
            if ordinal:
                emit("ordinal", parsed.value, prefix_start, end + len(ordinal.group(0)), Decimal(1))
                continue
            if glued.isalpha():
                unit_match = _GLUED_UNIT_RE.match(text, end)
                if not unit_match:
                    continue  # glued letters that are not a unit: an identifier such as "3PL" or "2FA"
                suffix_end = end + len(unit_match.group(0))

        step = (Decimal(1).scaleb(-parsed.decimals)) * scale_mult * step_factor
        value = parsed.value * scale_mult * step_factor
        if sign == "-":
            value = -value
        emit("number", value, prefix_start, max(suffix_end, end), step, unit, currency, parsed.style)

    tokens.sort(key=lambda t: t.start)
    return tokens


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------

_ROW_RE = re.compile(r"^(.*table(?: \d+)? r\d+)c\d+$")
_SHEET_ROW_RE = re.compile(r"^(.+!)[A-Z]+(\d+)$")


def _scope_for(unit: dict, index: int, line: int) -> str:
    """Key shared by numbers that sit on one visual row/paragraph (used for 'possible basis' hints)."""
    location = unit["location"]
    row = _ROW_RE.match(location)
    if row:
        return row.group(1)
    sheet = _SHEET_ROW_RE.match(location)
    if sheet:
        return sheet.group(1) + "row" + sheet.group(2)
    return f"{location}#{line}"


@dataclass
class Doc:
    path: Path
    language: str
    locale: str
    locale_evidence: dict
    tokens: list[Token]
    units: list[dict]
    warnings: list[str] = field(default_factory=list)


def detect_number_locale(units: list[dict], language: str) -> tuple[str, dict]:
    """Decide how ambiguous separators should be read, from the unambiguous numbers in the document."""
    evidence = {"pt": 0, "en": 0}
    for unit in units:
        text = unit["text"].translate(_CHAR_FOLD)
        for m in _CORE_RE.finditer(text):
            if _in_machine(unit.get("machine_spans"), m.start()):
                continue
            parsed = parse_number(m.group(0), "en")
            if parsed and parsed.style:
                evidence[parsed.style] += 1
    if evidence["pt"] > evidence["en"]:
        return "pt", evidence
    if evidence["en"] > evidence["pt"]:
        return "en", evidence
    return language, evidence


def load_doc(path: Path, locale_override: str | None = None) -> Doc:
    units, warnings = doc_text.extract_with_warnings(path)
    language = doc_text.detect_language(" ".join(u["text"] for u in units if not u.get("machine_spans")))
    locale, evidence = detect_number_locale(units, language)
    if locale_override:
        locale = locale_override
    tokens: list[Token] = []
    for index, unit in enumerate(units):
        if unit.get("formula"):
            continue
        lines = unit["text"].split("\n")
        if len(lines) == 1 or unit.get("machine_spans"):
            found = tokenize(unit["text"], locale, unit.get("machine_spans"), unit["location"], index)
            for token in found:
                token.scope = _scope_for(unit, index, 0)
            tokens += found
            continue
        # Multi-line units (bullets): tokenise per line so scopes and list numbering are per bullet.
        for line_no, line in enumerate(lines):
            found = tokenize(line, locale, None, unit["location"], index)
            for token in found:
                token.scope = _scope_for(unit, index, line_no)
            tokens += found
    return Doc(path, language, locale, evidence, tokens, units, warnings)


# ---------------------------------------------------------------------------
# Matching engine
# ---------------------------------------------------------------------------

class _Index:
    """Targets bucketed by key and sorted by value, so tolerant lookups stay fast on big sheets."""

    def __init__(self, tokens: Iterable[Token], key: Callable[[Token], tuple], use_abs: bool = False) -> None:
        self.key, self.use_abs = key, use_abs
        raw: dict[tuple, list[tuple[float, int, Token]]] = {}
        for n, token in enumerate(tokens):
            value = abs(token.number) if use_abs else token.number
            raw.setdefault(key(token), []).append((float(value), n, token))
        self.buckets = {k: sorted(v, key=lambda item: (item[0], item[1])) for k, v in raw.items()}
        self.floats = {k: [item[0] for item in v] for k, v in self.buckets.items()}
        self.max_step = {k: max((float(item[2].step) for item in v), default=0.0) for k, v in self.buckets.items()}
        self.used: set[int] = set()

    def take(self, token: Token, same_location: bool = False, exact: bool = False, consume: bool = True) -> Token | None:
        """Return the best unused match for `token` (and mark it used unless consume=False), or None."""
        bucket_key = self.key(token)
        bucket = self.buckets.get(bucket_key)
        if not bucket:
            return None
        value = abs(token.number) if self.use_abs else token.number
        window = max(float(token.step), self.max_step[bucket_key]) / 2 + 1e-9
        position = bisect.bisect_left(self.floats[bucket_key], float(value) - window)
        best, best_diff = None, None
        while position < len(bucket):
            number, _, candidate = bucket[position]
            position += 1
            if number > float(value) + window:
                break
            if id(candidate) in self.used or (same_location and candidate.location != token.location):
                continue
            other = abs(candidate.number) if self.use_abs else candidate.number
            diff = abs(other - value)
            limit = Decimal(0) if exact else max(token.step, candidate.step) / 2
            if diff <= limit and (best is None or diff < best_diff):
                best, best_diff = candidate, diff
                if diff == 0:
                    break
        if best is not None and consume:
            self.used.add(id(best))
        return best


@dataclass
class Pair:
    source: Token
    target: Token
    level: str   # exact | rounded | sign | currency | unit


def _key_strict(t: Token) -> tuple:
    return t.key()


def _key_no_currency(t: Token) -> tuple:
    return (t.kind, t.unit, "" if t.is_numeric else t.value)


def _key_no_unit(t: Token) -> tuple:
    return (t.kind, "" if t.is_numeric else t.value)


def match_multiset(source: list[Token], target: list[Token]) -> tuple[list[Pair], list[Token], list[Token]]:
    """Pair source and target tokens; return (pairs, unmatched_source, unmatched_target)."""
    pairs: list[Pair] = []
    remaining_source = list(source)

    def run(index: _Index, tokens: list[Token], level: str, same_location: bool, exact: bool,
            only_numeric: bool = False) -> list[Token]:
        left = []
        for token in tokens:
            if only_numeric and not token.is_numeric:
                left.append(token)
                continue
            hit = index.take(token, same_location=same_location, exact=exact)
            if hit is None:
                left.append(token)
            else:
                pairs.append(Pair(token, hit, level))
        return left

    strict = _Index(target, _key_strict)
    remaining_source = run(strict, remaining_source, "exact", True, True)       # same place, identical value
    remaining_source = run(strict, remaining_source, "exact", False, True)      # identical value elsewhere
    remaining_source = run(strict, remaining_source, "rounded", True, False)    # same place, within rounding
    remaining_source = run(strict, remaining_source, "rounded", False, False)

    def leftover_targets() -> list[Token]:
        return [t for t in target if id(t) not in strict.used]

    for level, key, use_abs in (("sign", _key_strict, True), ("currency", _key_no_currency, False),
                                ("unit", _key_no_unit, False)):
        if not remaining_source:
            break
        index = _Index([t for t in leftover_targets() if t.is_numeric], key, use_abs)
        before = len(pairs)
        remaining_source = run(index, remaining_source, level, False, False, only_numeric=True)
        for pair in pairs[before:]:
            strict.used.add(id(pair.target))
    return pairs, remaining_source, leftover_targets()


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------

def _count_by_location(tokens: list[Token]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token.location] = counts.get(token.location, 0) + 1
    return counts


def _likely_edits(missing: list[Token], extra: list[Token]) -> dict[int, Token]:
    """Pair each missing source number with an extra target number at the same location (probable edit)."""
    hints: dict[int, Token] = {}
    claimed: set[int] = set()
    by_location: dict[str, list[Token]] = {}
    for token in extra:
        by_location.setdefault(token.location, []).append(token)
    for token in missing:
        candidates = [t for t in by_location.get(token.location, []) if id(t) not in claimed and t.kind == token.kind]
        same_unit = [t for t in candidates if (t.unit, t.currency) == (token.unit, token.currency)]
        pool = same_unit or candidates
        if not pool:
            continue
        if token.is_numeric:
            pool = sorted(pool, key=lambda t: abs(t.number - token.number))
        hint = pool[0]
        claimed.add(id(hint))
        hints[id(token)] = hint
    return hints


def _format_notes(doc: Doc, role: str) -> list[str]:
    words = sum(doc_text.language_scores(" ".join(u["text"] for u in doc.units if not u.get("machine_spans"))))
    if words < MIN_DOC_WORDS_FOR_FORMAT_NOTE:
        return []
    wrong_style = "pt" if doc.language == "en" else "en"
    bad = [t for t in doc.tokens if t.style == wrong_style and t.is_numeric]
    if not bad:
        return []
    shape = {"pt": "pt-BR format (comma decimals / dot thousands)", "en": "English format (dot decimals / comma thousands)"}
    examples = "; ".join(f"{t.raw!r} at {t.location}" for t in bad[:MAX_FORMAT_NOTES])
    more = f" (+{len(bad) - MAX_FORMAT_NOTES} more)" if len(bad) > MAX_FORMAT_NOTES else ""
    return [f"{role} reads as {'English' if doc.language == 'en' else 'Portuguese'} but {len(bad)} number(s) use "
            f"{shape[wrong_style]}: {examples}{more}"]


def compare_docs(source: Doc, target: Doc) -> dict:
    pairs, missing, extra = match_multiset(source.tokens, target.tokens)
    hints = _likely_edits(missing, extra)

    def describe(token: Token, hint: Token | None = None) -> dict:
        data = token.to_dict()
        if hint is not None:
            data["likely_counterpart"] = hint.to_dict()
        return data

    reverse_hints = {id(hints[id(s)]): s for s in missing if id(s) in hints}
    missing_items = [describe(t, hints.get(id(t))) for t in missing]
    extra_items = [describe(t, reverse_hints.get(id(t))) for t in extra]

    differences = [{"type": p.level, "source": p.source.to_dict(), "target": p.target.to_dict()}
                   for p in pairs if p.level in ("sign", "currency", "unit")]
    rounded = [{"source": p.source.to_dict(), "target": p.target.to_dict()} for p in pairs if p.level == "rounded"]

    src_counts, tgt_counts = _count_by_location(source.tokens), _count_by_location(target.tokens)
    shared = set(src_counts) & set(tgt_counts)
    smaller = min(len(src_counts), len(tgt_counts)) or 1
    comparable = len(shared) / smaller >= LOCATION_OVERLAP_MIN
    count_diffs = []
    if comparable:
        first_seen: dict[str, int] = {}
        for token in source.tokens:
            first_seen.setdefault(token.location, token.unit_index)
        count_diffs = [{"location": loc, "source_count": src_counts[loc], "target_count": tgt_counts[loc]}
                       for loc in sorted(shared, key=lambda l: (first_seen[l], l))
                       if src_counts[loc] != tgt_counts[loc]]

    notes = _format_notes(target, "target")
    if source.language == target.language:
        notes.append(f"source and target both read as {'English' if source.language == 'en' else 'Portuguese'}: "
                     "is this the right pair of files?")
    exact = sum(1 for p in pairs if p.level == "exact")
    return {
        "command": "compare",
        "source": {"file": source.path.as_posix(), "language": source.language, "number_format": source.locale,
                   "numbers": len(source.tokens)},
        "target": {"file": target.path.as_posix(), "language": target.language, "number_format": target.locale,
                   "numbers": len(target.tokens)},
        "summary": {"matched_exact": exact, "matched_within_rounding": len(rounded),
                    "missing_in_target": len(missing), "extra_in_target": len(extra),
                    "matched_with_differences": len(differences), "location_count_differences": len(count_diffs),
                    "locations_comparable": comparable},
        "missing_in_target": missing_items,
        "extra_in_target": extra_items,
        "location_count_differences": count_diffs,
        "matched_with_differences": differences,
        "matched_within_rounding": rounded,
        "notes": notes + source.warnings + target.warnings,
    }


def _fmt_token(item: dict) -> str:
    raw, norm = item["raw"], item["normalized"]
    return f"{raw!r}" if raw == norm else f"{raw!r} = {norm}"


def render_compare(result: dict) -> str:
    s = result["summary"]
    lines = ["numbers_check compare",
             f"  source: {result['source']['file']}  ({result['source']['language']} text, "
             f"{result['source']['number_format']} number format, {result['source']['numbers']} numbers)",
             f"  target: {result['target']['file']}  ({result['target']['language']} text, "
             f"{result['target']['number_format']} number format, {result['target']['numbers']} numbers)", ""]
    problems = s["missing_in_target"] + s["extra_in_target"] + s["matched_with_differences"]
    if problems == 0:
        lines.append(f"RESULT: OK - all {result['source']['numbers']} source numbers are in the target "
                     f"({s['matched_exact']} identical, {s['matched_within_rounding']} within rounding); no extra numbers.")
    else:
        lines.append(f"RESULT: {s['missing_in_target']} source number(s) missing, {s['extra_in_target']} extra in target, "
                     f"{s['matched_with_differences']} matched with a sign/currency/unit difference. Fix or explain each.")

    def section(title: str, items: list[dict], side: str, counterpart_label: str) -> None:
        lines.extend(["", f"{title} ({len(items)})"])
        for item in items:
            lines.append(f"  - {_fmt_token(item)}  at {item['location']}")
            lines.append(f"      {side}: {item['snippet']}")
            hint = item.get("likely_counterpart")
            if hint:
                lines.append(f"      likely edited to {_fmt_token(hint)} ({counterpart_label}: {hint['snippet']})")

    if result["missing_in_target"]:
        section("(a) Source numbers missing from target", result["missing_in_target"], "source", "target")
    if result["extra_in_target"]:
        section("(b) Target numbers absent from source", result["extra_in_target"], "target", "source")
    if result["location_count_differences"]:
        lines.extend(["", f"(c) Locations whose number counts differ ({len(result['location_count_differences'])})"])
        for d in result["location_count_differences"]:
            lines.append(f"  - {d['location']}: source {d['source_count']}, target {d['target_count']}")
    elif not s["locations_comparable"]:
        lines.extend(["", "(c) Per-location counts skipped: the two files do not share enough locations "
                          "(different structure or format)."])
    if result["matched_with_differences"]:
        lines.extend(["", f"(d) Matched, but with a difference ({len(result['matched_with_differences'])})"])
        label = {"sign": "sign differs", "currency": "currency differs or is missing", "unit": "unit differs (% / p.p. / none)"}
        for d in result["matched_with_differences"]:
            lines.append(f"  - {label[d['type']]}: {_fmt_token(d['source'])} at {d['source']['location']}  ->  "
                         f"{_fmt_token(d['target'])} at {d['target']['location']}")
    if result["matched_within_rounding"]:
        lines.extend(["", f"Info: {len(result['matched_within_rounding'])} number(s) matched only after rounding "
                          "(precision changed):"])
        for d in result["matched_within_rounding"][:MAX_FORMAT_NOTES]:
            lines.append(f"  - {_fmt_token(d['source'])} -> {_fmt_token(d['target'])}  at {d['source']['location']}")
    if result["notes"]:
        lines.extend(["", "Notes"])
        lines.extend(f"  - {note}" for note in result["notes"])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# trace
# ---------------------------------------------------------------------------

def _is_year_like(token: Token) -> bool:
    """Bare years, year-months, quarter labels and fiscal years: period labels, not quantities."""
    if token.kind in ("quarter", "fy"):
        return True
    if token.kind == "date":
        return re.fullmatch(r"\d{4}-\d{2}", str(token.value)) is not None
    if token.kind == "number" and not token.unit and not token.currency and re.fullmatch(r"\d{4}", token.raw.strip()):
        return YEAR_RANGE[0] <= int(token.number) <= YEAR_RANGE[1]
    return False


class _SourceSet:
    """All numbers found in the sources, queryable with the same tolerance rules (not consumed on use)."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.strict = _Index(tokens, _key_strict)
        self.relaxed = _Index([t for t in tokens if t.is_numeric], _key_no_unit, use_abs=True)
        self.numeric = [t for t in tokens if t.is_numeric]

    def find(self, token: Token) -> tuple[Token, str] | None:
        """Look `token` up without consuming anything: one source number may back many deliverable numbers."""
        hit = self.strict.take(token, consume=False)
        if hit:
            return hit, "exact"
        if not token.is_numeric:
            return None
        hit = self.relaxed.take(token, consume=False)
        if hit:
            return hit, "unit/sign ignored"
        for shift in SCALE_SHIFTS:
            for factor, exponent in ((Decimal(10) ** shift, shift), (Decimal(10) ** -shift, -shift)):
                scaled = Token("number", token.number * factor, token.step * factor, token.unit, token.currency)
                hit = self.relaxed.take(scaled, consume=False)
                if hit:
                    return hit, f"scale shifted by 10^{exponent}"
        return None


def _basis_hint(token: Token, scope_tokens: list[Token]) -> str | None:
    """Look for a two-number calculation (same sentence/row) that reproduces an untraced number."""
    if not token.is_numeric:
        return None
    others = [t for t in scope_tokens if t is not token and t.kind == "number"]
    half_v = token.step / 2
    v = token.number
    for a in others:
        for b in others:
            if a is b:
                continue
            calcs = [("difference", a.number - b.number, a.step / 2 + b.step / 2, f"{a.raw} - {b.raw}"),
                     ("sum", a.number + b.number, a.step / 2 + b.step / 2, f"{a.raw} + {b.raw}")]
            if b.number != 0:
                rel = (a.step / 2 / abs(a.number) if a.number else Decimal(0)) + b.step / 2 / abs(b.number)
                ratio = a.number / b.number
                calcs += [("percent change", (ratio - 1) * 100, abs(ratio) * 100 * rel, f"{a.raw} vs {b.raw}"),
                          ("share, in %", ratio * 100, abs(ratio) * 100 * rel, f"{a.raw} / {b.raw}"),
                          ("ratio", ratio, abs(ratio) * rel, f"{a.raw} / {b.raw}")]
            for name, computed, error, label in calcs:
                if abs(computed - v) <= half_v + error:
                    return f"{name} of {label}"
    return None


def trace_docs(deliverable: Doc, sources: list[Doc], ignore_years: bool = True) -> dict:
    source_set = _SourceSet([t for doc in sources for t in doc.tokens])
    scopes: dict[str, list[Token]] = {}
    for token in deliverable.tokens:
        scopes.setdefault(token.scope, []).append(token)

    considered = [t for t in deliverable.tokens if not (ignore_years and _is_year_like(t))]
    traced_exact = traced_loose = 0
    loose, untraced = [], []
    for token in considered:
        found = source_set.find(token)
        if found is None:
            untraced.append(token)
        elif found[1] == "exact":
            traced_exact += 1
        else:
            traced_loose += 1
            loose.append({"number": token.to_dict(), "matched_via": found[1], "source_number": found[0].raw,
                          "source_location": found[0].location})

    by_location: dict[str, list[dict]] = {}
    for token in untraced:
        item = token.to_dict()
        basis = _basis_hint(token, scopes.get(token.scope, []))
        if basis:
            item["possible_basis"] = basis
        by_location.setdefault(token.location, []).append(item)

    return {
        "command": "trace",
        "deliverable": {"file": deliverable.path.as_posix(), "language": deliverable.language,
                        "number_format": deliverable.locale},
        "sources": [{"file": d.path.as_posix(), "number_format": d.locale, "numbers": len(d.tokens)} for d in sources],
        "summary": {"numbers_checked": len(considered), "traced": traced_exact, "traced_loosely": traced_loose,
                    "untraced": len(untraced), "ignored_period_labels": len(deliverable.tokens) - len(considered)},
        "untraced_by_location": by_location,
        "untraced": [item for items in by_location.values() for item in items],
        "traced_loosely": loose,
        "notes": ["Untraced numbers are either derived calculations (label them as derived and show the basis in the "
                  "deliverable) or fabrications (remove or source them).",
                  "Differences and ratios of source numbers (e.g. -2.8% computed from 86.2 and 88.7) legitimately appear "
                  "as untraced: verify them, do not delete them."]
                 + deliverable.warnings,
    }


def render_trace(result: dict) -> str:
    s = result["summary"]
    lines = ["numbers_check trace",
             f"  deliverable: {result['deliverable']['file']}  ({result['deliverable']['number_format']} number format)",
             "  sources:     " + ", ".join(f"{d['file']} ({d['numbers']} numbers)" for d in result["sources"]), ""]
    lines.append(f"RESULT: {s['untraced']} of {s['numbers_checked']} numbers in the deliverable match no source "
                 f"({s['traced']} traced exactly, {s['traced_loosely']} traced ignoring unit/sign/scale"
                 + (f"; {s['ignored_period_labels']} year/quarter labels ignored" if s["ignored_period_labels"] else "") + ").")
    for location, items in result["untraced_by_location"].items():
        lines.extend(["", location])
        for item in items:
            lines.append(f"  - {_fmt_token(item)}  [{item['kind']}]")
            lines.append(f"      {item['snippet']}")
            if item.get("possible_basis"):
                lines.append(f"      possible basis (verify, then label it as derived): {item['possible_basis']}")
    if result["traced_loosely"]:
        lines.extend(["", f"Info: {len(result['traced_loosely'])} number(s) matched a source only after ignoring "
                          "unit, sign or a 10^3 scale shift (see --json for the list)."])
    lines.extend(["", "Notes"] + [f"  - {n}" for n in result["notes"]])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _locale_arg(parser: argparse.ArgumentParser, flag: str, help_text: str) -> None:
    parser.add_argument(flag, choices=("pt", "en"), default=None, help=help_text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="numbers_check.py",
        description="Numeric fidelity (compare) and traceability (trace) checks for translated or generated deliverables. "
                    "Locale-aware: pt-BR 1.234,5 and en 1,234.5 are the same number; 'R$ 48,7 mi' equals 'BRL 48.7 million'.",
        epilog="Exit codes: 0 ran fine, 1 usage/IO error, 2 only with --strict when discrepancies exist.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    cmp_parser = sub.add_parser("compare", help="check that every number in SOURCE survives in TARGET (translations)")
    cmp_parser.add_argument("source")
    cmp_parser.add_argument("target")
    _locale_arg(cmp_parser, "--source-locale", "force how ambiguous separators in SOURCE are read (default: auto-detect)")
    _locale_arg(cmp_parser, "--target-locale", "force how ambiguous separators in TARGET are read (default: auto-detect)")
    cmp_parser.add_argument("--json", action="store_true", help="machine-readable JSON output")
    cmp_parser.add_argument("--strict", action="store_true", help="exit 2 if any discrepancy is found")

    trace_parser = sub.add_parser("trace", help="list deliverable numbers that appear in no source (no invented numbers)")
    trace_parser.add_argument("deliverable")
    trace_parser.add_argument("--sources", nargs="+", required=True, metavar="SRC", help="source files the numbers must come from")
    years = trace_parser.add_mutually_exclusive_group()
    years.add_argument("--ignore-years", dest="include_years", action="store_false",
                       help="ignore bare years, year-months and quarter labels (default)")
    years.add_argument("--include-years", dest="include_years", action="store_true",
                       help="also check years, year-months and quarter labels")
    trace_parser.set_defaults(include_years=False)
    _locale_arg(trace_parser, "--deliverable-locale", "force how ambiguous separators in the deliverable are read")
    _locale_arg(trace_parser, "--source-locale", "force how ambiguous separators in all sources are read")
    trace_parser.add_argument("--json", action="store_true", help="machine-readable JSON output")
    trace_parser.add_argument("--strict", action="store_true", help="exit 2 if any untraced number is found")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "compare":
            source = load_doc(Path(args.source), args.source_locale)
            target = load_doc(Path(args.target), args.target_locale)
            result = compare_docs(source, target)
            problems = (result["summary"]["missing_in_target"] + result["summary"]["extra_in_target"]
                        + result["summary"]["matched_with_differences"])
            text = render_compare(result)
        else:
            deliverable = load_doc(Path(args.deliverable), args.deliverable_locale)
            sources = [load_doc(Path(p), args.source_locale) for p in args.sources]
            result = trace_docs(deliverable, sources, ignore_years=not args.include_years)
            problems = result["summary"]["untraced"]
            text = render_trace(result)
    except (FileNotFoundError, doc_text.UnsupportedFormat, doc_text.MissingDependency) as exc:
        print(f"numbers_check: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # corrupt or protected files raise assorted library errors
        print(f"numbers_check: could not read input ({exc.__class__.__name__}: {exc})", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else text)
    return 2 if args.strict and problems else 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.stdout.flush()
    except BrokenPipeError:
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        exit_code = 0
    sys.exit(exit_code)
