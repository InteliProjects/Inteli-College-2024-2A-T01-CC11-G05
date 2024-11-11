# Use uma imagem base do Python
FROM python:3.11-slim

# Teste
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-por\
    && apt-get clean

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie os arquivos de requisitos
COPY requirements.txt .

RUN pip install --upgrade pip

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código-fonte do backend
COPY . .

# Comando para rodar o backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]