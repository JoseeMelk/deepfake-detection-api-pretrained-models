import os

BASE_WEIGHTS_DIR = os.path.join("app", "weights")

def list_available_models(model_type: str):
    """
    Lista los pesos disponibles para un tipo de modelo específico.
    Devuelve una lista de diccionarios con info de cada modelo.
    """
    model_dir = os.path.join(BASE_WEIGHTS_DIR, model_type)

    if not os.path.exists(model_dir):
        return None  # Si no existe la carpeta, devolvemos None

    models = []
    for fname in os.listdir(model_dir):
        fpath = os.path.join(model_dir, fname)

        # 🔹 Ignorar archivos ocultos y de git
        if fname.startswith(".") or fname.lower().startswith("git"):
            continue

        if os.path.isfile(fpath):
            models.append({
                "filename": fname,
                "size_bytes": os.path.getsize(fpath),
                "model_type": model_type
            })
    return models