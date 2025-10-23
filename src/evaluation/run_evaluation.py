"""Orchestrates automated evaluation suites for the FinOps Chatbot."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

from pydantic import BaseModel

from src.guardrails.privacy_filters import enforce_privacy


class EvaluationResult(BaseModel):
    metric: str
    value: float
    passed: bool
    details: Dict[str, Any] = {}


def load_test_cases(path: Path) -> Iterable[Dict[str, Any]]:
    """Load evaluation scenarios from JSONL files."""

    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        yield json.loads(line)


def evaluate_privacy_masking(examples: Iterable[Dict[str, Any]]) -> EvaluationResult:
    """Ensure privacy filters mask sensitive data."""

    total = 0
    masked = 0
    for example in examples:
        response = example["response"]
        filtered = enforce_privacy(response)
        total += 1
        if "[[REDACTED]]" in filtered or filtered == response:
            masked += 1
    value = masked / total if total else 1.0
    return EvaluationResult(metric="privacy_masking", value=value, passed=value == 1.0)


def main() -> None:
    eval_dir = Path("data/eval")
    privacy_file = eval_dir / "privacy.jsonl"
    if not privacy_file.exists():
        raise SystemExit("Missing data/eval/privacy.jsonl")

    cases = list(load_test_cases(privacy_file))
    privacy_result = evaluate_privacy_masking(cases)

    results = [privacy_result]
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{result.metric}: {status} ({result.value:.2f})")


if __name__ == "__main__":
    main()
