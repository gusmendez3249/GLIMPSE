# GLIMPSE - Setup Completo para Resolver Formularios/Exámenes
# Uso: .\setup-glimpse-completo.ps1

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  GLIMPSE - Setup Automatico Completo" -ForegroundColor Cyan
Write-Host "  Asistente para Formularios y Examenes" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$root = "D:\PROYECTOS_PERSONALES\GLIMPSE"
Set-Location $root

# ============================================
# BACKEND - Actualizar Prompts para Examenes
# ============================================

Write-Host "Actualizando Backend para Examenes..." -ForegroundColor Yellow

@'
class PromptService:
    """Prompts optimizados para resolver formularios y examenes"""
    
    PROMPTS = {
        "exam": """Eres un asistente para resolver preguntas de examen. Analiza la imagen y responde SOLO con la respuesta correcta.

INSTRUCCIONES CRÍTICAS:
1. Si es opción múltiple (A, B, C, D, etc.) → Responde SOLO la letra correcta
2. Si es Verdadero/Falso → Responde SOLO "Verdadero" o "Falso"
3. Si es pregunta abierta → Responde de forma DIRECTA y CONCISA (máximo 2 líneas)
4. Si es completar espacios → Responde SOLO las palabras faltantes
5. NO expliques, NO des contexto adicional, SOLO la respuesta

FORMATO DE RESPUESTA:
- Opción múltiple: B
- Verdadero/Falso: Verdadero
- Abierta: [respuesta directa]
- Completar: [palabra(s) faltante(s)]

Responde en español.""",
        
        "study": """Eres un tutor que ayuda a estudiar. Analiza la pregunta y proporciona la respuesta CON explicación breve.

INSTRUCCIONES:
1. Identifica el tipo de pregunta
2. Da la respuesta correcta
3. Explica BREVEMENTE por qué es correcta (máximo 3 líneas)

FORMATO:
**Respuesta:** [respuesta]
**Explicación:** [breve explicación]

Responde en español.""",
        
        "quick": """Analiza esta pregunta y responde de forma ULTRA BREVE.

INSTRUCCIONES:
- Si es opción múltiple → Solo la letra
- Si es otra cosa → Respuesta en máximo 1 línea
- Sin explicaciones

Responde en español.""",
        
        "detailed": """Eres un asistente visual experto. Analiza esta imagen de manera detallada.

INSTRUCCIONES:
1. Identifica el contenido principal
2. Si hay texto, transcríbelo con precisión
3. Si hay pregunta, identifica el tipo y responde
4. Proporciona contexto útil

Responde en español de forma estructurada.""",
        
        "code": """Analiza este código y explica qué hace o cómo resolver el problema.

INSTRUCCIONES:
1. Identifica el lenguaje
2. Explica la función o error
3. Si hay pregunta, respóndela
4. Sugiere solución si hay error

Responde en español de manera técnica."""
    }
    
    @classmethod
    def get_prompt(cls, mode='exam'):
        """Obtiene el prompt según el modo"""
        return cls.PROMPTS.get(mode, cls.PROMPTS['exam'])
    
    @classmethod
    def get_available_modes(cls):
        """Modos disponibles"""
        return list(cls.PROMPTS.keys())
'@ | Out-File -FilePath "backend\app\services\prompt_service.py" -Encoding UTF8

Write-Host "[✓] Backend actualizado" -ForegroundColor Green

# ============================================
# FRONTEND - Config Manager
# ============================================

Write-Host "Creando Config Manager..." -ForegroundColor Yellow

@'
const fs = require('fs');
const path = require('path');
const { app } = require('electron');

class ConfigManager {
    constructor() {
        this.configPath = path.join(app.getPath('userData'), 'glimpse-config.json');
        this.config = this.loadConfig();
    }

    getDefaultConfig() {
        return {
            // Modo principal de uso
            usageMode: 'exam', // exam, study, quick, detailed, code
            
            // Captura
            captureMode: 'invisible', // invisible, visual, minimal
            showSelectionFeedback: false, // Feedback visual al seleccionar
            
            // Atajos de teclado
            shortcuts: {
                captureExam: 'Shift+G',      // Modo examen (respuesta directa)
                captureStudy: 'Shift+H',     // Modo estudio (con explicación)
                captureQuick: 'Shift+J',     // Ultra rápido
                openSettings: 'Ctrl+Shift+G'
            },
            
            // Respuestas
            autoCopyToClipboard: true,        // Copiar respuesta automáticamente
            showNotification: true,           // Mostrar notificación
            notificationDuration: 5000,       // Duración en ms
            notificationPosition: 'bottom-right', // top-left, top-right, bottom-left, bottom-right
            
            // Formato de respuesta
            responseFormat: {
                multipleChoice: 'letter-only',  // letter-only, letter-with-text
                trueFalse: 'word',              // word, initial
                openEnded: 'concise'            // concise, detailed
            },
            
            // Prompts personalizados
            customPrompts: {
                exam: null,
                study: null,
                quick: null
            },
            
            // Avanzado
            backendUrl: 'http://127.0.0.1:5000',
            timeout: 30000,
            autoStartBackend: true,
            
            // UI
            theme: 'dark',
            language: 'es',
            playSound: false,
            
            // Privacidad
            saveHistory: false,
            clearHistoryOnExit: true
        };
    }

