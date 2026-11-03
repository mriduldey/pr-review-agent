"""Parse hosted pull/merge request URLs without provider API calls."""

import re
from urllib.parse import urlsplit

from pr_review_agent.scm.models import PRReference


_PATTERNS = {
    "github.com": ("github", r"([\w.-]+/[\w.-]+)/pull/([1-9]\d*)"),
    "gitlab.com": ("gitlab", r"([\w.-]+(?:/[\w.-]+)+)/-/merge_requests/([1-9]\d*)"),
    "bitbucket.org": ("bitbucket", r"([\w.-]+/[\w.-]+)/pull-requests/([1-9]\d*)"),
}


def parse_pr_reference(url: str) -> PRReference:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.port:
        raise ValueError("Expected a public HTTPS pull request URL")

    provider_pattern = _PATTERNS.get(parsed.hostname or "")
    if provider_pattern is None:
        raise ValueError("Unsupported Git provider hostname")

    provider, pattern = provider_pattern
    match = re.fullmatch(pattern, parsed.path.strip("/"))
    if not match:
        raise ValueError("Invalid pull/merge request URL path")

    repository, number = match.groups()
    return PRReference(provider, repository, int(number))