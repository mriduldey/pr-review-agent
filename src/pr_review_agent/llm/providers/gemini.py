import os

from openai import OpenAI

from pr_review_agent.core.config import LLM_MODEL


class GeminiProvider:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ["GEMINI_API_KEY"],
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

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