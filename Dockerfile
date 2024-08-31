# Utilizar una imagen base oficial de Python 3.10
FROM python:3.10-slim

# Crear un usuario sin privilegios
RUN addgroup --system appgroup && adduser --system --group appuser

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos a la imagen
COPY requirements.txt .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copiar el resto del código de la aplicación al contenedor
COPY . .

# Cambiar al usuario sin privilegios
USER appuser:appgroup

# Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
