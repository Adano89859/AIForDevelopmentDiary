# Development Diary - Guía de Instalación Completa

## 📦 Requisitos Previos

### Windows
- **Python 3.8+** - [Descargar](https://www.python.org/downloads/)
  - ⚠️ **IMPORTANTE:** Marca "Add Python to PATH" durante la instalación
- **Ollama** - [Descargar](https://ollama.ai/download)
- **Conexión a internet** - Para descargar modelo de IA (~4.7GB)

### Linux/Mac
- **Python 3.8+** (generalmente ya instalado)
  - Ubuntu/Debian: `sudo apt install python3 python3-pip`
  - macOS: `brew install python3`
- **Ollama** - [Descargar](https://ollama.ai/download)
- **Conexión a internet** - Para descargar modelo de IA

---

## 🚀 Instalación Automática (Recomendado)

### Windows

1. **Descomprime** el archivo ZIP en tu ubicación preferida
2. **Click derecho** en `install.bat`
3. **Selecciona** "Ejecutar como administrador"
4. **Espera** a que termine (puede tardar varios minutos):
   - ✅ Verifica Python
   - ✅ Verifica Ollama
   - ✅ Descarga modelo llama3.1:8b (~4.7GB)
   - ✅ Instala dependencias Python
   - ✅ Crea carpeta de datos
   - ✅ Genera acceso directo en el escritorio
5. **¡Listo!** Usa el acceso directo del escritorio

### Linux/Mac
```bash
# 1. Navegar a la carpeta
cd /ruta/a/development-diary

# 2. Dar permisos de ejecución
chmod +x install.sh

# 3. Ejecutar instalador
./install.sh

# 4. ¡Listo! Ejecutar aplicación
python3 app.py
```

---

## ▶️ Ejecutar la Aplicación

### Opción 1: Acceso directo (Windows)
- Doble click en el acceso directo del escritorio
- O ejecuta `DevelopmentDiary.exe`

### Opción 2: Ejecutable
```bash
# Windows
DevelopmentDiary.exe

# Linux/Mac
./DevelopmentDiary
```

### Opción 3: Python directo
```bash
# Windows
python app.py

# Linux/Mac
python3 app.py
```

**La aplicación se abrirá automáticamente en:** http://localhost:5000

---

## 🎤 Configuración de Reconocimiento de Voz (Opcional)

La aplicación incluye **dos métodos** de reconocimiento de voz:

### 🌐 Google Speech (Online) - Predeterminado
- ✅ **Máxima precisión** (~98%)
- ✅ **Vocabulario actualizado**
- ✅ **No requiere descargas**
- ⚠️ Requiere internet
- ⚠️ Límite gratuito: ~60 min/día

**Ya funciona sin configuración adicional.**

### 🔒 Vosk (Offline) - Privacidad
- ✅ **Sin internet**
- ✅ **Privacidad total**
- ✅ **Sin límites de uso**
- ⚠️ Requiere descargar modelo (~50MB o 1.4GB)

**Para activar Vosk:**

#### Opción A: Modelo grande (mejor precisión)
```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip" -OutFile "vosk-model.zip"
Expand-Archive -Path "vosk-model.zip" -DestinationPath "."
Remove-Item "vosk-model.zip"

# Linux/Mac
wget https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip
unzip vosk-model-es-0.42.zip
rm vosk-model-es-0.42.zip
```

#### Opción B: Modelo pequeño (más rápido)
```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip" -OutFile "vosk-small.zip"
Expand-Archive -Path "vosk-small.zip" -DestinationPath "."
Remove-Item "vosk-small.zip"

# Linux/Mac
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
rm vosk-model-small-es-0.42.zip
```

Una vez descargado, selecciona **🔒 Offline (Vosk)** en el dropdown de la aplicación.

---

## 📖 Guía Rápida de Uso

### 1. Documentar tu Código
1. Abre http://localhost:5000
2. Rellena: Autor, Proyecto, Rama, Commit/Problema
3. **Escribe o graba** tus notas:
   - ✍️ Escribe directamente
   - 🎤 Click en "Grabar" y habla
4. Activa "✨ Mejorar con IA" para formato automático
5. Click en "💾 Guardar Entrada"

### 2. Ver tu Historial
1. Click en "📖 Ver Entradas"
2. Explora tus entradas ordenadas por fecha
3. Filtra por proyecto
4. Busca en títulos y contenido
5. Click en una entrada para verla completa

### 3. Exportar a PDF
- **📄 PDF** - Exporta una entrada individual
- **📚 Rama completa** - Exporta todas las entradas de esa rama

### 4. Asistente IA
1. Click en "🤖 Asistente IA"
2. Selecciona modo:
   - 🔍 **Buscar Similar** - Encuentra problemas previos
   - 💡 **Sugerir Solución** - Obtén soluciones
   - 📂 **Archivos** - Identifica archivos relacionados
   - 📊 **Analizar** - Detecta patrones
3. Pregunta sobre tu código
4. Click en archivos referenciados para verlos

---

## 🔧 Solución de Problemas

### "Python no encontrado"
**Windows:**
1. Reinstala Python desde https://python.org/downloads
2. **MARCA "Add Python to PATH"** durante instalación
3. Reinicia la terminal

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python3
```

### "Ollama no encontrado"
1. Instala Ollama desde https://ollama.ai/download
2. Reinicia la terminal después de instalar
3. Verifica: `ollama --version`

### "Error al descargar modelo llama3.1:8b"
- Verifica conexión a internet
- El modelo pesa ~4.7GB, puede tardar 10-30 minutos
- Intenta manualmente:
```bash
  ollama pull llama3.1:8b
```

### "Puerto 5000 en uso"
1. Edita `app.py`
2. Busca la línea: `app.run(..., port=5000)`
3. Cambia `5000` por otro puerto (ej: `5001`)
4. Guarda y ejecuta de nuevo

### "Micrófono no funciona"
1. **Permite permisos** del micrófono en el navegador
2. Verifica que el micrófono funciona en otras apps
3. Prueba con ambos modos:
   - 🌐 Online (Google) - Predeterminado
   - 🔒 Offline (Vosk) - Si descargaste el modelo

### "Error generando PDF"
- Asegúrate de tener instalado: `pip install reportlab markdown2`
- Verifica que la carpeta `diary/` existe
- Reinicia la aplicación

### "La IA no mejora el texto"
1. Verifica que Ollama está corriendo:
```bash
   ollama list
```
2. Debería aparecer `llama3.1:8b`
3. Si no está, descárgalo:
```bash
   ollama pull llama3.1:8b
```

---

## 📝 Notas Importantes

- **Ubicación de datos:** Los diarios se guardan en `Development Diary/`
- **Portabilidad:** Puedes mover toda la carpeta sin problemas
- **Ollama:** Debe estar corriendo en segundo plano
- **Privacidad:** 
  - Vosk: Todo offline, datos en tu máquina
  - Google: Audio se envía a Google para transcripción
- **Límites:**
  - Google Speech: ~60 minutos/día gratis
  - Vosk: Sin límites
  - La conversión de voz a texto suele ser poco precisa

---

## 🆘 Soporte y Ayuda

### Verificar instalación
```bash
# Python
python --version    # Debe mostrar 3.8 o superior

# Ollama
ollama --version
ollama list         # Debe aparecer llama3.1:8b

# Dependencias Python
pip list | grep flask
pip list | grep vosk
```

### Logs y errores
- Los errores aparecen en la **consola** donde ejecutaste `python app.py`
- Copia el error completo para buscar ayuda

### Recursos
- **GitHub Issues:** [Reportar problemas](https://github.com/Adano89859/AIForDevelopmentDiary)
- **Documentación:** Ver `README.md`

---

## 🎉 ¡Listo para usar!

Ya puedes empezar a documentar tu código de forma profesional.

**Consejos:**
- 📝 Documenta al final del día mientras está fresco
- 🎤 Usa el micrófono para ser más rápido
- 🤖 Activa la IA para formato profesional
- 📊 Pregunta al asistente sobre errores recurrentes
- 📄 Exporta PDFs para reportes semanales

**¡Disfruta documentando tu código!** 📝✨