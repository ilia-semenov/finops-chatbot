"""Pydantic models for chat interface."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Citation(BaseModel):
    document_id: str = Field(..., description="Unique ID of the supporting document")
    access_tier: str = Field(..., description="Access tier of the cited document")
    excerpt: str = Field(..., description="Excerpt shown to the user")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to the chatbot")
    conversation_id: str = Field(..., description="Conversation tracking ID")
    access_tier: str = Field("public", description="Highest data tier requested")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Model-generated answer")
    citations: List[Citation] = Field(default_factory=list)
