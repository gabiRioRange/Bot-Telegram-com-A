# Usa Python 3.12
FROM python:3.12-slim

# Define diretório
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala libs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código (Lembre de NÃO ter a linha COPY .env .)
COPY src/ ./src/
COPY run.py .
COPY dashboard.py .

# Cria pasta de dados
RUN mkdir -p data/lancedb-store

# Comando padrão
CMD ["python", "run.py"]