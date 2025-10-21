# src/flows/logic_especialista/op5_config_zonas.py

def process_config_zonas():
    """Opción 5: Da instrucciones sobre la configuración de zonas (Enriquecido con referencias)."""
    
    return (
        "⚙️ *CONFIGURACIÓN DE ZONAS*\n"
        "Para agregar o modificar zonas:\n"
        "1. **Definición de Límites:** Utilice las **Coordenadas SERFOR (Data_Coords)** y las **Ubicaciones de Muestreo de Suelo (Data_Soil_Locs)** para establecer límites precisos.\n"
        "2. **Umbrales Ecológicos:** Las alertas (Semáforo) se basan en la **Altura de Referencia de Planta (Data_Alt_Ref)**. Si modifica los umbrales, asegúrese de usar datos validados.\n\n"
        "Comando de ejemplo: CONFIG ZONA TAM-19 ADD 123456N 789012E"
    )