import cv2
from PIL import Image
import numpy as np

# Solo usamos el clasificador frontal por defecto
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def cut_out_face(image: Image.Image) -> Image.Image:
    # Convertir PIL.Image a array de OpenCV
    img = np.array(image.convert('RGB'))
    img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # Detectar rostros
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=4,
        minSize=(30, 30),
        maxSize=(400, 400)
    )

    # Si se detecta al menos un rostro, recortamos el primero
    if len(faces) > 0:
        x, y, w, h = faces[0]
        # Margen adicional (por ejemplo, 10% del ancho y alto)
        margin_x = int(w * 0.0)
        margin_y = int(h * 0.0)

        # Nuevas coordenadas con margen, asegurando que no se salgan de la imagen
        x1 = max(x - margin_x, 0)
        y1 = max(y - margin_y, 0)
        x2 = min(x + w + margin_x, img_cv.shape[1])
        y2 = min(y + h + margin_y, img_cv.shape[0])

        recorte = img_cv[y1:y2, x1:x2]
        return Image.fromarray(cv2.cvtColor(recorte, cv2.COLOR_BGR2RGB))

    # Si no se detecta rostro, retornamos la imagen original
    return image
