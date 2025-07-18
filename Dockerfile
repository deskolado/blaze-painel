# Usa imagem leve do Python
FROM python:3.10-slim

# Instala o Tesseract e outras dependências básicas
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Define o diretório do app
WORKDIR /app

# Copia todos os arquivos do projeto
COPY . .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Define porta para o Flask
ENV PORT=10000

# Comando para rodar a aplicação
CMD ["python", "main.py"]
