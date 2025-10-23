# FinOps Chatbot

Initial scaffolding for the FinOps Foundation Retrieval Augmented Generation (RAG) chatbot.  
The project aligns with the AWS Bedrock-centered architecture defined in `FinOps Chatbot.md` and adds
guardrails plus evaluation primitives to protect sensitive content.

## Repository Map

- `docs/` – architecture, data source catalog, guardrail strategy, and evaluation plans.
- `src/backend/` – FastAPI service skeleton with role-aware access enforcement.
- `src/ingestion/` – placeholder ingestion pipeline abstractions.
- `src/guardrails/` – post-generation privacy filters for PII and confidential data.
- `src/evaluation/` – automated evaluation entrypoints for safety and fidelity checks.
- `config/` – guardrail configuration (YAML) and refusal prompt templates.
- `infrastructure/` – AWS CDK plan for infrastructure-as-code.

## Getting Started

1. Create and activate a Python 3.11 virtual environment.
2. Install core dependencies (FastAPI, Pydantic, httpx) once requirement files are added.
3. Implement connectors under `src/ingestion/` and wire them into Bedrock Knowledge Base indexing.
4. Configure Bedrock Guardrails according to `config/guardrails.yaml` and map policy ARNs to deployments.
5. Populate `data/eval/` with JSONL scenarios, then run `python -m src.evaluation.run_evaluation`.

## Next Steps

- Flesh out infrastructure stacks with AWS CDK constructs.
- Integrate Bedrock Knowledge Base retrieval and contextual grounding.
- Implement Chainlit UI that calls the FastAPI endpoint with Cognito-issued JWTs.
