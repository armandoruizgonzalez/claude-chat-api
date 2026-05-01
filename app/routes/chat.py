from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

from app.services.claude import get_claude_service, ClaudeService

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_history: List[Dict[str, Any]] = []
    system_prompt: Optional[str] = None
    max_tokens: int = 1024


class ChatResponse(BaseModel):
    response: str


def build_messages(request: ChatRequest) -> List[Dict[str, Any]]:
    """Build the messages list from conversation history and current message."""
    messages = []

    # Add conversation history
    for msg in request.conversation_history:
        if msg.get("role") in ["user", "assistant"]:
            messages.append({
                "role": msg["role"],
                "content": msg.get("content", "")
            })

    # Add current user message
    messages.append({
        "role": "user",
        "content": request.message
    })

    return messages


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to Claude and get a response."""
    try:
        service = get_claude_service()
        messages = build_messages(request)

        response_text = await service.send_message(
            messages=messages,
            system_prompt=request.system_prompt,
            max_tokens=request.max_tokens
        )

        return ChatResponse(response=response_text)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Claude: {str(e)}")


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Stream a response from Claude using Server-Sent Events."""
    try:
        service = get_claude_service()
        messages = build_messages(request)

        async def generate():
            async for chunk in service.stream_message(
                messages=messages,
                system_prompt=request.system_prompt,
                max_tokens=request.max_tokens
            ):
                # SSE format: data: {content}\n\n
                yield f"data: {json.dumps({'content': chunk})}\n\n"

            # Send done signal
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Claude: {str(e)}")
