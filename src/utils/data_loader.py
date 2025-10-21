# src/utils/data_loader.py
import joblib
import pandas as pd
from src import config
import warnings

warnings.filterwarnings("ignore", category=UserWarning) 

# Variables Globales (Contenedores)
ML_MODEL = None
LABEL_ENCODER = None
INDICATORS_DF = pd.DataFrame() # Contiene los datos procesados para el Especialista

def load_ml_artifacts():
    """Carga los modelos ML y los datos procesados bajo demanda (Lazy Loading)."""
    global ML_MODEL, LABEL_ENCODER, INDICATORS_DF
    
    # Si ya está cargado, no hacer nada
    if ML_MODEL is not None and not INDICATORS_DF.empty:
        return True

    try:
        # Carga de artefactos ML
        ML_MODEL = joblib.load(config.MODEL_FILE)
        LABEL_ENCODER = joblib.load(config.LE_FILE)
        INDICATORS_DF = pd.read_csv(config.INDICATORS_FILE)
        
        print("✅ Artefactos ML cargados exitosamente.")
        return True
    except Exception as e:
        print(f"❌ ERROR CRÍTICO al cargar artefactos ML. Asegúrese de ejecutar data_processor.py. Detalle: {e}")
        ML_MODEL = None
        LABEL_ENCODER = None
        INDICATORS_DF = pd.DataFrame()
        return False