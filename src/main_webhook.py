import os
from dotenv import load_dotenv
from src.flows.comunero_ivr import comunero_ivr
from src.flows.especialista_ivr import especialista_ivr
from src.utils import data_loader

# Cargar variables de entorno
load_dotenv()

# --- Cargar Artefactos ML Globalmente ANTES de cualquier flujo IVR ---
# Esto asegura que los modelos estén cargados y que la función solo se llame una vez.
if data_loader.load_ml_artifacts():
    print("Sistema Ocko listo para enrutamiento.")
# Cargar variables de entorno

# --- Simulación de Identificación de Usuarios ---
# En una aplicación real, esto se haría consultando una base de datos de usuarios
# basada en el 'from' number del webhook de WhatsApp.

COMUNERO_PHONE = os.getenv("COMUNERO_PHONE", "51987654321") # Simulación de un número de Comunero
ESPECIALISTA_PHONE = os.getenv("ESPECIALISTA_PHONE", "51912345678") # Simulación de un número de Especialista

# Función principal que simula la recepción del Webhook de Meta
def main_webhook_handler(incoming_message):
    """
    Simula la recepción de un mensaje del API de Meta y enruta al IVR correcto.
    
    Args:
        incoming_message (dict): Simula el payload del webhook de WhatsApp.
    """
    
    # 1. Extracción de datos (simplificada)
    phone_number = incoming_message.get("from", "UNKNOWN")
    user_input = incoming_message.get("body", "").strip()
    
    if not user_input:
        return "Ignorando mensaje vacío."

    # 2. Enrutamiento basado en el número de teléfono (simulación del rol)
    if phone_number == ESPECIALISTA_PHONE:
        rol = "ESPECIALISTA"
        response = especialista_ivr(phone_number, user_input)
    elif phone_number == COMUNERO_PHONE:
        rol = "COMUNERO"
        response = comunero_ivr(phone_number, user_input)
    else:
        rol = "NUEVO/NO AUTORIZADO"
        response = "Lo siento, tu número no está registrado. Por favor, contacta al administrador de Ocko."

    print(f"\n[WEBHOOK] Mensaje de {rol} ({phone_number}): '{user_input}'")
    print(f"[WEBHOOK] Enrutado. Respuesta generada por {rol} IVR.")
    return response

if __name__ == "__main__":
    
    # 🚨 NOTA: Debes añadir estos números al archivo .env o usar los valores por defecto aquí.
    # Simulación de un mensaje entrante (Comunero)
    print("--- SIMULACIÓN DE RECEPCIÓN: COMUNERO ---")
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "hola"})
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "1"})
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "TAM-18"})

    # Simulación de un mensaje entrante (Especialista)
    print("\n--- SIMULACIÓN DE RECEPCIÓN: ESPECIALISTA ---")
    main_webhook_handler({"from": ESPECIALISTA_PHONE, "body": "tecnico"})
    main_webhook_handler({"from": ESPECIALISTA_PHONE, "body": "4"})