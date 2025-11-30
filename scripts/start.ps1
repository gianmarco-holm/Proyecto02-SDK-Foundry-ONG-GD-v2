# scripts/start.ps1
# Script para levantar el servicio localmente con Docker Compose

param(
    [switch]$Rebuild
)

# Copiar el .env de ejemplo si no existe
if (-not (Test-Path -Path .\config\.env)) {
    Write-Host "Copiando config/.env.example -> config/.env"
    Copy-Item .\config\.env.example .\config\.env -ErrorAction SilentlyContinue
    Write-Host "Edita config/.env con tus claves: notepad .\config\.env"
}

if ($Rebuild) {
    Write-Host "Reconstruyendo imágenes (docker compose build --no-cache)..."
    docker compose build --no-cache
}

Write-Host "Levantando servicios (docker compose up -d)..."
docker compose up -d

Write-Host "Verificando health endpoint..."
try {
    $health = Invoke-RestMethod -Uri 'http://localhost:5001/api/health' -TimeoutSec 10
    Write-Host "API health:" ($health.status)
} catch {
    Write-Warning "No se pudo obtener /api/health localmente. Revisa los logs: docker compose logs -f api"
}

Write-Host "Hecho. Para ver logs: docker compose logs -f api"