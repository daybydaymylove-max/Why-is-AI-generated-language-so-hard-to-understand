"""
Core Auditor implementation for psycholinguistic intelligibility evaluation.
Theoretical Foundations: arXiv:2610.29162v1.
"""

import re
from typing import List, Dict
from intelligibility_linter.models import (
    AuditReport,
    SentenceDiagnostic,
    IssueDetail,
    IssueSeverity,
    FeatureCategory,
)
from intelligibility_linter.rules import RuleEngine


class IntelligibilityAuditor:
    """
    Evaluates text intelligibility against cognitive psycholinguistic constraints.
    Time Complexity: O(T) where T is total character length of the document.
    Space Complexity: O(T) for sentence and diagnostic representations.
    """

    def __init__(self, rule_engine: RuleEngine = None) -> None:
        self.rules = rule_engine or RuleEngine()

    def audit(self, text: str) -> AuditReport:
        """
        Runs comprehensive psycholinguistic audit across all sentences.
        Defensive: handles None, empty string, and malformed inputs gracefully.
        """
        if not text or not text.strip():
            return AuditReport(
                total_sentences=0,
                total_words=0,
                intelligibility_score=100,
                is_production_ready=True,
                diagnostics=[],
                summary_counts={cat.value: 0 for cat in FeatureCategory}
            )

        # Robust sentence splitting supporting English and Chinese punctuation
        raw_sentences = re.split(r'(?<=[.!?。！？\n])\s+', text.strip())
        diagnostics: List[SentenceDiagnostic] = []
        summary_counts: Dict[str, int] = {cat.value: 0 for cat in FeatureCategory}

        total_words = 0
        penalty_score = 0

        sentence_idx = 1
        for s in raw_sentences:
            cleaned = s.strip()
            if not cleaned:
                continue

            words = cleaned.split()
            word_count = len(words)
            total_words += word_count

            # Run all rules
            issues: List[IssueDetail] = []
            issues.extend(self.rules.check_inanimate_animate_mismatch(cleaned))
            issues.extend(self.rules.check_stacked_nouns(cleaned))
            issues.extend(self.rules.check_reduced_relative_clause(cleaned))
            issues.extend(self.rules.check_denominal_verbs(cleaned))
            issues.extend(self.rules.check_long_dependency(cleaned))

            for issue in issues:
                summary_counts[issue.category.value] += 1
                if issue.severity == IssueSeverity.ERROR:
                    penalty_score += 15
                elif issue.severity == IssueSeverity.WARNING:
                    penalty_score += 8
                else:
                    penalty_score += 3

            diagnostics.append(SentenceDiagnostic(
                sentence_index=sentence_idx,
                raw_text=cleaned,
                word_count=word_count,
                issues=issues
            ))
            sentence_idx += 1

        final_score = max(0, 100 - penalty_score)
        # Production readiness: score >= 85 and zero ERROR-level defects
        has_errors = any(
            any(i.severity == IssueSeverity.ERROR for i in d.issues)
            for d in diagnostics
        )
        is_production_ready = (final_score >= 85) and (not has_errors)

        return AuditReport(
            total_sentences=len(diagnostics),
            total_words=total_words,
            intelligibility_score=final_score,
            is_production_ready=is_production_ready,
            diagnostics=diagnostics,
            summary_counts=summary_counts
        )
