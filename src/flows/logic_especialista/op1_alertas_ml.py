# src/flows/logic_especialista/op1_alertas_ml.py

from src.utils import data_loader

def process_alertas_recuperacion():
    """Opción 1: Muestra alertas críticas (Red/Yellow) basadas en el ML."""
    
    if data_loader.INDICATORS_DF.empty:
        return "Error: No hay datos de indicadores procesados. Ejecute data_processor.py."

    df = data_loader.INDICATORS_DF.copy()

    # Identificar alertas críticas o de monitoreo
    alert_df = df[df['Semáforo'].isin(['Red', 'Yellow'])].sort_values(by='Avg_Fresh_weight', ascending=True)
    
    if alert_df.empty:
        return "✅ No hay alertas críticas (🔴) o medias (🟡) activas en las unidades evaluadas."
    
    red_count = (alert_df['Semáforo'] == 'Red').count()
    yellow_count = (alert_df['Semáforo'] == 'Yellow').count()
    
    # Detalle de las 3 zonas más críticas
    zonas_criticas_info = ""
    for _, row in alert_df.head(3).iterrows():
        semaforo = "🔴" if row['Semáforo'] == 'Red' else "🟡"
        zonas_criticas_info += (
            f"\n  - **{row['Evaluation_unit']}** ({semaforo}): Forraje {row['Avg_Fresh_weight']:.1f} kg/ha"
        )
    
    return (
        f"🚨 *RESUMEN DE ALERTAS DE RECUPERACIÓN*\n"
        f"🔴 **{red_count}** Zonas Críticas.\n"
        f"🟡 **{yellow_count}** Zonas de Monitoreo.\n\n"
        f"*Top 3 Zonas a Revisar:*{zonas_criticas_info}\n"
        "Acción: Ingrese el nombre de la zona para ver análisis detallado y recomendaciones."
    )