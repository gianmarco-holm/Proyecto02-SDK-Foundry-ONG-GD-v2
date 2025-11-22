#!/usr/bin/env python3
"""
web_server.py - Servidor HTTP para servir la página web de Green Dream
"""
import http.server
import socketserver
import webbrowser
import threading
import time
import os

def serve_website():
    Handler = http.server.SimpleHTTPRequestHandler  # Maneja solicitudes HTTP simples

    # Cambiar al directorio raíz del proyecto (donde está website.html)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)  # Cambia al directorio raíz del proyecto

    # Permitir reutilizar la dirección para evitar errores al reiniciar rápidamente
    socketserver.TCPServer.allow_reuse_address = True

    # Intentar enlazar a 8080 y si está ocupado probar puertos siguientes
    for PORT in range(8080, 8091):
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print(f"🌐 Servidor web iniciado en: http://localhost:{PORT}")
                print(f"📄 Página principal: http://localhost:{PORT}/website.html")
                print("📡 API funcionando en: http://localhost:5001")
                print("\n✅ Todo listo! Abriendo navegador...")

                # Abrir navegador después de 2 segundos
                def open_browser(port=PORT):
                    time.sleep(2)
                    try:
                        webbrowser.open(f'http://localhost:{port}/website.html')
                    except Exception:
                        pass

                browser_thread = threading.Thread(target=open_browser)
                browser_thread.daemon = True
                browser_thread.start()

                print("🔥 Presiona Ctrl+C para detener el servidor")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print('\nDeteniendo servidor...')
                return
        except OSError as e:
            # Puerto en uso, informar y probar siguiente
            print(f"Puerto {PORT} en uso (detalle: {e}). Probando {PORT + 1}...")
            continue

    print("❌ No fue posible abrir el servidor web en los puertos 8080-8090")

if __name__ == "__main__":
    serve_website()