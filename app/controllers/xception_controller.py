import torch
import torchvision.transforms as transforms
from PIL import Image
from app.utils.cut_out_face import cut_out_face
from app.utils.get_device import get_device
from app.utils.list_models import list_available_models
from app.models.models import model_selection

# Normalización usada en Xception
transform = transforms.Compose([
    transforms.Resize((299, 299)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# Cache de modelo
_loaded_models = {}

def list_xception_models():
    """Lista los pesos disponibles para el modelo Xception."""
    return list_available_models("xception")

def load_xception_model(weight_path: str, device: torch.device):
    """Carga el modelo desde weights y lo guarda en cache."""
    if weight_path in _loaded_models:
        return _loaded_models[weight_path]

    model = model_selection("xception", num_out_classes=2, dropout=0.5)
    state_dict = torch.load(weight_path, map_location=device)

    # Si fue entrenado con DataParallel
    if list(state_dict.keys())[0].startswith("module."):
        state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}

    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    _loaded_models[weight_path] = model
    return model


def predict_xception(image_path: str, weight_path: str, cut_face: bool = False, device: str = "cpu") -> dict:
    """Predice si una imagen es real o fake usando Xception."""
    torch_device = get_device(device)
    model = load_xception_model(weight_path, torch_device)

    image = Image.open(image_path).convert("RGB")
    if cut_face:
        image = cut_out_face(image)
        
    tensor = transform(image).unsqueeze(0).to(torch_device)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1).cpu().numpy()[0]
    
    CLASS_MAP = {
        1: "fake",  # Según el dataset Deepfake-Detection de HongguLiu
        0: "real"
    }
    pred_class = int(probs.argmax())

    return {
        "real": round(float(probs[0]), 6),
        "fake": round(float(probs[1]), 6),
        "prediction": CLASS_MAP[pred_class],
    }
