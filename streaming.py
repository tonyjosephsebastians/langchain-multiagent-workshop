from langchain.agents import create_agent
from env_config import get_model_name, raise_model_access_error, require_openai_api_key
from langchain_core.runnables import Runnable
from langchain.messages import AIMessageChunk

def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"
require_openai_api_key()
model_name = get_model_name()
# agent = create_agent(
#     model=f"openai:{model_name}",
#     tools=[get_weather],
# )
# for chunk in agent.stream(
#     {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
#     stream_mode="messages",
#     version="v2",
# ):
#     if chunk["type"] == "messages":
#         token, metadata = chunk["data"]
#         print(f"node: {metadata['langgraph_node']}")
#         print(f"content: {token.content_blocks}")
#         print("\n")


#common pattern

agent: Runnable = create_agent(
    model=f"openai:{model_name}",
    tools=[get_weather],
)

for token, metadata in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="messages",
):
    if not isinstance(token, AIMessageChunk):
        continue
    reasoning = [b for b in token.content_blocks if b["type"] == "reasoning"]
    text = [b for b in token.content_blocks if b["type"] == "text"]
    if reasoning:
        print(f"[thinking] {reasoning[0]['reasoning']}", end="")
    if text:
        print(text[0]["text"], end="")