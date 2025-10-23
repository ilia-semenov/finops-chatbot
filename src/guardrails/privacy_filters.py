"""Utilities for enforcing post-generation safety filters."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List

PII_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN format
    re.compile(r"\b(?:\d[ -]?){15,19}\b"),  # payment card numbers
    re.compile(r"(?i)\b(?:email|e-mail):?\s*[\w.-]+@[\w.-]+\.[a-z]{2,}\b"),
]

SENSITIVE_FINANCIAL_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r"(?i)\b(?:forecast|budget|run-rate|spend)\s+\$?\d+[\w.%$\s-]*"),
    re.compile(r"(?i)\b(?:nda|non-disclosure|confidential)\b"),
]


@dataclass
class Detection:
    """Represents a matched sensitive snippet."""

    category: str
    match: str
    start: int
    end: int


def detect_pii(text: str) -> List[Detection]:
    """Return PII detections within the provided text."""

    findings: List[Detection] = []
    for pattern in PII_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(Detection("pii", match.group(), match.start(), match.end()))
    return findings


def detect_sensitive_financials(text: str) -> List[Detection]:
    """Return potential sensitive financial details."""

    findings: List[Detection] = []
    for pattern in SENSITIVE_FINANCIAL_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(Detection("sensitive_financial", match.group(), match.start(), match.end()))
    return findings


def mask_findings(text: str, findings: Iterable[Detection], mask: str = "[[REDACTED]]") -> str:
    """Mask detected spans in the text."""

    result = text
    # Process matches in reverse order so indexes remain correct.
    for detection in sorted(findings, key=lambda d: d.start, reverse=True):
        result = result[: detection.start] + mask + result[detection.end :]
    return result


def enforce_privacy(text: str) -> str:
    """Detect and mask sensitive content in responses."""

    findings = detect_pii(text) + detect_sensitive_financials(text)
    if not findings:
        return text
    return mask_findings(text, findings)
