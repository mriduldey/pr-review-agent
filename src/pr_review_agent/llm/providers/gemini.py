"""Gemini provider implementation."""

from ..base import BaseLLM


class GeminiProvider(BaseLLM):
    """Gemini-backed LLM client."""

    def generate(self, prompt: str, **kwargs):
        """Generate a response using the Gemini provider."""
        raise NotImplementedError
