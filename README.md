# BASIC IOT ARCHITECTURE

This project implements a basic IoT architecture focused on the healthcare sector that simulates medical data collection from devices (sensors), processing through a gateway, and storage in a PostgreSQL database using MQTT communication.

## System Architecture

![Basic IoT Architecture](add_url)

The system consists of the following main components:

1. **Simulated Sensors**: Generate simulated medical data (body temperature, blood pressure, and heart rate)
2. **IoT Gateway**: Receives data from sensors through various protocols and publishes them to an MQTT broker
3. **MQTT Broker**: Manages communication between publishers and subscribers
4. **MQTT Subscriber**: Listens to topics of interest and stores data in PostgreSQL
5. **PostgreSQL Database**: Stores medical data for later analysis

All components run in Docker containers orchestrated using Docker Compose.

## Project Structure

```
basic-Iot-architecture/
├── docker-compose.yml
├── README.md
├── sensors/
│   ├── temperature_sensor/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── temperature_sensor.py
│   ├── pressure_sensor/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── sensor.proto
│   │   └── pressure_sensor.py
│   └── heartrate_sensor/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── heartrate_sensor.py
├── gateway/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── sensor.proto
│   └── gateway.py
├── mqtt_broker/
│   ├── Dockerfile
│   └── mosquitto.conf
├── subscriber/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── subscriber.py
└── db/
    ├── init.sql
    └── Dockerfile
```

## Technologies Used

- **Communication Protocols**: REST, WebSockets, gRPC, MQTT
- **Languages**: Python
- **Containers**: Docker, Docker Compose
- **Database**: PostgreSQL
- **MQTT Broker**: Eclipse Mosquitto

## Components

### 1. Simulated Sensors

#### Temperature Sensor
Generates body temperature data and sends it using the REST protocol.

```python
# Simplified example of temperature_sensor.py
import requests, random, datetime, time

def generate_temperature():
    return {
        "sensor_id": "Temp_001",
        "value": round(random.uniform(35, 38), 2),
        "unit": "C",
        "date": datetime.datetime.now().isoformat()
    }

# Sends data every 10 seconds using REST
```

#### Blood Pressure Sensor
Generates blood pressure data (systolic and diastolic) and sends it using gRPC.

```python
# Simplified example of pressure_sensor.py
import grpc, random, datetime
import sensor_pb2, sensor_pb2_grpc

def generate_pressure():
    return sensor_pb2.SensorData(
        sensor_id = "Press_001",
        systolic = round(random.uniform(100, 140), 1),
        diastolic = round(random.uniform(60, 90), 1),
        unit = "mmHg",
        date = datetime.datetime.now().isoformat()
    )

# Sends data every 10 seconds using gRPC
```

#### Heart Rate Sensor
Generates heart rate data and sends it using WebSockets.

```python
# Simplified example of heartrate_sensor.py
import websockets, asyncio, random, datetime, json

def generate_heart_rate():
    return {
        "sensor_id": "Heart_001",
        "value": random.randint(60, 100),
        "unit": "bpm",
        "date": datetime.datetime.now().isoformat()
    }

# Sends data every 7 seconds using WebSockets
```

### 2. IoT Gateway

The gateway receives data from different sensors through three different protocols:
- REST (HTTP): For the temperature sensor
- WebSockets: For the heart rate sensor
- gRPC: For the blood pressure sensor

After receiving the data, the gateway processes it and publishes it to the corresponding MQTT topics.

```python
# Simplified example of gateway.py
from flask import Flask, request
from flask_sock import Sock
import paho.mqtt.client as mqtt
import grpc
import sensor_pb2_grpc

# Handles REST requests
@app.route('/temperature', methods=['POST'])
def handle_temperature():
    # Receives and publishes temperature data

# Handles WebSocket connections
@sock.route('/heartrate')
def handle_heart_rate(ws):
    # Receives and publishes heart rate data

# Handles gRPC calls
class PressureSensor(sensor_pb2_grpc.SensorServiceServicer):
    # Receives and publishes blood pressure data
```

### 3. MQTT Broker

Eclipse Mosquitto is used as an MQTT broker to manage communication between the gateway (publisher) and the MQTT subscriber.

### 4. MQTT Subscriber

The MQTT subscriber listens to relevant topics and stores received data in the PostgreSQL database.

```python
# Simplified example of subscriber.py
import paho.mqtt.client as mqtt
import psycopg2
import json

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    
    # Insert data into PostgreSQL based on the sensor type
    # ...

# Subscription to topics: temperature, pressure, heartRate
```

### 5. PostgreSQL Database

The database stores sensor data for later analysis.

## Database Design

The PostgreSQL database is designed to store different types of medical data from various sensors. The database schema consists of three main tables:

### Temperature Table
```sql
CREATE TABLE temperature (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    value DECIMAL(5,2) NOT NULL,
    unit VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
```

### Blood Pressure Table
```sql
CREATE TABLE pressure (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    systolic DECIMAL(5,1) NOT NULL,
    diastolic DECIMAL(5,1) NOT NULL,
    unit VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
```

