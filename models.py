from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from env_config import get_model_name, raise_model_access_error, require_openai_api_key

class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")


def main() -> None:
    require_openai_api_key()
    model_name = get_model_name()
    model = init_chat_model(model_name)

    # response = model.invoke("Why do parrots talk?")
    # for response in model.batch_as_completed([
    #     "Why do parrots have colorful feathers?",
    #     "How do airplanes fly?",
    #     "What is quantum computing?"
    # ]):
    #     print(str(response))

    model_with_structure = model.with_structured_output(Movie, include_raw=True)

    try:
        response = model_with_structure.invoke(
            "Provide details about the movie Inception"
        )
    except Exception as exc:
        raise_model_access_error(model_name, exc)

    print(response)


if __name__ == "__main__":
    main()
