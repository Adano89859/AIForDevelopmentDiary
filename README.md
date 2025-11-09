# Development Diary 📝

**Diario de desarrollo inteligente con IA** para documentar tu código de forma profesional y automática.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Características

### 🤖 Documentación Inteligente
- **IA integrada (Ollama)** - Mejora automáticamente tus notas con formato Markdown rico
- **Reconocimiento de voz dual**:
  - 🔒 **Vosk Offline** - Privacidad total, sin internet
  - 🌐 **Google Speech** - Máxima precisión, vocabulario actualizado
- **Auto-formato** - Convierte notas rápidas en documentación profesional

### 📚 Gestión de Entradas
- **Historial visual** - Explora todas tus entradas con interfaz moderna
- **Organización por proyectos y ramas** - Compatible con flujos de Git
- **Búsqueda avanzada** - Filtra por proyecto, rama, autor o contenido
- **Referencias cruzadas** - El asistente identifica archivos relacionados

### 💡 Asistente IA
Pregunta sobre tu historial de desarrollo con **4 modos especializados**:
- 🔍 **Buscar Similar** - "¿He tenido este error antes?"
- 💡 **Sugerir Solución** - "¿Cómo puedo resolver X?"
- 📂 **Archivos Relacionados** - "¿Qué archivos debo revisar?"
- 📊 **Análisis de Patrones** - "¿Qué errores cometo más?"

### 📄 Exportación a PDF
- **Entrada individual** - Genera PDF con formato profesional
- **Rama completa** - Exporta todas las entradas de una rama ordenadas
- **Diseño elegante** - Colores, tablas y formato Markdown

### 🎨 Interfaz Moderna
- Diseño web con gradientes y efectos visuales
- Tema oscuro optimizado para developers
- Responsive (funciona en móviles)
- Notificaciones visuales

---

## 🚀 Instalación Rápida

### Opción 1: Instalador Automático (Recomendado)

#### Windows
1. Descarga el ZIP de la última versión
2. Descomprime
3. **Click derecho** en `install.bat` → **Ejecutar como administrador**
4. Espera a que termine
5. Usa el acceso directo del escritorio

#### Linux/Mac
```bash
cd /ruta/a/development-diary
chmod +x install.sh
./install.sh
```

### Opción 2: Instalación Manual
```bash
# Clonar repositorio
git clone https://github.com/tuusuario/development-diary.git
cd development-diary

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo de IA
ollama pull llama3.1:8b

# Descargar modelo de voz (opcional)
# Opción A: Modelo grande (1.4GB, mejor precisión)
wget https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip
unzip vosk-model-es-0.42.zip

# Opción B: Modelo pequeño (50MB, más rápido)
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip

# Ejecutar
python app.py
```

**Requisitos:**
- Python 3.8+
- Ollama con modelo llama3.1:8b
- ~2GB de espacio libre (modelo de voz opcional)

---

## 📖 Uso

### 1. Documentar Desarrollo

1. Abre http://localhost:5000
2. **Escribe o graba** tus notas:
   - ✍️ Escribe directamente
   - 🎤 Graba con voz (Vosk offline o Google online)
3. **Activa "✨ Mejorar con IA"** (opcional)
4. **Guarda** - Se organiza automáticamente por proyecto y rama

### 2. Explorar Historial

1. Click en **📖 Ver Entradas**
2. **Filtra** por proyecto
3. **Busca** en títulos y contenido
4. **Click en una entrada** para verla completa
5. **Exporta a PDF**:
   - 📄 Entrada individual
   - 📚 Rama completa

### 3. Asistente IA

1. Click en **🤖 Asistente IA**
2. **Selecciona modo**:
   - 🔍 Buscar Similar
   - 💡 Sugerir Solución
   - 📂 Archivos Relacionados
   - 📊 Analizar Patrones
3. **Pregunta** sobre tu código
4. **Click en archivos** referenciados para verlos

---

## 🛠️ Desarrollo

### Estructura del proyecto
```
DevelopmentDiary/
├── app.py                      # Servidor Flask principal
├── requirements.txt            # Dependencias Python
├── setup.py                    # Configuración de instalación
├── build_installer.py          # Script para crear instalador
│
├── templates/                  # Plantillas HTML
│   ├── index.html             # Página principal
│   ├── viewer.html            # Visor de entradas
│   └── assistant.html         # Asistente IA
│
├── static/                     # Recursos estáticos
│   ├── css/
│   │   ├── style.css          # Estilos principales
│   │   ├── viewer.css         # Estilos del visor
│   │   └── assistant-page.css # Estilos del asistente
│   └── js/
│       ├── app.js             # JavaScript principal
│       ├── viewer.js          # Lógica del visor
│       └── assistant-page.js  # Lógica del asistente
│
├── diary/                      # Módulos del diario
│   └── pdf_generator.py       # Generador de PDFs
│
├── config/                     # Configuración
│   └── config_manager.py      # Gestor de configuración
│
├── core/                       # Lógica del negocio
│   └── diary_logic.py         # Lógica del diario
│
├── installer/                  # Scripts de instalación
│   ├── install.bat            # Instalador Windows
│   ├── install.sh             # Instalador Linux/Mac
│   └── README_INSTALL.md      # Guía de instalación
│
├── vosk-model-es-0.42/        # Modelo de voz (opcional)
└── Development Diary/          # Datos (diarios)
    └── [Proyectos]/
        └── entries/
            └── *.md           # Entradas en Markdown
```

### Construir instalador
```bash
python build_installer.py
```

Esto genera una carpeta `installer_package/` con todo listo para distribuir.

---

## 🎯 Características Técnicas

### Backend (Python/Flask)
- Flask 3.0+ para servidor web
- Ollama para IA local (llama3.1:8b)
- Vosk para reconocimiento de voz offline
- Google Speech API para voz online
- ReportLab para generación de PDFs

### Frontend (HTML/CSS/JS)
- Vanilla JavaScript (sin frameworks)
- CSS moderno con gradientes y glassmorphism
- Marked.js para renderizado Markdown
- MediaRecorder API para captura de audio

### Almacenamiento
- Archivos Markdown con frontmatter YAML
- Organización por proyecto/rama/fecha
- Compatible con Git y versionado

---

## 📝 Roadmap

- [x] Sistema de diario básico
- [x] Integración con IA (Ollama)
- [x] Visor de entradas con búsqueda
- [x] Asistente inteligente con 4 modos
- [x] Reconocimiento de voz (Vosk + Google)
- [x] Exportar a PDF (individual y rama)
- [x] Sistema de instalación automático
- [ ] Estadísticas y gráficos
- [ ] Integración directa con Git
- [ ] Modo colaborativo (multi-usuario)
- [ ] Sincronización en la nube
- [ ] App móvil

---

## 📄 Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

---

## 🙏 Agradecimientos

- [Ollama](https://ollama.ai/) - IA local sin costos
- [Vosk](https://alphacephei.com/vosk/) - Reconocimiento de voz offline
- [Flask](https://flask.palletsprojects.com/) - Framework web minimalista
- [ReportLab](https://www.reportlab.com/) - Generación de PDFs
- [Marked.js](https://marked.js.org/) - Renderizado Markdown en navegador
- [Google Speech API](https://cloud.google.com/speech-to-text) - Transcripción de alta precisión

---

## 📞 Contacto

- **Proyecto:** [GitHub Repository](https://github.com/Adano89859/AIForDevelopmentDiary)

---

**¡Documenta tu código como un profesional!** 🚀

*Hecho con ❤️ por developers para developers*