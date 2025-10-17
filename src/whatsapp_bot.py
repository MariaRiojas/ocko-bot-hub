import os
import joblib
import pandas as pd
from dotenv import load_dotenv

# --- Configuración de Entorno y Rutas ---
load_dotenv()

# Credenciales del API de WhatsApp (Simuladas con Variables de Entorno)
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "SIMULATED_TOKEN")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "https://graph.whatsapp.com/v17.0/PHONE_ID/messages")
TEST_PHONE_ID = os.getenv("TEST_PHONE_ID", "1234567890") # ID del número de WhatsApp

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
MODELS_PATH = os.path.join(BASE_DIR, '..', 'models')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'processed')

MODEL_FILE = os.path.join(MODELS_PATH, 'random_forest_model.pkl')
LE_FILE = os.path.join(MODELS_PATH, 'label_encoder.pkl')
INDICATORS_FILE = os.path.join(PROCESSED_DATA_PATH, 'ML_Grassland_Indicators.csv')

# --- 1. Carga de Modelo y Datos ---

try:
    ML_MODEL = joblib.load(MODEL_FILE)
    LABEL_ENCODER = joblib.load(LE_FILE)
    INDICATORS_DF = pd.read_csv(INDICATORS_FILE)
    print("✅ Modelos ML e Indicadores cargados correctamente.")
except Exception as e:
    print(f"❌ Error al cargar artefactos de ML. Detalle: {e}")
    ML_MODEL = None
    LABEL_ENCODER = None
    INDICATORS_DF = pd.DataFrame()


# --- 2. Lógica de Comunicación de WhatsApp (Simulada) ---

def send_whatsapp_message(recipient_number, message_body):
    """
    SIMULA el envío de un mensaje de texto a través de la API de WhatsApp Business Cloud.
    
    En una implementación real, esta función usaría la librería 'requests' para enviar 
    una petición POST al WHATSAPP_API_URL con el token y el payload JSON.
    """
    
    # 🚨 NOTA: Esta es una SIMULACIÓN. Para un entorno real, usarías:
    # import requests
    # headers = {'Authorization': f'Bearer {WHATSAPP_API_TOKEN}', 'Content-Type': 'application/json'}
    # data = {
    #     "messaging_product": "whatsapp",
    #     "to": recipient_number,
    #     "type": "text",
    #     "text": {"body": message_body}
    # }
    # response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
    # return response.status_code

    # Simulando el éxito:
    print(f"   [API SIMULADA]: Mensaje enviado al número {recipient_number[:5]}... con el token OK.")
    return 200 # Retorna un código de estado 200 (Éxito)

# --- 3. Funciones de Flujo (Comunero) ---

def comunero_menu(user_input, phone_number):
    """Maneja el flujo del comunero y usa la API para enviar la respuesta."""
    
    # ... (El cuerpo de la función 'comunero_menu' es el mismo que antes, pero con 'phone_number' como argumento) ...
    # Menú Principal
    if user_input.lower() in ["hola", "menu", "0"]:
        response_text = (
            "🌳 *Bienvenido a Ocko (Comunero)*\n"
            "Selecciona una opción:\n"
            "1. Estado de mis pastos\n"
            "2. Agua y clima\n"
            "3. Enviar reporte\n"
            "4. Consejos prácticos\n"
            "5. Emergencia climática"
        )
    
    # 1. Estado de mis pastos 
    elif user_input == "1":
        response_text = "Por favor, ingresa el nombre de tu zona o unidad de evaluación (ej: TAM-18, ComunidadA) para el pronóstico."
        
    elif user_input.upper().startswith(('TAM-', 'COMUNIDAD')): # Asume que el input es la zona
        zona = user_input.upper()
        response_text = process_estado_pastos(zona)

    # 4. Consejos prácticos (Simulación)
    elif user_input == "4":
        response_text = ("💡 *Consejo de la Semana: Rotación.*\n"
                "Dado el vigor promedio, es un buen momento para planificar el siguiente ciclo de rotación. "
                "Permite un descanso de 60 días a las áreas utilizadas. ¿Deseas más detalles sobre manejo del forraje?")
        
    # El resto de las opciones simulan la continuación del flujo
    elif user_input == "2":
        response_text = "🌧️ Submenú Agua y Clima: ¿Deseas ver información de lluvia, temperatura o disponibilidad de agua?"
    elif user_input == "3":
        response_text = "📸 Submenú Reporte: ¿Qué tipo de reporte deseas enviar? (1. Foto, 2. Ubicación, 3. Problema general)"
    elif user_input == "5":
        response_text = "🚨 *EMERGENCIA CLIMÁTICA*: Conectando con el técnico de turno..."

    else:
        response_text = "Opción no válida. Por favor, ingresa el número de la opción o 'menu' para volver al inicio."
    
    # Enviamos la respuesta simulando el uso del API
    send_whatsapp_message(phone_number, response_text)
    return response_text # Retornamos el texto para la simulación de consola

