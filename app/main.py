from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.detect_deepfake_routes import router as deepfake_router

app = FastAPI(
    title="Deepfake Detection API",
    description="API para detectar si una imagen es real o fake",
    version="2.0.0"
)

# Configuración de CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Orígenes permitidos
    allow_credentials=True, # Si se están usando cookies o sesiones
    allow_methods=["*"], # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permitir todos los encabezados
)

# Incluir rutas
app.include_router(deepfake_router, prefix="/api")
