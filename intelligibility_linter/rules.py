"""
Linguistic Rule Engine for detecting 6 pathological AI compression features.
Theoretical Foundations: arXiv:2610.29162v1, DLT (Gibson 1998), UID (Levy & Jaeger 2007).
"""

import re
from typing import List
from intelligibility_linter.models import IssueDetail, FeatureCategory, IssueSeverity


class RuleEngine:
    """
    Deterministic rule engine for parsing psycholinguistic bottlenecks.
    Time Complexity: O(N) where N is the number of words in the sentence.
    Space Complexity: O(N) for tokenized representations.
    """

    def __init__(self) -> None:
        # Non-noun stop words to isolate noun compounds accurately
        self._stop_words = frozenset({
            "the", "a", "an", "in", "on", "at", "for", "with", "about", "to", "from",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
            "it", "this", "that", "these", "those", "and", "or", "but", "so", "as",
            "my", "your", "his", "her", "their", "our", "not", "no", "if", "when",
            "which", "while", "where", "why", "how", "all", "each", "every", "other",
            "another", "such", "than", "more", "most", "very", "too", "quite",
            "unusually", "quietly", "currently", "honestly", "actually", "simply",
            "they", "them", "we", "us", "you", "he", "him", "she", "her", "i", "me",
            "just", "also", "then", "now", "well", "into", "over", "after", "before",
            "by", "under", "above", "through", "during", "without"
        })

        # Animate action verbs that cause selectional restriction violations when paired with inanimate subjects
        self._animate_verbs = frozenset({
            "promise", "promises", "promised", "promising",
            "swallow", "swallows", "swallowed", "swallowing",
            "bite", "bites", "bit", "bitten", "biting",
            "forget", "forgets", "forgot", "forgotten", "forgetting",
            "hope", "hopes", "hoped", "hoping",
            "misunderstand", "misunderstands", "misunderstood", "misunderstanding",
            "ask", "asks", "asked", "asking",
            "expect", "expects", "expected", "expecting",
            "refuse", "refuses", "refused", "refusing",
            "crave", "craves", "craved", "craving",
            "eat", "eats", "ate", "eating", "eaten",
            "teach", "teaches", "taught", "teaching"
        })

        # Inanimate subject indicators
        self._inanimate_subjects = frozenset({
            "docstring", "function", "file", "method", "class", "code", "song",
            "chaos", "worksheet", "objection", "policy", "lattice", "pattern",
            "asymmetry", "process", "sentence", "logic", "rule", "module", "guitar",
            "snippet", "script", "algorithm", "variable", "database", "query"
        })

        # Ad-hoc denominal verbs that trigger syntactic re-evaluation
        self._denominal_verbs = frozenset({
            "footnote", "footnotes", "footnoted", "footnoting",
            "calendar", "calendars", "calendared", "calendaring",
            "cushion", "cushions", "cushioned", "cushioning",
            "bottle", "bottles", "bottled", "bottling",
            "mirror", "mirrors", "mirrored", "mirroring"
        })

    def check_inanimate_animate_mismatch(self, sentence: str) -> List[IssueDetail]:
        """
        Detects inanimate subjects combined with animate action verbs.
        Complexity: O(W) where W is word count.
        """
        if not sentence or not sentence.strip():
            return []

        issues: List[IssueDetail] = []
        tokens = [w.strip('.,;:"()[]{}').lower() for w in sentence.split()]
        num_tokens = len(tokens)

        for i in range(num_tokens - 1):
            w1 = tokens[i]
            w2 = tokens[i + 1]
            if w1 in self._inanimate_subjects and w2 in self._animate_verbs:
                phrase = f"{w1} {w2}"
                issues.append(IssueDetail(
                    category=FeatureCategory.INANIMATE_ANIMATE_MISMATCH,
                    severity=IssueSeverity.ERROR,
                    detected_phrase=phrase,
                    message=f"Inanimate subject '{w1}' paired with animate verb '{w2}' triggers P600 cognitive conflict.",
                    suggested_rewrite=f"Rephrase objectively: 'According to {w1}, ...' or use an inanimate predicate like 'indicates' / 'specifies'."
                ))
            elif i + 2 < num_tokens:
                w3 = tokens[i + 2]
                if w1 in self._inanimate_subjects and w3 in self._animate_verbs:
                    phrase = f"{w1} {w2} {w3}"
                    issues.append(IssueDetail(
                        category=FeatureCategory.INANIMATE_ANIMATE_MISMATCH,
                        severity=IssueSeverity.ERROR,
                        detected_phrase=phrase,
                        message=f"Inanimate subject '{w1}' paired with animate verb '{w3}' triggers P600 cognitive conflict.",
                        suggested_rewrite=f"Rephrase objectively without personifying '{w1}'."
                    ))
        return issues

    def check_stacked_nouns(self, sentence: str) -> List[IssueDetail]:
        """
        Detects compounds with 3 or more stacked nouns.
        Complexity: O(W) where W is word count.
        """
        if not sentence or not sentence.strip():
            return []

        issues: List[IssueDetail] = []
        words = re.findall(r'\b[A-Za-z0-9_-]+\b', sentence)
        candidate_stack: List[str] = []

        for w in words:
            lw = w.lower()
            if lw not in self._stop_words and len(w) > 2 and not lw.endswith("ly"):
                candidate_stack.append(w)
            else:
                if len(candidate_stack) >= 3:
                    stacked_phrase = " ".join(candidate_stack)
                    issues.append(IssueDetail(
                        category=FeatureCategory.STACKED_NOUNS,
                        severity=IssueSeverity.WARNING,
                        detected_phrase=stacked_phrase,
                        message=f"Stacked noun compound ('{stacked_phrase}') causes bracketing ambiguity.",
                        suggested_rewrite=f"Decouple using prepositional phrases (e.g. '... of ...' / '... for ...')."
                    ))
                candidate_stack = []

        if len(candidate_stack) >= 3:
            stacked_phrase = " ".join(candidate_stack)
            issues.append(IssueDetail(
                category=FeatureCategory.STACKED_NOUNS,
                severity=IssueSeverity.WARNING,
                detected_phrase=stacked_phrase,
                message=f"Stacked noun compound ('{stacked_phrase}') causes bracketing ambiguity.",
                suggested_rewrite=f"Decouple using prepositional phrases."
            ))
        return issues

    def check_reduced_relative_clause(self, sentence: str) -> List[IssueDetail]:
        """
        Detects reduced object relative clauses missing 'that' / 'which'.
        Complexity: O(W) via regex.
        """
        if not sentence or not sentence.strip():
            return []

        issues: List[IssueDetail] = []
        pattern = r'\b(the|a|an)\s+([a-zA-Z_-]+)\s+(you|they|we|she|he|i)\s+([a-zA-Z_-]+)\b'
        matches = re.finditer(pattern, sentence, flags=re.IGNORECASE)

        for m in matches:
            determiner = m.group(1)
            noun = m.group(2).lower()
            pronoun = m.group(3)
            verb = m.group(4).lower()
            if verb not in {"is", "are", "was", "were", "can", "could", "will", "would", "should"}:
                detected = m.group(0)
                issues.append(IssueDetail(
                    category=FeatureCategory.REDUCED_RELATIVE_CLAUSE,
                    severity=IssueSeverity.WARNING,
                    detected_phrase=detected,
                    message=f"Omission of relativizer in '{detected}' creates a garden-path risk under DLT.",
                    suggested_rewrite=f"Restore overt marker: '{determiner} {noun} that {pronoun} {verb}'."
                ))
        return issues

    def check_denominal_verbs(self, sentence: str) -> List[IssueDetail]:
        """
        Detects ad-hoc conversion of nouns into verbs.
        Complexity: O(W).
        """
        if not sentence or not sentence.strip():
            return []

        issues: List[IssueDetail] = []
        tokens = [w.strip('.,;:"()[]{}').lower() for w in sentence.split()]
        for t in tokens:
            if t in self._denominal_verbs:
                issues.append(IssueDetail(
                    category=FeatureCategory.DENOMINAL_VERB,
                    severity=IssueSeverity.INFO,
                    detected_phrase=t,
                    message=f"Ad-hoc denominal verb '{t}' forces readers into costly syntactic re-evaluation.",
                    suggested_rewrite=f"Replace with standard verbal construction (e.g. 'add a footnote to explain ...')."
                ))
        return issues

    def check_long_dependency(self, sentence: str, threshold: int = 30) -> List[IssueDetail]:
        """
        Detects overly long sentences exceeding human working memory buffer.
        Complexity: O(W).
        """
        if not sentence or not sentence.strip():
            return []

        words = sentence.split()
        if len(words) > threshold:
            return [IssueDetail(
                category=FeatureCategory.LONG_DEPENDENCY,
                severity=IssueSeverity.WARNING,
                detected_phrase=f"Sentence length: {len(words)} words",
                message=f"Exceeds recommended sentence length ({threshold} words); risks memory breakdown under DLT.",
                suggested_rewrite="Split into two or more independent clauses."
            )]
        return []
