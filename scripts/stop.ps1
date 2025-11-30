# scripts/stop.ps1
# Script para detener y eliminar los servicios levantados por docker compose

Write-Host "Deteniendo servicios..."
docker compose down

Write-Host "Contenedores y red eliminados. Para ver logs históricos: docker compose logs api"