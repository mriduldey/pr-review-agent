import json

from pr_review_agent.llm.client import get_llm
from pr_review_agent.llm.prompts import SYSTEM_PROMPT
from pr_review_agent.tools.definitions import TOOLS
from pr_review_agent.tools.handlers import FUNCTIONS


def run_agent(question, max_steps=10, *, functions=None, system_prompt=None):
    llm = get_llm()
    active_functions = FUNCTIONS if functions is None else functions

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT if system_prompt is None else system_prompt},
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        print(f"\n===== Agent Step {step + 1} =====")

        message = llm.chat(messages=messages, tools=TOOLS)
        messages.append(message)

        if not message.tool_calls:
            print("Agent finished")
            return message.content

        for call in message.tool_calls:
            tool_name = call.function.name
            print(f"Calling tool: {tool_name}")

            try:
                arguments = json.loads(call.function.arguments)
                if tool_name not in active_functions:
                    raise ValueError(f"Unknown tool: {tool_name}")
                result = active_functions[tool_name](**arguments)
            except Exception as e:
                result = f"Tool error: {e}"

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

    return "Agent stopped: Maximum steps reached"