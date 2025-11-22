"""Ejemplo sencillo para consultar la API desplegada.

Uso:
  python examples/query_api.py https://mi-dominio/api/chat "Tu pregunta aquí"

También puede usar la variable de entorno `API_URL`:
  set API_URL=https://mi-dominio/api/chat
  python examples/query_api.py "Tu pregunta aquí"
"""
import os
import sys
import requests


def main():
    if len(sys.argv) >= 3:
        api_url = sys.argv[1].rstrip('/')
        message = sys.argv[2]
    elif len(sys.argv) == 2:
        api_url = os.environ.get('API_URL')
        message = sys.argv[1]
        if not api_url:
            print('Error: debe indicar API URL como primer argumento o definir API_URL')
            sys.exit(1)
    else:
        print('Uso: python examples/query_api.py <API_URL> "Tu pregunta"')
        sys.exit(1)

    payload = {"message": message}

    try:
        resp = requests.post(api_url, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        print('Respuesta del servidor:')
        print(data)
    except Exception as e:
        print('Error consultando la API:', e)


if __name__ == '__main__':
    main()
