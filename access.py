from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from env_config import get_model_name, raise_model_access_error, require_openai_api_key



class CustomState(AgentState):
    user_id: str

@tool
def get_user_info(
    runtime: ToolRuntime
) -> str:
    """Look up user info."""
    user_id = runtime.state["user_id"]
    return "User is John Smith" if user_id == "user_123" else "Unknown user"
require_openai_api_key()
model_name = get_model_name()
agent = create_agent(
    model=f"openai:{model_name}",
    tools=[get_user_info],
    state_schema=CustomState,
)

result = agent.invoke({
    "messages": "look up user information",
    "user_id": "user_123"
})
print(result["messages"][-1].content)
# > User is John Smith.