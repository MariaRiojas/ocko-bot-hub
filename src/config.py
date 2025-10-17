import os

# Define la ruta base del proyecto a partir del script de configuración
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

# Rutas de Artefactos ML
MODELS_PATH = os.path.join(BASE_DIR, 'models')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')

MODEL_FILE = os.path.join(MODELS_PATH, 'random_forest_model.pkl')
LE_FILE = os.path.join(MODELS_PATH, 'label_encoder.pkl')
INDICATORS_FILE = os.path.join(PROCESSED_DATA_PATH, 'ML_Grassland_Indicators.csv')

# Estados de la Conversación (Necesario para el flujo de reportes)
STATE_MENU = 'MENU'
STATE_WAITING_ZONE = 'WAIT_ZONE'
STATE_WAITING_REPORT_TYPE = 'WAIT_RPT_TYPE'
STATE_WAITING_PHOTO = 'WAIT_PHOTO'
STATE_WAITING_OBSERVATION = 'WAIT_OBS'