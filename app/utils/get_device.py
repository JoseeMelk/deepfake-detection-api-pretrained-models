import torch
import platform

def get_device(device: str = "cpu"):
    """
    Devuelve el dispositivo correcto para torch.
    device puede ser 'cpu' o 'cuda'.
    Si se pide 'cuda' pero no hay GPU disponible, devuelve 'cpu'.
    """
    if device == "cuda" and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")
