"""api_chat.py

Pequeño wrapper para arrancar la API de chat desde la consola usando
`python src/api_chat.py` (consistente con las instrucciones del README).
Importa la aplicación Flask definida en `api_complete.py`.
"""
import os
import sys

# Asegurar que el paquete src esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_complete import app

if __name__ == '__main__':
    # Ejecutar la misma app que api_complete en el puerto 5001
    app.run(host='0.0.0.0', port=5001, debug=True)
