"""CLI entry point: metadata, changed files, or local LLM review."""

import argparse
from dataclasses import asdict

from pr_review_agent.agent.reviewer import run_agent
from pr_review_agent.core.config import GITHUB_TOKEN
from pr_review_agent.core.pr_context import PRContext
from pr_review_agent.core.state import pr, reset_pr
from pr_review_agent.llm.prompts import PR_REVIEW_SYSTEM_PROMPT
from pr_review_agent.scm.base import SCMError
from pr_review_agent.scm.github import GitHubProvider
from pr_review_agent.scm.parser import parse_pr_reference
from pr_review_agent.tools.handlers import create_pr_handlers

MAX_REVIEW_FILES = 30  # Prototype guardrail, not an SCM provider limit.
MAX_REVIEW_PATCH_CHARS = 60_000  # Prototype LLM input guardrail.


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect or locally review a pull request")
    parser.add_argument("url", nargs="?", help="Full public pull request URL")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--files", action="store_true", help="List changed files (no LLM)")
    mode.add_argument("--review", action="store_true", help="Review changed-file patches with LLM")
    mode.add_argument("--demo", action="store_true", help="Run original local simulation")
    args = parser.parse_args(argv)

    if args.demo:
        if args.url:
            parser.error("--demo does not accept a PR URL")
        reset_pr()
        answer = run_agent(f"Review demo PR #{pr['number']} using our team coding standards.")
        print("\n===== Demo Review Summary =====\n", answer)
        print("\n===== Demo State =====\n", pr)
        return

    if not args.url:
        parser.error("provide a PR URL, or use --demo")

    try:
        reference = parse_pr_reference(args.url)
        if reference.provider != "github":
            raise SCMError(f"{reference.provider} API support is not implemented yet")

        provider = GitHubProvider(GITHUB_TOKEN)
        metadata = provider.get_pull_request(reference)
        print(f"PR: {reference.repository}#{reference.number}")
        print(f"Title: {metadata.title}")
        print(f"State: {metadata.state.upper()}")
        print(f"Head SHA: {metadata.head_sha}")
        print(f"Changed-file count: {metadata.changed_files}")

        if not (args.files or args.review):
            return

        files = provider.get_changed_files(reference)
        updated = provider.get_pull_request(reference)
        if (updated.head_sha != metadata.head_sha
                or updated.changed_files != metadata.changed_files):
            raise SCMError("PR changed while retrieving files; retry")

        if args.files:
            for changed in files:
                print(f"- {changed.filename} [{changed.status}] "
                      f"+{changed.additions}/-{changed.deletions}")
            return

        if not files:
            raise SCMError("No changed files to review")
        if len(files) > MAX_REVIEW_FILES:
            raise SCMError(f"Prototype review supports at most {MAX_REVIEW_FILES} files")
        missing_patches = [changed.filename for changed in files if changed.patch is None]
        if missing_patches:
            raise SCMError(f"Cannot review files without text patches: {missing_patches}")
        if sum(len(changed.patch) for changed in files) > MAX_REVIEW_PATCH_CHARS:
            raise SCMError("PR patch content too large for prototype review")

        context = PRContext(reference, metadata, tuple(files))
        functions, result = create_pr_handlers(context)
        filenames = "\n".join(changed.filename for changed in context.files)
        answer = run_agent(
            f"Review PR #{reference.number}: {metadata.title}\n"
            f"Changed files to inspect:\n{filenames}",
            max_steps=max(10, len(files) + 3),
            functions=functions,
            system_prompt=PR_REVIEW_SYSTEM_PROMPT,
        )
        if result.status == "PENDING" or len(result.inspected_files) != len(files):
            raise SCMError("Incomplete review: not all files inspected or status unset")
        if not answer or answer.startswith("Agent stopped: Maximum steps reached"):
            raise SCMError("Review agent did not produce a completed summary")
        print("\n===== Review Summary =====\n", answer)
        print("\n===== Local Review Result =====\n", asdict(result))

    except (ValueError, SCMError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()