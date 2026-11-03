# Imagem base com Python
FROM python:3.12-slim

# Diretorio de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependencias
COPY requirements.txt .

# Instala as bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Copia o codigo da aplicacao
COPY app.py .

# Informa a porta utilizada pela aplicacao
EXPOSE 8000

# Comando executado ao iniciar o container
CMD ["python", "app.py"]