# ... (La función 'process_estado_pastos' es la misma que antes) ...
def process_estado_pastos(zona):
    # ... (El cuerpo de la función sigue siendo el mismo) ...
    if ML_MODEL is None:
        return f"Error interno: El modelo de predicción no está disponible. Intenta más tarde o reporta una emergencia (5)."

    # --- SIMULACIÓN DE DATOS NUEVOS PARA LA ZONA ---
    vigor_predicho = 15
    utilizacion_predicha = 15
    
    # Creamos el DataFrame para la predicción
    new_data = pd.DataFrame({
        'Avg_Plant_vigor': [vigor_predicho], 
        'Avg_Utilization_degree': [utilizacion_predicha]
    })
    
    # Predicción del Modelo ML
    prediction_encoded = ML_MODEL.predict(new_data)
    semaforo = LABEL_ENCODER.inverse_transform(prediction_encoded)[0]
    
    # Lógica de Recomendación Basada en la Predicción
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
        f"Modelo Predictivo (ML) basado en vigor y utilización:\n"
        f"  - Vigor Detectado: {vigor_predicho}\n"
        f"  - Utilización: {utilizacion_predicha}\n\n"
        f"📝 **Recomendación:** {recomendacion}"
    )


# --- 4. Funciones de Flujo (Especialista) ---

def especialista_menu(user_input, phone_number):
    """Maneja el flujo del especialista y usa la API para enviar la respuesta."""
    
    # ... (El cuerpo de la función 'especialista_menu' es el mismo que antes, con 'phone_number') ...
    if user_input.lower() in ["tecnico", "menu", "0"]:
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

    # 1. Alertas de recuperación 
    elif user_input == "1":
        response_text = process_alertas_recuperacion()
    
    # 4. Validar predicciones 
    elif user_input == "4":
        response_text = process_validar_predicciones()

    # El resto de las opciones simulan la continuación del flujo
    elif user_input == "2":
        response_text = "🔗 *Mapas:* Enlace enviado a tu correo. (Simulación: Enlace a GEO-Viewer aquí)"
    elif user_input == "3":
        response_text = "📝 *Reportes:* Hay 3 reportes pendientes de la última semana. ¿Desea ver detalles por número?"
    elif user_input == "5":
        response_text = "⚙️ *Configuración:* Para agregar/modificar zonas, ingrese el comando: CONFIG ZONA <NOMBRE> <COORDENADAS>."
    elif user_input == "6":
        response_text = "📧 *Reporte Auto:* Reporte semanal generado y enviado al correo del equipo. Finaliza flujo."

    else:
        response_text = "Opción de Especialista no válida. Ingrese el número o 'tecnico'."

    # Enviamos la respuesta simulando el uso del API
    send_whatsapp_message(phone_number, response_text)
    return response_text # Retornamos el texto para la simulación de consola

