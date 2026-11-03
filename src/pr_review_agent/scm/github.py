"""GitHub implementation of the SCM provider contract using PyGithub."""

from github import Auth, Github, GithubException
from requests.exceptions import RequestException

from pr_review_agent.scm.base import SCMError
from pr_review_agent.scm.models import ChangedFile, PRMetadata, PRReference


class GitHubProvider:
    def __init__(self, token: str | None = None):
        auth = Auth.Token(token) if token else None
        self.client = Github(auth=auth, per_page=100, timeout=15)

    def _pull(self, ref: PRReference):
        if ref.provider != "github":
            raise SCMError(f"GitHubProvider cannot handle {ref.provider!r}")
        return self.client.get_repo(ref.repository).get_pull(ref.number)

    def get_pull_request(self, ref: PRReference) -> PRMetadata:
        try:
            pr = self._pull(ref)
            return PRMetadata(
                title=pr.title,
                state="merged" if pr.merged else pr.state.lower(),
                head_sha=pr.head.sha,
                changed_files=pr.changed_files,
            )
        except GithubException as exc:
            raise _api_error(exc) from exc
        except RequestException as exc:
            raise SCMError("Network error while contacting GitHub") from exc

    def get_changed_files(self, ref: PRReference) -> list[ChangedFile]:
        try:
            pr = self._pull(ref)
            if pr.changed_files > 3000:
                raise SCMError("GitHub exposes at most 3,000 changed files per PR")

            # PyGithub fetches additional API pages while this is iterated.
            files = [
                ChangedFile(
                    filename=file.filename,
                    status=file.status,
                    additions=file.additions,
                    deletions=file.deletions,
                    patch=getattr(file, "patch", None),
                    previous_filename=getattr(file, "previous_filename", None),
                )
                for file in pr.get_files()
            ]
            if len(files) != pr.changed_files:
                raise SCMError(
                    f"Incomplete GitHub file list: got {len(files)} of "
                    f"{pr.changed_files} files"
                )
            return files
        except GithubException as exc:
            raise _api_error(exc) from exc
        except RequestException as exc:
            raise SCMError("Network error while contacting GitHub") from exc


def _api_error(exc: GithubException) -> SCMError:
    descriptions = {
        401: "invalid or expired GitHub token",
        403: "access denied or rate limit exceeded",
        404: "repository or PR not found or inaccessible",
    }
    reason = descriptions.get(exc.status, "GitHub API request failed")
    return SCMError(f"GitHub API HTTP {exc.status}: {reason}")