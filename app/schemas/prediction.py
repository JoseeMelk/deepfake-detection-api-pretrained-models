from pydantic import BaseModel

class PredictionResponse(BaseModel):
    fake: float
    real: float
    prediction: str
