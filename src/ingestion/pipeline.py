"""Data ingestion orchestrator for FinOps Chatbot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class DocumentWriter(Protocol):
    def write(self, *, key: str, body: bytes, metadata: dict) -> None:
        """Persist a processed document with metadata."""


@dataclass
class IngestionJobContext:
    source_name: str
    run_id: str
    access_tier: str


@dataclass
class RawArtifact:
    key: str
    body: bytes
    metadata: dict


class IngestionPipeline:
    """Runs source-specific processors and writes cleaned documents."""

    def __init__(self, writer: DocumentWriter) -> None:
        self.writer = writer

    def process(self, context: IngestionJobContext, artifact: RawArtifact) -> None:
        normalized = self._normalize(artifact)
        enriched_metadata = {
            **artifact.metadata,
            "access_tier": context.access_tier,
            "source": context.source_name,
            "run_id": context.run_id,
        }
        self.writer.write(
            key=normalized.key,
            body=normalized.body,
            metadata=enriched_metadata,
        )

    def _normalize(self, artifact: RawArtifact) -> RawArtifact:
        """Placeholder normalization that trims whitespace."""

        body = artifact.body.strip()
        return RawArtifact(key=artifact.key, body=body, metadata=artifact.metadata)
