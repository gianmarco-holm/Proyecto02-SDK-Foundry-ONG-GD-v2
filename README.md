# 🌱 Green Dream RAG Assistant

Servicio backend (API) para la integración del asistente virtual de Green Dream ONG.
Este proyecto implementa un asistente RAG (Retrieval-Augmented Generation) que combina búsqueda en una base de conocimiento local con un modelo de Azure AI Foundry.

**Resumen rápido:**

- **Qué es:** API REST que responde consultas de chat enriquecidas con contexto RAG.
- **Objetivo:** Servir como backend para incrustar un chat en una página web externa.
- **Tecnologías:** Python, Flask, Azure AI Foundry, Docker, Gunicorn.

## **Arquitectura**

```sh
repo-root/
├── src/                  # Código fuente
│   ├── api_complete.py   # App Flask (entrypoint: `app`)
│   ├── assistant_rag.py  # Lógica del asistente + RAG
│   ├── chat_client.py    # Cliente Azure AI Foundry (lee AZURE_AI_* desde env o config/.env)
│   └── rag_system.py     # Carga y búsqueda en `knowledge_base/`
├── knowledge_base/       # JSON con cursos, artículos y revistas
├── config/               # Configuración local (ej.: `config/.env.example`)
├── notebooks/            # Notebooks de prueba (p. ej. `test_api.ipynb`)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## **Scripts para desarrolladores**

Se han añadido scripts PowerShell útiles para arrancar y detener el servicio con Docker Compose desde Windows.

- `scripts/start.ps1` — copia `config/.env.example` a `config/.env` si no existe, opcionalmente reconstruye las imágenes y levanta los servicios.
  - Uso básico:

```powershell
# Desde la raíz del repositorio
.\scripts\start.ps1
```

  - Forzar reconstrucción de imágenes (opcional):

```powershell
.\scripts\start.ps1 -Rebuild
```

  - Qué hace el script:
    - Si `config/.env` no existe, lo crea a partir de `config/.env.example`.
    - (Opcional) `-Rebuild` ejecuta `docker compose build --no-cache`.
    - Ejecuta `docker compose up -d` y comprueba el endpoint `/api/health`.

- `scripts/stop.ps1` — detiene y elimina los servicios levantados por Docker Compose:

```powershell
.\scripts\stop.ps1
```

Notas:

- Si PowerShell restringe la ejecución de scripts, puedes habilitar temporalmente la ejecución con (ejecutar como administrador):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

- Asegúrate de editar `config/.env` con tus credenciales antes de ejecutar `start.ps1` si el script no las creó automáticamente.

## **Requisitos**

- **Docker** y **docker-compose** (recomendado para despliegue).
- Python 3.8+ (solo si ejecutas localmente sin Docker).

## **Instalación (local, sin Docker)**

- Clona el repositorio y crea un entorno virtual si lo deseas:

```powershell
git clone <tu-repositorio>
cd Proyecto02-SDK-Foundry-ONG-GD-v2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## **Variables de entorno / Configuración**

- Archivo de ejemplo: `config/.env.example` (no contiene claves reales).
- Variables principales:
  - `AZURE_AI_ENDPOINT`: Endpoint de Azure AI Foundry.
  - `AZURE_AI_KEY`: API Key de Azure AI Foundry.

- Para desarrollo copia y edita:

```powershell
Copy-Item .\config\.env.example .\config\.env
notepad .\config\.env
# Rellena AZURE_AI_ENDPOINT y AZURE_AI_KEY
```

> Nota: NO subir `config/.env` con claves reales al repositorio. Usa `config/.env.example` como plantilla.

## **Despliegue con Docker Compose (recomendado)**

- Construir y levantar el servicio API:

```powershell
# Desde la raíz del repo
docker compose build --no-cache
docker compose up -d
```

- Verificar estado de la API:

```powershell
# Health check
Invoke-RestMethod http://localhost:5001/api/health
# Ver logs
docker compose logs -f api
```

## **Uso de la API**

- Endpoint principal: `POST http://localhost:5001/api/chat`
- Health check: `GET http://localhost:5001/api/health`

- Ejemplo de petición (Python):

```python
import requests

resp = requests.post('http://localhost:5001/api/chat', json={"message": "¿Qué cursos recomiendas sobre energías renovables?"})
data = resp.json()
print(data.get('response'))
```

La respuesta JSON contiene al menos las claves `success`, `response` (texto) y `source`.

## **Notebook de prueba**

- Ruta: `notebooks/test_api.ipynb`.
- Objetivo: comprobar `/api/health` y enviar un POST de ejemplo a `/api/chat`.
- Uso rápido (desde Jupyter): abre el notebook y ejecuta las celdas en orden. El notebook detecta automáticamente `localhost` o `host.docker.internal`.
