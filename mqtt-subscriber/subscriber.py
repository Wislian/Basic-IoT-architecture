import paho.mqtt.client as mqtt
import json
import os
import time
import sys

sys.stdout.reconfigure(line_buffering=True)

MQTT_BROKER_ADDRESS = os.environ.get("MQTT_BROKER_ADDRESS", "mqtt-broker")
MQTT_PORT = 1883
MQTT_TOPICS = os.environ.get("MQTT_TOPICS", "temperature,pressure,heartRate").split(",")


def on_message(client, userdata, message):
    topic = message.topic
    try:
        payload = json.loads(message.payload.decode())
        print(f"\n[{topic.upper()}] Message received:")
        print(json.dumps(payload, indent=2))
        print("-" * 50)
    except Exception as e:
        print(f"Error to process message {topic}: {e}")
        print(f"Payload: {message.payload.decode()}")


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