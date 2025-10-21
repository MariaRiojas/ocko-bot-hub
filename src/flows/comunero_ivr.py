# src/flows/comunero_ivr.py

from src.utils import api_handler
from src import config
# Importaciones de lógica específica (5 opciones)
from src.flows.logic_comunero import op1_pastos_ml
from src.flows.logic_comunero import op2_agua_clima
from src.flows.logic_comunero import op3_reporte_seq
from src.flows.logic_comunero import op4_consejos_context
from src.flows.logic_comunero import op5_emergencia 

# --- Persistencia de estado (GLOBAL para ambos IVR) ---
user_states = {} 
user_reports = {} 
STATE_AWAITING_CLIMA_OPTION = 'AWAIT_CLIMA_OPT'

def comunero_ivr(phone_number, user_input):
    """
    Función principal que dirige el flujo del Comunero (5 Opciones).
    """
    user_input = user_input.strip()
    
    if phone_number not in user_states:
        user_states[phone_number] = config.STATE_MENU
        
    # --- 1. Manejo de Estados Secuenciales (Opción 3: Reportes) ---
    if user_states[phone_number] not in [config.STATE_MENU, config.STATE_WAITING_ZONE]:
        response_text = op3_reporte_seq.handle_report_step(phone_number, user_input, user_states, user_reports)
        if response_text:
            api_handler.send_whatsapp_message(phone_number, response_text)
            return response_text
    
    # --- 2. Manejo del Menú Principal ---
    
    # Opciones de reinicio
    if user_input.lower() in ["hola", "menu", "0", "volver"]:
        user_states[phone_number] = config.STATE_MENU
        response_text = (
            "🌳 *Bienvenida a Ocko (Menú Principal)*\n"
            "1. Estado pastos (Predicción ML)\n"
            "2. Agua y clima\n"
            "3. Enviar reporte (Secuencial)\n"
            "4. Consejos prácticos\n"
            "5. Emergencia"
        )
    
    # Opción 1: Estado pastos (Solicita zona)
    elif user_input == "1":
        user_states[phone_number] = config.STATE_WAITING_ZONE
        response_text = "Por favor, ingresa el nombre de tu zona o unidad de evaluación (ej: TAM-18) para el pronóstico."
        
    # Lógica de la Opción 1: Recibe la zona
    elif user_states[phone_number] == config.STATE_WAITING_ZONE and user_input.upper().startswith(('TAM-', 'COMUNIDAD', 'ZONA')):
        user_states[phone_number] = config.STATE_MENU
        response_text = op1_pastos_ml.process_estado_pastos(user_input.upper())
        
    # Opción 2: Agua y clima (Muestra submenú)
    elif user_input == "2":
        user_states[phone_number] = STATE_AWAITING_CLIMA_OPTION # ⬅️ Establece el nuevo estado
        response_text = op2_agua_clima.get_sub_menu()
        
    # Lógica de la Opción 2: Recibe la sub-opción (1, 2, o 3)
    elif user_input in ["1", "2", "3"] and user_states[phone_number] == STATE_AWAITING_CLIMA_OPTION: # ⬅️ Solo procesa si estamos en el submenú de clima
         user_states[phone_number] = config.STATE_MENU # Vuelve al menú principal
         response_text = op2_agua_clima.process_agua_clima_data(user_input)
         
    # Opción 3: Enviar reporte (Inicia el flujo secuencial)
    elif user_input == "3":
        # Ahora esta opción será manejada correctamente porque no fue interceptada por la Opción 2
        response_text = op3_reporte_seq.start_report_flow(phone_number, user_states, user_reports)
        
    # Opción 4: Consejos prácticos
    elif user_input == "4":
        response_text = op4_consejos_context.process_consejos_practicos()
        
    # Opción 5: Emergencia
    elif user_input == "5":
        response_text = op5_emergencia.process_emergencia(phone_number)
        
    else:
        response_text = "Opción no válida. Ingresa el número de la opción o 'menu' para volver al inicio."

    api_handler.send_whatsapp_message(phone_number, response_text)
    return response_text