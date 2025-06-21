#!/bin/bash

cleanup() {
    echo "Encerrando todos os processos..."
    kill $ns_pid $srv_pid $cli_pid 2>/dev/null
}
trap cleanup EXIT 

echo "Verificando dependências do sistema..."

install_libxcb_cursor() {
    # Verifica se a biblioteca já está presente no sistema
    if ldconfig -p | grep -q "libxcb-cursor"; then
        echo "Biblioteca libxcb-cursor já está instalada."
        return
    fi

    echo "Biblioteca libxcb-cursor NÃO encontrada. Tentando instalar..."

    # Detecta distribuição e instala usando o gerenciador de pacotes adequado
    if [ -f /etc/debian_version ]; then
        echo "Distribuição baseada em Debian detectada."
        sudo apt update
        sudo apt install -y libxcb-cursor0
    elif [ -f /etc/arch-release ]; then
        echo "Distribuição baseada em Arch Linux detectada."
        sudo pacman -Sy --noconfirm libxcb-cursor
    elif [ -f /etc/redhat-release ]; then
        echo "Distribuição baseada em Red Hat detectada."
        sudo dnf install -y xcb-util-cursor
    else
        echo "Sistema operacional não reconhecido. Instale a biblioteca libxcb-cursor manualmente se necessário."
    fi
}

install_libxcb_cursor


echo "Iniciando nameServer..."
python -m Pyro5.nameserver & 
ns_pid=$!

echo "Iniciando servidor..."
python servidor/src/ControladoraServidor.py & 
srv_pid=$!

sleep 8

echo "Iniciando cliente..."
python cliente/src/ClienteMain.py &
cli_pid=$!

wait $cli_pid