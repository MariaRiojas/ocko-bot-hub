# src/utils/api_handler.py
import os
from dotenv import load_dotenv

load_dotenv()
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "SIMULATED_TOKEN")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "https://graph.whatsapp.com/v17.0/PHONE_ID/messages")

def send_whatsapp_message(recipient_number, message_body):
    """
    SIMULA el envío de un mensaje de texto a través de la API de WhatsApp.
    """
    print(f"   [API SIMULADA]: Mensaje enviado a {recipient_number[:5]}... Contenido: {message_body[:50]}...")
    return 200