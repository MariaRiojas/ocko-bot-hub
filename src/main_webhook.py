# src/main_webhook.py

import os
from dotenv import load_dotenv
from src.flows.comunero_ivr import comunero_ivr
from src.flows.especialista_ivr import especialista_ivr
from src.utils import data_loader 

# Cargar variables de entorno
load_dotenv()

# --- CARGAR ARTEFACTOS ML GLOBALMENTE ---
# Esto inicializa los modelos y datos para ambos IVR
data_loader.load_ml_artifacts() 
if data_loader.ML_MODEL is not None:
    print("✅ Sistema Ocko: Artefactos ML cargados. Listo para enrutamiento.")
# ----------------------------------------

# --- Simulación de Identificación de Usuarios ---
COMUNERO_PHONE = os.getenv("COMUNERO_PHONE", "51987654321")
ESPECIALISTA_PHONE = os.getenv("ESPECIALISTA_PHONE", "51912345678") 

def main_webhook_handler(incoming_message):
    """
    Función que simula el manejo del payload del webhook de Meta y enruta al IVR correcto.
    """
    
    phone_number = incoming_message.get("from", "UNKNOWN")
    user_input = incoming_message.get("body", "").strip()
    
    if not user_input:
        return "Ignorando mensaje vacío."

    # Enrutamiento basado en el número de teléfono
    if phone_number == ESPECIALISTA_PHONE:
        rol = "ESPECIALISTA"
        # Llama al IVR del Especialista
        response = especialista_ivr(phone_number, user_input)
    elif phone_number == COMUNERO_PHONE:
        rol = "COMUNERO"
        # Llama al IVR del Comunero
        response = comunero_ivr(phone_number, user_input)
    else:
        rol = "NUEVO/NO AUTORIZADO"
        response = "Lo siento, tu número no está registrado. Por favor, contacta al administrador de Ocko."

    print(f"\n[WEBHOOK] Mensaje de {rol} ({phone_number}): '{user_input}'")
    print(f"[WEBHOOK] Enrutado. Respuesta generada por {rol} IVR.")
    return response

if __name__ == "__main__":
    
    print("\n\n=============== INICIO SIMULACIÓN WEBHOOK OCKO ===============\n")
    
    # 1. Simulación de Flujo Comunero Completo
    print("--- 1. SIMULACIÓN: FLUJO COMUNERO (Predicción y Reporte Secuencial) ---")
    
    # Menú
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "hola"})
    
    # Opción 1: Predicción ML
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "1"})
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "TAM-18"})
    
    # Opción 3: Inicio de Reporte Secuencial
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "3"})
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "1"}) # Tipo: Foto
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "foto_del_pasto.png"}) # Paso 2: Foto
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "UTM 18S 345678"}) # Paso 3: Ubicación
    main_webhook_handler({"from": COMUNERO_PHONE, "body": "Hay mucho ganado y poco forraje."}) # Paso 4: Observación (Finaliza)

    # 2. Simulación de Flujo Especialista
    print("\n--- 2. SIMULACIÓN: FLUJO ESPECIALISTA (Gestión y Validación) ---")
    
    # Menú
    main_webhook_handler({"from": ESPECIALISTA_PHONE, "body": "tecnico"})
    
    # Opción 1: Alertas
    main_webhook_handler({"from": ESPECIALISTA_PHONE, "body": "1"})
    
    # Opción 4: Validar ML
    main_webhook_handler({"from": ESPECIALISTA_PHONE, "body": "4"})