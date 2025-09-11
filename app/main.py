from fastapi import FastAPI
from app.routes.detect_deepfake_routes import router as deepfake_router

app = FastAPI(
    title="Deepfake Detection API",
    description="API para detectar si una imagen es real o fake",
    version="2.0.0"
)

# Incluir rutas
app.include_router(deepfake_router, prefix="/api")
