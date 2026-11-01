"""Mock PR state."""


class PRState:
    """Simple in-memory representation of a pull request."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
