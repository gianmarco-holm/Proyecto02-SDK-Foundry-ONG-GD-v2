# Guía de Instalación - Green Dream RAG Assistant

## 🔧 Instalación Paso a Paso

### 1. Preparar el Entorno

```bash
# Verificar Python (requiere 3.8+)
python --version

# Clonar o descargar el proyecto
git clone <repositorio>
cd green-dream-assistant
```

### 2. Crear Entorno Virtual

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Azure AI Foundry

1. **Crear cuenta en Azure Portal**
2. **Crear Azure AI Foundry Project**
3. **Obtener credenciales:**
   - API Key
   - Endpoint URL

4. **Configurar variables de entorno:**
   ```bash
   # Editar config/.env
   AZURE_AI_ENDPOINT="https://tu-proyecto.services.ai.azure.com/models"
   AZURE_AI_KEY="tu-api-key-aqui"
   ```

### 5. Probar la Instalación

```bash
# Probar el cliente de Azure
python -c "from src.chat_client import client; print('✅ Azure client OK')"

# Iniciar servidor web
python src/web_server.py

# En otra terminal, iniciar API
python src/api_chat.py

# Abrir: http://localhost:8080/website.html
```

## 🚨 Problemas Comunes

### Error: Módulo no encontrado
```bash
# Solución: Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### Error: Puerto ocupado
```bash
# Windows
taskkill /F /IM python.exe

# Linux/Mac
sudo lsof -ti:8080 | xargs kill -9
```

### Error: Azure connection
- Verificar archivo `config/.env`
- Comprobar conectividad a internet
- Validar API Key en Azure Portal

## ✅ Verificación Final

Si todo funciona correctamente deberías poder:
1. ✅ Ver la página web en http://localhost:8080/website.html
2. ✅ Chatear con el asistente
3. ✅ Recibir respuestas personalizadas
4. ✅ Ver logs en la consola

¡Listo para usar! 🎉