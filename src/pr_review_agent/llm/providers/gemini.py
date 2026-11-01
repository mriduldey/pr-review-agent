"""Gemini provider implementation."""

from pr_review_agent.core.config import LLM_MODEL
from pr_review_agent.llm.base import LLMProvider

class GeminiProvider(LLMProvider):
    """Gemini-backed LLM client."""

    def chat(self, messages, tools=None):
        """Generate a response using the Gemini provider."""
        raise NotImplementedError
