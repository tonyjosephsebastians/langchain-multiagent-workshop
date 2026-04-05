# from pydantic import BaseModel, Field
# from langchain.agents import create_agent
# from env_config import get_model_name, raise_model_access_error, require_openai_api_key


# class ContactInfo(BaseModel):
#     """Contact information for a person."""
#     name: str = Field(description="The name of the person")
#     email: str = Field(description="The email address of the person")
#     phone: str = Field(description="The phone number of the person")

# require_openai_api_key()
# model_name = get_model_name()
# agent = create_agent(
#     model=f"openai:{model_name}",
#     response_format=ContactInfo  # Auto-selects ProviderStrategy
# )

# result = agent.invoke({
#     "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
# })

# print(result["structured_response"])
# # ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')



#Tool strategy


from pydantic import BaseModel, Field
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from env_config import get_model_name, raise_model_access_error, require_openai_api_key





class ProductReview(BaseModel):
    """Analysis of a product review."""
    rating: int | None = Field(description="The rating of the product", ge=1, le=5)
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review")
    key_points: list[str] = Field(description="The key points of the review. Lowercase, 1-3 words each.")

require_openai_api_key()
model_name = get_model_name()
agent = create_agent(
    model=f"openai:{model_name}",
    response_format=ToolStrategy(schema=ProductReview)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
print(result["structured_response"])
# ProductReview(rating=5, sentiment='positive', key_points=['fast shipping', 'expensive'])