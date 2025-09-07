from app.utils.cut_out_face import cut_out_face
from PIL import Image

def cut_face(image_path):
    """
    Corta la cara de una imagen y lo retorna como una nueva imagen.
    Si no se detecta ninguna cara, retorna la imagen original.
    """
    image = Image.open(image_path).convert("RGB")
    return cut_out_face(image)