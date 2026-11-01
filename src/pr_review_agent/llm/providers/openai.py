"""OpenAI provider implementation."""

from ..base import BaseLLM


class OpenAIProvider(BaseLLM):
    """OpenAI-backed LLM client."""

    def generate(self, prompt: str, **kwargs):
        """Generate a response using the OpenAI provider."""
        raise NotImplementedError
