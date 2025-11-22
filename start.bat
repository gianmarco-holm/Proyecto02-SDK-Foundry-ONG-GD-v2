@echo off
REM start.bat - Script para iniciar Green Dream RAG Assistant (Windows)

echo 🌱 Iniciando Green Dream RAG Assistant...

REM Verificar que estamos en el directorio correcto
if not exist "requirements.txt" (
    echo ❌ Error: Ejecutar desde el directorio raíz del proyecto
    pause
    exit /b 1
)

REM Activar entorno virtual
if exist ".venv" (
    echo 🔧 Activando entorno virtual...
    call .venv\Scripts\activate
) else (
    echo ⚠️  Entorno virtual no encontrado. Creando...
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
)

REM Verificar configuración
if not exist "config\.env" (
    echo ❌ Error: Archivo config\.env no encontrado
    echo 📝 Crear config\.env con las credenciales de Azure AI Foundry
    pause
    exit /b 1
)

echo ✅ Configuración verificada

REM Iniciar servidor web en background
echo 🌐 Iniciando servidor web (puerto 8080)...
start "Green Dream Web Server" python src\web_server.py

REM Esperar un poco
timeout /t 3 /nobreak >nul

REM Iniciar API de chat en background
echo 🤖 Iniciando API de chat (puerto 5001)...
start "Green Dream API" python src\api_complete.py

REM Esperar un poco más
timeout /t 3 /nobreak >nul

echo.
echo 🎉 ¡Green Dream RAG Assistant iniciado!
echo 🌐 Página web: http://localhost:8080/website.html
echo 📡 API: http://localhost:5001/api/health
echo.
echo 👋 Cierra las ventanas de los servidores para detener los servicios
echo.

REM Abrir página web automáticamente
start http://localhost:8080/website.html

pause