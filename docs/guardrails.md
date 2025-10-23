# Guardrail Strategy

## Objectives

1. Prevent leakage of confidential or embargoed FinOps material to unauthorized users.
2. Block exposure of personally identifiable information (PII) and credential-like secrets.
3. Maintain factual grounding by ensuring the model only answers from approved sources.
4. Enforce tone, safety, and acceptable use policies aligned with FinOps Foundation guidelines.

## Guardrail Layers

| Layer | Scope | Implementation |
| ----- | ----- | -------------- |
| **Ingestion Filters** | Documents | Lambda pre-processors using Amazon Comprehend, custom regex, and DLP detectors classify sensitivity and redact PII before storage. |
| **Metadata Access Control** | Retrieval | Access tier attributes stored in DynamoDB; retrieval orchestrator filters documents exceeding caller clearance. |
| **Bedrock Guardrails** | Generation | Use Amazon Bedrock Guardrails policies for PII redaction, sensitive topics, prompt injection, and content filters. |
| **Custom Safety Checks** | Post-generation | Python filters in `src/guardrails/privacy_filters.py` run regex and ML-based detectors; optionally call OpenAI/Anthropic moderation if approved. |
| **Human-in-the-loop Review** | Continuous | Flagged conversations routed to compliance reviewers via EventBridge + SNS. |

## Data-Type Specific Policies

### Public Content
- Allow full retrieval and citation.
- Require attribution footnotes.
- Cache embeddings for cost efficiency; low latency required.

### Member-Only Content
- Serve responses only to authenticated `finops_member` users.
- Auto-redact user names and Slack handles during ingestion.
- Include disclaimer: "Member insights – do not share externally."

### Internal Content
- Limit to `finops_internal` role; enforce request-time check.
- Require justification field; log to audit stream.
- Run hallucination detector to ensure summaries align with source paragraphs.

### Confidential / Licensed Content
- Default deny; must include `requires_confidential = true` flag and valid reason.
- Mask all monetary figures unless explicitly permitted.
- Use template that ensures the bot references license constraints.
- Block if question is outside approved scope; respond with refusal pattern from `config/refusal_prompts.md`.

## Prompt Hardening

- System prompt includes red-team tested instructions to use only retrieved context, cite sources, and obey access tiers.
- Include `context_guard` tool that validates chunk provenance before inclusion.
- Employ Bedrock Contextual Grounding to cross-check citations.

## Response Safety Checks

1. `detect_pii(text)` – Named entity recognition for PII/PHI; mask with `[[REDACTED]]`.
2. `detect_sensitive_financials(text)` – Regex + heuristics for unreleased budgets, forecasts, or benchmark figures.
3. `detect_confidential_markers(context)` – Blocks responses quoting documents tagged `confidential` when user access < required.
4. `detect_prompt_injection(history)` – Evaluate last user turn for injection keywords; fallback to refusal if suspicious.

## Audit & Metrics

- Track guardrail blocks vs. allowed responses; alert if block rate > 5% per day.
- Capture reasons in CloudWatch Logs with structured JSON.
- Weekly review of randomly sampled conversations from each access tier.

## Incident Response

- If leakage detected, trigger AWS Security Hub incident.
- Revoke offending document embedding and re-index after remediation.
- Notify content owners and run root-cause analysis within 48 hours.
