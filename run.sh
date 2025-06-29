#!/bin/bash

# Nombre del entorno virtual
VENV_DIR="env"

# Activar entorno virtual o crearlo si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual"
    python3 -m venv "$VENV_DIR"
    echo "Entorno virtual creado en '$VENV_DIR'"
fi

# Activar entorno virtual
source "$VENV_DIR/bin/activate"

if [ ! -f "$VENV_DIR/requirements.installed" ]; then
    echo "Instalando dependencias"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch "$VENV_DIR/requirements.installed"
    echo "Dependencias instaladas."
fi

# Verificar si .gitignore existe, si no, crearlo
if [ ! -f ".gitignore" ]; then
    touch .gitignore
    echo "Archivo .gitignore creado."
    echo "$VENV_DIR/" >> .gitignore
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

python3 run.py
