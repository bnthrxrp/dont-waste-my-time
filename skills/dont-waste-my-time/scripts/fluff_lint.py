#!/usr/bin/env python3
"""fluff_lint.py - anti-fluff heuristic linter for executive writing (English and Portuguese).

THIS IS A HEURISTIC AID FOR HUMAN JUDGMENT, NOT A JUDGE. It finds patterns that
usually signal padding, unsupported claims or weak structure. Some findings will
be false positives (quote them or ignore them); text that passes can still be
bad. Use it to point your attention, then decide.

Usage
-----
    python3 fluff_lint.py FILE [FILE ...] [--lang auto|en|pt] [--json] [--strict]

    FILE      anything doc_text.py reads: .pptx .docx .xlsx .csv .md .txt .html
    --lang    language of the text; "auto" (default) detects it per file from
              stopword frequencies. Language selects phrase lists and thresholds.
    --json    machine-readable output
    --strict  exit 2 if any high-severity finding exists (for use as a gate)

Exit codes: 0 ran fine; 1 usage/IO error (unreadable file, missing library);
2 only with --strict when high-severity findings exist (1 wins if both happen).

Rules (id, severity)
--------------------
FILLER (medium)           generic openers and padding ("in today's rapidly changing",
                          "vale ressaltar", "going forward"...). Lists: FILLER_EN, FILLER_PT.
UNSUPPORTED_CLAIM (high)  evaluative words (significant, robust, forte, expressivo...) in a
                          sentence with no quantity, and none in the adjacent sentences of
                          the same paragraph. Years and quarter labels do not count as
                          quantities. Fix: add the number, or delete the adjective.
VAGUE_ACTION (medium)     action items without substance ("continue to monitor", "review
                          pricing", "acompanhar", "dar seguimento") that name neither a date
                          nor an owner. Only phrased-as-action text counts: the phrase must
                          start the sentence, follow a modal ("will", "should", "deve"), or sit
                          under a Next steps / Actions / Recommendations heading.
HEDGE (low)               stacked hedges (2+ of very/really/quite/muito/bastante/talvez...
                          in one sentence) or any hedge in a title.
LONG_SENTENCE (low)       over 35 words (EN) / 40 (PT). Plain-language guidance commonly
                          targets an average of ~15-25 words per sentence; 35 is a
                          conservative outlier threshold. Portuguese runs longer for the same
                          content (longer words, more function words), hence 40.
REPETITION (medium)       near-duplicate sentences anywhere in the document (>= 8 words,
                          token-set Jaccard >= 0.8). "Source:/Note:" lines are exempt.
LABEL_TITLE (high, pptx)  slide titles that name a topic instead of stating a takeaway:
                          in a stoplist (Agenda, Overview, Next Steps...) or <= 4 words with
                          no verb-like word and no digit. Slide 1 is exempt.
DENSE_SLIDE (medium, pptx) more than 70 words or more than 6 bullets of body text on one slide
                          (notes, tables, charts and source lines excluded). Heuristic limits
                          in the spirit of the "6 lines / 6 words" slide rules of thumb.

Every finding has: rule, severity, location, snippet (<= 120 chars), suggestion.
The summary counts findings by rule and severity and ends with a one-line verdict.
Phrase lists and thresholds are module-level constants; extend them freely.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent))
import doc_text  # noqa: E402  (shared extraction; must follow the sys.path tweak)

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------

SNIPPET_LIMIT = 120                      # max characters of quoted context in a finding
LONG_SENTENCE_WORDS = {"en": 35, "pt": 40}  # see module docstring for the rationale
REPETITION_MIN_WORDS = 8                 # shorter sentences repeat legitimately (headers, labels)
REPETITION_JACCARD = 0.8                 # token-set similarity that counts as "the same sentence"
HEDGE_MIN_PER_SENTENCE = 2               # one hedge is fine; stacked hedges blur the claim
LABEL_TITLE_MAX_WORDS = 4                # a 4-word noun phrase is almost always a label, not a claim
DENSE_SLIDE_MAX_WORDS = 70               # ~1 minute of reading; heuristic, not a law
DENSE_SLIDE_MAX_BULLETS = 6              # heuristic upper bound for scannable bullets
SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}

# ---------------------------------------------------------------------------
# Phrase lists (case-insensitive, word-boundary, hyphen/space tolerant, accent tolerant)
# ---------------------------------------------------------------------------

FILLER_EN = [
    # scene-setting openers
    "in today's rapidly changing", "in today's rapidly evolving", "in today's fast-paced", "in today's dynamic",
    "in today's competitive", "in today's digital age", "in today's world", "in today's business environment",
    "in an ever-changing", "in an increasingly", "in a rapidly", "rapidly evolving", "rapidly changing",
    "ever-evolving", "ever-changing", "fast-paced environment", "dynamic and challenging",
    # throat-clearing
    "it is important to note", "it's important to note", "it is worth noting", "it's worth noting",
    "it is worth mentioning", "it should be noted", "it goes without saying", "needless to say",
    "as a matter of fact", "at this point in time", "due to the fact that", "in the event that",
    "as you may already be aware", "as you may know", "as you are aware", "it is crucial to",
    "plays a crucial role", "plays a pivotal role", "plays a key role", "plays a vital role",
    "more important than ever", "this report aims to", "this document aims to", "aims to provide", "the purpose of this document is to",
    # email filler
    "i just wanted to", "just wanted to", "i wanted to reach out", "feel free to reach out",
    "do not hesitate to", "don't hesitate to", "please don't hesitate", "please let me know your thoughts",
    "i hope this email finds you well", "i hope this finds you well", "at your earliest convenience",
    "thank you for your continued", "continued dedication and hard work", "hard work and dedication",
    "reach out", "touch base", "circle back", "ping you",
    # consultant-speak
    "holistic", "leverage synergies", "synergistic", "move the needle", "going forward", "moving forward",
    "at the end of the day", "comprehensive overview", "comprehensive and holistic", "best-in-class",
    "world-class", "cutting-edge", "state-of-the-art", "game-changer", "game changing", "paradigm shift",
    "deep dive", "low-hanging fruit", "think outside the box", "win-win", "take it to the next level",
    "unlock the full potential", "unlock value", "value-add", "mission-critical", "delve into", "delve deeper",
    "navigate the complexities", "testament to", "underscores the importance",
]

FILLER_PT = [
    # scene-setting openers
    "no cenário atual", "no cenário econômico atual", "em um mundo cada vez mais", "em um cenário cada vez mais",
    "em um ambiente cada vez mais", "no mundo atual", "no mundo corporativo atual", "nos dias de hoje",
    "nos dias atuais", "cada vez mais competitivo", "em constante transformação", "em constante evolução",
    "em constante mudança", "mercado dinâmico e desafiador", "ambiente dinâmico e desafiador",
    # throat-clearing
    "vale ressaltar", "vale destacar", "vale mencionar", "vale salientar", "vale lembrar",
    "vale a pena ressaltar", "é importante destacar", "é importante ressaltar", "é importante salientar",
    "é importante mencionar", "é válido ressaltar", "é válido destacar", "é fundamental destacar",
    "cabe destacar", "cabe ressaltar", "cabe salientar", "cabe mencionar", "importante frisar",
    "diante do exposto", "diante do cenário", "nesse sentido", "neste sentido", "nesse contexto",
    "neste contexto", "em suma", "em linhas gerais", "de forma geral", "de maneira geral", "de modo geral",
    "no que tange", "no que diz respeito", "no que concerne", "desnecessário dizer", "não é segredo que",
    "como já é de conhecimento de todos", "como é de conhecimento", "como todos sabem", "como é sabido",
    "o presente relatório tem como objetivo", "o presente documento tem por objetivo",
    "este relatório tem como objetivo", "tem como objetivo apresentar",
    # email filler
    "qualquer dúvida, estou à disposição", "fico à disposição", "ficamos à disposição",
    "não hesite em entrar em contato", "espero que este e-mail o encontre bem", "agradecemos a dedicação",
    "empenho e dedicação", "dedicação e empenho", "fazer um alinhamento", "realizar um alinhamento",
    "fazer um follow-up", "dar um follow",
    # consultant-speak
    "alavancar sinergias", "visão holística", "abordagem holística", "olhar holístico", "holístico",
    "mudar o patamar", "mudar de patamar", "próximo patamar", "novo patamar", "virar a chave",
    "mover o ponteiro", "ao final do dia", "no final do dia", "no fim do dia", "daqui para frente",
    "daqui pra frente", "de agora em diante", "visão abrangente", "análise abrangente", "visão geral abrangente",
    "mudança de paradigma", "quebra de paradigma", "quebrar paradigmas", "classe mundial", "pensar fora da caixa",
    "ganha-ganha", "levar ao próximo nível",
    # English jargon that Brazilian corporate writing imports wholesale
    "deep dive", "game changer", "game-changer", "best-in-class", "best in class", "world-class", "cutting-edge",
    "low-hanging fruit", "win-win", "touch base", "mergulho profundo",
]

# Optional replacement advice for specific phrases (normalised: lower-case, single spaces).
# Anything not listed gets the generic suggestion.
FILLER_HINTS = {
    "going forward": "Replace with the actual date or period ('from Q1', 'from January').",
    "moving forward": "Replace with the actual date or period, or delete.",
    "reach out": "Say the real action: email, call or meet - and name who and when.",
    "touch base": "Say the real action: meet, call or email - and name who and when.",
    "holistic": "Name what is covered instead of calling it holistic (which functions, which markets).",
    "move the needle": "Quantify the movement you expect (metric, size, date).",
    "leverage synergies": "State the synergy as a number and an owner, or cut it.",
    "deep dive": "Say what will be analysed and what decision it feeds.",
    "daqui para frente": "Troque pela data ou período concreto.",
    "vale ressaltar": "Corte a expressão e comece pelo fato.",
    "vale destacar": "Corte a expressão e comece pelo fato.",
    "nesse sentido": "Corte a expressão; ligue as frases pela lógica, não por conectores vazios.",
    "mudar o patamar": "Diga quanto, em qual indicador e até quando.",
    "no cenário atual": "Corte a abertura e comece pelo resultado ou pela decisão.",
}
FILLER_DEFAULT_HINT = {
    "en": "Delete it and lead with the fact (what changed, by how much, so what).",
    "pt": "Corte a expressão e comece pelo fato (o que mudou, quanto, e daí).",
}

CLAIM_EN = [
    r"significant(?:ly)?", r"substantial(?:ly)?", r"excellent", r"exceptional(?:ly)?", r"outstanding", r"robust",
    r"strong(?:est|er|ly)?", r"solid", r"remarkabl[ey]", r"impressive(?:ly)?", r"tremendous(?:ly)?",
    r"dramatic(?:ally)?", r"unprecedented", r"huge",
]
CLAIM_PT = [
    r"significativ[oa]s?", r"significativamente", r"expressiv[oa]s?", r"expressivamente", r"excelentes?",
    r"excepciona(?:l|is)", r"robust[oa]s?", r"s[óo]lid[oa]s?", r"fortes?", r"fortemente", r"not[áa]ve(?:l|is)",
    r"impressionantes?", r"enormes?", r"extraordin[áa]ri[oa]s?",
]
# "statistically significant" is a precise term, not an evaluative adjective.
CLAIM_EXEMPT = re.compile(r"statistically\s+significant|estatisticamente\s+significativ", re.I)

HEDGE_EN = [r"very", r"really", r"quite", r"somewhat", r"basically", r"actually", r"rather(?!\s+than)", r"fairly",
            r"perhaps", r"possibly", r"arguably", r"maybe", r"kind\s+of", r"sort\s+of", r"a\s+bit"]
HEDGE_PT = [r"muit[oa]s?", r"bastantes?", r"realmente", r"basicamente", r"praticamente", r"talvez", r"relativamente",
            r"possivelmente", r"um\s+pouco", r"de\s+certa\s+forma", r"de\s+certo\s+modo", r"mais\s+ou\s+menos"]

VAGUE_EN = [
    r"continue(?:s|d)?\s+to\s+(?:monitor|explore|evaluate|assess|review|look)", r"continue\s+monitoring",
    r"monitor(?:ing)?\s+(?:closely|the\s+(?:situation|market|trend|trends))", r"keep\s+an\s+eye\s+on",
    r"explore\s+(?:the\s+)?(?:options|alternatives|opportunities|possibilities)",
    r"consider\s+(?:the\s+)?(?:options|alternatives|possibilities)",
    r"evaluate\s+(?:the\s+)?(?:options|alternatives|possibilities)",
    r"review\s+(?:the\s+)?pric(?:ing|es)", r"follow[\s-]?up", r"look\s+into",
    r"improve\s+(?:the\s+)?(?:internal\s+)?(?:communication|collaboration|alignment)", r"align(?:ing)?\s+with",
    r"take\s+(?:the\s+)?(?:necessary\s+|appropriate\s+)?(?:action|steps|measures)",
    r"strengthen\s+(?:the\s+)?(?:relationships?|partnerships?|communication)",
]
VAGUE_PT = [
    r"acompanhar", r"monitorar", r"continuar\s+(?:a\s+)?(?:monitorando|acompanhando|avaliando)",
    r"avaliar\s+(?:as\s+)?(?:possibilidades|alternativas|op[çc][õo]es)",
    r"estudar\s+(?:as\s+)?(?:alternativas|possibilidades|op[çc][õo]es)",
    r"considerar\s+(?:as\s+)?(?:op[çc][õo]es|alternativas|possibilidades)",
    r"explorar\s+(?:as\s+)?(?:op[çc][õo]es|alternativas|oportunidades)",
    r"(?:revisar|rever)\s+(?:os\s+)?pre[çc]os?", r"melhorar\s+(?:a\s+)?comunica[çc][ãa]o(?:\s+interna)?",
    r"dar\s+seguimento", r"fazer\s+(?:um\s+)?acompanhamento", r"follow[\s-]?up", r"alinhar\s+com",
    r"tomar\s+(?:as\s+)?(?:a[çc][õo]es|provid[êe]ncias|medidas)",
    r"refor[çc]ar\s+(?:a\s+)?comunica[çc][ãa]o",
]

# Context that makes a vague phrase an action item rather than description.
OBLIGATION_EN = r"\b(?:will|shall|should|must|need(?:s)?\s+to|plan(?:s)?\s+to|going\s+to|we'll|let's|to\s+do|todo)\b"
OBLIGATION_PT = (r"\b(?:vamos|iremos|ir[áa]|dever[áa]|deve|devem|devemos|precisa|precisam|precisamos|"
                 r"planejamos|pretendemos|ser[áa]|ser[ãa]o)\b")
ACTION_HEADING = re.compile(
    r"next\s+steps?|action(?:s|\s+items?)?|recommendations?|decisions?|to-?do|what\s+we\s+(?:need|ask)|"
    r"pr[óo]ximos?\s+passos?|a[çc][õo]es|a[çc][ãa]o|recomenda|decis[ãa]o|decis[õo]es|encaminhamentos", re.I)

# Deadline / date vocabulary. A bare "by" is too common ("driven by"), so it must precede a time word.
_MONTHS = (r"january|february|march|april|june|july|august|september|october|november|december|"
           r"janeiro|fevereiro|mar[çc]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro")
_MONTH_ABBR = r"jan|feb|fev|mar|apr|abr|may|mai|jun|jul|aug|ago|sep|sept|set|oct|out|nov|dec|dez"
_WEEKDAYS = (r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|segunda|ter[çc]a|quarta|quinta|sexta|"
             r"s[áa]bado|domingo")
DEADLINE_RE = re.compile(
    rf"""\b(?:{_MONTHS})\b
      | \b(?:{_MONTH_ABBR})\.?\s*\d{{1,2}}\b | \b\d{{1,2}}\s*(?:{_MONTH_ABBR})\b | \b(?:{_MONTH_ABBR})[/\-']\d{{2,4}}\b
      | \b(?:19|20)\d{{2}}\b
      | \b\d{{1,2}}[/.\-]\d{{1,2}}(?:[/.\-]\d{{2,4}})?\b
      | \bq[1-4]\b | \b[1-4]t(?:\d{{2,4}})?\b | \bh[12]\b | \b[12]s\d{{2}}\b
      | \bby\s+(?:the\s+)?(?:end|next|early|mid|late|eod|eow|q[1-4]|\d|{_MONTHS}|{_WEEKDAYS})
      | \bat[ée]\b | \bpara\s+(?:o\s+)?(?:dia|fim|final)\b | \bantes\s+d[eo]\b | \bbefore\s+(?:the\s+)?(?:end|\d|{_MONTHS})
      | \bwithin\s+\d+ | \bem\s+\d+\s+dias\b | \b\d+\s*(?:days?|weeks?|months?|dias|semanas|meses)\b
      | \b(?:this|next|last)\s+(?:week|month|quarter|year)\b | \b(?:esta|pr[óo]xima|pr[óo]ximo)\s+(?:semana|m[êe]s|trimestre|ano)\b
      | \bend\s+of\s+(?:the\s+)?(?:week|month|quarter|year)\b | \bfim\s+d[oa]\s+(?:semana|m[êe]s|trimestre|ano)\b
      | \b(?:eod|eow|eom|eoq|eoy|tomorrow|amanh[ãa]|deadline|due|prazo)\b
      | \b(?:weekly|monthly|quarterly|daily|semanal|mensal|trimestral|diari[ao]|semanalmente|mensalmente)\b
      | \b(?:{_WEEKDAYS})(?:-feira)?\b""",
    re.I | re.X,
)
ROLE_EN = re.compile(r"\b(?:CEO|CFO|COO|CMO|CTO|CRO|CIO|CPO|VP|SVP|EVP|director|manager|head\s+of|owner|team|committee|"
                     r"board|department)\b|@\w+", re.I)
ROLE_PT = re.compile(r"\b(?:CEO|CFO|COO|CMO|CTO|CRO|CIO|CPO|VP|diretor(?:a|ia)?|gerente|ger[êe]ncia|coordenador(?:a)?|"
                     r"respons[áa]vel|equipe|time|comit[êe]|conselho|departamento|supervisor(?:a)?)\b|@\w+", re.I)
# Capitalised words that are places or calendar words, not people/teams.
NOT_AN_OWNER = frozenset(
    """North South East West Northeast Southeast Midwest Southwest Mountain Pacific Atlantic Mid-Atlantic America Americas
    Europe Asia Africa Oceania Brazil Brasil China India Japan Korea Germany France Spain Nordeste Sudeste Sul Norte
    Centro-Oeste Monday Tuesday Wednesday Thursday Friday Saturday Sunday January February March April May June July
    August September October November December Q1 Q2 Q3 Q4 The A An We I It This That These Those Our Its""".split()
)

# Label-title vocabulary.
LABEL_STOPLIST = frozenset(
    """agenda;background;overview;sales overview;market data;next steps;challenges;conclusion;conclusions;thank you;
    questions;q&a;qa;introduction;summary;executive summary;recap;highlights;key highlights;results;performance;
    financials;financial overview;market overview;customer feedback;appendix;contents;table of contents;objectives;
    goals;scope;methodology;approach;recommendations;recommendation;discussion;update;status;timeline;roadmap;
    strategy;risks;opportunities;key takeaways;takeaways;any questions;thanks;about us;company overview;our team;
    contexto;visao geral;proximos passos;destaques;obrigado;obrigada;perguntas;duvidas;conclusao;introducao;resumo;
    resumo executivo;resultados;desempenho;apendice;anexo;anexos;objetivos;escopo;metodologia;recomendacoes;
    recomendacao;cronograma;riscos;oportunidades;desafios;panorama;panorama geral;sumario;indice;
    perguntas e respostas""".replace("\n", " ").split(";")
)
LABEL_STOPLIST = frozenset(entry.strip() for entry in LABEL_STOPLIST if entry.strip())
# Verb-like words for LABEL_TITLE. Words that are as often nouns in business titles ("cost cuts",
# "price increases", "the miss") are deliberately left out: without a part-of-speech tagger a false
# "has a verb" only lets a label slip through, while a false "no verb" would flag a real takeaway.
VERBISH_EN = frozenset(
    """is are was were be been being has have had do does did will would can could should must may might shall
    grew grow grows growing fell rose lost won led beat drive drives drove ran made took gave got saw came went kept held
    left paid improve improves reduce reduces deliver delivers remain remains stay stays keep keeps make makes
    take takes give gives get gets require requires exceed exceeds outpace outpaces outperform outperforms
    underperform underperforms erode erodes narrow narrows widen widens expand expands shrink shrinks recover
    recovers slip slips stall stalls double doubles approve decide thank""".split()
)
VERBISH_PT = frozenset(
    """é são foi foram será serão está estão ficou ficaram tem têm teve deve devem precisa precisam exige exigem requer
    cresceu crescem cresce caiu caem cai subiu sobe superou atingiu bateu perdeu ganhou mantém manteve reduziu reduz
    aumentou aumenta pressiona pressionou concentra concentram impulsionou puxou compensou limita limitou depende
    dependem pode podem permite precisamos devemos vamos vai vão há houve gera geram custa custam pede pedem""".split()
)
# Infinitives/past forms are verbs, but a few common nouns share the endings.
PT_NOT_VERBS = frozenset("líder poder mulher qualquer lazer colher caráter cenário valor mercado".split())

SOURCE_LINE = re.compile(r"^\s*(?:source|sources|note|notes|fonte|fontes|nota|notas)\b\s*[:\-–]|^\s*\*", re.I)

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

_ACCENT_GROUPS = ("aáàâãä", "eéèêë", "iíìîï", "oóòôõö", "uúùûü", "cç")
_CHAR_CLASS = {ch: "[" + group + "]" for group in _ACCENT_GROUPS for ch in group}


def _loose_pattern(phrase: str) -> str:
    """Regex for a literal phrase: tolerant of accents, apostrophe style and space/hyphen variants."""
    words = re.split(r"[\s\-]+", phrase.strip().lower())
    pieces = []
    for word in words:
        chars = []
        for ch in word:
            if ch in ("'", "’"):
                chars.append("['’]")
            else:
                chars.append(_CHAR_CLASS.get(ch) or re.escape(ch))
        pieces.append("".join(chars))
    return r"[\s\-]+".join(pieces)


def _compile_phrases(phrases: Iterable[str]) -> re.Pattern:
    ordered = sorted(set(phrases), key=len, reverse=True)  # longest first so specific phrases win
    return re.compile(r"(?<!\w)(?:" + "|".join(_loose_pattern(p) for p in ordered) + r")(?!\w)", re.I)


def _compile_regexes(patterns: Iterable[str]) -> re.Pattern:
    return re.compile(r"(?<!\w)(?:" + "|".join(patterns) + r")(?!\w)", re.I)


def _normalise_phrase(text: str) -> str:
    return re.sub(r"[\s\-]+", " ", text.lower().replace("’", "'")).strip()


def _fold(text: str) -> str:
    """Lower-case and strip accents (for stoplist comparison)."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


FILLER_RES = {"en": _compile_phrases(FILLER_EN), "pt": _compile_phrases(FILLER_PT)}
CLAIM_RES = {"en": _compile_regexes(CLAIM_EN), "pt": _compile_regexes(CLAIM_PT)}
HEDGE_RES = {"en": _compile_regexes(HEDGE_EN), "pt": _compile_regexes(HEDGE_PT)}
VAGUE_RES = {"en": _compile_regexes(VAGUE_EN), "pt": _compile_regexes(VAGUE_PT)}
OBLIGATION_RES = {"en": re.compile(OBLIGATION_EN, re.I), "pt": re.compile(OBLIGATION_PT, re.I)}
ROLE_RES = {"en": ROLE_EN, "pt": ROLE_PT}
FILLER_HINT_MAP = {_normalise_phrase(k): v for k, v in FILLER_HINTS.items()}

# Quarter/year labels are periods, not quantities, so they do not support a claim.
_PERIOD_LABELS = re.compile(r"\b[Qq][1-4]\b|\b[1-4][Tt]\d{0,4}\b|\b[Hh][12]\b|\b(?:19|20)\d{2}\b|\bFY\s?\d{2,4}\b")
_ABBREVIATIONS = frozenset(
    """vs etc eg ie approx no nº sr sra dr dra mr mrs ms inc ltd co corp fig est ex cap al aprox av pp p.p ca cf resp
    tel sec seq ref jan fev mar abr mai jun jul ago set out nov dez""".split()
)
_BULLET_PREFIX = re.compile(r"^\s*(?:[-*•–—+]\s+|\d{1,3}[.)]\s+|\(\d{1,3}\)\s+|\[[ xX]\]\s+)+")
_SENTENCE_END = re.compile(r"""([.!?…]+["'”’)\]]*)(\s+)(?=["'“‘(\[]?[A-ZÀ-ÝÁÉÍÓÚÂÊÔÃÕÇ0-9])""")


def has_quantity(text: str) -> bool:
    """True if `text` has a digit that is not just a year/quarter label."""
    return bool(re.search(r"\d", _PERIOD_LABELS.sub(" ", text)))


def strip_markup(text: str) -> str:
    """Remove markdown/HTML decoration so rules see the words, not the syntax."""
    text = text.replace(" ", " ").replace("’", "'")
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)         # images -> alt text
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)          # links -> label
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)            # bare URLs
    text = re.sub(r"<[^>]+>", " ", text)                          # stray HTML tags
    text = re.sub(r"(\*\*|__)(.+?)\1", r"\2", text)               # bold
    text = re.sub(r"(?<![\w*])\*(\S[^*]*?)\*(?![\w*])", r"\1", text)  # italics
    text = re.sub(r"`([^`]*)`", r"\1", text)                      # inline code
    text = re.sub(r"^\s{0,3}>+\s?", "", text)                     # blockquote marker
    return re.sub(r"[ \t]+", " ", text).strip()


