from openai import OpenAI

from pr_review_agent.core.config import LLM_MODEL
from pr_review_agent.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = OpenAI()

    def chat(self, messages, tools=None):
        params = {
            "model": LLM_MODEL,
            "messages": messages,
        }

        if tools is not None:
            params["tools"] = tools
            params["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**params)

        return response.choices[0].message