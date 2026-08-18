# Usar una imagen base ligera de Python 3.11
FROM python:3.13

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias de Python
COPY requerimientos.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requerimientos.txt

# Copiar el código del proyecto al contenedor. Copia todos los archivos desde tu proyecto en mi maquina dentro de la imagen contenedor usando la isntrucción COPY
COPY . .

# Exponer el puerto predeterminado de Cloud Run (8080)
EXPOSE 8080

#No corre por el usuario root
RUN useradd app

# Comando para arrancar la aplicación con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]