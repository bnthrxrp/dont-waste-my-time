"""Tests for fluff_lint.py: known findings in the weak deck, clean text stays clean, rule edge cases."""
import json
import tempfile
import unittest
from pathlib import Path

import _helpers as h
import fluff_lint as fl


def lint_text(text: str, lang: str = "auto", kind: str = "line"):
    """Lint a multi-line string as if it were a markdown file (one unit per line)."""
    units = [{"location": f"line {i}", "kind": kind, "text": line, "line": i}
             for i, line in enumerate(text.split("\n"), start=1) if line.strip()]
    findings, used = fl.lint_units(units, lang)
    return findings, used


def rules(findings):
    return [f.rule for f in findings]


class WeakDeck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = fl.lint_file(h.WEAK_DECK, "auto")
        cls.findings = cls.report["findings"]

    def of(self, rule):
        return [f for f in self.findings if f["rule"] == rule]

    def test_language_detected(self):
        self.assertEqual(self.report["language"], "en")

    def test_label_titles_flagged_with_high_severity(self):
        labels = {f["snippet"]: f for f in self.of("LABEL_TITLE")}
        for title in ("Agenda", "Background", "Sales Overview", "Market Data", "Regional Performance",
                      "Customer Feedback", "Challenges", "Next Steps", "Thank You — Questions?"):
            self.assertIn(title, labels)
            self.assertEqual(labels[title]["severity"], "high")
        self.assertNotIn("Q3 Business Review", labels, "the title slide is exempt")

    def test_vague_next_steps_flagged_but_specific_one_is_not(self):
        vague = [f["snippet"] for f in self.of("VAGUE_ACTION")]
        for item in ("Continue monitoring the market", "Review pricing", "Improve internal communication",
                     "Follow up with customers"):
            self.assertIn(item, vague)
        self.assertFalse([s for s in vague if "Brandt" in s], "the Brandt bullet names a deadline and an exit")

    def test_background_filler_flagged(self):
        matched = {f["matched"].lower() for f in self.of("FILLER")}
        self.assertIn("going forward", matched)
        self.assertTrue(all(f["location"] == "slide 3 / body" for f in self.of("FILLER")))

    def test_dense_slide_ten_bullets(self):
        dense = {f["location"]: f for f in self.of("DENSE_SLIDE")}
        self.assertIn("slide 4", dense)
        self.assertEqual(dense["slide 4"]["bullets"], 10)
        self.assertIn("slide 3", dense)  # one 82-word paragraph
        self.assertNotIn("slide 9", dense)

    def test_every_finding_has_the_required_fields(self):
        for f in self.findings:
            self.assertEqual({"rule", "severity", "location", "snippet", "suggestion"} <= set(f), True)
            self.assertLessEqual(len(f["snippet"]), 120)
            self.assertIn(f["severity"], ("high", "medium", "low"))

    def test_summary_and_verdict(self):
        summary = self.report["summary"]
        self.assertEqual(summary["by_rule"]["LABEL_TITLE"], 9)
        self.assertEqual(summary["by_severity"]["high"], 9)
        self.assertTrue(self.report["verdict"].startswith("Verdict: fix before sending"))


class OtherFixtures(unittest.TestCase):
    def test_markdown_report_findings(self):
        report = fl.lint_file(h.REPORT_MD, "auto")
        by_rule = {}
        for f in report["findings"]:
            by_rule.setdefault(f["rule"], []).append(f)
        self.assertTrue(any("rapidly evolving" in f["matched"].lower() for f in by_rule["FILLER"]))
        claim_locations = {f["location"] for f in by_rule["UNSUPPORTED_CLAIM"]}
        self.assertIn("line 37", claim_locations)   # "Strong season, shelf gains" table cell
        self.assertIn("line 52", claim_locations)   # conclusion: solid / strong with no numbers
        self.assertNotIn("LABEL_TITLE", by_rule)    # not a deck

    def test_portuguese_deck_label_titles(self):
        report = fl.lint_file(h.PT_DECK, "auto")
        self.assertEqual(report["language"], "pt")
        flagged = {f["snippet"] for f in report["findings"] if f["rule"] == "LABEL_TITLE"}
        self.assertEqual(flagged, {"Destaques do trimestre", "Desempenho por canal", "Margem e verba promocional",
                                   "Próximos passos"})
        self.assertIn("rótulo", report["findings"][0]["suggestion"])

    def test_spreadsheet_and_csv_do_not_produce_noise(self):
        for path in (h.PRICING_XLSX, h.KPI_CSV):
            self.assertEqual(fl.lint_file(path, "auto")["findings"], [], path.name)


