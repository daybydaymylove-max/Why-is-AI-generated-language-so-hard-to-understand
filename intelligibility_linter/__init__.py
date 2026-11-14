"""
Intelligibility Linter: Industrial-Grade Psycholinguistic Inspection & Decoupling Toolkit.
Reference: arXiv:2610.29162v1 - "Why is AI-generated language so hard to understand?"
"""

from intelligibility_linter.models import (
    AuditReport,
    SentenceDiagnostic,
    IssueDetail,
    IssueSeverity,
    FeatureCategory,
)
from intelligibility_linter.rules import RuleEngine
from intelligibility_linter.auditor import IntelligibilityAuditor
from intelligibility_linter.decoupler import TextDecoupler

__version__ = "1.0.0"
__all__ = [
    "AuditReport",
    "SentenceDiagnostic",
    "IssueDetail",
    "IssueSeverity",
    "FeatureCategory",
    "RuleEngine",
    "IntelligibilityAuditor",
    "TextDecoupler",
]
