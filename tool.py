from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  
from env_config import get_model_name, raise_model_access_error, require_openai_api_key


def get_final_text(result: dict) -> str:
    messages = result.get("messages", [])

    for message in reversed(messages):
        content = getattr(message, "content", "")
        if content:
            return content

    return "No final response returned."


def main() -> None:
    require_openai_api_key()
    model_name = get_model_name()
    agent = create_agent(
        model=f"openai:{model_name}",
        checkpointer=InMemorySaver(),
    )

    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
            {"configurable": {"thread_id": "1"}},
        )
    except Exception as exc:
        raise_model_access_error(model_name, exc)

    print(get_final_text(result))


if __name__ == "__main__":
    main()

