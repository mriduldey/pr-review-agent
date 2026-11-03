"""Provider-neutral pull request data."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PRReference:
    provider: str
    repository: str
    number: int


@dataclass(frozen=True)
class PRMetadata:
    title: str
    state: str
    head_sha: str
    changed_files: int


@dataclass(frozen=True)
class ChangedFile:
    filename: str
    status: str
    additions: int
    deletions: int
    patch: str | None = None
    previous_filename: str | None = None