### Heart Rate Table
```sql
CREATE TABLE heart_rate (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    value INTEGER NOT NULL,
    unit VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
```

### Entity Relationship Diagram (ERD)

```
temperature
+------------+-------------+------+-----+---------+
| Field      | Type        | Null | Key | Default |
+------------+-------------+------+-----+---------+
| id         | SERIAL      | NO   | PK  | AUTO    |
| sensor_id  | VARCHAR(50) | NO   |     | NULL    |
| value      | DECIMAL(5,2)| NO   |     | NULL    |
| unit       | VARCHAR(10) | NO   |     | NULL    |
| timestamp  | TIMESTAMP   | NO   |     | NULL    |
+------------+-------------+------+-----+---------+

pressure
+------------+-------------+------+-----+---------+
| Field      | Type        | Null | Key | Default |
+------------+-------------+------+-----+---------+
| id         | SERIAL      | NO   | PK  | AUTO    |
| sensor_id  | VARCHAR(50) | NO   |     | NULL    |
| systolic   | DECIMAL(5,1)| NO   |     | NULL    |
| diastolic  | DECIMAL(5,1)| NO   |     | NULL    |
| unit       | VARCHAR(10) | NO   |     | NULL    |
| timestamp  | TIMESTAMP   | NO   |     | NULL    |
+------------+-------------+------+-----+---------+

heart_rate
+------------+-------------+------+-----+---------+
| Field      | Type        | Null | Key | Default |
+------------+-------------+------+-----+---------+
| id         | SERIAL      | NO   | PK  | AUTO    |
| sensor_id  | VARCHAR(50) | NO   |     | NULL    |
| value      | INTEGER     | NO   |     | NULL    |
| unit       | VARCHAR(10) | NO   |     | NULL    |
| timestamp  | TIMESTAMP   | NO   |     | NULL    |
+------------+-------------+------+-----+---------+
```

## Protocol Buffers (gRPC)

The system uses Protocol Buffers for the blood pressure sensor communication via gRPC. Below is the definition of the protocol:

```protobuf
syntax = "proto3";

package sensor_data;

service SensorService {
    rpc SendPressure (SensorData) returns (Empty);
}

message SensorData {
    string sensor_id = 1;
    float systolic = 2;
    float diastolic = 3;
    string unit = 4;
    string date = 5;
}

message Empty {}
```

This protocol defines a service `SensorService` with a method `SendPressure` that takes `SensorData` as input and returns an `Empty` message. The `SensorData` message contains fields for `sensor_id`, `systolic` and `diastolic` blood pressure values, measurement `unit`, and `date`.

## Setup and Execution

### Prerequisites

- Docker and Docker Compose installed on your system
- Git (optional, for cloning the repository)

### Steps to Run the System

1. Clone the repository:
   ```bash
   git clone https://github.com/Wislian/Basic-IoT-architecture.git
   cd Basic-IoT-architecture
   ```

2. Start the containers with Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. To stop the containers:
   ```bash
   docker-compose down
   ```

### Verifying Operation

1. Sensors will automatically start sending data
2. The gateway will receive this data and publish it to MQTT topics
3. The MQTT subscriber will store the data in PostgreSQL
4. To view the stored data:
   ```bash
   docker exec -it postgres-db psql -U postgres -d healthcare
   ```
   ```sql
   SELECT * FROM temperature ORDER BY timestamp DESC LIMIT 10;
   SELECT * FROM pressure ORDER BY timestamp DESC LIMIT 10;
   SELECT * FROM heart_rate ORDER BY timestamp DESC LIMIT 10;
   ```

## Port Configuration

- **Sensors**: Do not expose ports, only communicate with the gateway
- **Gateway**: 
  - REST: Port 5000
  - WebSockets: Port 5000 (same Flask instance)
  - gRPC: Port 7777
- **MQTT Broker**: Port 1883
- **PostgreSQL**: Port 5432

## References and Resources

This project was developed based on knowledge and examples from the following resources:

### Communication Protocols
- **gRPC Implementation**: 
  - YouTube Tutorial: [gRPC Python Tutorial](https://www.youtube.com/watch?v=WB37L7PjI5k)
  - Official Documentation: [gRPC Python QuickStart](https://grpc.io/docs/languages/python/quickstart/)
  
- **MQTT Implementation**:
  - GitHub Repository: [mosquitto-python-example](https://github.com/roppert/mosquitto-python-example)

- **WebSocket Implementation**:
  - YouTube Tutorial: [WebSocket Python Tutorial](https://www.youtube.com/watch?v=Rctz-kCvuwE)

- **REST API Implementation**:
  - YouTube Tutorial: [REST API Python Tutorial](https://www.youtube.com/watch?v=z3YMz-Gocmw)

These resources provided valuable insights and examples for implementing the various communication protocols used in this project.
## Authors

- Carlos Camacho
- Willian Chapid
- Luis Felipe Martinez
