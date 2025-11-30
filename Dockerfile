FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Evitar crear .pyc y forzar salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependencias del sistema mínimo
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar el código de la aplicación
COPY . /app

# Puerto expuesto por la API Flask
EXPOSE 5001

# Ejecutar Gunicorn apuntando al módulo Flask dentro de src/
# (api_complete.py define `app` en la raíz de `src`)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--chdir", "src", "api_complete:app", "--workers", "2", "--threads", "4"]
