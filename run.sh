#!/bin/bash

cleanup() {
    echo "Encerrando todos os processos..."
    kill $ns_pid $srv_pid $cli_pid 2>/dev/null
}
trap cleanup EXIT 

echo "Verificando dependências do sistema..."

install_libxcb_cursor() {
    if ldd /usr/bin/python3 2>/dev/null | grep -q "libxcb-cursor"; then
        echo "libxcb-cursor já está presente."
    else
        echo "Tentando instalar libxcb-cursor0..."
        if [ -f /etc/debian_version ]; then
            sudo apt update
            sudo apt install -y libxcb-cursor0
        elif [ -f /etc/arch-release ]; then
            sudo pacman -Sy --noconfirm libxcb-cursor
        elif [ -f /etc/redhat-release ]; then
            sudo dnf install -y xcb-util-cursor
        else
            echo "Sistema operacional não reconhecido. Instale libxcb-cursor manualmente se necessário."
        fi
    fi
}

install_libxcb_cursor


echo "Iniciando nameServer..."
python -m Pyro5.nameserver & 
ns_pid=$!

echo "Iniciando servidor..."
python servidor/src/ControladoraServidor.py & 
srv_pid=$!

sleep 10

echo "Iniciando cliente..."
python cliente/src/ClienteMain.py &
cli_pid=$!

wait $cli_pid