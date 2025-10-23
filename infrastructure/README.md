# Infrastructure Overview

This directory will contain AWS CDK (Python) stacks for the FinOps Chatbot.

## Planned Stacks

- `networking_stack.py` – VPC, subnets, security groups, IAM roles.
- `data_platform_stack.py` – S3 buckets, DynamoDB tables, Bedrock Knowledge Bases, OpenSearch Serverless.
- `application_stack.py` – ECS services (API, Chainlit UI), AppConfig, CloudWatch dashboards.
- `ingestion_stack.py` – EventBridge, Step Functions, Lambda connectors, Glue jobs.

Each stack will expose parameters for environment (`dev/staging/prod`) and guardrail policy ARNs. CI/CD will synthesize templates and deploy via GitHub Actions workflows.
