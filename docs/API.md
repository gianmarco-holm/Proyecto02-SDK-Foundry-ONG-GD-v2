# Documentación de la API - Green Dream RAG Assistant

## 🔌 Endpoints Disponibles

### Base URL
```
http://localhost:5001
```

## 📡 Chat Principal

### `POST /api/chat`

Envía un mensaje al asistente de Green Dream y recibe una respuesta personalizada.

**Request:**
```http
POST /api/chat
Content-Type: application/json

{
  "message": "¿Qué cursos me recomendarías para aprender sobre energías renovables?"
}
```

**Response (Success):**
```json
{
  "success": true,
  "response": "Te recomiendo estos excelentes cursos de Green Dream sobre energías renovables:\n\n🌞 **Energía Solar Básica** - $120, 4 semanas\n- Introducción a paneles solares\n- Cálculo de instalaciones\n- Casos prácticos\n\n💨 **Energía Eólica** - $150, 6 semanas\n- Fundamentos de aerodinámica\n- Diseño de parques eólicos\n- Evaluación de recursos\n\n¿Te interesa alguno en particular?",
  "source": "Green Dream Simple API"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Descripción del error"
}
```

**Códigos de Estado:**
- `200` - Éxito
- `400` - Request inválido (falta campo 'message')
- `500` - Error interno del servidor

## 🏥 Health Check

### `GET /api/health`

Verifica que la API esté funcionando correctamente.

**Request:**
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Green Dream Simple API"
}
```

## 💡 Ejemplos de Uso

### Python
```python
import requests

# Enviar mensaje
response = requests.post(
    "http://localhost:5001/api/chat",
    json={"message": "Hola, ¿qué cursos ofrecen?"}
)

if response.status_code == 200:
    data = response.json()
    if data["success"]:
        print(data["response"])
    else:
        print(f"Error: {data['error']}")
```

### JavaScript (Frontend)
```javascript
async function chatWithAssistant(message) {
    try {
        const response = await fetch('http://localhost:5001/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.response;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Uso
chatWithAssistant("¿Qué artículos recomiendan sobre sostenibilidad?")
    .then(response => console.log(response))
    .catch(error => console.error(error));
```

### URL
```bash
# Chat
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Cuéntame sobre los programas de Green Dream"}'

# Health check
curl http://localhost:5001/api/health
```

## 🎯 Tipos de Consultas Soportadas

### 1. **Recomendaciones de Cursos**
```json
{
  "message": "Soy estudiante de ingeniería, ¿qué cursos me recomendarías?"
}
```

### 2. **Información General**
```json
{
  "message": "¿Qué es Green Dream ONG?"
}
```

### 3. **Búsqueda Específica**
```json
{
  "message": "Quiero aprender sobre energías renovables"
}
```

### 4. **Consultas de Precios**
```json
{
  "message": "¿Cuánto cuestan los cursos de sostenibilidad?"
}
```

## ⚠️ Limitaciones y Consideraciones

### Rate Limiting
- Actualmente no hay límites de rate
- Recomendado: máximo 60 requests/minuto por cliente

### Tamaño de Mensaje
- Máximo recomendado: 1000 caracteres
- El sistema está optimizado para consultas conversacionales

### Contexto
- Cada request es independiente (stateless)
- No mantiene historial de conversación entre requests

### Timeout
- Timeout por defecto: 30 segundos
- Para consultas complejas puede tardar 5-10 segundos

## 🔧 Configuración y Personalización

### Variables de Entorno
```bash
# config/.env
AZURE_AI_ENDPOINT="https://tu-proyecto.services.ai.azure.com/models"
AZURE_AI_KEY="tu-api-key"
```

### Puerto Personalizado
Editar `src/api_chat.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Cambiar puerto aquí
```

### Personalizar Respuestas
Editar el prompt en `src/api_chat.py`:
```python
UserMessage(content=f"Eres el asistente de Green Dream ONG. [Tu prompt personalizado]: {user_message}")
```

## 📊 Monitoreo y Logs

### Logs de Consola
La API muestra logs detallados en la consola:
```
🚀 Iniciando API simplificada...
📥 Request recibido: {"message": "Hola"}
✅ Respuesta enviada exitosamente
```

### Health Monitoring
```bash
# Script de monitoreo simple
while true; do
  curl -s http://localhost:5001/api/health | jq '.status'
  sleep 30
done
```

## 🚨 Manejo de Errores

### Errores Comunes

**400 - Bad Request:**
```json
{
  "error": "Campo 'message' requerido"
}
```

**500 - Internal Server Error:**
```json
{
  "success": false,
  "error": "Error de conexión con Azure AI"
}
```

### Debug Mode
Ejecutar en modo debug:
```bash
python src/api_chat.py --debug
```

## 🔐 Seguridad

### CORS
- Configurado para permitir requests desde cualquier origen
- En producción, configurar orígenes específicos

### API Keys
- Las API keys de Azure se cargan desde variables de entorno
- Nunca incluir keys en el código fuente

### HTTPS
- En producción, usar HTTPS
- Configurar certificados SSL apropiados

---

Para más información, consultar el [README principal](../README.md) o la [guía de instalación](INSTALACION.md).