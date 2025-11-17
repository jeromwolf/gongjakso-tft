"""
AI Client Utilities

Anthropic Claude API client
"""
from anthropic import AsyncAnthropic
from core.config import settings
from loguru import logger


_anthropic_client = None


def get_anthropic_client() -> AsyncAnthropic:
    """
    Get Anthropic API client (singleton)

    Returns:
        AsyncAnthropic client instance
    """
    global _anthropic_client

    if _anthropic_client is None:
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is not configured")

        _anthropic_client = AsyncAnthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )
        logger.info("Anthropic API client initialized")

    return _anthropic_client
