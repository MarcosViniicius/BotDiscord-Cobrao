# Dockerfile para Bot Discord Cobrão
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Variáveis de ambiente (pode ser sobrescrito pelo docker-compose)
ENV PYTHONUNBUFFERED=1

# Comando para iniciar o bot
CMD ["python", "main.py"]
