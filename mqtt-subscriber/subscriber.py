import paho.mqtt.client as mqtt
import json
import os
import time
import sys
import psycopg2

sys.stdout.reconfigure(line_buffering=True)


POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "healthdb")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")

try:
    db_conn = psycopg2.connect(
        host=POSTGRES_HOST,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=5432
    )
    db_conn.autocommit = True
    db_cursor = db_conn.cursor()
    print("[DB] Connected to PostgreSQL successfully.")
except Exception as e:
    print(f"[DB] PostgreSQL connection failed: {e}")
    sys.exit(1)

MQTT_BROKER_ADDRESS = os.environ.get("MQTT_BROKER_ADDRESS", "mqtt-broker")
MQTT_PORT = 1883
MQTT_TOPICS = os.environ.get("MQTT_TOPICS", "temperature,pressure,heartRate").split(",")


# def on_message(client, userdata, message):
#     topic = message.topic
#     try:
#         payload = json.loads(message.payload.decode())
#         print(f"\n[{topic.upper()}] Message received:")
#         print(json.dumps(payload, indent=2))
#         print("-" * 50)
#     except Exception as e:
#         print(f"Error to process message {topic}: {e}")
#         print(f"Payload: {message.payload.decode()}")

def on_message(client, userdata, message):
    topic = message.topic
    try:
        payload = json.loads(message.payload.decode())
        print(f"\n[{topic.upper()}] Message received:")
        print(json.dumps(payload, indent=2))
        print("-" * 50)

        sensor_id = payload.get("sensor_id")
        unit = payload.get("unit")
        value = payload.get("value")
        timestamp = payload.get("date")

        if topic == "temperature":
            db_cursor.execute(
                "INSERT INTO temperature (person_id, sensor_id, value, unit, timestamp) VALUES (%s, %s, %s, %s, %s)",
                (1, 1, value, unit, timestamp)
            )

        elif topic == "heartRate":
            db_cursor.execute(
                "INSERT INTO heart_rate (person_id, sensor_id, value, unit, timestamp) VALUES (%s, %s, %s, %s, %s)",
                (1, 1, value, unit, timestamp)
            )

        elif topic == "pressure":
            systolic = payload.get("systolic")
            diastolic = payload.get("diastolic")
            db_cursor.execute(
                "INSERT INTO blood_pressure (person_id, sensor_id, systolic, diastolic, unit, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
                (1, 1, systolic, diastolic, unit, timestamp)
            )

    except Exception as e:
        print(f"[ERROR] Processing message from {topic}: {e}")



def on_connect(client, userdata, flags, rc, properties = None):
    if rc == 0:
        print(f"Succesful connection to broker {MQTT_BROKER_ADDRESS}")
        
        
        for topic in MQTT_TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
    else:
        print(f"Connection error with code: {rc}")

def main():
    print(f"starting MQTT connection...")
    print(f"Broker: {MQTT_BROKER_ADDRESS}:{MQTT_PORT}")
    print(f"Topics: {MQTT_TOPICS}")
    
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"mqtt_subscriber")
    client.on_connect = on_connect
    client.on_message = on_message

    
    connected = False
    retry_count = 0
    max_retries = 10
    
    while not connected and retry_count < max_retries:
        try:
            print(f"trying to connect to MQTT broker ({retry_count+1}/{max_retries})...")
            client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT)
            connected = True
        except Exception as e:
            retry_count += 1
            print(f"Error to connect: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
    
    if not connected:
        print("Can't to connected to MQTT broker after various trieds. Exiting.")
        sys.exit(1)
    
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Subscriber finished by user")
    finally:
        client.disconnect()
        print("MQTT broker disconnected")

if __name__ == "__main__":
    main()