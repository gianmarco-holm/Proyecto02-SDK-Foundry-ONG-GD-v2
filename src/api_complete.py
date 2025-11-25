
# green_dream_api.py - API REST para integrar con página web
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Agregar el directorio actual al path para importar nuestros módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant_rag import AsistenteGreenDreamRAG

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)  # Permitir requests desde el frontend

# Inicializar el asistente RAG (una sola vez al inicio)
print("🚀 Inicializando Green Dream RAG Assistant...")
assistant_initialized = False
assistant_init_error = None
asistente = None
try:
    asistente = AsistenteGreenDreamRAG()
    assistant_initialized = True
    print("✅ API lista para recibir consultas")
except Exception as e:
    assistant_init_error = str(e)
    assistant_initialized = False
    print(f"⚠️ Error inicializando asistente: {e}")

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal para chatear con el asistente Green Dream"""
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({"error": "Campo 'message' requerido"}), 400

        user_message = data['message']

        # Procesar con RAG
        respuesta = asistente.preguntar_con_rag(user_message, stream=False)

        return jsonify({
            "success": True,
            "response": respuesta,
            "source": "Green Dream RAG Assistant"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint para verificar que la API está funcionando"""
    payload = {
        "status": "healthy",
        "service": "Green Dream Chat API",
        "version": "1.0.0",
        "assistant_initialized": assistant_initialized
    }
    if assistant_init_error:
        payload["assistant_error"] = assistant_init_error

    return jsonify(payload)


@app.route('/api/debug', methods=['GET'])
def debug_info():
    """Información de diagnóstico útil para desarrollo local."""
    return jsonify({
        "service": "Green Dream Chat API",
        "assistant_initialized": assistant_initialized,
        "assistant_error": assistant_init_error
    })


@app.route('/')
def index():
    """Raíz: información mínima de la API (sin servir archivos estáticos)."""
    return jsonify({
        "service": "Green Dream Chat API",
        "message": "API only — use /api/* endpoints. The static website is not served here.",
        "endpoints": ["/api/health", "/api/chat", "/api/debug"]
    })

if __name__ == '__main__':
    # Ejecutar en modo desarrollo
    app.run(host='0.0.0.0', port=5001, debug=True)
