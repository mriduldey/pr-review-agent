"""Application entry point."""


from pr_review_agent.agent.reviewer import run_agent
from pr_review_agent.core.state import pr, reset_pr


def main():
    reset_pr()

    answer = run_agent(
        "Review PR #247 using our team coding standards."
    )

    print("\n===== Review Summary =====")
    print(answer)

    print("\n===== Final PR State =====")
    print(pr)


if __name__ == "__main__":
    main()
