FROM python:3.11.9

WORKDIR /app

COPY sensor.proto .
COPY pressure_sensor.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt\
&& python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. sensor.proto
CMD ["python", "pressure_sensor.py"]