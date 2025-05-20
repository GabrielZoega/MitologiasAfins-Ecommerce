FROM python:3.10-slim

# Desabilitar bufferização da saída
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY src/ ./src/

#EXPOSE 3000

CMD ["python", "src/EndPointServidor.py"]