"""Provider factory/selection."""


from pr_review_agent.core.config import LLM_PROVIDER
from pr_review_agent.llm.providers.openai import OpenAIProvider
from pr_review_agent.llm.providers.anthropic import AnthropicProvider
from pr_review_agent.llm.providers.gemini import GeminiProvider

def get_llm():
    if LLM_PROVIDER == "openai":
        return OpenAIProvider()
    elif LLM_PROVIDER == "anthropic":
        return AnthropicProvider()
    elif LLM_PROVIDER == "gemini":
        return GeminiProvider()
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")