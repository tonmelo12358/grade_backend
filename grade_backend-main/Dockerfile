# Use uma imagem base do Python
FROM python:3.11-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o contêiner
COPY . .

# Define o comando de execução da API
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
