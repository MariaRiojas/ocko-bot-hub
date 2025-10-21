# src/flows/especialista_ivr.py

from src.utils import api_handler
from src import config
# Importaciones de lógica específica (6 opciones)
from src.flows.logic_especialista import op1_alertas_ml
from src.flows.logic_especialista import op2_mapas_link
from src.flows.logic_especialista import op3_reportes_summary
from src.flows.logic_especialista import op4_validar_ml
from src.flows.logic_especialista import op5_config_zonas
from src.flows.logic_especialista import op6_reporte_auto

# --- Persistencia de estado (Reusa el estado global) ---
# En un sistema real, el estado se cargaría desde una DB/cache
especialista_states = {} 

def especialista_ivr(phone_number, user_input):
    """
    Función principal que dirige el flujo del Especialista (6 Opciones).
    """
    user_input = user_input.strip()
    
    if phone_number not in especialista_states:
        especialista_states[phone_number] = config.STATE_ESPECIALISTA_MENU
        
    # Opciones de reinicio
    if user_input.lower() in ["tecnico", "menu", "0", "volver"]:
        especialista_states[phone_number] = config.STATE_ESPECIALISTA_MENU
        response_text = (
            "🔬 *Modo Técnico (Menú Principal)*\n"
            "1. Alertas | 2. Mapas | 3. Reportes\n"
            "4. Validar | 5. Configurar | 6. Reporte auto\n"
            "(Responde con el número de la opción.)"
        )
    
    # Delegación de lógica a los módulos específicos (1-6)
    elif user_input == "1":
        response_text = op1_alertas_ml.process_alertas_recuperacion()
        
    elif user_input == "2":
        response_text = op2_mapas_link.process_mapas_link()
        
    elif user_input == "3":
        response_text = op3_reportes_summary.process_reportes_summary()
        
    elif user_input == "4":
        response_text = op4_validar_ml.process_validar_predicciones()
        
    elif user_input == "5":
        response_text = op5_config_zonas.process_config_zonas()
        
    elif user_input == "6":
        response_text = op6_reporte_auto.process_reporte_auto()

    else:
        response_text = "Opción de Especialista no válida. Ingrese el número o 'tecnico' para el menú."

    api_handler.send_whatsapp_message(phone_number, response_text)
    return response_text