# src/utils/data_processor.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os
from src import config 
import h5py # Necesario para simular guardar modelos Keras/TensorFlow

# --- Funciones de Carga, Agregación, y Entrenamiento (Simplificadas) ---

def load_data():
    """Carga los DataFrames necesarios para el ML Core."""
    try:
        # Usando rutas de config
        df_forraje = pd.read_csv(config.PATH_FORRAJE)
        df_vigor = pd.read_csv(config.PATH_VIGOR)
        df_utilizacion = pd.read_csv(config.PATH_UTILIZACION)
        return df_forraje, df_vigor, df_utilizacion
    except FileNotFoundError as e:
        print(f"Error: Archivo {os.path.basename(e.filename)} no encontrado en {config.RAW_DATA_PATH}.")
        return None, None, None

def aggregate_and_merge(df_forraje, df_vigor, df_utilizacion):
    """Agrega Fresh_weight, Vigor, y Utilización por unidad/fecha."""
    
    df_target = df_forraje.groupby(['Evaluation_unit', 'Date'])['Fresh_weight'].mean().reset_index()
    df_target.rename(columns={'Fresh_weight': 'Avg_Fresh_weight'}, inplace=True)

    df_vigor_agg = df_vigor.groupby(['Evaluation_unit', 'Date'])['Plant_vigor'].mean().reset_index()
    df_vigor_agg.rename(columns={'Plant_vigor': 'Avg_Plant_vigor'}, inplace=True)

    df_util_agg = df_utilizacion.groupby(['Evaluation_unit', 'Date'])['Utilization_degree'].mean().reset_index()
    df_util_agg.rename(columns={'Utilization_degree': 'Avg_Utilization_degree'}, inplace=True)

    df_ml = df_target.merge(df_vigor_agg, on=['Evaluation_unit', 'Date'], how='left')
    df_ml = df_ml.merge(df_util_agg, on=['Evaluation_unit', 'Date'], how='left')
    return df_ml

def preprocess_data(df_ml):
    # ... (Lógica de definir semáforo e imputación robusta, como se definió previamente) ...
    def define_semaforo(weight):
        if weight > 50: return 'Green'
        elif weight > 35: return 'Yellow'
        else: return 'Red'
    df_ml['Semáforo'] = df_ml['Avg_Fresh_weight'].apply(define_semaforo)

    df_ml['Avg_Plant_vigor'] = pd.to_numeric(df_ml['Avg_Plant_vigor'], errors='coerce')
    df_ml['Avg_Utilization_degree'] = pd.to_numeric(df_ml['Avg_Utilization_degree'], errors='coerce')
    
    for col in ['Avg_Plant_vigor', 'Avg_Utilization_degree']:
        col_mean = df_ml[col].mean()
        df_ml[col].fillna(col_mean if pd.notna(col_mean) else 0, inplace=True)
    
    df_ml.dropna(subset=['Avg_Fresh_weight', 'Semáforo'], inplace=True)

    X = df_ml[['Avg_Plant_vigor', 'Avg_Utilization_degree']]
    y = df_ml['Semáforo']
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    return X, y_encoded, le, df_ml

def train_and_save_all_models(X, y_encoded, le, df_ml):
    """Entrena y guarda los tres modelos del proyecto Ocko."""
    
    # ... (Lógica para entrenamiento de Random Forest (ML Core)) ...
    
    # 1. Guardar Artefactos del ML Core (Random Forest)
    os.makedirs(config.MODELS_PATH + '/core_tabular_ml', exist_ok=True)
    joblib.dump(model, config.MODELS_PATH + '/core_tabular_ml/random_forest_model.pkl')
    joblib.dump(le, config.MODELS_PATH + '/core_tabular_ml/label_encoder.pkl')

    # 2. Simular y Guardar Modelos No Tabulares (CNN y LSTM)
    os.makedirs(config.MODELS_PATH + '/non_tabular_ml', exist_ok=True)
    
    # Modelo 2: CNN para Reportes (Visión por Computadora)
    with h5py.File(config.MODELS_PATH + '/non_tabular_ml/cnn_report_classifier.h5', 'w') as f:
         f.attrs['model_type'] = 'CNN_Image_Classifier'

    # Modelo 3: LSTM para Clima (Series de Tiempo)
    with h5py.File(config.MODELS_PATH + '/non_tabular_ml/lstm_climate_predictor.h5', 'w') as f:
         f.attrs['model_type'] = 'LSTM_Time_Series'

    print(f"\n✅ Todos los modelos (RF, CNN, LSTM) y datos procesados guardados exitosamente.")

def train_and_save_model(X, y_encoded, le, df_ml):
    # ... (Lógica de entrenamiento y guardado en config.MODELS_PATH) ...
    if len(X) < 5:
        print("Advertencia: Muestras insuficientes para un entrenamiento fiable. Cancelando guardado.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)

    # Guardar Artefactos
    os.makedirs(config.PROCESSED_DATA_PATH, exist_ok=True)
    os.makedirs(config.MODELS_PATH, exist_ok=True)
    joblib.dump(model, config.MODEL_FILE)
    joblib.dump(le, config.LE_FILE)
    df_ml.to_csv(config.INDICATORS_FILE, index=False)
    print(f"\n✅ Modelos ML y datos procesados guardados exitosamente.")

def main():
    df_forraje, df_vigor, df_utilizacion = load_data()
    if df_forraje is None: return

    df_ml = aggregate_and_merge(df_forraje, df_vigor, df_utilizacion)
    if df_ml.empty: return

    X, y_encoded, le, df_ml_processed = preprocess_data(df_ml)
    train_and_save_model(X, y_encoded, le, df_ml_processed)

if __name__ == "__main__":
    main()