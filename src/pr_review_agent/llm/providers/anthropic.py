"""Anthropic provider implementation."""

from ..base import BaseLLM


class AnthropicProvider(BaseLLM):
    """Anthropic-backed LLM client."""

    def generate(self, prompt: str, **kwargs):
        """Generate a response using the Anthropic provider."""
        raise NotImplementedError
