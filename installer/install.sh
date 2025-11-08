#!/bin/bash

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         DEVELOPMENT DIARY - INSTALADOR AUTOMÁTICO            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Función para verificar comandos
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}[✓]${NC} $2 encontrado"
        return 0
    else
        echo -e "${RED}[!]${NC} $2 no encontrado"
        return 1
    fi
}

# 1. Verificar Python
echo -e "\n${YELLOW}[1/6]${NC} Verificando Python..."
if check_command python3 "Python"; then
    python3 --version
else
    echo -e "${RED}[!]${NC} Instala Python 3.8 o superior"
    echo "    Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "    macOS: brew install python3"
    exit 1
fi

# 2. Verificar pip
echo -e "\n${YELLOW}[2/6]${NC} Verificando pip..."
if check_command pip3 "pip"; then
    pip3 --version
else
    echo -e "${RED}[!]${NC} Instalando pip..."
    python3 -m ensurepip --upgrade
fi

# 3. Verificar Ollama
echo -e "\n${YELLOW}[3/6]${NC} Verificando Ollama..."
if check_command ollama "Ollama"; then
    ollama --version
else
    echo -e "${RED}[!]${NC} Ollama no está instalado"
    echo "    Descarga desde: https://ollama.ai/download"
    exit 1
fi

# 4. Verificar modelo
echo -e "\n${YELLOW}[4/6]${NC} Verificando modelo llama3.1:8b..."
if ollama list | grep -q "llama3.1:8b"; then
    echo -e "${GREEN}[✓]${NC} Modelo llama3.1:8b listo"
else
    echo -e "${YELLOW}[→]${NC} Descargando modelo (esto puede tardar)..."
    ollama pull llama3.1:8b
    if [ $? -ne 0 ]; then
        echo -e "${RED}[!]${NC} Error descargando el modelo"
        exit 1
    fi
fi

# 5. Instalar dependencias
echo -e "\n${YELLOW}[5/6]${NC} Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}[!]${NC} Error instalando dependencias"
    exit 1
fi
echo -e "${GREEN}[✓]${NC} Dependencias instaladas"

# 6. Crear carpeta de datos
echo -e "\n${YELLOW}[6/6]${NC} Creando carpeta de datos..."
mkdir -p "Development Diary"
echo -e "${GREEN}[✓]${NC} Carpeta creada"

# Dar permisos de ejecución
chmod +x DevelopmentDiary 2>/dev/null || true

echo -e "\n${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              ✓ INSTALACIÓN COMPLETADA ✓                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}[→]${NC} Puedes iniciar la aplicación:"
echo "    ./DevelopmentDiary"
echo ""
echo -e "${GREEN}[→]${NC} O directamente con Python:"
echo "    python3 app.py"
echo ""
echo -e "${GREEN}[→]${NC} La aplicación se abrirá en: http://localhost:5000"
echo ""