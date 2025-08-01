from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Model(BaseModel):
    """OpenAI-compatible model object"""
    type: Literal["model"] = "model"
    id: str = Field(..., description="The model identifier")
    display_name: str = Field(..., description="Human-readable name of the model")
    created_at: str = Field(..., description="ISO 8601 timestamp of when the model was created")
    # OpenAI compatibility fields
    created: Optional[int] = Field(None, description="Unix timestamp (for OpenAI compatibility)")
    owned_by: Optional[str] = Field(default="anthropic", description="Organization that owns the model")
    object: Optional[Literal["model"]] = Field(default="model", description="Object type (for OpenAI compatibility)")


class ModelList(BaseModel):
    """OpenAI-compatible model list response"""
    data: List[Model]
    has_more: bool = False
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    # OpenAI compatibility field
    object: Optional[Literal["list"]] = Field(default="list", description="Object type (for OpenAI compatibility)")


# Define the available models
AVAILABLE_MODELS = [
    Model(
        id="claude-opus-4-20250514",
        display_name="Claude Opus 4",
        created_at="2025-05-22T00:00:00Z",
        created=1716336000,  # Unix timestamp for 2025-05-22
    ),
    Model(
        id="claude-sonnet-4-20250514",
        display_name="Claude Sonnet 4",
        created_at="2025-05-22T00:00:00Z",
        created=1716336000,  # Unix timestamp for 2025-05-22
    ),
]


def get_model_by_id(model_id: str) -> Optional[Model]:
    """Get a model by its ID"""
    for model in AVAILABLE_MODELS:
        if model.id == model_id:
            return model
    return None


def get_all_models() -> ModelList:
    """Get all available models"""
    if not AVAILABLE_MODELS:
        return ModelList(data=[], has_more=False)
    
    return ModelList(
        data=AVAILABLE_MODELS,
        has_more=False,
        first_id=AVAILABLE_MODELS[0].id,
        last_id=AVAILABLE_MODELS[-1].id,
    )