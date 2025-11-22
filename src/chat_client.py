# chat_client.py - Cliente de Azure AI Foundry
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Cargar configuración desde config/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

API_KEY = os.getenv("AZURE_AI_KEY")
ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")

# Eliminar comillas envolventes si existen (ej. "https://..." en .env)
def _strip_quotes(val: str | None) -> str | None:
    if not val:
        return val
    return val.strip().strip('"').strip("'")

API_KEY = _strip_quotes(API_KEY)
ENDPOINT = _strip_quotes(ENDPOINT)

if not API_KEY or not ENDPOINT:
    raise ValueError("Debes configurar AZURE_AI_KEY y AZURE_AI_ENDPOINT en tu archivo config/.env")

# Si el endpoint vino con /api/projects/... lo reducimos al base resource
if "/api/projects/" in ENDPOINT:
    ENDPOINT = ENDPOINT.split("/api/projects/")[0]

client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(API_KEY)
)
