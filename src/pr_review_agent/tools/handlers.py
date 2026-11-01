"""Tool implementations."""

from pr_review_agent.core.config import DATA_DIR
from pr_review_agent.core.state import pr


def read_file(filename):
    # Restrict the agent to the approved sample files.
    allowed_files = {
        "team_standards.md",
        "payment_utils.py",
        "auth.py",
        "order.py",
    }

    if filename not in allowed_files:
        return f"ERROR: File not allowed: {filename}"

    return (DATA_DIR / filename).read_text(encoding="utf-8")


def post_review_comment(filename, comment):
    pr["comments"].append({
        "file": filename,
        "comment": comment
    })
    return "Comment saved"


def set_pr_status(status):
    if status not in ["PASS", "BLOCKED"]:
        return "ERROR: status must be PASS or BLOCKED"

    pr["status"] = status
    return "PR status updated"


FUNCTIONS = {
    "read_file": read_file,
    "post_review_comment": post_review_comment,
    "set_pr_status": set_pr_status,
}