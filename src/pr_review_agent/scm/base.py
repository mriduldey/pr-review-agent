"""Small contract shared by SCM adapters."""

from typing import Protocol

from pr_review_agent.scm.models import ChangedFile, PRMetadata, PRReference


class SCMError(RuntimeError):
    """A provider operation failed or returned incomplete PR data."""


class SCMProvider(Protocol):
    def get_pull_request(self, ref: PRReference) -> PRMetadata: ...

    def get_changed_files(self, ref: PRReference) -> list[ChangedFile]: ...