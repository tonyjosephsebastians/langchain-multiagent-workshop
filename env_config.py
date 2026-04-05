import os

from dotenv import load_dotenv


load_dotenv()


def require_openai_api_key() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in the local .env file.")


def get_model_name(default: str = "gpt-4.1-mini") -> str:
    model_name = os.getenv("OPENAI_MODEL", default).strip()

    if not model_name:
        raise RuntimeError("Set OPENAI_MODEL in the local .env file.")

    return model_name


def raise_model_access_error(model_name: str, exc: Exception) -> None:
    message = str(exc)
    if "model_not_found" in message or "must be verified to use the model" in message:
        raise RuntimeError(
            f"Model '{model_name}' is not available for this API key. "
            "Set OPENAI_MODEL in .env to a model your account can access, "
            "or verify your organization if you want to use gpt-5."
        ) from exc

    raise exc