class CleanText(unittest.TestCase):
    CLEAN = (
        "Q3 net sales fell 2.8% to $86.2M because EMEA volume dropped 11% after Competitor X cut prices.\n"
        "Gross margin was 23.4%, 4.5 points below last year, driven by raw material costs up 14%.\n"
        "Decision needed: the CFO approves exit from the Brandt contract by December 31 to free 6,800 tonnes."
    )

    def test_clean_sample_has_no_findings(self):
        findings, _ = lint_text(self.CLEAN)
        self.assertEqual(findings, [])

    def test_clean_deck_titles_pass(self):
        titles = ["Q3 Review", "EMEA price cuts drove an 11% volume drop", "Raw materials rose 14%; pricing recovered only 2%",
                  "We should exit the Brandt contract by December 31"]
        units = [{"location": f"slide {i} / title", "kind": "title", "text": t, "slide": i}
                 for i, t in enumerate(titles, start=1)]
        findings, _ = fl.lint_units(units, "en")
        self.assertEqual([f for f in findings if f.rule == "LABEL_TITLE"], [])


class Rules(unittest.TestCase):
    def test_unsupported_claim_needs_a_quantity(self):
        self.assertEqual(rules(lint_text("Sales were strong across all regions.")[0]), ["UNSUPPORTED_CLAIM"])
        self.assertEqual(lint_text("Sales were strong at 12% above budget.")[0], [])
        # A number in the adjacent sentence of the same paragraph supports the claim.
        self.assertEqual(lint_text("Revenue grew 12% in Q3. This was a strong result.")[0], [])
        # Period labels are not quantities.
        self.assertEqual(rules(lint_text("A strong 2026 for the division.")[0]), ["UNSUPPORTED_CLAIM"])
        self.assertEqual(lint_text("The gap is statistically significant.")[0], [])

    def test_portuguese_claims_and_filler(self):
        findings, lang = lint_text("O resultado foi muito expressivo no trimestre.")
        self.assertEqual(lang, "pt")
        self.assertEqual(rules(findings), ["UNSUPPORTED_CLAIM"])
        self.assertEqual(lint_text("O resultado foi expressivo: +12% vs. 3T25 no trimestre.", "pt")[0], [])
        findings, _ = lint_text("Vale ressaltar que, no cenário atual, o time deve alavancar sinergias.", "pt")
        self.assertEqual(rules(findings), ["FILLER"] * 3)
        self.assertEqual(lint_text("Vale ressaltar que a margem caiu", "pt")[0][0].rule, "FILLER")
        self.assertEqual(lint_text("VALE RESSALTAR que a margem caiu", "pt")[0][0].rule, "FILLER")  # case-insensitive
        self.assertEqual(lint_text("Vale ressaltar que a margem caiu", "pt")[0][0].extra["matched"], "Vale ressaltar")

    def test_filler_matches_whole_phrases_only_and_tolerates_variants(self):
        self.assertEqual(rules(lint_text("We will reach out to the Best-In-Class suppliers.", "en")[0]), ["FILLER", "FILLER"])
        self.assertEqual(lint_text("The outreach program reached 4 regions.", "en")[0], [])
        self.assertEqual(rules(lint_text("IN TODAY’S RAPIDLY CHANGING market we grew 3%.", "en")[0]), ["FILLER"])

    def test_phrase_lists_are_big_enough_and_extendable(self):
        self.assertGreaterEqual(len(set(fl.FILLER_EN)), 40)
        self.assertGreaterEqual(len(set(fl.FILLER_PT)), 40)
        self.assertTrue(all(isinstance(p, str) for p in fl.FILLER_EN + fl.FILLER_PT))

    def test_vague_action_rules(self):
        self.assertEqual(rules(lint_text("We will continue to monitor the situation.")[0]), ["VAGUE_ACTION"])
        self.assertEqual(lint_text("Review pricing by March 15.")[0], [])                # has a date
        self.assertEqual(lint_text("The CFO will review pricing.")[0], [])               # has an owner
        self.assertEqual(lint_text("Review pricing with Maria.")[0], [])                 # has a named owner
        self.assertEqual(lint_text("Monitoring of pricing is ongoing and follow up was done.")[0], [])  # description
        findings, lang = lint_text("Acompanhar a ruptura nas redes regionais")
        self.assertEqual((lang, rules(findings)), ("pt", ["VAGUE_ACTION"]))
        self.assertEqual(lint_text("Acompanhar a ruptura até 30/11 (Diretoria Comercial)", "pt")[0], [])
        self.assertEqual(lint_text("O objetivo é acompanhar a evolução do indicador.", "pt")[0], [])

    def test_vague_action_under_next_steps_heading(self):
        def lint_under_heading(bullet):
            units = [{"location": "line 1", "kind": "heading", "text": "Next steps", "line": 1},
                     {"location": "line 2", "kind": "line", "text": bullet, "line": 2}]
            return rules(fl.lint_units(units, "en")[0])
        # Under a Next steps heading a vague phrase counts even mid-sentence.
        self.assertEqual(lint_under_heading("- The launch needs us to explore options for pricing"), ["VAGUE_ACTION"])
        self.assertEqual(lint_under_heading("- We should explore options for the launch"), ["VAGUE_ACTION"])
        self.assertEqual(lint_under_heading("- Marketing should explore options for the launch"), [])  # actor named

    def test_hedges_need_stacking_except_in_titles(self):
        self.assertEqual(rules(lint_text("We are quite confident that this is basically fine.")[0]), ["HEDGE"])
        self.assertEqual(lint_text("We are quite confident.")[0], [])
        self.assertEqual(lint_text("We chose price rather than volume.")[0], [])  # "rather than" is not a hedge
        title = [{"location": "slide 2 / title", "kind": "title", "text": "Margins are somewhat lower", "slide": 2}]
        self.assertEqual(rules(fl.lint_units(title, "en")[0]), ["HEDGE"])
        self.assertEqual(rules(lint_text("Isso é bastante importante e praticamente certo.", "pt")[0]), ["HEDGE"])

    def test_long_sentence_thresholds_differ_by_language(self):
        sentence36 = " ".join(["word"] * 35) + " end."
        sentence38 = " ".join(["palavra"] * 37) + " fim."
        self.assertEqual(rules(lint_text(sentence36, "en")[0]), ["LONG_SENTENCE"])
        self.assertEqual(lint_text(" ".join(["word"] * 34) + " end.", "en")[0], [])
        self.assertEqual(lint_text(sentence38, "pt")[0], [])
        self.assertEqual(rules(lint_text(" ".join(["palavra"] * 41), "pt")[0]), ["LONG_SENTENCE"])
        self.assertEqual((fl.LONG_SENTENCE_WORDS["en"], fl.LONG_SENTENCE_WORDS["pt"]), (35, 40))

    def test_repetition_reports_both_locations(self):
        text = ("The Midwest region was affected by weather, competitive activity and the delisting of Digestia.\n\n"
                "Margin fell because of promotional spend and mix.\n\n"
                "The Midwest region was affected by weather, competitive activity and the delisting of Digestia too.")
        # One line per paragraph with blank lines between them: use explicit line numbers.
        units = [{"location": "line 1", "kind": "line", "text": text.split("\n\n")[0], "line": 1},
                 {"location": "line 3", "kind": "line", "text": text.split("\n\n")[1], "line": 3},
                 {"location": "line 5", "kind": "line", "text": text.split("\n\n")[2], "line": 5}]
        findings = [f for f in fl.lint_units(units, "en")[0] if f.rule == "REPETITION"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].location, "line 5")
        self.assertEqual(findings[0].extra["related_location"], "line 1")

    def test_repetition_ignores_short_sentences_and_source_lines(self):
        units = [{"location": f"line {i}", "kind": "line", "text": t, "line": i * 2}
                 for i, t in enumerate(["Source: company data, IQVIA scanner data, Q3 2026 close.",
                                        "Source: company data, IQVIA scanner data, Q3 2026 close.",
                                        "Net sales fell.", "Net sales fell."], start=1)]
        self.assertEqual([f for f in fl.lint_units(units, "en")[0] if f.rule == "REPETITION"], [])

    def test_label_title_rules(self):
        self.assertEqual(fl._is_label_title("Agenda", "en"), ("stock", 0))
        self.assertEqual(fl._is_label_title("Q3 results", "en"), ("short", 2))      # a period label is not a number
        self.assertIsNone(fl._is_label_title("Revenue fell 3% in Q3", "en"))         # digit
        self.assertIsNone(fl._is_label_title("Costs are rising", "en"))              # verb
        self.assertIsNone(fl._is_label_title("Five reasons we lost EMEA share this year", "en"))  # > 4 words
        self.assertEqual(fl._is_label_title("Próximos passos", "pt"), ("stock", 0))
        self.assertIsNone(fl._is_label_title("Renegociar acordos com redes", "pt"))  # infinitive verb
        self.assertIsNone(fl._is_label_title("Preços sobem 5%", "pt"))

    def test_dense_slide_threshold(self):
        def slide(words, bullets):
            per = max(1, words // bullets)
            paragraphs = [" ".join(["word"] * per) for _ in range(bullets)]
            return [{"location": "slide 2 / body", "kind": "body", "text": "\n".join(paragraphs),
                     "paragraphs": paragraphs, "slide": 2}]
        self.assertEqual(fl.check_dense_slides(slide(60, 6), "en"), [])
        self.assertEqual(len(fl.check_dense_slides(slide(60, 7), "en")), 1)
        self.assertEqual(len(fl.check_dense_slides(slide(75, 3), "en")), 1)


class Cli(unittest.TestCase):
    def test_strict_exits_2_only_on_high_findings(self):
        self.assertEqual(h.run_script("fluff_lint.py", h.WEAK_DECK).returncode, 0)
        self.assertEqual(h.run_script("fluff_lint.py", h.WEAK_DECK, "--strict").returncode, 2)
        self.assertEqual(h.run_script("fluff_lint.py", h.PRICING_XLSX, "--strict").returncode, 0)

    def test_json_output_structure_and_multiple_files(self):
        proc = h.run_script("fluff_lint.py", h.WEAK_DECK, h.PT_DECK, "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual([f["language"] for f in data["files"]], ["en", "pt"])
        self.assertIn("disclaimer", data)
        self.assertEqual(data["totals"]["high"], 9 + 4)

    def test_text_output_has_summary_and_verdict(self):
        out = h.run_script("fluff_lint.py", h.WEAK_DECK).stdout
        self.assertIn("Summary", out)
        self.assertIn("by rule:", out)
        self.assertIn("Verdict:", out)
        self.assertIn("HIGH   LABEL_TITLE", out)

    def test_lang_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.md"
            path.write_text("Going forward the team will deliver.\n", encoding="utf-8")
            data = json.loads(h.run_script("fluff_lint.py", path, "--lang", "pt", "--json").stdout)
            self.assertEqual(data["files"][0]["language"], "pt")
            self.assertEqual(data["files"][0]["findings"], [])  # PT list has no "going forward"

    def test_errors_exit_1(self):
        proc = h.run_script("fluff_lint.py", "/nonexistent.md")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("No such file", proc.stderr)

    def test_help_states_it_is_a_heuristic(self):
        out = h.run_script("fluff_lint.py", "--help").stdout
        self.assertIn("NOT A JUDGE", out)


if __name__ == "__main__":
    unittest.main()
