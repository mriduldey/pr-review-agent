"""Provider factory/selection."""


def get_client(provider: str, **kwargs):
    """Return an LLM client instance for the selected provider."""
    raise NotImplementedError
