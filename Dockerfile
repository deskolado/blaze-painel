FROM python:3.10-slim

# Instala Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr libglib2.0-0 libsm6 libxext6 libxrender-dev && apt-get clean

# Cria diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto para o container
COPY . /app

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Flask
EXPOSE 10000

# Comando para iniciar o app
CMD ["python", "main.py"]
