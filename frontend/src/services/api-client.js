const fetch = require('node-fetch');
const { clipboard } = require('electron');

class ApiClient {
    constructor() {
        this.baseUrl = 'http://127.0.0.1:5000';
    }

    setConfig(configManager) {
        this.configManager = configManager;
        this.baseUrl = configManager.get('backendUrl');
    }

    async analyzeImage(imageBase64, mode = null) {
        try {
            // Usar modo de configuración si no se especifica
            if (!mode && this.configManager) {
                mode = this.configManager.get('usageMode');
            }

            if (!mode) {
                mode = 'exam';
            }

            // Obtener prompt personalizado si existe
            const customPrompt = this.configManager
                ? this.configManager.get(`customPrompts.${mode}`)
                : null;

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
                timeout: 30000
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP ${response.status}`);
            }

            const result = await response.json();

            // Auto-copiar al portapapeles
            const autoCopy = this.configManager
                ? this.configManager.get('autoCopyToClipboard')
                : true;

            if (autoCopy) {
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
