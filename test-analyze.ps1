# Test completo del análisis de imagen
$json = @"
{
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mNk+M9Qz0AEYBxVSF+FAP0QAwH8cj9WAAAAAElFTkSuQmCC",
    "mode": "quick"
}
"@

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PROBANDO ENDPOINT /analyze" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Enviando imagen a Gemini..." -ForegroundColor Yellow
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/analyze" -Method Post -Body $json -ContentType "application/json"
    
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  ✅ RESPUESTA EXITOSA" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Análisis de Gemini:" -ForegroundColor Cyan
    Write-Host $response.response -ForegroundColor White
    Write-Host ""
    Write-Host "⚙️  Modo usado: $($response.mode)" -ForegroundColor Yellow
    Write-Host "🔢 Peticiones restantes: $($response.remaining_requests)/20" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    
} catch {
    Write-Host "============================================" -ForegroundColor Red
    Write-Host "  ❌ ERROR" -ForegroundColor Red
    Write-Host "============================================" -ForegroundColor Red
    Write-Host ""
    Write-Host $_.Exception.Message -ForegroundColor Red
}