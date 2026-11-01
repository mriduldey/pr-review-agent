"""Common LLM interface."""

from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Base contract for all model providers."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs):
        """Generate a completion from the model."""
        raise NotImplementedError
