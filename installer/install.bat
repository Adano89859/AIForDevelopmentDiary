@echo off
chcp 65001 > nul
color 0A
title Development Diary - Instalador

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         DEVELOPMENT DIARY - INSTALADOR AUTOMÁTICO            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Este instalador necesita privilegios de administrador
    echo [!] Click derecho en install.bat y "Ejecutar como administrador"
    pause
    exit /b 1
)

echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Python no está instalado
    echo [!] Descárgalo desde: https://www.python.org/downloads/
    echo [!] Asegúrate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)
python --version
echo [✓] Python encontrado

echo.
echo [2/6] Verificando Ollama...
ollama --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Ollama no está instalado
    echo [!] Descárgalo desde: https://ollama.ai/download
    pause
    exit /b 1
)
ollama --version
echo [✓] Ollama encontrado

echo.
echo [3/6] Verificando modelo llama3.1:8b...
ollama list | findstr "llama3.1:8b" >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Modelo llama3.1:8b no encontrado
    echo [→] Descargando modelo (esto puede tardar varios minutos)...
    ollama pull llama3.1:8b
    if %errorLevel% neq 0 (
        echo [!] Error descargando el modelo
        pause
        exit /b 1
    )
)
echo [✓] Modelo llama3.1:8b listo

echo.
echo.
echo [4/7] Instalando dependencias de Python...
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo [!] Error instalando dependencias
    pause
    exit /b 1
)
echo [✓] Dependencias instaladas

echo.
echo [5/7] Verificando modelo de voz Vosk (opcional)...
if exist "vosk-model-es-0.42" (
    echo [✓] Modelo grande de Vosk encontrado
) else if exist "vosk-model-small-es-0.42" (
    echo [✓] Modelo pequeño de Vosk encontrado
) else (
    echo [i] Modelo de Vosk no encontrado (opcional)
    echo [i] La aplicación usará Google Speech (online) por defecto
    echo [i] Para modo offline, descarga:
    echo     https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip
)

echo.
echo [6/7] Creando carpeta de datos...
if not exist "Development Diary" mkdir "Development Diary"
echo [✓] Carpeta creada

echo.
echo [7/7] Creando acceso directo...
set SCRIPT_DIR=%~dp0
set TARGET=%SCRIPT_DIR%DevelopmentDiary.exe
set SHORTCUT=%USERPROFILE%\Desktop\Development Diary.lnk

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%TARGET%'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Save()"

if exist "%SHORTCUT%" (
    echo [✓] Acceso directo creado en el escritorio
) else (
    echo [!] No se pudo crear el acceso directo
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              ✓ INSTALACIÓN COMPLETADA ✓                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo [→] Puedes iniciar la aplicación desde:
echo     - El acceso directo en el escritorio
echo     - O ejecutando: DevelopmentDiary.exe
echo.
echo [→] La aplicación se abrirá en: http://localhost:5000
echo.

pause