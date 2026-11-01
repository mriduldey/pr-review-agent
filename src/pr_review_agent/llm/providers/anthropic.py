"""Anthropic provider implementation."""

from pr_review_agent.core.config import LLM_MODEL
from pr_review_agent.llm.base import LLMProvider

class AnthropicProvider(LLMProvider):
    """Anthropic-backed LLM client."""

    def chat(self, messages, tools=None):
        """Generate a response using the Anthropic provider."""
        raise NotImplementedError
