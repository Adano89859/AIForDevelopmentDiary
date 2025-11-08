# Development Diary - Guía de Instalación

## 📦 Requisitos Previos

### Windows
- **Python 3.8+** - [Descargar](https://www.python.org/downloads/)
  - ⚠️ Marca "Add Python to PATH" durante la instalación
- **Ollama** - [Descargar](https://ollama.ai/download)

### Linux/Mac
- **Python 3.8+** (generalmente ya instalado)
- **Ollama** - [Descargar](https://ollama.ai/download)

---

## 🚀 Instalación

### Windows

1. **Descomprime** el archivo ZIP
2. **Click derecho** en `install.bat`
3. **Selecciona** "Ejecutar como administrador"
4. **Espera** a que termine la instalación
5. **Usa el acceso directo** en el escritorio

### Linux/Mac
```bash
# Navegar a la carpeta
cd /ruta/a/development-diary

# Dar permisos
chmod +x install.sh

# Ejecutar instalador
./install.sh
```

---

## ▶️ Ejecutar la aplicación

### Opción 1: Acceso directo (Windows)
- Doble click en el acceso directo del escritorio

### Opción 2: Ejecutable
```bash
# Windows
DevelopmentDiary.exe

# Linux/Mac
./DevelopmentDiary
```

### Opción 3: Python directo
```bash
python app.py
```

La aplicación se abrirá en: **http://localhost:5000**

---

## 🔧 Solución de Problemas

### "Python no encontrado"
- Reinstala Python y marca "Add to PATH"
- O añade manualmente Python al PATH del sistema

### "Ollama no encontrado"
- Instala Ollama desde https://ollama.ai/download
- Reinicia la terminal después de instalar

### "Error al descargar modelo"
- Verifica tu conexión a internet
- El modelo pesa ~4.7GB, puede tardar
- Intenta manualmente: `ollama pull llama3.1:8b`

### Puerto 5000 en uso
- Edita `app.py` y cambia `port=5000` a otro puerto

---

## 📝 Notas

- Los diarios se guardan en: `Development Diary/`
- Puedes mover esta carpeta sin problemas
- La aplicación necesita Ollama corriendo en segundo plano

---

## 🆘 Soporte

Si tienes problemas:
1. Revisa la consola para ver errores
2. Verifica que Ollama está corriendo: `ollama list`
3. Verifica Python: `python --version`

¡Disfruta documentando tu código! 📝✨