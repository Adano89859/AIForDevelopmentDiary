# Development Diary 📝

**Diario de desarrollo inteligente con IA** para documentar tu código de forma profesional y automática.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Características

- 🤖 **IA integrada** - Mejora automáticamente tus notas con formato Markdown rico
- 📚 **Historial visual** - Explora todas tus entradas con una interfaz moderna
- 💡 **Asistente inteligente** - Pregunta sobre problemas previos y obtén soluciones
- 🌿 **Gestión de ramas** - Organiza por proyectos y ramas de Git
- 🎨 **Interfaz moderna** - Diseño web con gradientes y efectos visuales
- 📁 **Referencias cruzadas** - El asistente identifica archivos relacionados
- 🔍 **4 modos de análisis**:
  - Buscar problemas similares
  - Sugerir soluciones
  - Identificar archivos relacionados
  - Analizar patrones de errores

---

## 🚀 Instalación Rápida

### Descargar Release
1. Ve a [Releases](https://github.com/tuusuario/development-diary/releases)
2. Descarga el ZIP de la última versión
3. Descomprime
4. Ejecuta `install.bat` (Windows) o `install.sh` (Linux/Mac)

### Instalación Manual
```bash
# Clonar repositorio
git clone https://github.com/tuusuario/development-diary.git
cd development-diary

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

**Requisitos:**
- Python 3.8+
- Ollama con modelo llama3.1:8b

---

## 📖 Uso

1. **Abre la aplicación** en http://localhost:5000
2. **Documenta tu desarrollo**:
   - Escribe o graba tus notas
   - La IA las formatea automáticamente
   - Se guardan por proyecto y rama
3. **Explora tu historial** en el visor
4. **Pregunta al asistente** sobre problemas previos

---

## 🛠️ Desarrollo

### Estructura del proyecto
```
DevelopmentDiary/
├── app.py                 # Servidor Flask
├── templates/            # HTML
├── static/              # CSS, JS
├── config/              # Configuración
└── Development Diary/   # Datos (diarios)
```

### Construir instalador
```bash
python build_installer.py
```

---

## 📝 Roadmap

- [x] Sistema de diario básico
- [x] Integración con IA (Ollama)
- [x] Visor de entradas
- [x] Asistente inteligente
- [ ] Reconocimiento de voz (Vosk)
- [ ] Exportar a PDF
- [ ] Estadísticas y gráficos
- [ ] Integración con Git

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

---

## 🙏 Agradecimientos

- [Ollama](https://ollama.ai/) - IA local
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Marked.js](https://marked.js.org/) - Renderizado Markdown

---

**¡Documenta tu código como un profesional!** 🚀