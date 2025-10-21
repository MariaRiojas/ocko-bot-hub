# src/flows/logic_comunero/op1_pastos_ml.py
import pandas as pd
from src.utils import data_loader

def process_estado_pastos(zona):
    """Opción 1: Usa el modelo ML para predecir el estado del pastizal."""
    if data_loader.ML_MODEL is None:
        return f"Error interno: El modelo de predicción no está disponible. Reporte una emergencia (5)."

    # SIMULACIÓN DE DATOS NUEVOS
    vigor_predicho = 15  
    utilizacion_predicha = 15 
    
    new_data = pd.DataFrame({'Avg_Plant_vigor': [vigor_predicho], 'Avg_Utilization_degree': [utilizacion_predicha]})
    
    prediction_encoded = data_loader.ML_MODEL.predict(new_data)
    semaforo = data_loader.LABEL_ENCODER.inverse_transform(prediction_encoded)[0]
    
    # Lógica de Recomendación 
    if semaforo == 'Green':
        emoji = "🟢"
        recomendacion = "Sus pastos están saludables. Continúe con la rotación planificada."
    elif semaforo == 'Yellow':
        emoji = "🟡"
        recomendacion = "El sistema detecta riesgo. Monitoree de cerca la zona."
    else: # Red
        emoji = "🔴"
        recomendacion = "¡ALERTA CRÍTICA! Active la rotación inmediata y notifique al técnico."

    return (
        f"🌳 *ESTADO PASTOS (Zona: {zona})*\n"
        f"Semáforo Predictivo: **{semaforo}** {emoji}\n\n"
        f"📝 **Recomendación:** {recomendacion}"
    )