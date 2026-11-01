import json

from pr_review_agent.llm.client import get_llm
from pr_review_agent.llm.prompts import SYSTEM_PROMPT
from pr_review_agent.tools.definitions import TOOLS
from pr_review_agent.tools.handlers import FUNCTIONS


def run_agent(question, max_steps=10):
    llm = get_llm()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        print(f"\n===== Agent Step {step + 1} =====")

        # THINK: Ask the LLM what to do next
        message = llm.chat(
            messages=messages,
            tools=TOOLS,
        )

        messages.append(message)

        # STOP: No more tool calls
        if not message.tool_calls:
            print("Agent finished")
            return message.content

        # ACT: Execute requested tools
        for call in message.tool_calls:
            tool_name = call.function.name
            print(f"Calling tool: {tool_name}")

            try:
                arguments = json.loads(
                    call.function.arguments
                )

                if tool_name not in FUNCTIONS:
                    raise ValueError(
                        f"Unknown tool: {tool_name}"
                    )

                result = FUNCTIONS[tool_name](**arguments)

            except Exception as e:
                result = f"Tool error: {e}"

            # OBSERVE: Return tool result to LLM
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

    return "Agent stopped: Maximum steps reached"