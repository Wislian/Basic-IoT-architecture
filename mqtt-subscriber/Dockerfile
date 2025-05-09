FROM python:3.11.9

WORKDIR /app

# Instalar dependencias
RUN pip install paho-mqtt
RUN pip install psycopg2

# Copiar el código fuente
COPY subscriber.py .

# Comando para ejecutar el suscriptor
CMD ["python", "subscriber.py"]