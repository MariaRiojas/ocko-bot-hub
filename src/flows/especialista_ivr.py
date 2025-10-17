from src import config
import pandas as pd
from src.utils import api_handler # Solo importamos api_handler directamente
from src.utils import data_loader # Importamos data_loader como un objeto explícito
# --- Simulación de persistencia de estado (para submenús futuros) ---
especialista_states = {} # {phone_number: config.STATE_MENU}

# --- Lógica de la Opción 1: Alertas de Recuperación (ML) ---

def process_alertas_recuperacion():
    """
    Usa el DataFrame de Indicadores ML para identificar zonas en estado de alerta (Red/Yellow).
    """
    # Cargar artefactos para asegurar que los datos procesados están listos
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
    for index, row in alert_df.head(3).iterrows():
        semaforo = "🔴" if row['Semáforo'] == 'Red' else "🟡"
        zonas_criticas_info += (
            f"\n  - **{row['Evaluation_unit']}** ({semaforo}): Forraje {row['Avg_Fresh_weight']:.1f} kg/ha"
        )
    
    return (
        f"🚨 *RESUMEN DE ALERTAS DE RECUPERACIÓN*\n"
        f"🔴 **{red_count}** Zonas Críticas.\n"
        f"🟡 **{yellow_count}** Zonas de Monitoreo.\n\n"
        f"*Top 3 Zonas a Revisar:*{zonas_criticas_info}\n\n"
        "Acción: Ingrese el nombre de la zona para ver análisis detallado y recomendaciones."
    )

# --- Lógica de la Opción 4: Validar Predicciones (ML) ---

def process_validar_predicciones():
    """
    Informa sobre el estado del modelo ML, basándose en el balance de clases.
    """
    if data_loader.INDICATORS_DF.empty:
        return "Error: No se pudo acceder a los datos de indicadores. Ejecute data_processor.py."

    df = data_loader.INDICATORS_DF
    muestras = len(df)
    clases_distintas = df['Semáforo'].value_counts()
    
    # Lógica de Alerta de Validación
    if clases_distintas.count() < 3:
        alerta = "**URGENTE: ¡Datos Desbalanceados!**"
        recomendacion = ("Necesitamos urgentemente datos de campo (reportes manuales) que resulten en las clases 'Yellow' y 'Red' "
                         "para balancear el entrenamiento del modelo y evitar predicciones sesgadas.")
    else:
        alerta = "Normal, pero requiere monitoreo."
        recomendacion = "El modelo está en uso. Considere una revalidación manual si las predicciones satelitales son inconsistentes."

    reporte_clases = "\n".join([f"  - {clase}: {count}" for clase, count in clases_distintas.items()])
    
    return (
        f"📊 *VALIDACIÓN DEL MODELO DE PREDICCIÓN*\n"
        f"Estado Actual: {alerta}\n\n"
        f"Métricas del Dataset de Entrenamiento:\n"
        f" - Muestras Totales: {muestras}\n"
        f" - Distribución de Clases:{reporte_clases}\n\n"
        f"📝 **Recomendación:** {recomendacion}"
    )

# --- Función Principal del IVR Especialista ---

def especialista_ivr(phone_number, user_input):
    """
    Función principal que dirige el flujo del Especialista (Modo Técnico).
    """
    user_input = user_input.strip()
    
    # Opciones de reinicio
    if user_input.lower() in ["tecnico", "menu", "0", "volver"]:
        especialista_states[phone_number] = config.STATE_MENU
        response_text = (
            "🔬 *Modo Técnico (Especialista)*\n"
            "Selecciona una opción:\n"
            "1. Alertas de recuperación (ML)\n"
            "2. Mapas interactivos\n"
            "3. Reportes comunitarios\n"
            "4. Validar predicciones (ML)\n"
            "5. Configurar zonas\n"
            "6. Reporte automático"
        )
    
    # Opción 1: Alertas (ML)
    elif user_input == "1":
        response_text = process_alertas_recuperacion()
        
    # Opción 2: Mapas interactivos
    elif user_input == "2":
        response_text = "🔗 *Mapas:* Enviando enlace al sistema GEO-Viewer. (URL: https://geo.ocko.com/map/ID)"
        
    # Opción 3: Reportes comunitarios
    elif user_input == "3":
        # En la vida real, consultaría la tabla de reportes llenada por el comunero_ivr
        response_text = "📝 *Reportes:* Actualmente hay **3 reportes** no revisados del canal Comunero. ¿Desea ver detalles por número o zona?"
        
    # Opción 4: Validar predicciones (ML)
    elif user_input == "4":
        response_text = process_validar_predicciones()
        
    # Opción 5: Configurar zonas
    elif user_input == "5":
        response_text = "⚙️ *Configuración:* Ingrese el comando: CONFIG ZONA <NOMBRE> <COORDENADAS> o CONFIG VIGOR <UMBRAL> para ajustar el modelo."
        
    # Opción 6: Reporte automático
    elif user_input == "6":
        response_text = "📧 *Reporte Auto:* Generando y enviando el reporte semanal consolidado a gerencia. Finaliza flujo."

    else:
        response_text = "Opción de Especialista no válida. Ingrese el número o 'tecnico' para el menú."

    # Enviar la respuesta usando el handler simulado
    api_handler.send_whatsapp_message(phone_number, response_text)
    return response_text


if __name__ == "__main__":
    # --- SIMULACIÓN DIRECTA DEL IVR ---
    
    TEST_PHONE = "51912345678"

    print("\n\n=============== SIMULACIÓN: IVR Especialista COMPLETO ===============\n")
    
    # 1. Flujo Principal
    especialista_ivr(TEST_PHONE, "tecnico")
    
    # 2. Flujo 1: Alertas de Recuperación (ML)
    print("\n--- 1. FLUJO: ALERTAS (ML) ---")
    especialista_ivr(TEST_PHONE, "1")
    
    # 3. Flujo 4: Validar Predicciones (ML)
    print("\n--- 4. FLUJO: VALIDAR ML ---")
    especialista_ivr(TEST_PHONE, "4")
    
    # 4. Flujos de Gestión (2, 3, 5, 6)
    print("\n--- 2, 3, 5, 6: FLUJOS DE GESTIÓN ---")
    especialista_ivr(TEST_PHONE, "2")
    especialista_ivr(TEST_PHONE, "3")
    especialista_ivr(TEST_PHONE, "5")
    especialista_ivr(TEST_PHONE, "6")