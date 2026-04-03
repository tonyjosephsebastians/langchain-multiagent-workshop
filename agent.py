import os
from langchain.agents import create_agent
from dotenv import load_dotenv


load_dotenv()


def require_openai_api_key() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in the local .env file.")


def get_model_name() -> str:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()

    if not model_name:
        raise RuntimeError("Set OPENAI_MODEL in the local .env file.")

    return model_name


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


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
        tools=[get_weather],
        system_prompt="You are a helpful assistant",
    )

    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
        )
    except Exception as exc:
        message = str(exc)
        if "model_not_found" in message or "must be verified to use the model" in message:
            raise RuntimeError(
                f"Model '{model_name}' is not available for this API key. "
                "Set OPENAI_MODEL in .env to a model your account can access, "
                "or verify your organization if you want to use gpt-5."
            ) from exc
        raise

    print(get_final_text(result))


if __name__ == "__main__":
    main()
