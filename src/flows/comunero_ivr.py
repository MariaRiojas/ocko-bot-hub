from src.utils import api_handler, data_loader
from src import config
import pandas as pd
from src.utils import api_handler, data_loader
from src import config

# --- Simulación de persistencia de estado de usuario ---
# En una aplicación real (usando Flask/FastAPI), estos estados se guardarían en 
# una base de datos o en una caché (Redis) para cada número de teléfono.
user_states = {} # {phone_number: config.STATE_MENU}
user_reports = {} # {phone_number: {'type': '', 'obs': ''}}

# --- Lógica de la Opción 1 (ML) ---

def process_estado_pastos(zona):
    """Usa el modelo ML para predecir el estado del pastizal."""
    if data_loader.ML_MODEL is None:
        return f"Error interno: El modelo de predicción no está disponible. Intenta más tarde o reporta una emergencia (5)."

    # SIMULACIÓN DE DATOS NUEVOS (En un entorno real, esto vendría de una API)
    vigor_predicho = 15  # Valor Alto
    utilizacion_predicha = 15 # Valor Bajo
    
    new_data = pd.DataFrame({'Avg_Plant_vigor': [vigor_predicho], 'Avg_Utilization_degree': [utilizacion_predicha]})
    
    prediction_encoded = data_loader.ML_MODEL.predict(new_data)
    semaforo = data_loader.LABEL_ENCODER.inverse_transform(prediction_encoded)[0]
    
    # Lógica de Recomendación (ajustada a la predicción)
    if semaforo == 'Green':
        emoji = "🟢"
        recomendacion = "Sus pastos están saludables. ¡Excelente manejo! Continúe con la rotación planificada."
    elif semaforo == 'Yellow':
        emoji = "🟡"
        recomendacion = "El forraje es adecuado, pero el sistema detecta riesgo. Monitoree de cerca la zona."
    else: # Red
        emoji = "🔴"
        recomendacion = "¡ALERTA CRÍTICA! El pastizal muestra signos de degradación. Active la rotación inmediata y notifique al técnico."

    return (
        f"🌳 *ESTADO PASTOS (Zona: {zona})*\n"
        f"Semáforo Predictivo: **{semaforo}** {emoji}\n\n"
        f"📝 **Recomendación:** {recomendacion}"
    )

# --- Lógica de la Opción 2 (Agua y Clima) ---

def process_agua_clima(sub_option):
    """Maneja el submenú de Agua y Clima."""
    
    if sub_option == "1":
        return "🌧️ *Nivel de Lluvia:* Acumulado del último mes: 80 mm. Pronóstico: Lluvias ligeras esta semana. (Fuente: CONAGUA)."
    elif sub_option == "2":
        return "🌡️ *Temperatura y Viento:* Máx 18°C, Mín 5°C. Viento promedio 15 km/h. Se esperan cielos despejados."
    elif sub_option == "3":
        return "🌊 *Estado de Ríos:* El río [Nombre] presenta un caudal [Normal/Bajo]. No hay alerta de desborde."
    else:
        return "Opción de Agua y Clima no válida. Por favor, selecciona 1, 2 o 3."

# --- Lógica de la Opción 3 (Reporte Secuencial) ---

def process_reporte(phone_number, user_input):
    """Maneja el flujo secuencial de Envío de Reporte (Opción 3)."""
    
    current_state = user_states.get(phone_number, config.STATE_MENU)
    response_text = ""
    
    if current_state == config.STATE_MENU:
        # Inicio del flujo de reporte
        if user_input == "3":
            user_states[phone_number] = config.STATE_WAITING_REPORT_TYPE
            return "📸 Submenú Reporte:\n1. Pastizal (foto)\n2. Ubicación GPS\n3. Problema (texto)"

    elif current_state == config.STATE_WAITING_REPORT_TYPE:
        # El usuario seleccionó el tipo de reporte (1, 2, o 3)
        if user_input == "1":
            user_states[phone_number] = config.STATE_WAITING_PHOTO
            user_reports[phone_number] = {'type': 'Foto Pastizal'}
            return "Por favor, envíanos la **foto** del pastizal. Asegúrate de que se vea bien la zona."
        
        # Simulación de otros tipos de reporte
        elif user_input in ["2", "3"]:
            user_states[phone_number] = config.STATE_WAITING_OBSERVATION
            report_type = "Ubicación GPS" if user_input == "2" else "Problema General"
            user_reports[phone_number] = {'type': report_type}
            return f"Reporte tipo '{report_type}' seleccionado. Ahora, por favor, describe brevemente la **observación**."
        else:
            return "Opción no válida. Por favor, selecciona 1, 2 o 3 para el tipo de reporte."

    elif current_state == config.STATE_WAITING_PHOTO:
        # Asume que cualquier input aquí es la foto (o una confirmación de la foto)
        # En la vida real, se validaría el tipo de MIME (image/jpeg, etc.)
        
        # Simulación de guardar la foto y pasar al siguiente paso
        user_reports[phone_number]['photo'] = "RECEIVED" # Simula la recepción de la imagen
        user_states[phone_number] = config.STATE_WAITING_OBSERVATION
        return "✅ Foto recibida. Por favor, describe brevemente el **problema u observación** (ej: sobrepastoreo, sequía)."

    elif current_state == config.STATE_WAITING_OBSERVATION:
        # El usuario ingresa la descripción final
        report_id = f"RPT-{pd.Timestamp.now().year}-{len(user_reports) + 1}"
        
        # Guardar la observación y finalizar el reporte
        user_reports[phone_number]['observation'] = user_input
        
        # Aquí se enviaría el reporte completo al especialista o a una base de datos
        print(f"   [Sistema]: Reporte Finalizado: {user_reports[phone_number]}") 
        
        # Resetear el estado y volver al menú
        user_states[phone_number] = config.STATE_MENU
        return f"¡Gracias! Tu reporte N° **{report_id}** ha sido enviado al especialista. Volviendo al Menú Principal."

    return None # Si no está en un estado de reporte, devuelve None para continuar con el menú principal


