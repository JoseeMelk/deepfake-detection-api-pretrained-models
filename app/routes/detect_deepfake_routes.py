from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import tempfile
import os
import io
from app.controllers.huggingface_controller import predict_image
from app.controllers.xception_controller import predict_xception, list_xception_models
from app.controllers.cut_face_controller import cut_face
from app.controllers.ensemble_controller import average_probabilities, majority_vote
from app.models.response import ModelsResponse, AvailableModelsResponse, EnsembleResponse, ModelPrediction
router = APIRouter(tags=["Deepfake Detection"])

@router.post("/huggingface", response_model=ModelsResponse)
async def detect_huggingface(
    file: UploadFile = File(...),
    recortar_cara: bool = Form(False),
    device: str = Form("cpu")  # "cpu" o "cuda"
):
    """
    Detecta si una imagen es un deepfake utilizando el modelo HuggingFace.
    """
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
    """
    Detecta si una imagen es un deepfake utilizando el modelo Xception.
    """
    ext = os.path.splitext(file.filename)[-1].lower()  # ".png", ".jpg", etc.
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name
        
    weight_path = os.path.join("app", "weights", "xception", model_name)
    
    result = predict_xception(tmp_path, weight_path, cut_face=recortar_cara, device=device)

    return {"result": result}

@router.post("/cut_face")
async def cut_out_face(
    file: UploadFile = File(...)
):
    """
    Recorta la cara de la imagen proporcionada, es para probar si el recorte funciona correctamente en tu imagen.
    """
    ext = os.path.splitext(file.filename)[-1].lower()  # ".png", ".jpg", etc.
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # Ejecutar recorte
    result_image = cut_face(tmp_path)

    # Convertir la imagen resultante en un stream
    img_bytes = io.BytesIO()
    result_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")


@router.post("/ensemble/detect", response_model=EnsembleResponse)
async def detect_ensemble(
    file: UploadFile = File(...),
    recortar_cara: bool = Form(False),
    device: str = Form("cpu")
):
    """
    Detecta si una imagen es un deepfake utilizando un ensemble de modelos (HuggingFace + todos los Xception disponibles).
    """
    ext = os.path.splitext(file.filename)[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    results = []

    # 🔹 HuggingFace
    hf_result = predict_image(tmp_path, recortar=recortar_cara, device=device)
    results.append(ModelPrediction(
        model_name="huggingface-deepfake-detector-v1",
        prediction=hf_result["prediction"],
        real=hf_result["real"],
        fake=hf_result["fake"]
    ))

    # 🔹 Xception (todos los pesos en carpeta)
    xception_models = list_xception_models()
    if xception_models:
        for model_info in xception_models:
            weight_path = os.path.join("app", "weights", "xception", model_info["filename"])
            xcep_result = predict_xception(tmp_path, weight_path, cut_face=recortar_cara, device=device)

            results.append(ModelPrediction(
                model_name=model_info["filename"],
                prediction=xcep_result["prediction"],
                real=xcep_result["real"],
                fake=xcep_result["fake"]
            ))

    final_decision_majority = majority_vote(results)
    final_decision_average = average_probabilities(results)
    return EnsembleResponse(
        results=results,
        final_decision_majority=final_decision_majority,
        final_decision_average=final_decision_average
    )
