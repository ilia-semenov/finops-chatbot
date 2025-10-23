"""FastAPI service entrypoint for FinOps Chatbot."""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException

from src.backend.dependencies import RequestContext, get_request_context
from src.backend.schemas import ChatRequest, ChatResponse

app = FastAPI(title="FinOps Chatbot API")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, context: RequestContext = Depends(get_request_context)) -> ChatResponse:
    """Handle chat requests with role-aware guardrails."""

    if not context.is_authorized_for(request.access_tier):
        raise HTTPException(status_code=403, detail="Access denied for requested content tier")

    # TODO: Plug into retrieval orchestrator and Bedrock Guardrails.
    answer = "This is a placeholder response."
    return ChatResponse(answer=answer, citations=[])
