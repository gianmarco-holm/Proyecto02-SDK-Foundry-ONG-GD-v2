# chat_client.py - Cliente de Azure AI Foundry
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import logging

# Intentar leer variables del entorno primero; si no existen, cargar config/.env
env_endpoint = os.getenv("AZURE_AI_ENDPOINT")
env_key = os.getenv("AZURE_AI_KEY")

if not env_endpoint or not env_key:
    # Intentar cargar archivo config/.env como respaldo (útil en desarrollo)
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

API_KEY = env_key or os.getenv("AZURE_AI_KEY")
ENDPOINT = env_endpoint or os.getenv("AZURE_AI_ENDPOINT")

def _strip_quotes(val: str | None) -> str | None:
    if not val:
        return val
    return val.strip().strip('"').strip("'")

API_KEY = _strip_quotes(API_KEY)
ENDPOINT = _strip_quotes(ENDPOINT)

# Por seguridad, no fallar en la importación: si faltan las variables, exponer client=None
if not API_KEY or not ENDPOINT:
    logging.warning("AZURE_AI_KEY o AZURE_AI_ENDPOINT no configurados. El cliente de Azure no estará disponible hasta configurar las variables de entorno.")
    client = None
else:
    # Normalizar endpoint si contiene /api/projects/
    if "/api/projects/" in ENDPOINT:
        ENDPOINT = ENDPOINT.split("/api/projects/")[0]

    client = ChatCompletionsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(API_KEY)
    )
