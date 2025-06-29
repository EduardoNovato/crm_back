#!/bin/bash

# Detectar sistema operativo
OS_TYPE="$(uname -s)"
case "$OS_TYPE" in
    Linux*)     OS="Linux" ;;
    Darwin*)    OS="Mac" ;;
    CYGWIN*|MINGW*|MSYS*) OS="Windows" ;;
    *)          OS="Desconocido" ;;
esac

echo "Sistema operativo detectado: $OS"

# Detectar si usar python o python3
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Python no está instalado. Abortando."
    exit 1
fi

# Nombre del entorno virtual
VENV_DIR="env"

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual"
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo "Entorno virtual creado en '$VENV_DIR'"
fi

# Activar entorno virtual según sistema
if [ "$OS" = "Windows" ]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# Instalar dependencias si aún no se han instalado
if [ ! -f "$VENV_DIR/requirements.installed" ]; then
    echo "Instalando dependencias"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch "$VENV_DIR/requirements.installed"
    echo "Dependencias instaladas."
fi

# Verificar o crear .gitignore
if [ ! -f ".gitignore" ]; then
    echo "Creando archivo .gitignore"
    echo "$VENV_DIR/" > .gitignore
    echo ".env" >> .gitignore
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo "*.pyo" >> .gitignore
    echo "*.pyd" >> .gitignore
    echo "instance/" >> .gitignore
    echo "*.db" >> .gitignore
    echo "Archivo .gitignore creado."
fi

# Cargar variables de entorno desde .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Archivo .env no encontrado. Abortando."
    exit 1
fi

# Definir entorno: dev o prod
ENV=${1:-dev}

if [ "$ENV" = "dev" ]; then
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    echo "Ejecutando en modo DESARROLLO"
elif [ "$ENV" = "prod" ]; then
    export FLASK_ENV=production
    export FLASK_DEBUG=0
    echo "Ejecutando en modo PRODUCCIÓN"
else
    echo "Entorno desconocido: $ENV"
    echo "Uso: ./run.sh [dev|prod]"
    exit 1
fi

# Ejecutar app
$PYTHON_CMD run.py
