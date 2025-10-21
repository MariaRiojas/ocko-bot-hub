import os

# Define la ruta base del proyecto a partir del script de configuración
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

# Rutas de Artefactos ML y Procesados
MODELS_PATH = os.path.join(BASE_DIR, 'models')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')

MODEL_FILE = os.path.join(MODELS_PATH, 'random_forest_model.pkl')
LE_FILE = os.path.join(MODELS_PATH, 'label_encoder.pkl')
INDICATORS_FILE = os.path.join(PROCESSED_DATA_PATH, 'ML_Grassland_Indicators.csv')
STATE_AWAITING_CLIMA_OPTION = 'AWAIT_CLIMA_OPT'

# --- RUTAS DE ARCHIVOS RAW (USANDO NOMBRES SIMPLIFICADOS) ---
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'tabular') 

# Archivos usados por el ML Core y Flujos
PATH_FORRAJE = os.path.join(RAW_DATA_PATH, 'Data_DispoGrass.csv')          # 04 DispoGrass
PATH_VIGOR = os.path.join(RAW_DATA_PATH, 'Data_PlantVigor.csv')              # 06 PlantVigor
PATH_UTILIZACION = os.path.join(RAW_DATA_PATH, 'Data_SpeciesUtilization.csv')  # 07 SpeciesUtilization

# Archivos de Referencia y Contexto
PATH_COORDS = os.path.join(RAW_DATA_PATH, 'Data_Coords.csv')            # Data_CoordCondition-SERFOR
PATH_ALT_REF = os.path.join(RAW_DATA_PATH, 'Data_Alt_Ref.csv')          # 03 Reference Height
PATH_SOIL_LOCS = os.path.join(RAW_DATA_PATH, 'Data_Soil_Locs.csv')      # Soil Sampling Locations
PATH_DENSITY = os.path.join(RAW_DATA_PATH, 'Data_Densidad.csv')         # 01 Bulk Density
PATH_TOC = os.path.join(RAW_DATA_PATH, 'Data_TOC.csv')                  # 01 Total Organic Carbon

# Estados de la Conversación
STATE_MENU = 'MENU'
STATE_WAITING_ZONE = 'WAIT_ZONE'
STATE_WAITING_REPORT_TYPE = 'WAIT_RPT_TYPE'
STATE_WAITING_PHOTO = 'WAIT_PHOTO'
STATE_WAITING_LOCATION = 'WAIT_LOC'
STATE_WAITING_OBSERVATION = 'WAIT_OBS'
STATE_ESPECIALISTA_MENU = 'ESPECIALISTA_MENU'