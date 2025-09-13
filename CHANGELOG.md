# 📑 CHANGELOG.md

## [2.0.0] - 2025-09-10
### 🚀 Added
- Nuevo endpoint `/ensemble/detect` para ejecutar **ensemble de modelos** (HuggingFace + todos los Xception disponibles).  
  - Devuelve decisiones basadas en **votación mayoritaria** y **promedio de probabilidades**.  
- Documentación más clara en los endpoints (`docstring` en cada ruta).  

### 🛠 Changed
- Respuestas de los endpoints ahora son **consistentes** usando modelos de Pydantic:
  - `ModelsResponse`
  - `AvailableModelsResponse`
  - `EnsembleResponse`
- En `xception/detect` ahora se debe enviar el nombre del peso disponible en `/xception/weights`.  
- `huggingface` y `xception` ya no devuelven `{"result": {...}}` sino directamente un objeto `ModelsResponse`.  

### 🐛 Fixed
- Error de compatibilidad CPU/GPU: ahora los modelos se cargan dinámicamente en el `device` correcto (`cpu` o `cuda`).  
- Bug de cacheo de pesos solucionado: no se rompe al alternar entre CPU y GPU en llamadas consecutivas.  

---

## [1.0.0] - 2025-09-01
### 🚀 Initial release
- Endpoint `/huggingface` para detección con modelo HuggingFace.  
- Endpoint `/xception/detect` para detección con pesos preentrenados de Xception.  
- Endpoint `/xception/weights` para listar modelos disponibles.  
- Endpoint `/cut_face` para recortar la cara de una imagen.  
