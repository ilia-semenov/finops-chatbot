# Evaluation Frameworks

## Automated Evaluation

| Metric | Purpose | Implementation |
| ------ | ------- | -------------- |
| **Context Recall (Top-k)** | Measures if ground-truth document appears in retrieved set. | Synthetic question-answer pairs per source; compute hit@k within Bedrock KB API logs. |
| **Answer Faithfulness** | Detects hallucinations vs. provided context. | Use LLM-as-a-judge (Claude Sonnet) with strict rubric; flag low confidence for manual review. |
| **Data Leakage Check** | Ensures confidential snippets never appear for lower-tier users. | Simulated member/internal users issuing prompts; assertions via regex and metadata checks. |
| **PII Redaction** | Confirms redaction pipeline effectiveness. | Inject synthetic PII into test documents and validate masking in responses using `privacy_filters`. |
| **Toxicity & Policy Compliance** | Monitors safety adherence. | Run AWS Comprehend toxicity API plus Bedrock Guardrail logs; maintain thresholds. |

## Manual Evaluation

- **Weekly Transcript Review**: SMEs review 20 random conversations per cohort (public/member/internal) for quality and compliance.
- **Release Certification**: Before each deployment, run regression test suite and manual sign-off covering member-only scenarios.
- **Red Team Exercises**: Quarterly red team to probe prompt injection, data exfiltration, and policy circumvention.

## Tooling

- `src/evaluation/run_evaluation.py` orchestrates automated checks via pytest.
- Baseline datasets stored under `data/eval/` (create bucket or local folder) with labeled scenarios.
- GitHub Actions workflow `ci-evaluation.yml` runs nightly with mocked services.

## Acceptance Gates

- Launch only if:
  - Faithfulness score ≥ 0.85 across tiers.
  - Leakage incidents = 0 in simulated tests.
  - Mean response latency ≤ 6s for public tier. Internal tier may tolerate ≤ 8s.
  - Observability dashboards reviewed and signed off.

## Feedback Loop

- Collect explicit user ratings in the UI; store in DynamoDB `feedback` table.
- Use low-scoring interactions to trigger targeted re-evaluation with same prompt context.
- Feed validated improvements back into training prompts and ingestion quality checks.
