# Test con imagen válida (1x1 pixel rojo)
$json = @"
{
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==",
    "mode": "detailed"
}
"@

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PROBANDO ENDPOINT /analyze (IMAGEN VÁLIDA)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Enviando imagen válida a Gemini..." -ForegroundColor Yellow
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
    Write-Host "Status Code:" $_.Exception.Response.StatusCode.value__ -ForegroundColor Red
    Write-Host "Mensaje:" $_.Exception.Message -ForegroundColor Red
}