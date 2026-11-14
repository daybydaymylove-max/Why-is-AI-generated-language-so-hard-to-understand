"""
Unit Tests for TextDecoupler.
Verifies the 4-step decoupling pipeline against pathological patterns.
"""

import unittest
from intelligibility_linter import TextDecoupler, IntelligibilityAuditor


class TestTextDecoupler(unittest.TestCase):
    def setUp(self):
        self.decoupler = TextDecoupler()
        self.auditor = IntelligibilityAuditor()

    def test_step1_destack_nouns(self):
        text = "We improved dotfile backup path handling for developers."
        reconstructed = self.decoupler.step1_destack_nouns(text)
        self.assertIn("handling of backup paths for dotfiles", reconstructed)

    def test_step2_realign_animacy(self):
        text = "The docstring promises proper validation."
        reconstructed = self.decoupler.step2_realign_animacy(text)
        self.assertIn("according to the docstring,", reconstructed)

    def test_step3_restore_relativizers(self):
        text = "This is the job you hate."
        reconstructed = self.decoupler.step3_restore_relativizers(text)
        self.assertIn("the job that you hate", reconstructed)

    def test_step4_remedy_denominal_verbs(self):
        text = "Please footnote it."
        reconstructed = self.decoupler.step4_remedy_denominal_verbs(text)
        self.assertIn("add an explanatory footnote to clarify it", reconstructed)

    def test_full_pipeline_improves_intelligibility_score(self):
        bad_text = "The docstring promises dotfile backup path handling without errors. Please footnote it."
        report_before = self.auditor.audit(bad_text)

        reconstructed = self.decoupler.decouple_and_reconstruct(bad_text)
        report_after = self.auditor.audit(reconstructed)

        self.assertGreater(report_after.intelligibility_score, report_before.intelligibility_score)


if __name__ == "__main__":
    unittest.main()
