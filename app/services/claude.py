import os
from typing import AsyncGenerator, List, Dict, Any, Optional
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeService:
    """Service for interacting with Claude API."""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = AsyncAnthropic(api_key=api_key)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

    async def send_message(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024
    ) -> str:
        """Send a message to Claude and get a response."""
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt or "You are a helpful assistant.",
            messages=messages
        )
        return response.content[0].text

    async def stream_message(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024
    ) -> AsyncGenerator[str, None]:
        """Stream a response from Claude."""
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt or "You are a helpful assistant.",
            messages=messages
        ) as stream:
            async for text in stream.text_stream:
                yield text


# Global service instance
_claude_service: Optional[ClaudeService] = None


def get_claude_service() -> ClaudeService:
    """Get or create the Claude service instance."""
    global _claude_service
    if _claude_service is None:
        _claude_service = ClaudeService()
    return _claude_service
