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
            usageMode: 'exam',
            captureMode: 'invisible',
            showSelectionFeedback: false,
            shortcuts: {
                captureExam: 'Shift+G',
                captureStudy: 'Shift+H',
                captureQuick: 'Shift+J',
                openSettings: 'Ctrl+Shift+G'
            },
            autoCopyToClipboard: true,
            showNotification: true,
            notificationDuration: 5000,
            notificationPosition: 'bottom-right',
            responseFormat: {
                multipleChoice: 'letter-only',
                trueFalse: 'word',
                openEnded: 'concise'
            },
            customPrompts: {
                exam: null,
                study: null,
                quick: null
            },
            backendUrl: 'http://127.0.0.1:5000',
            timeout: 30000,
            autoStartBackend: true,
            theme: 'dark',
            language: 'es',
            playSound: false,
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