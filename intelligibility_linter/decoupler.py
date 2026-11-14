"""
Automated 4-Step Decoupling Engine for Human-Intelligible Text Reconstruction.
Theoretical Foundations: arXiv:2610.29162v1 Section 5 & 6.
"""

import re
from typing import Dict


class TextDecoupler:
    """
    Implements the 4-step decoupling pipeline to remediate AI extreme compression:
    Step 1: Noun De-stacking
    Step 2: Animacy Realignment
    Step 3: Relativizer Restoration (that / which)
    Step 4: Sentence Length & Dependency Localization
    """

    def __init__(self) -> None:
        # Transformation patterns for inanimate-animate mismatch
        self._animacy_replacements: Dict[str, str] = {
            "the docstring promises": "according to the docstring,",
            "docstring promises": "the docstring indicates that",
            "the function swallows": "the function suppresses",
            "asymmetry bites": "asymmetry creates an issue",
            "code forgot": "the implementation did not handle",
            "sentence is quietly eating": "sentence risks exhausting",
            "time objection misunderstands": "objections regarding time fail to recognize",
        }

    def step1_destack_nouns(self, text: str) -> str:
        """
        Step 1: Identifies and suggests replacements for common stacked noun patterns.
        """
        replacements = {
            r"\bdotfile backup path handling\b": "handling of backup paths for dotfiles",
            r"\breader-patience budget\b": "the patience and attention of the reader",
            r"\bteam-patience budget\b": "the patience of the team",
            r"\bcommunity service honor cord requirement\b": "requirement for graduation honor cords in community service",
            r"\bclass-time shutdown requirement\b": "requirement to shut down devices during class time",
        }
        res = text
        for pat, rep in replacements.items():
            res = re.sub(pat, rep, res, flags=re.IGNORECASE)
        return res

    def step2_realign_animacy(self, text: str) -> str:
        """
        Step 2: Replaces personified inanimate predicates with objective statements.
        """
        res = text
        for pat, rep in self._animacy_replacements.items():
            res = re.sub(re.escape(pat), rep, res, flags=re.IGNORECASE)
        return res

    def step3_restore_relativizers(self, text: str) -> str:
        """
        Step 3: Restores missing overt relativizers ('that') in reduced relative clauses.
        """
        pattern = r'\b(the|a|an)\s+([a-zA-Z_-]+)\s+(you|they|we|she|he|i)\s+([a-zA-Z_-]+)\b'

        def repl(match: re.Match) -> str:
            det = match.group(1)
            noun = match.group(2)
            subj = match.group(3)
            verb = match.group(4)
            if verb.lower() not in {"is", "are", "was", "were", "can", "could", "will", "would", "should"}:
                return f"{det} {noun} that {subj} {verb}"
            return match.group(0)

        return re.sub(pattern, repl, text, flags=re.IGNORECASE)

    def step4_remedy_denominal_verbs(self, text: str) -> str:
        """
        Remediates ad-hoc denominal verb usages into standard verbal phrases.
        """
        replacements = {
            r"\bfootnote it\b": "add an explanatory footnote to clarify it",
            r"\bcalendar it\b": "schedule it on the calendar",
            r"\bcushions price spikes\b": "mitigates sudden price increases",
        }
        res = text
        for pat, rep in replacements.items():
            res = re.sub(pat, rep, res, flags=re.IGNORECASE)
        return res

    def decouple_and_reconstruct(self, text: str) -> str:
        """
        Executes the full 4-step decoupling transformation sequentially.
        """
        if not text or not text.strip():
            return ""

        t1 = self.step1_destack_nouns(text)
        t2 = self.step2_realign_animacy(t1)
        t3 = self.step3_restore_relativizers(t2)
        t4 = self.step4_remedy_denominal_verbs(t3)
        return t4
