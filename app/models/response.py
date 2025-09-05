from pydantic import BaseModel, Field
from typing import List

class PredictionResult(BaseModel):
    real: float = Field(..., ge=0, le=1, description="Probabilidad de que sea real (0–1)")
    fake: float = Field(..., ge=0, le=1, description="Probabilidad de que sea fake (0–1)")
    prediction: str = Field(..., description="Etiqueta predicha: 'real' o 'fake'")

class ModelsResponse(BaseModel):
    result: PredictionResult
    
    
class ModelInfo(BaseModel):
    filename: str
    size_bytes: int
    model_type: str

class AvailableModelsResponse(BaseModel):
    available_models: List[ModelInfo]