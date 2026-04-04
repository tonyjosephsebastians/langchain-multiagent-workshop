import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


load_dotenv()

model = init_chat_model("gpt-5.2")

#response = model.invoke("Why do parrots talk?")

# for response in model.batch_as_completed([
#     "Why do parrots have colorful feathers?",
#     "How do airplanes fly?",
#     "What is quantum computing?"
# ]):
#     print(str(response))



#structured output


from pydantic import BaseModel, Field

class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")

model_with_structure = model.with_structured_output(Movie, include_raw=True)
response = model_with_structure.invoke("Provide details about the movie Inception")
print(response)