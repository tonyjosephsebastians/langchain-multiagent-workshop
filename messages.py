from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from env_config import get_model_name, raise_model_access_error, require_openai_api_key


def main() -> None:
    require_openai_api_key()
    model_name = get_model_name()
    model = init_chat_model(model_name)

    system_msg = SystemMessage("You are a helpful assistant.")
    human_msg = HumanMessage("Hello, how are you?")

    try:
        response = model.invoke([system_msg, human_msg])
    except Exception as exc:
        raise_model_access_error(model_name, exc)

    print(response.content)


if __name__ == "__main__":
    main()
