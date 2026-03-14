#!/bin/bash
# Script de auto-instalação e execução para Linux

echo "--- Albion Online Road Script (Linux Bootstrap) ---"

# Detectar gerenciador de pacotes
if [ -f /etc/debian_version ]; then
    PKGMGR="sudo apt-get install -y"
    DEPS="python3-tk python3-pip libx11-6"
elif [ -f /etc/redhat-release ]; then
    PKGMGR="sudo dnf install -y"
    DEPS="python3-tkinter python3-pip libX11"
else
    echo "Distribuição não detectada automaticamente. Por favor, instale python3-tk e libx11 manualmente."
fi

if [ ! -z "$PKGMGR" ]; then
    echo "Instalando dependências do sistema..."
    $PKGMGR $DEPS
fi

echo "Configurando ambiente Python..."
python3 -m venv .venv_linux
source .venv_linux/bin/activate

echo "Instalando bibliotecas Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Dando permissões de execução..."
chmod +x main.py

echo "Iniciando aplicação..."
python3 main.py
