from pydantic import BaseModel, Field
from typing import List, Dict
from PIL import Image

class PredictionResult(BaseModel):
    model_name: str = Field(..., description="Nombre del peso usado para la predicción")
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

class DecisionResult(BaseModel):
    prediction: str
    confidence: float

class EnsembleResponse(BaseModel):
    results: List[PredictionResult]
    final_decision_majority: DecisionResult
    final_decision_average: DecisionResult