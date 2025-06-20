.PHONY: all stop

all:
	@echo "Iniciando nameServer e servidor em paralelo..."
	@python -m Pyro5.nameserver & echo $$! > nameserver.pid; \
	python servidor/src/ControladoraServidor.py & echo $$! > servidor.pid; \
	sleep 2; \
	echo "Iniciando cliente..."; \
	python cliente/src/ClienteMain.py & echo $$! > cliente.pid

stop:
	@echo "Parando todos os processos..."
	@-kill -9 $$(cat nameserver.pid) 2>/dev/null || true
	@-kill -9 $$(cat servidor.pid) 2>/dev/null || true
	@-kill -9 $$(cat cliente.pid) 2>/dev/null || true
	@rm -f *.pid