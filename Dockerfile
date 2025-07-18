# Base com Python 3
FROM python:3.10-slim

# Instalações de sistema necessárias (incluindo tesseract)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    && apt-get clean

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto para o container
COPY . .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Porta do Flask
ENV PORT 10000

# Comando para iniciar o app
CMD ["python", "main.py"]