# ... (Las funciones 'process_alertas_recuperacion' y 'process_validar_predicciones' son las mismas que antes) ...
def process_alertas_recuperacion():
    # ... (Cuerpo igual) ...
    if INDICATORS_DF.empty:
        return "Error: No hay datos de indicadores procesados para generar alertas."

    alert_df = INDICATORS_DF[INDICATORS_DF['Semáforo'].isin(['Red', 'Yellow'])]
    
    if alert_df.empty:
        return "✅ No hay alertas críticas (🔴) o medias (🟡) activas en las unidades evaluadas."
    
    red_count = (alert_df['Semáforo'] == 'Red').sum()
    yellow_count = (alert_df['Semáforo'] == 'Yellow').sum()
    
    zonas_criticas = alert_df[alert_df['Semáforo'] == 'Red']['Evaluation_unit'].unique()
    zonas_list = ', '.join(zonas_criticas[:5])

    return (
        f"🚨 *ALERTAS DE RECUPERACIÓN*\n"
        f"🔴 **{red_count}** Zonas Críticas (Red).\n"
        f"🟡 **{yellow_count}** Zonas de Monitoreo (Yellow).\n\n"
        f"Zonas 🔴: {zonas_list}{'...' if len(zonas_criticas) > 5 else ''}\n"
        "Acción: Ingrese una zona para ver análisis detallado y recomendaciones."
    )

def process_validar_predicciones():
    # ... (Cuerpo igual) ...
    muestras = len(INDICATORS_DF)
    clases_unicas = INDICATORS_DF['Semáforo'].nunique()

    return (
        f"📊 *VALIDACIÓN DE PREDICCIONES*\n"
        f"Estado del modelo: **Requiere Validación Urgente**\n\n"
        f"Detalles:\n"
        f" - Muestras Totales: {muestras}\n"
        f" - Clases de Semáforo encontradas: {clases_unicas} (El modelo entrenó solo en {clases_unicas} clases).\n"
        "Recomendación: Necesitamos datos de campo para las clases faltantes (Yellow/Red) "
        "para evitar sesgos en la predicción. Priorice la validación en zonas de baja disponibilidad."
    )


# --- 5. Función de Simulación del Bot ---

def run_bot_simulation(rol, mensaje, phone_number):
    """Función que dirige el flujo al Comunero o Especialista y simula la respuesta."""
    print(f"\n[{rol.upper()} - {phone_number}]: Mensaje entrante: '{mensaje}'")
    
    if rol.lower() == 'comunero':
        response = comunero_menu(mensaje, phone_number)
    elif rol.lower() == 'especialista':
        response = especialista_menu(mensaje, phone_number)
    else:
        response = "Rol no reconocido. Ingrese 'comunero' o 'especialista' para iniciar."
        
    print(f"[{rol.upper()}]: Respuesta saliente (Contenido):\n{response}")
    return response

if __name__ == "__main__":
    
    # ⚠️ ASEGÚRATE DE TENER EL ARCHIVO .env CON LAS VARIABLES ANTES DE USAR ESTA SECCIÓN
    COMUNERO_PHONE = "51987654321" # Número de prueba simulado para el comunero
    ESPECIALISTA_PHONE = "51912345678" # Número de prueba simulado para el especialista

    print("\n\n=============== INICIO SIMULACIÓN OCKO BOT (CON API WHATSAPP SIMULADA) ===============\n")

    # 1. Flujo Comunero
    run_bot_simulation("comunero", "hola", COMUNERO_PHONE)
    run_bot_simulation("comunero", "1", COMUNERO_PHONE)
    run_bot_simulation("comunero", "TAM-18", COMUNERO_PHONE) # Usa el modelo ML
    run_bot_simulation("comunero", "5", COMUNERO_PHONE) # Emergencia

    print("\n----------------------------------------------------")

    # 2. Flujo Especialista
    run_bot_simulation("especialista", "tecnico", ESPECIALISTA_PHONE)
    run_bot_simulation("especialista", "4", ESPECIALISTA_PHONE) # Validar Predicciones (ML)
    run_bot_simulation("especialista", "6", ESPECIALISTA_PHONE) # Reporte auto