"""Common LLM interface."""

from typing import Protocol


class LLMProvider(Protocol):
    def chat(self, messages, tools=None):
        ...