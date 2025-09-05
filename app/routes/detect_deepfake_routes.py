from fastapi import APIRouter, UploadFile, File, Form
import tempfile
import os
from app.controllers.huggingface_controller import predict_image
from app.controllers.xception_controller import predict_xception, list_xception_models
from app.models.response import ModelsResponse, AvailableModelsResponse

router = APIRouter(tags=["Deepfake Detection"])

@router.post("/huggingface", response_model=ModelsResponse)
async def detect_huggingface(
    file: UploadFile = File(...),
    recortar_cara: bool = Form(False),
    device: str = Form("cpu")  # "cpu" o "cuda"
):
    ext = os.path.splitext(file.filename)[-1].lower()  # ".png", ".jpg", etc.
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    result = predict_image(tmp_path, recortar=recortar_cara, device=device)

    return {"result": result}

@router.get("/xception/weights", response_model=AvailableModelsResponse)
async def available_models():
    """
    Lista los pesos disponibles para el modelo Xception.
    """
    model_type = "xception"
    models = list_xception_models()

    if models is None:
        return {"error": f"No existe la carpeta {model_type}"}

    return {"available_models": models}

@router.post("/xception/detect", response_model=ModelsResponse)
async def detect_xception(
    file: UploadFile = File(...),
    model_name: str = Form("deepfake_c0_xception.pkl"),
    recortar_cara: bool = Form(False),
    device: str = Form("cpu")  # "cpu" o "cuda"
):
    ext = os.path.splitext(file.filename)[-1].lower()  # ".png", ".jpg", etc.
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name
        
    weight_path = os.path.join("app", "weights", "xception", model_name)
    
    result = predict_xception(tmp_path, weight_path, cut_face=recortar_cara, device=device)

    return {"result": result}

