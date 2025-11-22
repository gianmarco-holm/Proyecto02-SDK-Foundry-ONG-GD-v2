# 🌱 Green Dream RAG Assistant

Sistema de asistente virtual inteligente para **Green Dream ONG**, una organización dedicada al desarrollo sostenible para jóvenes. Utiliza tecnología RAG (Retrieval-Augmented Generation) con Azure AI Foundry para proporcionar recomendaciones personalizadas sobre cursos, artículos y recursos de sostenibilidad.

## 🎯 Características Principales

- **🤖 Asistente IA Especializado**: Conocimiento específico de Green Dream ONG
- **📚 Base de Conocimiento RAG**: Búsqueda inteligente en cursos, artículos y revistas
- **🌐 Interfaz Web Moderna**: Página web responsive con chat integrado
- **⚡ API REST**: Endpoints listos para integración
- **🔗 Azure AI Foundry**: Powered by GPT-4o

## 🏗️ Arquitectura del Proyecto

```
green-dream-assistant/
├── 📁 src/                     # Código fuente
│   ├── api_chat.py            # API de chat principal (puerto 5001)
│   ├── api_complete.py        # API completa con RAG (puerto 5000)
│   ├── assistant_rag.py       # Asistente con RAG
│   ├── assistant.py           # Asistente base
│   ├── chat_client.py         # Cliente Azure AI Foundry
│   ├── rag_system.py          # Sistema de búsqueda RAG
│   └── web_server.py          # Servidor HTTP (puerto 8080)
├── 📁 knowledge_base/         # Base de conocimiento
│   ├── articulos.json         # Artículos de sostenibilidad
│   ├── cursos.json           # Cursos disponibles
│   └── revistas.json         # Revistas especializadas
├── 📁 config/                 # Configuración
│   └── .env                  # Variables de entorno
├── 📁 docs/                   # Documentación
├── 🌐 website.html           # Página web principal
├── 📋 main.ipynb             # Notebook de desarrollo
├── 📦 requirements.txt       # Dependencias Python
└── 📖 README.md             # Este archivo
```

## 🚀 Instalación y Configuración

### 1. **Prerrequisitos**
- Python 3.8 o superior
- Cuenta de Azure con acceso a Azure AI Foundry
- Git (opcional)

### 2. **Clonar el Repositorio**
```bash
git clone <tu-repositorio>
cd green-dream-assistant
```

### 3. **Crear Entorno Virtual**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 4. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 5. **Configurar Azure AI Foundry**

1. **Crear recursos en Azure Portal:**
   - Azure AI Foundry Project
   - Obtener API Key y Endpoint

2. **Configurar variables de entorno:**
   ```bash
   # Editar config/.env
   AZURE_AI_ENDPOINT="https://tu-proyecto.services.ai.azure.com/models"
   AZURE_AI_KEY="tu-api-key-aqui"
   ```

## 🎮 Uso del Sistema

### **Opción 1: Aplicación Web Completa (Recomendado)**

1. **Iniciar el servidor web:**
   ```bash
   python src/web_server.py
   ```

2. **Iniciar la API de chat:**
   ```bash
   python src/api_chat.py
   ```

3. **Abrir en navegador:**
   ```
   http://localhost:8080/website.html
   ```

### **Opción 2: Solo API**

```bash
# API simple (recomendada)
python src/api_chat.py

# API con RAG completo
python src/api_complete.py
```

### **Opción 3: Jupyter Notebook**

```bash
jupyter notebook main.ipynb
```

## 🔌 API Endpoints

### **Chat Principal**
```http
POST http://localhost:5001/api/chat
Content-Type: application/json

{
  "message": "¿Qué cursos me recomendarías para aprender sobre energías renovables?"
}
```

**Respuesta:**
```json
{
  "success": true,
  "response": "Te recomiendo estos cursos de Green Dream...",
  "source": "Green Dream Simple API"
}
```

### **Health Check**
```http
GET http://localhost:5001/api/health
```

## 💡 Ejemplos de Uso

### **Consultas de Ejemplo:**
- "Hola, soy estudiante universitario. ¿Qué cursos tienes?"
- "Me interesa aprender sobre sostenibilidad ambiental"
- "¿Qué recomiendas para energías renovables?"
- "Cuéntame sobre los programas de Green Dream"
- "Quiero artículos sobre cambio climático"

### **Uso Programático:**
```python
import requests

# Enviar mensaje al asistente
response = requests.post(
    "http://localhost:5001/api/chat",
    json={"message": "¿Qué cursos ofrecen?"}
)

data = response.json()
print(data["response"])
```

## 🛠️ Desarrollo y Personalización

### **Agregar Contenido a la Base de Conocimiento:**

1. **Editar archivos JSON en `knowledge_base/`:**
   ```json
   // knowledge_base/cursos.json
   {
     "titulo": "Nuevo Curso de Sostenibilidad",
     "categoria": "Ambiental",
     "precio": "$150",
     "duracion": "6 semanas",
     // ... más campos
   }
   ```

2. **Reiniciar la API para cargar el nuevo contenido**

### **Personalizar el Asistente:**

Editar `src/assistant_rag.py`:
```python
self.system_prompt = """Tu nuevo prompt personalizado..."""
```

### **Modificar la Interfaz Web:**

Editar `website.html` para cambiar:
- Colores y estilos
- Contenido de la página
- Comportamiento del chat

## 🔧 Troubleshooting

### **Problemas Comunes:**

1. **Error de conexión a Azure:**
   - Verificar `config/.env`
   - Comprobar conectividad a internet
   - Validar API Key y Endpoint

2. **Puerto ocupado:**
   - Cambiar puerto en el código
   - Matar procesos: `taskkill /F /IM python.exe` (Windows)

3. **Módulos no encontrados:**
   - Activar entorno virtual
   - Reinstalar dependencias: `pip install -r requirements.txt`

4. **Chat no responde:**
   - Verificar que ambos servidores estén corriendo
   - Revisar console del navegador (F12)
   - Comprobar endpoint en `website.html`

### **Logs y Debugging:**

```bash
# Ver logs detallados
python src/api_chat.py --debug

# Verificar estado de la API
curl http://localhost:5001/api/health
```

## 📈 Roadmap y Mejoras Futuras

- [ ] **Autenticación de usuarios**
- [ ] **Base de datos vectorial (Pinecone/Chroma)**
- [ ] **Búsqueda semántica avanzada**
- [ ] **Análisis de sentimientos**
- [ ] **Integración con calendarios**
- [ ] **Notificaciones push**
- [ ] **Dashboard de administración**
- [ ] **API de estadísticas**

## 🤝 Contribuir

1. Fork del proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Equipo

- **Desarrollado para**: Green Dream ONG
- **Tecnología**: Azure AI Foundry + Flask + HTML/CSS/JS
- **Modelo IA**: GPT-4o

## 📞 Soporte

Para problemas técnicos o consultas:
- 📧 **Email**: soporte@greendream.org
- 🐛 **Issues**: [GitHub Issues](https://github.com/tu-repo/issues)
- 📖 **Documentación**: Ver carpeta `docs/`

---

**🌱 Green Dream ONG - Construyendo un futuro sostenible con tecnología innovadora**