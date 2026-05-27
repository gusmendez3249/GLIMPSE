# GLIMPSE 👁️

Asistente visual con IA que captura zonas de tu pantalla y las analiza con **Claude** (Anthropic) o **Groq**. Pensado para resolver exámenes, estudiar y obtener respuestas rápidas sin salir de lo que estás haciendo.

---

## Requisitos previos

| Herramienta | Versión mínima |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |

También necesitas al menos una API key de:
- [Anthropic (Claude)](https://console.anthropic.com/) — proveedor principal
- [Groq](https://console.groq.com/) — proveedor alternativo (opcional)

---

## Instalación

### 1. Backend (Python / Flask)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Frontend (Electron)

```powershell
cd frontend
npm install
```

---

## Configuración

Crea el archivo `backend/.env` (ya existe uno de ejemplo) y rellena tus keys:

```env
# Proveedor principal: "claude" o "groq"
PRIMARY_AI_PROVIDER=claude

# Anthropic Claude
CLAUDE_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Groq (opcional)
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.2-11b-vision-preview

# Servidor Flask
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_ENV=development
```

---

## Cómo usar

### Paso 1 — Levanta el backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python run.py
```

Verás algo así cuando esté listo:

```
============================================================
  GLIMPSE Backend Server
  URL: http://127.0.0.1:5000
  AI Provider: CLAUDE
  Claude API: OK
============================================================
```

### Paso 2 — Inicia el frontend (Electron)

Abre otra terminal:

```powershell
cd frontend
npm start
```

La app aparecerá **minimizada en la bandeja del sistema** (system tray). No verás ninguna ventana abierta; eso es normal.

---

## Uso diario

### Atajos de teclado globales

| Atajo | Modo | Descripción |
|---|---|---|
| `Shift + L` | **Examen** | Responde preguntas de opción múltiple de forma concisa |
| `Shift + H` | **Estudio** | Explicación detallada del contenido capturado |
| `Shift + J` | **Rápido** | Respuesta corta y directa |
| `Ctrl + Shift + G` | — | Abre la ventana de configuración |

### Flujo de captura

1. Presiona un atajo → aparece una **pantalla de selección** sobre todo lo demás.
2. Arrastra para seleccionar la zona que quieres analizar (pregunta, imagen, texto, etc.).
3. Suelta el ratón → GLIMPSE envía la captura al backend y la IA responde.
4. El resultado aparece según el **modo de visualización** activo.

---

## Modos de visualización

Puedes cambiar el modo desde el **menú del tray** (clic derecho en el ícono de la bandeja):

| Modo | Comportamiento |
|---|---|
| 👻 **Invisible** | La respuesta aparece como un pequeño tooltip discreto junto al cursor y desaparece en 3 segundos. Ideal para exámenes. |
| 🎨 **Visual** | La respuesta aparece como una notificación completa en la esquina inferior derecha de la pantalla. |

---

## Configuración avanzada

Abre el panel de configuración con `Ctrl + Shift + G` o desde el menú del tray → **⚙️ Configuración**. Desde ahí puedes:

- Cambiar el proveedor de IA (Claude / Groq)
- Ajustar el tiempo de duración de las notificaciones
- Modificar los atajos de teclado

---

## Estructura del proyecto

```
GLIMPSE/
├── backend/          # Servidor Flask + servicios de IA
│   ├── app/
│   │   ├── api/      # Endpoints REST
│   │   ├── services/ # Claude, Groq, prompts
│   │   └── core/     # Config, logger
│   ├── requirements.txt
│   └── run.py        # Punto de entrada del servidor
└── frontend/         # App de escritorio Electron
    └── src/
        ├── main/     # Proceso principal (atajos, capturas, tray)
        ├── renderer/ # Páginas HTML (captura, notificación, settings)
        └── services/ # Cliente API, config, screenshots
```
