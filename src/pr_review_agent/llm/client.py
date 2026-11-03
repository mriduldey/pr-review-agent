"""Select an implemented LLM provider."""

from pr_review_agent.core.config import LLM_PROVIDER
from pr_review_agent.llm.providers.openai import OpenAIProvider
from pr_review_agent.llm.providers.gemini import GeminiProvider


def get_llm():
    if LLM_PROVIDER == "openai":
        return OpenAIProvider()
    if LLM_PROVIDER == "gemini":
        return GeminiProvider()
    if LLM_PROVIDER == "anthropic":
        raise ValueError("Anthropic LLM provider is a stub and is not implemented")
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")