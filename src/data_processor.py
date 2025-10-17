import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

# --- Configuración de Rutas (Solución Final) ---

# Define la ruta base del proyecto a partir del script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')
MODELS_PATH = os.path.join(BASE_DIR, 'models')

# Archivos CSV necesarios para el ML (usando nombres cortos verificados)
PATH_DISPO_GRASS = os.path.join(RAW_DATA_PATH, 'Data_DispoGrass.csv')
PATH_PLANT_VIGOR = os.path.join(RAW_DATA_PATH, 'Data_PlantVigor.csv')
PATH_SPECIES_UTILIZATION = os.path.join(RAW_DATA_PATH, 'Data_SpeciesUtilization.csv')

# --- Funciones de Procesamiento ---

def load_data():
    """Carga los DataFrames necesarios para el ML."""
    
    # Bloque de Diagnóstico (temporalmente comentado para ejecución limpia)
    # print(f"Cargando desde: {RAW_DATA_PATH}")
    
    try:
        # Cargamos los archivos usando los nombres cortos verificados
        df_dispo_grass = pd.read_csv(PATH_DISPO_GRASS)
        df_plant_vigor = pd.read_csv(PATH_PLANT_VIGOR)
        df_species_util = pd.read_csv(PATH_SPECIES_UTILIZATION)
        return df_dispo_grass, df_plant_vigor, df_species_util
    except Exception as e:
        print(f"Error al cargar un archivo. Asegúrate de que los archivos 'Data_DispoGrass.csv', 'Data_PlantVigor.csv', y 'Data_SpeciesUtilization.csv' existen en la carpeta raw. Detalle: {e}")
        return None, None, None

def aggregate_and_merge(df_dispo_grass, df_plant_vigor, df_species_util):
    """Agrega y fusiona los datos para crear el conjunto de entrenamiento."""

    # 1. Target: Peso Fresco (Fresh_weight)
    df_target = df_dispo_grass.groupby(['Evaluation_unit', 'Date'])['Fresh_weight'].mean().reset_index()
    df_target.rename(columns={'Fresh_weight': 'Avg_Fresh_weight'}, inplace=True)

    # 2. Feature: Vigor de Plantas (Plant_vigor)
    df_vigor = df_plant_vigor.groupby(['Evaluation_unit', 'Date'])['Plant_vigor'].mean().reset_index()
    df_vigor.rename(columns={'Plant_vigor': 'Avg_Plant_vigor'}, inplace=True)

    # 3. Feature: Grado de Utilización (Utilization_degree)
    df_util = df_species_util.groupby(['Evaluation_unit', 'Date'])['Utilization_degree'].mean().reset_index()
    df_util.rename(columns={'Utilization_degree': 'Avg_Utilization_degree'}, inplace=True)

    # 4. Merge Flexible (Left Merge basado en el Target)
    df_ml = df_target.merge(df_vigor, on=['Evaluation_unit', 'Date'], how='left')
    df_ml = df_ml.merge(df_util, on=['Evaluation_unit', 'Date'], how='left')

    return df_ml

def preprocess_data(df_ml):
    """Define el Semáforo, maneja faltantes y prepara X e y."""

    def define_semaforo(weight):
        if weight > 50:
            return 'Green'
        elif weight > 35:
            return 'Yellow'
        else:
            return 'Red'

    df_ml['Semáforo'] = df_ml['Avg_Fresh_weight'].apply(define_semaforo)

    # --- INICIO SOLUCIÓN PARA NaN ---

    # Convertir a float (numérico) para asegurar la compatibilidad con el modelo
    df_ml['Avg_Plant_vigor'] = pd.to_numeric(df_ml['Avg_Plant_vigor'], errors='coerce')
    df_ml['Avg_Utilization_degree'] = pd.to_numeric(df_ml['Avg_Utilization_degree'], errors='coerce')
    
    # Imputación Robusta: Si la media de la columna es NaN (porque la columna es completamente NaN), 
    # imputamos con 0. De lo contrario, imputamos con la media.
    
    for col in ['Avg_Plant_vigor', 'Avg_Utilization_degree']:
        col_mean = df_ml[col].mean()
        
        # 1. Si la media es válida (no es NaN), usamos la media.
        if pd.notna(col_mean):
            df_ml[col].fillna(col_mean, inplace=True)
        
        # 2. Si la media es NaN (columna completamente vacía), usamos 0.
        else:
            df_ml[col].fillna(0, inplace=True)
            print(f"Advertencia: La columna '{col}' estaba vacía y se imputó con 0.")

    # Aseguramos que no queden NaN en las variables objetivo o peso fresco (ya que no se pueden predecir)
    df_ml.dropna(subset=['Avg_Fresh_weight', 'Semáforo'], inplace=True)

    # --- FIN SOLUCIÓN PARA NaN ---
    
    # Variables Predictoras (Features) y Variable Objetivo (Target)
    X = df_ml[['Avg_Plant_vigor', 'Avg_Utilization_degree']]
    y = df_ml['Semáforo']
    
    # Codificación de la variable objetivo
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    return X, y_encoded, le, df_ml

def train_and_save_model(X, y_encoded, le, df_ml):
    """Entrena el modelo, lo evalúa y guarda los resultados/modelo."""
    
    if len(X) < 5:
        print("Advertencia: Muestras insuficientes para un entrenamiento fiable.")
        return

    # Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Entrenamiento del modelo Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)

    # Evaluación
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)

    print("\n--- Resultados del Entrenamiento del Modelo Random Forest ---")
    print(f"Muestras de entrenamiento: {len(X_train)}")
    print("Reporte de Clasificación (Consola para el Especialista):")
    for label in le.classes_:
        print(f"  Clase {label}: Precisión={report[label]['precision']:.2f}, Recall={report[label]['recall']:.2f}, F1-Score={report[label]['f1-score']:.2f}")

    # Guardar Artefactos
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    os.makedirs(MODELS_PATH, exist_ok=True)
    
    df_ml.to_csv(os.path.join(PROCESSED_DATA_PATH, 'ML_Grassland_Indicators.csv'), index=False)
    print(f"\n✅ Datos procesados guardados en: {PROCESSED_DATA_PATH}")

    joblib.dump(model, os.path.join(MODELS_PATH, 'random_forest_model.pkl'))
    joblib.dump(le, os.path.join(MODELS_PATH, 'label_encoder.pkl'))
    print(f"✅ Modelo y codificador guardados en: {MODELS_PATH}")

def main():
    """Función principal para ejecutar todo el flujo."""
    df_dispo_grass, df_plant_vigor, df_species_util = load_data()
    
    if df_dispo_grass is None:
        return

    df_ml = aggregate_and_merge(df_dispo_grass, df_plant_vigor, df_species_util)
    
    if df_ml.empty:
        print("Error: No se pudieron fusionar los datos. El conjunto final está vacío.")
        return

    X, y_encoded, le, df_ml_processed = preprocess_data(df_ml)
    
    train_and_save_model(X, y_encoded, le, df_ml_processed)

if __name__ == "__main__":
    main()