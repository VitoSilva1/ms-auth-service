# Imagen base
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos requerimientos e instalamos dependencias
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el proyecto completo
COPY ./app ./app

# Comando para correr el microservicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]