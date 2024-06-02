# Use uma imagem base que tenha Python e outras dependências necessárias
FROM python:3.12.3-windowsservercore

# Defina o diretório de trabalho como /app
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho no contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos para o diretório de trabalho no contêiner
COPY . .

# Exponha a porta 5000 para o serviço Flask (se necessário)
# EXPOSE 5000

# Execute o serviço quando o contêiner for iniciado
CMD ["python", "hand_detection_service.py"]
