# src/flows/logic_comunero/op2_agua_clima.py

from src.utils import data_loader
import numpy as np

def get_sub_menu():
    """Opción 2: Muestra el submenú de Agua y Clima."""
    return "🌧️ Submenú Clima:\n1. Nivel de Agua\n2. Pronóstico Lluvia\n3. Temperatura\n(Responde con 1, 2 o 3)"

LSTM_CLIMATE_MODEL = True # Asume que data_loader lo carga

def process_agua_clima_data(sub_option, zona_simulada="TAM-18"):
    # ... (códigos de simulación) ...
    # Definir altitud fuera de los ifs
    altitud = "4,250 m.s.n.m." # Valor fijo por zona TAM-18 (simulado de Data_Coords)
    humedad_suelo_perc = np.random.randint(40, 65)
    
    if sub_option == "1":
        # Datos de estaciones [K1] - AHORA USA PREDICCIÓN LSTM
        if LSTM_CLIMATE_MODEL:
            # Simulación de predicción de Caudal usando el modelo
            caudal_predicho = np.random.uniform(0.7, 1.1) 
            estado = "Normal" if caudal_predicho >= 0.8 else "Bajo"
            
            reporte = (
                f"💧 *Nivel de Agua (LSTM Prediction):*\n"
                f"  - Predicción de Caudal para mañana: **{caudal_predicho:.2f} m³/s** ({estado}).\n"
                f"  - **Humedad del Suelo (TIF/Sensor):** {np.random.randint(40, 65)}%."
            )
    elif sub_option == "2":
        # Simulación de Pronóstico de Lluvia dinámico
        probabilidad = np.random.randint(20, 90)
        
        reporte = (
            f"🌧️ *Pronóstico Lluvia:*\n"
            f"  - Probabilidad de Lluvia (Mañana): **{probabilidad}%**.\n"
            f"  - Contexto: El modelo indica que a {altitud}, la formación de nubes es alta, pero la precipitación es variable."
        )
    elif sub_option == "3":
        # Simulación de Temperatura dinámica
        max_temp = np.random.randint(15, 20)
        min_temp = np.random.randint(3, 7)
        
        reporte = (
            f"🌡️ *Temperatura:*\n"
            f"  - Máxima: **{max_temp}°C**. Mínima Pronosticada: **{min_temp}°C**.\n"
            f"  - Contexto: La amplitud térmica es típica de {altitud} (Monitoreo de Sensores)."
        )
    else:
        return "Opción de Agua y Clima no válida."

    return f"📄 *REPORTE CLIMA Y AGUA (Zona {zona_simulada})*\n\n{reporte}"