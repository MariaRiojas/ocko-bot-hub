# src/flows/logic_especialista/op4_validar_ml.py

from src.utils import data_loader

def process_validar_predicciones():
    """Opción 4: Reporte de Validación del Modelo (Enriquecido con referencias de suelo)."""
    
    if data_loader.INDICATORS_DF.empty:
        return "Error: No se pudo acceder a los datos de indicadores. Ejecute data_processor.py."

    df = data_loader.INDICATORS_DF
    muestras = len(df)
    clases_distintas = df['Semáforo'].value_counts()
    
    if clases_distintas.count() < 3:
        alerta = "**URGENTE: ¡Datos Desbalanceados!**"
        recomendacion = (
            "Necesitamos más muestras de campo para Yellow/Red.\n"
            "Priorice la recolección de datos de **Carbono Orgánico (Data_TOC)** y **Densidad Aparente (Data_Densidad)** "
            "para mejorar la precisión del modelo predictivo."
        )
    else:
        alerta = "Normal, pero requiere monitoreo."
        recomendacion = "El modelo está en uso. Valide las predicciones contrastando con mediciones recientes de **Altura de Referencia (Data_Alt_Ref)**."

    reporte_clases = "\n".join([f"  - {clase}: {count}" for clase, count in clases_distintas.items()])
    
    return (
        f"📊 *VALIDACIÓN DEL MODELO DE PREDICCIÓN*\n"
        f"Estado Actual: {alerta}\n"
        f"Muestras Totales: {muestras}\n"
        f"Distribución de Clases:\n{reporte_clases}\n\n"
        f"📝 **Recomendación:** {recomendacion}"
    )