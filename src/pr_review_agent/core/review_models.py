"""Execution-scoped, provider-neutral review output."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReviewComment:
    filename: str
    body: str
    line: int | None = None  # Diff line mapping is out of scope for this prototype.


@dataclass
class ReviewResult:
    number: int
    status: str = "PENDING"
    comments: list[ReviewComment] = field(default_factory=list)
    inspected_files: set[str] = field(default_factory=set)