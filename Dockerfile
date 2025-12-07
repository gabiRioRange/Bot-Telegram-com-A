# 1. Usa uma imagem oficial do Python leve (Slim)
FROM python:3.10-slim

# 2. Define o fuso horário para o Brasil (Opcional, mas bom para logs)
ENV TZ=America/Sao_Paulo

# 3. Cria a pasta de trabalho dentro do container
WORKDIR /app

# 4. Copia apenas o requirements primeiro (para aproveitar o cache)
COPY requirements.txt .

# 5. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o resto do código para dentro
COPY . .

# 7. Comando para rodar o bot
CMD ["python", "bot.py"]