#!/bin/bash

cleanup() {
    echo "Encerrando todos os processos..."
    kill $ns_pid $srv_pid $cli_pid 2>/dev/null
}
trap cleanup EXIT 

echo "Iniciando nameServer..."
python -m Pyro5.nameserver & 
ns_pid=$!

echo "Iniciando servidor..."
python servidor/src/ControladoraServidor.py & 
srv_pid=$!

sleep 2

echo "Iniciando cliente..."
python cliente/src/ClienteMain.py &
cli_pid=$!

wait $cli_pid