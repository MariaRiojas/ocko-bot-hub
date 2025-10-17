# src/utils/data_loader.py

import joblib
import pandas as pd
from src import config
import warnings
# Suprimimos la advertencia si el DF está vacío y se carga
warnings.filterwarnings("ignore", category=UserWarning) 

ML_MODEL = None
LABEL_ENCODER = None
INDICATORS_DF = pd.DataFrame() # Inicia vacío

def load_ml_artifacts():
    """Carga los modelos ML y los datos procesados bajo demanda."""
    global ML_MODEL, LABEL_ENCODER, INDICATORS_DF
    
    # 1. Ya cargado, salir para evitar recarga
    if ML_MODEL is not None and not INDICATORS_DF.empty:
        return True

    try:
        ML_MODEL = joblib.load(config.MODEL_FILE)
        LABEL_ENCODER = joblib.load(config.LE_FILE)
        INDICATORS_DF = pd.read_csv(config.INDICATORS_FILE)
        print("✅ Artefactos ML cargados exitosamente por load_ml_artifacts().")
        return True
    except Exception as e:
        print(f"❌ ERROR CRÍTICO al cargar artefactos ML. Detalle: {e}")
        ML_MODEL = None
        LABEL_ENCODER = None
        INDICATORS_DF = pd.DataFrame()
        return False