def split_sentences(paragraph: str) -> list[tuple[str, int]]:
    """Split a paragraph into (sentence, start_offset). Conservative: avoids splitting on abbreviations."""
    sentences: list[tuple[str, int]] = []
    start = 0
    for match in _SENTENCE_END.finditer(paragraph):
        before = paragraph[start:match.start()].split()
        last = before[-1].lower().rstrip(".") if before else ""
        ends_with_period = match.group(1).startswith(".")
        is_initial = len(last) == 1 and last.isalpha() and paragraph[match.start() - 1:match.start()].isupper()
        if ends_with_period and (last in _ABBREVIATIONS or is_initial):
            continue
        end = match.start() + len(match.group(1))
        sentences.append((paragraph[start:end].strip(), start))
        start = match.end()
    tail = paragraph[start:].strip()
    if tail:
        sentences.append((tail, start))
    return sentences


def word_count(text: str) -> int:
    return sum(1 for token in text.split() if re.search(r"\w", token))


def make_snippet(text: str, start: int | None = None, end: int | None = None, limit: int = SNIPPET_LIMIT) -> str:
    """Quote `text` in at most `limit` characters.

    With a match span the window is centred on it; without one the start of the text is quoted.
    Cuts land on word boundaries so the quote never begins or ends mid-word.
    """
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    budget = limit - 2  # room for the two ellipsis characters
    if start is None:
        lo = 0
    else:
        centre = (start + (len(text) if end is None else end)) // 2
        lo = max(0, min(centre - budget // 2, len(text) - budget))
    hi = min(len(text), lo + budget)
    if lo > 0 and text[lo - 1] != " ":
        space = text.find(" ", lo, lo + 20)
        lo = space + 1 if space != -1 else lo
    if hi < len(text) and text[hi] != " ":
        space = text.rfind(" ", hi - 20, hi)
        hi = space if space != -1 else hi
    return ("…" if lo > 0 else "") + text[lo:hi].strip() + ("…" if hi < len(text) else "")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    rule: str
    severity: str
    location: str
    snippet: str
    suggestion: str
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        data = {"rule": self.rule, "severity": self.severity, "location": self.location,
                "snippet": self.snippet, "suggestion": self.suggestion}
        data.update(self.extra)
        return data


@dataclass
class Paragraph:
    location: str
    kind: str
    text: str
    slide: int | None
    heading: str          # nearest preceding title/heading, used to recognise "Next steps" sections
    order: int            # document order, for stable sorting


def iter_paragraphs(units: list[dict]) -> Iterator[Paragraph]:
    """Turn extraction units into lintable paragraphs.

    Bullets (newline-separated in a pptx text frame) and table cells become separate
    paragraphs; consecutive hard-wrapped markdown/text lines are merged into one.
    """
    order = 0
    heading = ""
    current_slide: int | None = None
    pending: dict | None = None  # md/txt lines being merged into one paragraph

    def emit_pending() -> Iterator[Paragraph]:
        nonlocal pending, order
        if pending is not None:
            order += 1
            label = pending["first"] if pending["first"] == pending["last"] else f"{pending['first']}-{pending['last']}"
            yield Paragraph(f"line {label}", "line", strip_markup(" ".join(pending["parts"])), None, heading, order)
            pending = None

    for unit in units:
        if unit.get("code") or unit.get("formula") or unit["kind"] == "chart":
            continue
        slide = unit.get("slide")
        if slide != current_slide:
            current_slide = slide
            if slide is not None:
                heading = ""
        kind, text = unit["kind"], unit["text"]
        if kind in ("title", "heading"):
            yield from emit_pending()
            heading = strip_markup(text)
        line_no = unit.get("line")
        is_plain_line = (kind == "line" and line_no is not None and not text.lstrip().startswith(("|", ">"))
                         and not _BULLET_PREFIX.match(text))
        if is_plain_line:
            if pending is not None and pending["last"] + 1 == line_no:
                pending["parts"].append(text)
                pending["last"] = line_no
            else:
                yield from emit_pending()
                pending = {"first": line_no, "last": line_no, "parts": [text]}
            continue
        yield from emit_pending()
        if text.lstrip().startswith("|") or unit.get("cells") is not None:
            cells = unit.get("cells") or [c for c in text.strip().strip("|").split("|")]
            for cell in cells:
                cell = strip_markup(cell)
                if cell and re.search(r"[^\W\d_]", cell):
                    order += 1
                    yield Paragraph(unit["location"], "table", cell, slide, heading, order)
            continue
        for part in text.split("\n"):
            cleaned = strip_markup(_BULLET_PREFIX.sub("", part))
            if cleaned and re.search(r"[^\W_]", cleaned):
                order += 1
                yield Paragraph(unit["location"], kind, cleaned, slide, heading, order)
    yield from emit_pending()


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

def check_filler(paragraphs: list[Paragraph], lang: str) -> list[Finding]:
    findings = []
    for para in paragraphs:
        for match in FILLER_RES[lang].finditer(para.text):
            hint = FILLER_HINT_MAP.get(_normalise_phrase(match.group(0)), FILLER_DEFAULT_HINT[lang])
            findings.append(Finding(
                "FILLER", "medium", para.location, make_snippet(para.text, match.start(), match.end()),
                f"Filler: '{match.group(0)}'. {hint}", {"matched": match.group(0)}))
    return findings


def check_unsupported_claims(paragraphs: list[Paragraph], lang: str) -> list[Finding]:
    findings = []
    for para in paragraphs:
        sentences = split_sentences(para.text)
        for index, (sentence, offset) in enumerate(sentences):
            cleaned = CLAIM_EXEMPT.sub(" ", sentence)
            matches = list(CLAIM_RES[lang].finditer(cleaned))
            if not matches:
                continue
            # A number in the neighbouring sentence of the same paragraph supports the claim
            # ("Revenue grew 12%. This was a strong result.").
            neighbourhood = [sentences[j][0] for j in (index - 1, index, index + 1) if 0 <= j < len(sentences)]
            if any(has_quantity(s) for s in neighbourhood):
                continue
            words = sorted({m.group(0).lower() for m in matches})
            first = matches[0]
            findings.append(Finding(
                "UNSUPPORTED_CLAIM", "high", para.location,
                make_snippet(sentence, first.start(), first.end()),
                (f"'{', '.join(words)}' is a judgment with no number behind it. Quantify it (vs budget, vs prior "
                 "year, vs market) or delete the adjective." if lang == "en" else
                 f"'{', '.join(words)}' é um julgamento sem número. Quantifique (vs orçado, vs ano anterior, "
                 "vs mercado) ou elimine o adjetivo."),
                {"matched": words}))
    return findings


def _has_owner(sentence: str, lang: str) -> bool:
    if ROLE_RES[lang].search(sentence):
        return True
    words = re.findall(r"[A-ZÀ-Ý][\wÀ-ÿ'-]+", sentence)
    first_word = sentence.split()[0].strip("\"'“([") if sentence.split() else ""
    for word in words:
        if word == first_word or word in NOT_AN_OWNER or word.isupper():
            continue
        if re.fullmatch(r"[A-ZÀ-Ý][a-zà-ÿ]{2,}[\wÀ-ÿ'-]*", word):
            return True
    return False


def check_vague_actions(paragraphs: list[Paragraph], lang: str) -> list[Finding]:
    findings = []
    for para in paragraphs:
        if para.kind == "title":
            continue
        # The whole paragraph (bullet/line/cell) is the unit for "has a date / has an owner".
        if DEADLINE_RE.search(para.text) or _has_owner(para.text, lang):
            continue
        in_action_section = bool(ACTION_HEADING.search(para.heading))
        for sentence, offset in split_sentences(para.text):
            for match in VAGUE_RES[lang].finditer(sentence):
                before = sentence[:match.start()].strip(" ,;:-–")
                at_start = len(before.split()) <= 1 or not before  # allow one leading word ("Then", "Also")
                after_modal = bool(OBLIGATION_RES[lang].search(before))
                if not (at_start or after_modal or in_action_section):
                    continue
                findings.append(Finding(
                    "VAGUE_ACTION", "medium", para.location, make_snippet(para.text, offset + match.start(), offset + match.end()),
                    (f"'{match.group(0)}' has no owner and no date. Rewrite as: <who> will <specific verb + object> "
                     "by <date>, and say what result to expect." if lang == "en" else
                     f"'{match.group(0)}' não tem responsável nem prazo. Reescreva: <quem> vai <verbo específico + "
                     "objeto> até <data>, e diga qual resultado se espera."),
                    {"matched": match.group(0)}))
                break  # one finding per sentence is enough
    return findings


def check_hedges(paragraphs: list[Paragraph], lang: str) -> list[Finding]:
    findings = []
    for para in paragraphs:
        is_title = para.kind == "title"
        for sentence, offset in split_sentences(para.text):
            matches = list(HEDGE_RES[lang].finditer(sentence))
            if len(matches) >= HEDGE_MIN_PER_SENTENCE or (is_title and matches):
                words = [m.group(0).lower() for m in matches]
                findings.append(Finding(
                    "HEDGE", "low", para.location, make_snippet(sentence, matches[0].start(), matches[-1].end()),
                    (f"Hedges ({', '.join(words)}) blur the claim. State it plainly, or state the uncertainty "
                     "explicitly (range, confidence, what would change your mind)." if lang == "en" else
                     f"Atenuadores ({', '.join(words)}) enfraquecem a afirmação. Afirme com clareza, ou declare a "
                     "incerteza de forma explícita (faixa, confiança, o que mudaria a conclusão)."),
                    {"matched": words}))
    return findings


def check_long_sentences(paragraphs: list[Paragraph], lang: str) -> list[Finding]:
    limit = LONG_SENTENCE_WORDS[lang]
    findings = []
    for para in paragraphs:
        for sentence, _ in split_sentences(para.text):
            count = word_count(sentence)
            if count > limit:
                findings.append(Finding(
                    "LONG_SENTENCE", "low", para.location, make_snippet(sentence),
                    (f"{count} words (limit {limit}). Split at the first 'and/but/which' into sentences that each "
                     "carry one idea." if lang == "en" else
                     f"{count} palavras (limite {limit}). Divida na primeira conjunção em frases de uma ideia só."),
                    {"words": count}))
    return findings


def _normalised_tokens(sentence: str) -> frozenset[str]:
    return frozenset(re.findall(r"\w+", _fold(sentence)))


def check_repetition(paragraphs: list[Paragraph]) -> list[Finding]:
    entries = []  # (tokens, location, sentence)
    for para in paragraphs:
        if SOURCE_LINE.match(para.text):
            continue  # source/footnote lines are legitimately repeated
        for sentence, _ in split_sentences(para.text):
            if word_count(sentence) >= REPETITION_MIN_WORDS:
                entries.append((_normalised_tokens(sentence), para.location, sentence))
    if len(entries) < 2:
        return []

    # Prefix filtering: two sets with Jaccard >= t must share a token among their rarest
    # tokens, so only sentences sharing one are compared (keeps long documents fast).
    frequency: dict[str, int] = {}
    for tokens, _, _ in entries:
        for token in tokens:
            frequency[token] = frequency.get(token, 0) + 1
    index: dict[str, list[int]] = {}
    findings, reported = [], set()
    for i, (tokens, location, sentence) in enumerate(entries):
        ordered = sorted(tokens, key=lambda t: (frequency[t], t))
        prefix_len = len(ordered) - int(REPETITION_JACCARD * len(ordered) + 1e-9) + 1
        candidates = set()
        for token in ordered[:prefix_len]:
            candidates.update(index.get(token, ()))
            index.setdefault(token, []).append(i)
        for j in sorted(candidates):
            other_tokens, other_location, other_sentence = entries[j]
            union = len(tokens | other_tokens)
            if union and len(tokens & other_tokens) / union >= REPETITION_JACCARD and (j, i) not in reported:
                reported.add((j, i))
                findings.append(Finding(
                    "REPETITION", "medium", location, make_snippet(sentence),
                    f"Near-duplicate of the sentence at {other_location}. Say it once, where it matters most.",
                    {"related_location": other_location, "related_snippet": make_snippet(other_sentence)}))
                break  # one report per sentence
    return findings


def _is_label_title(title: str, lang: str) -> tuple[str, int] | None:
    """Return ("stock", 0) or ("short", n_words) if `title` looks like a topic label, else None."""
    folded = re.sub(r"[^\w&\s]", " ", _fold(title))
    folded = re.sub(r"\s+", " ", folded).strip()
    segments = [s.strip() for s in re.split(r"\s[—–\-:|/]\s|[—–|:/]", _fold(title)) if s.strip()]
    segments = [re.sub(r"[^\w&\s]", "", s).strip() for s in segments]
    if folded in LABEL_STOPLIST or (segments and all(s in LABEL_STOPLIST for s in segments)):
        return ("stock", 0)
    words = re.findall(r"[\w&]+(?:['’-][\w]+)*", title)
    # A quantity makes a title a claim ("EMEA margin -6 pp"); a bare period label ("Q3 results") does not.
    if has_quantity(title) or len(words) > LABEL_TITLE_MAX_WORDS:
        return None
    verbs = VERBISH_PT if lang == "pt" else VERBISH_EN
    for word in (w.lower() for w in words):
        if word in verbs:
            return None
        if lang == "en" and len(word) >= 5 and word.endswith("ed"):
            return None
        if lang == "pt" and word not in PT_NOT_VERBS and (
                (len(word) >= 4 and word.endswith(("ou", "iu"))) or (len(word) >= 6 and word.endswith(("aram", "eram", "iram")))
                or (len(word) >= 5 and word.endswith(("ar", "er", "ir")))):
            return None
    return ("short", len(words))


_LABEL_REASONS = {
    "en": {"stock": "a stock topic label", "short": "a label ({n} words, no verb, no number)"},
    "pt": {"stock": "um rótulo de tópico padrão", "short": "um rótulo ({n} palavras, sem verbo e sem número)"},
}


def check_label_titles(units: list[dict], lang: str) -> list[Finding]:
    findings = []
    for unit in units:
        if unit["kind"] != "title" or unit.get("slide") in (None, 1):
            continue
        label = _is_label_title(unit["text"], lang)
        if label:
            reason = _LABEL_REASONS[lang][label[0]].format(n=label[1])
            findings.append(Finding(
                "LABEL_TITLE", "high", unit["location"], make_snippet(unit["text"]),
                (f"Title is {reason}, not a takeaway. Rewrite as a full sentence: <metric> <verb> <number> because "
                 "<driver> (state the conclusion the slide proves)." if lang == "en" else
                 f"O título é {reason}, não uma conclusão. Reescreva como frase completa: <indicador> "
                 "<verbo> <número> por causa de <causa> (a conclusão que o slide prova)."),
                {"slide": unit.get("slide")}))
    return findings


def check_dense_slides(units: list[dict], lang: str) -> list[Finding]:
    by_slide: dict[int, list[str]] = {}
    for unit in units:
        slide = unit.get("slide")
        if slide is None or unit["kind"] != "body" or slide == 1:
            continue
        for paragraph in unit.get("paragraphs") or unit["text"].split("\n"):
            if paragraph.strip() and not SOURCE_LINE.match(paragraph):
                by_slide.setdefault(slide, []).append(paragraph.strip())
    findings = []
    for slide, bullets in sorted(by_slide.items()):
        words = sum(word_count(b) for b in bullets)
        if words > DENSE_SLIDE_MAX_WORDS or len(bullets) > DENSE_SLIDE_MAX_BULLETS:
            findings.append(Finding(
                "DENSE_SLIDE", "medium", f"slide {slide}",
                make_snippet(f"{bullets[0]} ... (+{len(bullets) - 1} more)" if len(bullets) > 1 else bullets[0]),
                (f"{words} words in {len(bullets)} bullet(s) (heuristic limits: {DENSE_SLIDE_MAX_WORDS} words, "
                 f"{DENSE_SLIDE_MAX_BULLETS} bullets). Keep one message and the 3-5 points that prove it; move the "
                 "rest to the notes or an appendix, or split the slide." if lang == "en" else
                 f"{words} palavras em {len(bullets)} marcador(es) (limites heurísticos: {DENSE_SLIDE_MAX_WORDS} palavras, "
                 f"{DENSE_SLIDE_MAX_BULLETS} marcadores). Mantenha uma mensagem e os 3-5 pontos que a provam; "
                 "mova o resto para as notas ou um anexo, ou divida o slide."),
                {"slide": slide, "words": words, "bullets": len(bullets)}))
    return findings


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def lint_units(units: list[dict], lang: str = "auto") -> tuple[list[Finding], str]:
    """Run every rule over extracted units. Returns (findings, language_used)."""
    if lang == "auto":
        lang = doc_text.detect_language(" ".join(u["text"] for u in units if not u.get("machine_spans")))
    paragraphs = list(iter_paragraphs(units))
    findings: list[Finding] = []
    findings += check_filler(paragraphs, lang)
    findings += check_unsupported_claims(paragraphs, lang)
    findings += check_vague_actions(paragraphs, lang)
    findings += check_hedges(paragraphs, lang)
    findings += check_long_sentences(paragraphs, lang)
    findings += check_repetition(paragraphs)
    findings += check_label_titles(units, lang)
    findings += check_dense_slides(units, lang)

    # Stable order: severity first (what to fix first), then position in the document.
    location_order = {}
    for i, unit in enumerate(units):
        location_order.setdefault(unit["location"], i)
    findings.sort(key=lambda f: (SEVERITY_RANK[f.severity], location_order.get(f.location, 10**9), f.rule))
    return findings, lang


def summarise(findings: list[Finding]) -> dict:
    by_rule: dict[str, int] = {}
    by_severity = {"high": 0, "medium": 0, "low": 0}
    for finding in findings:
        by_rule[finding.rule] = by_rule.get(finding.rule, 0) + 1
        by_severity[finding.severity] += 1
    high_rules = sorted({f.rule for f in findings if f.severity == "high"})
    return {"total": len(findings), "by_rule": dict(sorted(by_rule.items())),
            "by_severity": by_severity, "high_rules": high_rules}


def verdict(summary: dict) -> str:
    high, medium, low = (summary["by_severity"][s] for s in ("high", "medium", "low"))
    if summary["total"] == 0:
        return "Verdict: no heuristic findings. Still read it once as the audience would - the linter cannot judge substance."
    if high:
        return (f"Verdict: fix before sending - {high} high-severity finding(s) ({', '.join(summary['high_rules'])}), "
                f"plus {medium} medium and {low} low.")
    if medium:
        return f"Verdict: tighten before sending - {medium} medium and {low} low finding(s), none high."
    return f"Verdict: minor polish only - {low} low-severity finding(s)."


def lint_file(path: Path, lang: str) -> dict:
    units, warnings = doc_text.extract_with_warnings(path)
    findings, used_lang = lint_units(units, lang)
    summary = summarise(findings)
    return {
        "file": path.as_posix(), "format": doc_text.file_format(path), "language": used_lang,
        "units": len(units), "warnings": warnings,
        "findings": [f.to_dict() for f in findings], "summary": summary, "verdict": verdict(summary),
    }


def render_text(report: dict) -> str:
    lines = [f"== {report['file']}  (language: {report['language']}, {report['units']} text units) =="]
    for warning in report["warnings"]:
        lines.append(f"warning: {warning}")
    for f in report["findings"]:
        lines.append(f"{f['severity'].upper():<6} {f['rule']:<17} {f['location']}")
        lines.append(f"       > {f['snippet']}")
        if f.get("related_location"):
            lines.append(f"       also at {f['related_location']}: {f['related_snippet']}")
        lines.append(f"       -> {f['suggestion']}")
    summary = report["summary"]
    lines.append("")
    lines.append("Summary")
    if summary["by_rule"]:
        lines.append("  by rule:     " + ", ".join(f"{r} {n}" for r, n in summary["by_rule"].items()))
    sev = summary["by_severity"]
    lines.append(f"  by severity: high {sev['high']}, medium {sev['medium']}, low {sev['low']}  (total {summary['total']})")
    lines.append("  " + report["verdict"])
    lines.append("  Heuristic aid, not a judge: ignore findings that are wrong for this text.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="fluff_lint.py",
        description="Anti-fluff heuristic linter for executive writing in English and Portuguese. "
                    "A HEURISTIC AID FOR HUMAN JUDGMENT, NOT A JUDGE: expect some false positives, and clean "
                    "output does not prove the writing is good.",
        epilog="Rules: FILLER, UNSUPPORTED_CLAIM, VAGUE_ACTION, HEDGE, LONG_SENTENCE, REPETITION, "
               "LABEL_TITLE (pptx), DENSE_SLIDE (pptx). Exit codes: 0 ok, 1 usage/IO error, "
               "2 only with --strict when a high-severity finding exists.",
    )
    parser.add_argument("files", nargs="+", help="files to lint (.pptx .docx .xlsx .csv .md .txt .html)")
    parser.add_argument("--lang", choices=("auto", "en", "pt"), default="auto", help="language (default: auto-detect)")
    parser.add_argument("--json", action="store_true", help="machine-readable JSON output")
    parser.add_argument("--strict", action="store_true", help="exit 2 if any high-severity finding exists")
    args = parser.parse_args(argv)

    reports, errors = [], []
    for name in args.files:
        path = Path(name)
        try:
            reports.append(lint_file(path, args.lang))
        except (FileNotFoundError, doc_text.UnsupportedFormat, doc_text.MissingDependency) as exc:
            errors.append(f"{path.as_posix()}: {exc}")
        except Exception as exc:  # corrupt/protected files raise assorted library errors
            errors.append(f"{path.as_posix()}: could not read ({exc.__class__.__name__}: {exc})")

    high_total = sum(r["summary"]["by_severity"]["high"] for r in reports)
    if args.json:
        payload = {
            "files": reports, "errors": errors,
            "totals": {"high": high_total,
                       "medium": sum(r["summary"]["by_severity"]["medium"] for r in reports),
                       "low": sum(r["summary"]["by_severity"]["low"] for r in reports)},
            "disclaimer": "Heuristic aid for human judgment, not a judge.",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(render_text(r) for r in reports))
    for error in errors:
        print(f"fluff_lint: {error}", file=sys.stderr)

    if errors:
        return 1
    if args.strict and high_total:
        return 2
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.stdout.flush()
    except BrokenPipeError:
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        exit_code = 0
    sys.exit(exit_code)
