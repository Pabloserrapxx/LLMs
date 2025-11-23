# Use uma imagem base leve
FROM python:3.9-slim

# Define o diretório de trabalho como /app
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código (backend e frontend)
COPY . .

# Muda para o diretório do backend para rodar o uvicorn
WORKDIR /app/backend

# Comando para iniciar o servidor Uvicorn
# host 0.0.0.0 permite acesso externo ao container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
