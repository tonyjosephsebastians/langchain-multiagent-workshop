# from langchain.agents import create_agent
# from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware

# # agent = create_agent(
# #     model="gpt-4.1",
# #     tools=[...],
# #     middleware=[
# #         SummarizationMiddleware(...),
# #         HumanInTheLoopMiddleware(...)
# #     ],
# # )

# Human in the loop

# import sys
# from pathlib import Path

# from langchain.agents import create_agent
# from langchain.agents.middleware import HumanInTheLoopMiddleware
# from langgraph.checkpoint.memory import InMemorySaver


# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# if str(PROJECT_ROOT) not in sys.path:
#     sys.path.insert(0, str(PROJECT_ROOT))

# from env_config import get_model_name, require_openai_api_key

# def your_read_email_tool(email_id: str) -> str:
#     """Mock function to read an email by its ID."""
#     return f"Email content for ID: {email_id}"

# def your_send_email_tool(recipient: str, subject: str, body: str) -> str:
#     """Mock function to send an email."""
#     return f"Email sent to {recipient} with subject '{subject}'"


# def main() -> None:
#     require_openai_api_key()
#     model_name = get_model_name()
#     agent = create_agent(
#         model=f"openai:{model_name}",
#         tools=[your_read_email_tool, your_send_email_tool],
#         checkpointer=InMemorySaver(),
#         middleware=[
#             HumanInTheLoopMiddleware(
#                 interrupt_on={
#                     "your_send_email_tool": {
#                         "allowed_decisions": ["approve", "edit", "reject"],
#                     },
#                     "your_read_email_tool": False,
#                 }
#             ),
#         ],
#     )

#     print(agent)


# if __name__ == "__main__":
#     main()


## tool call limit 

# from langchain.agents import create_agent
# from langchain.agents.middleware import ToolCallLimitMiddleware


# global_limiter = ToolCallLimitMiddleware(thread_limit=20, run_limit=10)
# search_limiter = ToolCallLimitMiddleware(tool_name="search", thread_limit=5, run_limit=3)
# database_limiter = ToolCallLimitMiddleware(tool_name="query_database", thread_limit=10)
# strict_limiter = ToolCallLimitMiddleware(tool_name="scrape_webpage", run_limit=2, exit_behavior="error")

# agent = create_agent(
#     model="gpt-4.1",
#     tools=[search_tool, database_tool, scraper_tool],
#     middleware=[global_limiter, search_limiter, database_limiter, strict_limiter],
# )


#PII detection

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
import re


# Method 1: Regex pattern string
agent1 = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
        ),
    ],
)

# Method 2: Compiled regex pattern
agent2 = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        PIIMiddleware(
            "phone_number",
            detector=re.compile(r"\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}"),
            strategy="mask",
        ),
    ],
)

# Method 3: Custom detector function
def detect_ssn(content: str) -> list[dict[str, str | int]]:
    """Detect SSN with validation.

    Returns a list of dictionaries with 'text', 'start', and 'end' keys.
    """
    import re
    matches = []
    pattern = r"\d{3}-\d{2}-\d{4}"
    for match in re.finditer(pattern, content):
        ssn = match.group(0)
        # Validate: first 3 digits shouldn't be 000, 666, or 900-999
        first_three = int(ssn[:3])
        if first_three not in [0, 666] and not (900 <= first_three <= 999):
            matches.append({
                "text": ssn,
                "start": match.start(),
                "end": match.end(),
            })
    return matches

agent3 = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        PIIMiddleware(
            "ssn",
            detector=detect_ssn,
            strategy="hash",
        ),
    ],
)