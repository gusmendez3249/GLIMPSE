const { app, BrowserWindow, globalShortcut, screen, ipcMain, Tray, Menu } = require('electron');
const path = require('path');

let configManager;
let apiClient;
let screenshotService;

let mainWindow;
let captureWindow;
let cursorWindow;
let notificationWindow;
let settingsWindow;
let tray;

// Al iniciar la app
app.whenReady().then(() => {
    // Cargar módulos después de que Electron esté listo
    configManager = require('../services/config-manager');
    apiClient = require('../services/api-client');
    screenshotService = require('../services/screenshot-service');

    // Inicializar apiClient con configManager
    apiClient.setConfig(configManager);

    createMainWindow();
    createTray();
    registerShortcuts();

    console.log('✓ GLIMPSE iniciado');
    console.log('✓ Atajos registrados');
    console.log(`✓ Modo actual: ${configManager.get('captureMode')}`);
});

// Ventana principal (oculta)
function createMainWindow() {
    mainWindow = new BrowserWindow({
        width: 1,
        height: 1,
        show: false,
        frame: false,
        transparent: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('src/renderer/pages/index.html');
}

// System Tray
function createTray() {
    try {
        const iconPath = path.join(__dirname, '../../src/assets/icons/icon.ico');
        tray = new Tray(iconPath);

        updateTrayMenu();

        tray.setToolTip('GLIMPSE - Asistente de Exámenes');
    } catch (error) {
        console.error('Error creando tray:', error);
    }
}

function updateTrayMenu() {
    const captureMode = configManager.get('captureMode');
    const modeText = captureMode === 'invisible' ? '👻 Invisible' : '🎨 Visual';

    const contextMenu = Menu.buildFromTemplate([
        {
            label: `Modo actual: ${modeText}`,
            enabled: false
        },
        { type: 'separator' },
        {
            label: '📸 Capturar (Shift+X)',
            click: () => startCapture('exam')
        },
        { type: 'separator' },
        {
            label: 'Cambiar Modo',
            submenu: [
                {
                    label: '👻 Modo Invisible',
                    type: 'radio',
                    checked: captureMode === 'invisible',
                    click: () => {
                        configManager.set('captureMode', 'invisible');
                        updateTrayMenu();
                    }
                },
                {
                    label: '🎨 Modo Visual',
                    type: 'radio',
                    checked: captureMode === 'visual',
                    click: () => {
                        configManager.set('captureMode', 'visual');
                        updateTrayMenu();
                    }
                }
            ]
        },
        { type: 'separator' },
        {
            label: '⚙️ Configuración',
            click: openSettings
        },
        { type: 'separator' },
        {
            label: '❌ Salir',
            click: () => app.quit()
        }
    ]);

    tray.setContextMenu(contextMenu);
}

// Registrar atajos
function registerShortcuts() {
    // Shift+X - Modo Examen
    globalShortcut.register('Shift+X', () => startCapture('exam'));
    // Shift+H - Modo Estudio
    globalShortcut.register('Shift+H', () => startCapture('study'));
    // Shift+J - Modo Rápido
    globalShortcut.register('Shift+J', () => startCapture('quick'));
    // Shift+Z - Modo Pregunta Abierta (Copia exacta al portapapeles)
    globalShortcut.register('Shift+Z', () => startCapture('open_text'));
    // Ctrl+Shift+G - Configuración
    globalShortcut.register('Ctrl+Shift+G', openSettings);
    console.log('✓ Atajos registrados: Shift+X (examen), Shift+H (estudio), Shift+J (rápido), Shift+Z (texto abierto)');
}

// Iniciar captura
function startCapture(mode) {
    const captureMode = configManager.get('captureMode');

    captureWindow = new BrowserWindow({
        fullscreen: true,
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        skipTaskbar: true,
        hasShadow: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    const htmlFile = captureMode === 'invisible'
        ? 'src/renderer/pages/capture.html'
        : 'src/renderer/pages/capture-visual.html';

    captureWindow.loadFile(htmlFile);
    captureWindow.webContents.once('did-finish-load', () => {
        captureWindow.webContents.send('init-capture', { mode });
    });
}

// Ventana flotante en esquina inferior derecha (MODO INVISIBLE)
function showCursorWindow(text, position) {
    if (cursorWindow && !cursorWindow.isDestroyed()) {
        cursorWindow.close();
    }

    // Tamaño más pequeño y discreto
    const textLength = text.length;
    const width = Math.min(Math.max(textLength * 8, 60), 250);
    const height = 30;

    const { width: screenWidth, height: screenHeight } = screen.getPrimaryDisplay().workAreaSize;

    cursorWindow = new BrowserWindow({
        width: width,
        height: height,
        x: screenWidth - width - 20,
        y: screenHeight - height - 20,
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        skipTaskbar: true,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    cursorWindow.setIgnoreMouseEvents(true);
    cursorWindow.loadFile('src/renderer/pages/cursor-tooltip.html');

    cursorWindow.webContents.once('did-finish-load', () => {
        cursorWindow.webContents.send('show-text', text);
    });

    // Auto-cerrar después de 3 segundos (más discreto)
    setTimeout(() => {
        if (cursorWindow && !cursorWindow.isDestroyed()) {
            cursorWindow.close();
        }
    }, 3000);
}

// Notificación completa (MODO VISUAL)
function showNotification(response, mode) {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    if (notificationWindow && !notificationWindow.isDestroyed()) {
        notificationWindow.close();
    }

    notificationWindow = new BrowserWindow({
        width: 400,
        height: 250,
        x: width - 420,
        y: height - 270,
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        skipTaskbar: true,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    notificationWindow.loadFile('src/renderer/pages/notification.html');

    notificationWindow.webContents.once('did-finish-load', () => {
        notificationWindow.webContents.send('show-notification', {
            response,
            mode
        });
    });

    // Auto-cerrar después de tiempo configurado
    const duration = configManager.get('notificationDuration') || 8000;
    setTimeout(() => {
        if (notificationWindow && !notificationWindow.isDestroyed()) {
            notificationWindow.close();
        }
    }, duration);
}

// Configuración
function openSettings() {
    if (settingsWindow && !settingsWindow.isDestroyed()) {
        settingsWindow.focus();
        return;
    }

    settingsWindow = new BrowserWindow({
        width: 600,
        height: 700,
        title: 'GLIMPSE - Configuración',
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    settingsWindow.loadFile('src/renderer/pages/settings.html');

    settingsWindow.on('closed', () => {
        settingsWindow = null;
    });
}

// IPC Handlers
ipcMain.on('capture-complete', async (event, data) => {
    if (captureWindow) {
        captureWindow.close();
        captureWindow = null;
    }

    const { bounds, mode, cursorPosition } = data;
    const captureMode = configManager.get('captureMode');

    try {
        // Capturar y procesar
        const fullScreen = await screenshotService.captureFullScreen();
        const croppedImage = await screenshotService.cropImage(fullScreen, bounds);
        const base64Image = screenshotService.imageToBase64(croppedImage);

        // Analizar con backend
        const result = await apiClient.analyzeImage(base64Image, mode);

        // Mostrar resultado según el modo
        const displayResponse = mode === 'open_text' ? 'Lis' : result.response;

        if (captureMode === 'invisible') {
            // MODO INVISIBLE: Mostrar tooltip discreto al lado del cursor
            showCursorWindow(displayResponse, cursorPosition);
            console.log('✓ Resultado mostrado en tooltip:', displayResponse === 'Lis' ? '(Oculto - copiado al portapapeles)' : displayResponse);
        } else {
            // MODO VISUAL: Notificación completa
            showNotification(displayResponse, mode);
        }

    } catch (error) {
        console.error('Error:', error);

        if (captureMode === 'invisible') {
            console.error('❌ Error en análisis:', error.message);
            if (cursorPosition) {
                showCursorWindow('❌ Error', cursorPosition);
            }
        } else {
            showNotification(`Error: ${error.message}`, mode);
        }
    }
});

ipcMain.on('capture-cancel', () => {
    if (captureWindow) {
        captureWindow.close();
        captureWindow = null;
    }
});

ipcMain.on('close-notification', () => {
    if (notificationWindow && !notificationWindow.isDestroyed()) {
        notificationWindow.close();
        notificationWindow = null;
    }
});

ipcMain.on('get-config', (event) => {
    event.reply('config-data', configManager.getAll());
});

ipcMain.on('save-config', (event, newConfig) => {
    configManager.update(newConfig);

    // Re-registrar atajos
    globalShortcut.unregisterAll();
    registerShortcuts();

    // Actualizar menú del tray
    updateTrayMenu();

    event.reply('config-saved', { success: true });
});

// Limpiar al salir
app.on('will-quit', () => {
    globalShortcut.unregisterAll();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});