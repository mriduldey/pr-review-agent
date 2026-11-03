"""Immutable review inputs for a single pull request."""

from dataclasses import dataclass

from pr_review_agent.scm.models import ChangedFile, PRMetadata, PRReference


@dataclass(frozen=True)
class PRContext:
    reference: PRReference
    metadata: PRMetadata
    files: tuple[ChangedFile, ...]

    def __post_init__(self):
        if len(self.files) != self.metadata.changed_files:
            raise ValueError("PR context file count does not match metadata")
        if len({file.filename for file in self.files}) != len(self.files):
            raise ValueError("PR context contains duplicate filenames")