    loadConfig() {
        try {
            if (fs.existsSync(this.configPath)) {
                const data = fs.readFileSync(this.configPath, 'utf8');
                const saved = JSON.parse(data);
                return { ...this.getDefaultConfig(), ...saved };
            }
        } catch (error) {
            console.error('Error loading config:', error);
        }
        return this.getDefaultConfig();
    }

    saveConfig() {
        try {
            fs.writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
            return true;
        } catch (error) {
            console.error('Error saving config:', error);
            return false;
        }
    }

    get(key) {
        const keys = key.split('.');
        let value = this.config;
        for (const k of keys) {
            value = value[k];
            if (value === undefined) return null;
        }
        return value;
    }

    set(key, value) {
        const keys = key.split('.');
        let obj = this.config;
        for (let i = 0; i < keys.length - 1; i++) {
            obj = obj[keys[i]];
        }
        obj[keys[keys.length - 1]] = value;
        this.saveConfig();
    }

    update(updates) {
        this.config = { ...this.config, ...updates };
        this.saveConfig();
    }

    getAll() {
        return { ...this.config };
    }
}

module.exports = new ConfigManager();
'@ | Out-File -FilePath "frontend\src\services\config-manager.js" -Encoding UTF8

Write-Host "[✓] Config Manager creado" -ForegroundColor Green

# ============================================
# FRONTEND - API Client
# ============================================

Write-Host "Creando API Client..." -ForegroundColor Yellow

@'
const fetch = require('node-fetch');
const { clipboard } = require('electron');
const configManager = require('./config-manager');

class ApiClient {
    constructor() {
        this.baseUrl = configManager.get('backendUrl');
    }

    async analyzeImage(imageBase64, mode = null) {
        try {
            // Usar modo de configuración si no se especifica
            if (!mode) {
                mode = configManager.get('usageMode');
            }

            // Obtener prompt personalizado si existe
            const customPrompt = configManager.get(`customPrompts.${mode}`);

            const response = await fetch(`${this.baseUrl}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image: imageBase64,
                    mode: mode,
                    custom_prompt: customPrompt
                }),
                timeout: configManager.get('timeout')
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP ${response.status}`);
            }

            const result = await response.json();
            
            // Auto-copiar al portapapeles si está habilitado
            if (configManager.get('autoCopyToClipboard')) {
                clipboard.writeText(result.response);
            }

            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/health`, {
                timeout: 5000
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}

module.exports = new ApiClient();
'@ | Out-File -FilePath "frontend\src\services\api-client.js" -Encoding UTF8

Write-Host "[✓] API Client creado" -ForegroundColor Green

# ============================================
# FRONTEND - Screenshot Service
# ============================================

Write-Host "Creando Screenshot Service..." -ForegroundColor Yellow

@'
const { desktopCapturer, screen } = require('electron');
const sharp = require('sharp');

class ScreenshotService {
    async captureFullScreen() {
        const sources = await desktopCapturer.getSources({
            types: ['screen'],
            thumbnailSize: screen.getPrimaryDisplay().size
        });

        if (sources.length === 0) {
            throw new Error('No se pudo capturar la pantalla');
        }

        return sources[0].thumbnail.toPNG();
    }

    async cropImage(imageBuffer, bounds) {
        const display = screen.getPrimaryDisplay();
        const metadata = await sharp(imageBuffer).metadata();
        
        const scaleX = metadata.width / display.size.width;
        const scaleY = metadata.height / display.size.height;

        const cropBounds = {
            left: Math.max(0, Math.round(bounds.x * scaleX)),
            top: Math.max(0, Math.round(bounds.y * scaleY)),
            width: Math.round(bounds.width * scaleX),
            height: Math.round(bounds.height * scaleY)
        };

        // Ajustar si excede límites
        if (cropBounds.left + cropBounds.width > metadata.width) {
            cropBounds.width = metadata.width - cropBounds.left;
        }
        if (cropBounds.top + cropBounds.height > metadata.height) {
            cropBounds.height = metadata.height - cropBounds.top;
        }

        return await sharp(imageBuffer)
            .extract(cropBounds)
            .png({ quality: 90 })
            .toBuffer();
    }

    imageToBase64(buffer) {
        return `data:image/png;base64,${buffer.toString('base64')}`;
    }
}

module.exports = new ScreenshotService();
'@ | Out-File -FilePath "frontend\src\services\screenshot-service.js" -Encoding UTF8

Write-Host "[✓] Screenshot Service creado" -ForegroundColor Green

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Setup Completo!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "1. cd frontend" -ForegroundColor White
Write-Host "2. npm install" -ForegroundColor White
Write-Host "3. Te dare el resto del codigo..." -ForegroundColor White