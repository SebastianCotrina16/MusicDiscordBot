# Utilice una imagen base de Python
FROM python:3.9-slim-buster

# Mantenga el pip al día
RUN pip install --no-cache-dir --upgrade pip

# Crear un directorio de trabajo
WORKDIR /app

# Instale las dependencias de FFmpeg y libffi
RUN apt-get update && \
    apt-get install -y ffmpeg libffi-dev && \
    apt-get clean

# Copie los archivos del proyecto
COPY . /app

# Instale las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Ejecute el bot de discord cuando el contenedor se inicie.
CMD ["python", "-m", "bot"]
