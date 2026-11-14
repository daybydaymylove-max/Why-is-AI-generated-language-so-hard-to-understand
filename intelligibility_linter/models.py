"""
Data Transfer Objects (DTO) and Type Definitions for Intelligibility Linter.
Based on research: arXiv:2610.29162v1.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class IssueSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class FeatureCategory(str, Enum):
    INANIMATE_ANIMATE_MISMATCH = "INANIMATE_ANIMATE_MISMATCH"
    STACKED_NOUNS = "STACKED_NOUNS"
    REDUCED_RELATIVE_CLAUSE = "REDUCED_RELATIVE_CLAUSE"
    DENOMINAL_VERB = "DENOMINAL_VERB"
    LONG_DEPENDENCY = "LONG_DEPENDENCY"
    UNATTESTED_NGRAM = "UNATTESTED_NGRAM"


@dataclass(frozen=True)
class IssueDetail:
    """
    Represents a single psycholinguistic intelligibility defect.
    Space Complexity: O(1) per issue instance.
    """
    category: FeatureCategory
    severity: IssueSeverity
    detected_phrase: str
    message: str
    suggested_rewrite: Optional[str] = None


@dataclass
class SentenceDiagnostic:
    """
    Diagnostic results for an individual sentence.
    """
    sentence_index: int
    raw_text: str
    word_count: int
    issues: List[IssueDetail] = field(default_factory=list)

    @property
    def has_issues(self) -> bool:
        return len(self.issues) > 0


@dataclass
class AuditReport:
    """
    Aggregated audit report for a complete text document.
    """
    total_sentences: int
    total_words: int
    intelligibility_score: int
    is_production_ready: bool
    diagnostics: List[SentenceDiagnostic]
    summary_counts: dict