# --- Función Principal del IVR Comunero ---

def comunero_ivr(phone_number, user_input):
    """
    Función principal que dirige el flujo del Comunero.
    Verifica el estado de la conversación antes de procesar el menú.
    """
    user_input = user_input.strip()
    
    # Inicializar el estado si es la primera vez
    if phone_number not in user_states:
        user_states[phone_number] = config.STATE_MENU
        
    # --- 1. Manejo de Estados Secuenciales (Reportes) ---
    # Intenta procesar el mensaje como parte de un flujo secuencial (ej. Reporte)
    if user_states[phone_number] != config.STATE_MENU:
        response_text = process_reporte(phone_number, user_input)
        if response_text:
            api_handler.send_whatsapp_message(phone_number, response_text)
            return response_text # El flujo secuencial ha manejado el mensaje
    
    # --- 2. Manejo del Menú Principal (Estado 'MENU') ---
    
    # Opciones de reinicio
    if user_input.lower() in ["hola", "menu", "0", "volver"]:
        user_states[phone_number] = config.STATE_MENU
        response_text = (
            "🌳 *Bienvenido a Ocko (Comunero)*\n"
            "Selecciona una opción:\n"
            "1. Estado de mis pastos (Predicción ML)\n"
            "2. Agua y clima\n"
            "3. Enviar reporte (Secuencial)\n"
            "4. Consejos prácticos\n"
            "5. Emergencia climática"
        )
    
    # Opción 1: Estado de mis pastos (ML)
    elif user_input == "1":
        user_states[phone_number] = config.STATE_WAITING_ZONE
        response_text = "Por favor, ingresa el nombre de tu zona o unidad de evaluación (ej: TAM-18, ComunidadA) para el pronóstico."
        
    # Lógica de la Opción 1: Recibe la zona
    elif user_states[phone_number] == config.STATE_WAITING_ZONE and user_input.upper().startswith(('TAM-', 'COMUNIDAD', 'ZONA')):
        user_states[phone_number] = config.STATE_MENU # Finaliza flujo de zona
        response_text = process_estado_pastos(user_input.upper())
        
    # Opción 2: Agua y clima (Submenú)
    elif user_input == "2":
        user_states[phone_number] = config.STATE_WAITING_REPORT_TYPE # Temporalmente usamos este estado para submenú
        response_text = process_agua_clima("sub_menu") # Pide el submenú
        
    # Lógica de la Opción 2: Recibe la sub-opción
    elif user_input in ["2.1", "2.2", "2.3"]: # Simulación de subopciones 1, 2, 3
         user_states[phone_number] = config.STATE_MENU
         response_text = process_agua_clima(user_input[-1]) # Pasa '1', '2' o '3'
         
    # Opción 3: Enviar reporte (Inicia el flujo secuencial, luego es manejado por process_reporte)
    elif user_input == "3":
        response_text = process_reporte(phone_number, user_input)
        
    # Opción 4: Consejos prácticos
    elif user_input == "4":
        response_text = ("💡 *Consejo de la Semana: Rotación.*\n"
                         "El vigor de la planta es clave. Evita el sobrepastoreo para maximizar el rebrote. "
                         "¿Deseas más detalles sobre manejo del forraje?")
        
    # Opción 5: Emergencia climática
    elif user_input == "5":
        response_text = "🚨 *EMERGENCIA CLIMÁTICA*: Conectando con el técnico de turno, espere un momento..."
        
    else:
        response_text = "Opción no válida. Por favor, ingresa el número de la opción o 'menu' para volver al inicio."

    # Si la respuesta se generó, la enviamos y la retornamos
    api_handler.send_whatsapp_message(phone_number, response_text)
    return response_text


if __name__ == "__main__":
    # --- SIMULACIÓN DIRECTA DEL IVR (Usada por main_webhook.py en un entorno real) ---
    
    TEST_PHONE = "51987654321"

    print("\n\n=============== SIMULACIÓN: IVR Comunero COMPLETO ===============\n")
    
    # 1. Flujo ML (Opción 1)
    print("--- 1. FLUJO: ESTADO PASTOS (ML) ---")
    comunero_ivr(TEST_PHONE, "hola")
    comunero_ivr(TEST_PHONE, "1")
    comunero_ivr(TEST_PHONE, "TAM-18")
    
    # 2. Flujo Agua y Clima (Opción 2)
    print("\n--- 2. FLUJO: AGUA Y CLIMA ---")
    comunero_ivr(TEST_PHONE, "2")
    comunero_ivr(TEST_PHONE, "2.1")
    
    # 3. Flujo Reporte Secuencial (Opción 3)
    print("\n--- 3. FLUJO: REPORTE SECUENCIAL ---")
    comunero_ivr(TEST_PHONE, "3") # Inicia
    comunero_ivr(TEST_PHONE, "1") # Tipo: Foto
    # Asume que aquí viene la foto
    comunero_ivr(TEST_PHONE, "archivo_de_foto.jpg") # Simula el envío de la foto
    comunero_ivr(TEST_PHONE, "Vi sobrepastoreo cerca del río en zona norte.") # Observación
    
    # 4. Opción directa (Opción 4)
    print("\n--- 4. FLUJO: CONSEJOS ---")
    comunero_ivr(TEST_PHONE, "4")