"""App settings."""


class Settings:
    """Application configuration container."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
