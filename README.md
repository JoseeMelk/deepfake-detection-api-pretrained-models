# Deepfake API – Pre-trained Models

API construida con **FastAPI** para la detección de *deepfakes* en imágenes, utilizando modelos preentrenados de **HuggingFace** y **Xception**.  
Recibe una imagen, la procesa (opcionalmente recorta el rostro) y devuelve una predicción con probabilidades de **real** o **fake**.

---

## 🚀 Características
- **Modelos soportados**:
  - [`deepfake-detector-model-v1`](https://huggingface.co/prithivMLmods/deepfake-detector-model-v1) de HuggingFace.
  - Modelos **Xception** con pesos preentrenados (`.pkl` / `.pth`).
- **Predicción en CPU o GPU** (`device: cpu | cuda`).
- **Endpoints REST** listos para pruebas con imágenes.
- Respuesta estructurada en formato JSON con probabilidades.

---

## 📂 Estructura del proyecto
```
app/
 ├── controllers/        # Lógica de predicción (HuggingFace, Xception)
 ├── models/             # Definición de redes y modelos preentrenados
 ├── routes/             # Endpoints de FastAPI
 ├── schemas/            # Sin nada todavia
 ├── services/           # Servicios auxiliares (sin nada todavia)
 ├── utils/              # Utilidades (recorte de cara, obtencion de dispositivo cpu o cuda, etc.)
 ├── weights/            # Pesos de los modelos (Xception aquí)
 │   └── xception/
 │       ├── deepfake_c0_xception.pkl
 │       ├── ffpp_c23.pth
 │       └── ffpp_c40.pth
 └── main.py             # Punto de entrada FastAPI
 └── 📁test_images
 │   └── 📁reporte_visual #Generado por el test
 │   └── 📁resultados     #Generado por el test
 │   └── example.png      #imagen de ejemplo
 └── 📁tests
     └── 📁recortar_rostro
         ├── test_calidad_deteccion.py #Verifica la calidad del recorte a comparación de la imagen real
         └── test_recorte_real.py      #Realiza un recorte de rostro de las imagenes que estan en test_images
```

---

## ⚡ Instalación
### Se contempla que ya se tiene instalado torch, torchaudio y torchvision, ya sea con cuda o no

1. Clona el repositorio:
   ```bash
   git https://github.com/JoseeMelk/deepfake-detection-api-pretrained-models.git
   cd deepfake-detection-api-pretrained-models
   ```

2. Crea un entorno virtual e instala dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Coloca los modelos Xception en la carpeta:
   ```
   app/weights/xception/
   ```

   Los modelos pueden obtenerse desde:  
   - [Google Drive – Deepfake Detection Weights](https://drive.google.com/drive/folders/1GNtk3hLq6sUGZCGx8fFttvyNYH8nrQS8)

---

## ▶️ Ejecución

Ejecuta la API con `uvicorn`:

```bash
uvicorn app.main:app --reload
```

Abrirá la API en:
- Documentación interactiva Swagger → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternativa Redoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 Endpoints principales

### 🔹 HuggingFace
**POST** `/huggingface`  
Sube una imagen y devuelve predicción con el modelo HuggingFace.

Parámetros (form-data):
- `file`: Imagen (`.png`, `.jpg`, `.jpeg`)
- `recortar_cara`: `true/false` (opcional, default `false`)
- `device`: `"cpu"` o `"cuda"`

Ejemplo respuesta:
```json
{
  "result": {
    "real": 0.12,
    "fake": 0.88,
    "prediction": "fake"
  }
}
```

---

### 🔹 Xception – Pesos disponibles
**GET** `/xception/weights`  
Devuelve la lista de modelos disponibles en `app/weights/xception/`.

Ejemplo respuesta:
```json
{
  "available_models": [
    {
      "filename": "deepfake_c0_xception.pkl",
      "size_bytes": 83519096,
      "model_type": "xception"
    },
    {
      "filename": "ffpp_c23.pth",
      "size_bytes": 83519096,
      "model_type": "xception"
    }
  ]
}
```

---

### 🔹 Xception – Detección
**POST** `/xception/detect`  
Sube una imagen y selecciona un modelo Xception para predicción.

Parámetros (form-data):
- `file`: Imagen (`.png`, `.jpg`, `.jpeg`)
- `model_name`: Nombre del modelo en `app/weights/xception/` (ej. `deepfake_c0_xception.pkl`)
- `recortar_cara`: `true/false` (opcional)
- `device`: `"cpu"` o `"cuda"`

---

---

### 🔹 Recortar Cara – Detección
**POST** `/cut_face`  
Sube una imagen y se envía, te devuelve la imagen procesada.

Parámetros (form-data):
- `file`: Imagen (`.png`, `.jpg`, `.jpeg`)

---

## 📜 Créditos y fuentes

Este proyecto hace uso y adaptación de:
- Modelos de HuggingFace: [deepfake-detector-model-v1](https://huggingface.co/prithivMLmods/deepfake-detector-model-v1)  
- Pesos de Xception compartidos en: [Google Drive - HongguLiu/Deepfake-Detection](https://drive.google.com/drive/folders/1GNtk3hLq6sUGZCGx8fFttvyNYH8nrQS8)  
- Código base y arquitecturas de: [HongguLiu/Deepfake-Detection](https://github.com/HongguLiu/Deepfake-Detection)

---

## ⚖️ Licencia
Este proyecto se distribuye bajo la licencia **MIT**, pero los modelos y fragmentos de código mantienen la licencia original de sus autores.  
