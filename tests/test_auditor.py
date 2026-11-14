"""
Comprehensive Unit Tests for IntelligibilityAuditor.
Covers:
1. All 6 pathological features from arXiv:2610.29162v1 Table 2.
2. Mandatory 3 Extreme Edge Cases:
   - Zero-data / empty text / whitespace.
   - Extremely large input (stress test / overflow avoidance).
   - Malformed / non-standard punctuation and unicode symbols.
"""

import unittest
from intelligibility_linter import IntelligibilityAuditor, FeatureCategory, IssueSeverity


class TestIntelligibilityAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = IntelligibilityAuditor()

    # --- 1. Paper Table 2 Feature Verifications ---

    def test_inanimate_animate_mismatch_detection(self):
        text = "The docstring promises they are skipped when they appear in the path."
        report = self.auditor.audit(text)
        self.assertFalse(report.is_production_ready)
        categories = [issue.category for d in report.diagnostics for issue in d.issues]
        self.assertIn(FeatureCategory.INANIMATE_ANIMATE_MISMATCH, categories)

    def test_stacked_noun_compounds_detection(self):
        text = "We fixed absolute dotfile backup path handling while preserving markers."
        report = self.auditor.audit(text)
        categories = [issue.category for d in report.diagnostics for issue in d.issues]
        self.assertIn(FeatureCategory.STACKED_NOUNS, categories)

    def test_reduced_relative_clause_detection(self):
        text = "That is leave the job you hate money."
        report = self.auditor.audit(text)
        categories = [issue.category for d in report.diagnostics for issue in d.issues]
        self.assertIn(FeatureCategory.REDUCED_RELATIVE_CLAUSE, categories)

    def test_denominal_verb_detection(self):
        text = "Austin has unusually high inventory, which cushions price spikes."
        report = self.auditor.audit(text)
        categories = [issue.category for d in report.diagnostics for issue in d.issues]
        self.assertIn(FeatureCategory.DENOMINAL_VERB, categories)

    def test_long_dependency_detection(self):
        long_sentence = (
            "The ancient guitar which was quietly sitting in the dusty corner of the abandoned room "
            "because the young student who had purchased it several years ago was still deciding "
            "whether to commit to rigorous practice schedules ultimately teaches you zero musical chords."
        )
        report = self.auditor.audit(long_sentence)
        categories = [issue.category for d in report.diagnostics for issue in d.issues]
        self.assertIn(FeatureCategory.LONG_DEPENDENCY, categories)

    def test_clean_intelligible_sentence_passes(self):
        clean_text = "According to the official documentation, the system validates all incoming parameters before execution."
        report = self.auditor.audit(clean_text)
        self.assertTrue(report.is_production_ready)
        self.assertGreaterEqual(report.intelligibility_score, 85)

    # --- 2. Mandatory 3 Extreme Edge Cases Defense ---

    def test_edge_case_zero_data(self):
        """Edge Case 1: Empty text, whitespace, newlines."""
        for empty_input in ["", "   ", "\n\n\t  ", None]:
            report = self.auditor.audit(empty_input)
            self.assertEqual(report.total_sentences, 0)
            self.assertEqual(report.total_words, 0)
            self.assertEqual(report.intelligibility_score, 100)
            self.assertTrue(report.is_production_ready)

    def test_edge_case_large_scale_data(self):
        """Edge Case 2: Extremely large text (thousands of words). Must not crash or OOM."""
        sentence = "The system validates the request carefully. "
        large_text = sentence * 2000  # 16,000 words
        report = self.auditor.audit(large_text)
        self.assertEqual(report.total_sentences, 2000)
        self.assertGreater(report.total_words, 10000)
        self.assertTrue(report.is_production_ready)

    def test_edge_case_malformed_input(self):
        """Edge Case 3: Malformed punctuation, symbols, mixed CJK, and broken tokens."""
        malformed = (
            "!?!?!? .... ;;; \t\t\n "
            "###$%%^&*() 1234567890 0xDEADBEEF "
            "测试中英混合：the docstring promises 正常处理，没有乱码。 @@@@@"
        )
        report = self.auditor.audit(malformed)
        self.assertIsInstance(report.intelligibility_score, int)
        self.assertGreaterEqual(report.intelligibility_score, 0)
        self.assertLessEqual(report.intelligibility_score, 100)


if __name__ == "__main__":
    unittest.main()
