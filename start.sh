#!/bin/bash
# start.sh - Script para iniciar Green Dream RAG Assistant (Linux/Mac)

echo "🌱 Iniciando Green Dream RAG Assistant..."

# Verificar que estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Ejecutar desde el directorio raíz del proyecto"
    exit 1
fi

# Activar entorno virtual
if [ -d ".venv" ]; then
    echo "🔧 Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "⚠️  Entorno virtual no encontrado. Creando..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

# Verificar configuración
if [ ! -f "config/.env" ]; then
    echo "❌ Error: Archivo config/.env no encontrado"
    echo "📝 Crear config/.env con las credenciales de Azure AI Foundry"
    exit 1
fi

echo "✅ Configuración verificada"

# Función para matar procesos al salir
cleanup() {
    echo "🛑 Deteniendo servidores..."
    kill $WEB_PID 2>/dev/null
    kill $API_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar servidor web en background
echo "🌐 Iniciando servidor web (puerto 8080)..."
python src/web_server.py &
WEB_PID=$!

# Esperar un poco
sleep 2

# Iniciar API de chat en background
echo "🤖 Iniciando API de chat (puerto 5001)..."
python src/api_complete.py &
API_PID=$!

# Esperar un poco más
sleep 3

echo ""
echo "🎉 ¡Green Dream RAG Assistant iniciado!"
echo "🌐 Página web: http://localhost:8080/website.html"
echo "📡 API: http://localhost:5001/api/health"
echo ""
echo "👋 Presiona Ctrl+C para detener todos los servicios"
echo ""

# Mantener el script corriendo
wait