"""Original demo tools plus handlers bound to one real PR review."""

from pr_review_agent.core.config import DATA_DIR
from pr_review_agent.core.pr_context import PRContext
from pr_review_agent.core.review_models import ReviewComment, ReviewResult
from pr_review_agent.core.state import pr


def read_file(filename):
    # Intentionally vulnerable demo fixtures: never use this handler for real PRs.
    allowed_files = {"team_standards.md", "payment_utils.py", "auth.py", "order.py"}
    if filename not in allowed_files:
        return f"ERROR: File not allowed: {filename}"
    return (DATA_DIR / filename).read_text(encoding="utf-8")


def post_review_comment(filename, comment):
    pr["comments"].append({"file": filename, "comment": comment})
    return "Comment saved"


def set_pr_status(status):
    if status not in ("PASS", "BLOCKED"):
        return "ERROR: status must be PASS or BLOCKED"
    pr["status"] = status
    return "PR status updated"


FUNCTIONS = {
    "read_file": read_file,
    "post_review_comment": post_review_comment,
    "set_pr_status": set_pr_status,
}


def create_pr_handlers(context: PRContext):
    """Make isolated handlers and a typed local result for this execution."""
    by_name = {file.filename: file for file in context.files}
    result = ReviewResult(number=context.reference.number)

    def read_pr_file(filename):
        changed = by_name.get(filename)
        if changed is None:
            return f"ERROR: File not in this PR: {filename}"
        if changed.patch is None:
            return f"ERROR: No text patch for {filename} (possibly binary or truncated)"
        result.inspected_files.add(filename)
        return f"File: {filename}\nStatus: {changed.status}\nDiff:\n{changed.patch}"

    def save_comment(filename, comment):
        if filename not in by_name:
            return f"ERROR: File not in this PR: {filename}"
        if filename not in result.inspected_files:
            return f"ERROR: Read the changed file before commenting: {filename}"
        if not comment.strip():
            return "ERROR: Comment must not be empty"
        result.comments.append(ReviewComment(filename=filename, body=comment))
        return "Comment saved locally (not published to GitHub)"

    def update_status(status):
        if status not in ("PASS", "BLOCKED"):
            return "ERROR: status must be PASS or BLOCKED"
        if len(result.inspected_files) != len(context.files):
            return "ERROR: Inspect all changed files before setting a final status"
        result.status = status
        return "Review status updated locally"

    return {
        "read_file": read_pr_file,
        "post_review_comment": save_comment,
        "set_pr_status": update_status,
    }, result