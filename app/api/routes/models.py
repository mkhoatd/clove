from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.dependencies.auth import AuthDep
from app.models.openai import  get_model_by_id, get_all_models

router = APIRouter()


@router.get("/models", response_model=None)
async def list_models(_: AuthDep) -> JSONResponse:
    """List available models in OpenAI-compatible format"""
    model_list = get_all_models()
    
    # Convert to dict and ensure proper JSON formatting
    response_data = model_list.model_dump(exclude_none=True)
    
    return JSONResponse(content=response_data)


@router.get("/models/{model_id}", response_model=None)
async def get_model(model_id: str, _: AuthDep) -> JSONResponse:
    """Get a specific model by ID in OpenAI-compatible format"""
    model = get_model_by_id(model_id)
    
    if not model:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_id}' not found"
        )
    
    # Convert to dict and ensure proper JSON formatting
    response_data = model.model_dump(exclude_none=True)
    
    return JSONResponse(content=response_data)