# src/flows/logic_comunero/op3_reporte_seq.py

from src import config
import pandas as pd
from src.utils import geo_handler
import numpy as np

CNN_REPORT_CLASSIFIER = True

def start_report_flow(phone_number, user_states, user_reports):
    """Opción 3: Inicia el flujo secuencial de reporte."""
    user_states[phone_number] = config.STATE_WAITING_REPORT_TYPE
    return "📸 Submenú Reporte: ¿Qué deseas reportar?\n1. Pastizal (foto)\n2. Problema (texto)"

def handle_report_step(phone_number, user_input, user_states, user_reports):
    """Procesa el mensaje del usuario: TIPO -> FOTO -> UBICACIÓN -> OBSERVACIÓN -> CONFIRMACIÓN."""
    current_state = user_states.get(phone_number)
    
    # Maneja mensajes de reinicio
    if user_input.lower() in ["cancelar", "menu"]:
        user_states[phone_number] = config.STATE_MENU
        return "Flujo de reporte cancelado. Volviendo al Menú Principal."

    # 1. PASO: TIPO DE REPORTE (Asegura la secuencia de 4 pasos para la Opción 1)
    if current_state == config.STATE_WAITING_REPORT_TYPE:
        if user_input == "1":
            user_states[phone_number] = config.STATE_WAITING_PHOTO
            user_reports[phone_number] = {'type': 'Foto Pastizal', 'location': 'Pendiente', 'obs': 'Pendiente'}
            return "✅ Reporte iniciado. Por favor, envíanos la **foto** del pastizal."
        
        elif user_input == "2":
            user_states[phone_number] = config.STATE_WAITING_OBSERVATION
            user_reports[phone_number] = {'type': 'Problema General', 'photo': 'N/A', 'location': 'N/A'}
            return "✅ Reporte iniciado. Por favor, describe brevemente tu **observación** o problema."

        return "Opción de reporte no válida. Selecciona 1 o 2."

    # 2. PASO: SOLICITA FOTO (Input es la foto/confirmación)
    elif current_state == config.STATE_WAITING_PHOTO:
        user_reports[phone_number]['photo'] = user_input # Guarda la referencia a la foto/texto
        user_states[phone_number] = config.STATE_WAITING_LOCATION
        # Va a Solicita ubicación
        return "📷 Foto recibida. Por favor, envíanos tu **ubicación GPS** o una descripción de tu localización."

    elif current_state == config.STATE_WAITING_LOCATION:
        user_reports[phone_number]['location'] = user_input
        
        # --- NUEVA LÓGICA DE CLASIFICACIÓN (RETROALIMENTA MODELO [P]) ---
        if 'Foto Pastizal' in user_reports[phone_number]['type'] and CNN_REPORT_CLASSIFIER:
            
            # 1. Simula el preprocesamiento
            image_tensor = geo_handler.process_image_for_cnn(user_reports[phone_number]['photo'])
            
            # 2. Simula la clasificación CNN
            clasificacion = np.random.choice(['Sobrepastoreo', 'Buen Vigor', 'Sequía Severa'])
            
            user_reports[phone_number]['cnn_class'] = clasificacion
            print(f"   [CNN CLASIFICADOR]: Imagen clasificada como: {clasificacion}")
            
        # ---------------------------------------------------------------------

        user_states[phone_number] = config.STATE_WAITING_OBSERVATION
        return "📍 Ubicación registrada. Finalmente, describe tu **observación** o el problema específico que viste."

    # 4. PASO: SOLICITA OBSERVACIÓN (FINAL) -> Confirma recepción [Q]
    elif current_state == config.STATE_WAITING_OBSERVATION:
        import pandas as pd
        report_id = f"RPT-{pd.Timestamp.now().year}-{len(user_reports) + 1}"
        # ... (Lógica de finalización) ...
        user_reports[phone_number]['observation'] = user_input

        print(f"   [Sistema]: Reporte N° {report_id} finalizado y enviado al especialista: {user_reports[phone_number]}")

        confirmacion = f"✅ ¡Gracias! Tu reporte N° **{report_id}** ha sido recibido.\n"
        if user_reports[phone_number].get('cnn_class'):
            confirmacion += f"Nuestra herramienta preliminar lo clasificó como: **{user_reports[phone_number]['cnn_class']}**."
            
        user_states[phone_number] = config.STATE_MENU
        return confirmacion
    
    return None