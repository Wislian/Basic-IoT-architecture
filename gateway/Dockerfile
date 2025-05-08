FROM python:3.11.9

WORKDIR /app

COPY . .
#COPY sensor.proto .
#COPY gateway.py .
#COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

#RUN sleep 5 && python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. sensor.proto


CMD ["python", "gateway.py"]