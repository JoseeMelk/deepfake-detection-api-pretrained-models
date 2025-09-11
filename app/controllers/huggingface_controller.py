from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import torch
from app.utils.cut_out_face import cut_out_face
from app.utils.get_device import get_device
from app.models.response import PredictionResult

MODEL_NAME = "prithivMLmods/deepfake-detector-model-v1"
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = SiglipForImageClassification.from_pretrained(MODEL_NAME)

id2label = {"0": "fake", "1": "real"}

def predict_image(image_path: str, recortar: bool = False, device: str = "cpu") -> dict:
    image = Image.open(image_path).convert("RGB")
    
    # Recortar cara si se pidió
    if recortar:
        image = cut_out_face(image)

    inputs = processor(images=image, return_tensors="pt")

    torch_device = get_device(device)
    model.to(torch_device)
    inputs = {k: v.to(torch_device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)[0].cpu()

    return PredictionResult(
        model_name="deepfake-detector-model-v1",
        real=float(probs[1]),
        fake=float(probs[0]),
        prediction=id2label[str(torch.argmax(probs).item())]
    )
