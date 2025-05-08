import sys
from flask import Flask, request, jsonify
from flask_sock import Sock
import paho.mqtt.client as mqtt
import threading
import json
import sensor_pb2, sensor_pb2_grpc, grpc
from concurrent import futures
import os
import time
from google.protobuf.json_format import MessageToJson

sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)
sock = Sock(app)

MQTT_BROKER_ADDRESS = os.environ.get("MQTT_BROKER_ADDRESS", "mqtt-broker")
MQTT_PORT = 1883
MQTT_TOPICS = ("temperature", "pressure", "heartRate")

gateway_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"gateway_publisher")
def publish_to_mqtt(topic, data):
    try:
        result = gateway_client.publish(topic, json.dumps(data))
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[MQTT] publish to {topic}: {data['sensor_id']}")
        else:
            print(f"[MQTT ERROR] can't publish {topic}. code: {result.rc}")
    except Exception as e:
        print(f"[MQTT ERROR] Error to publish {topic}: {e}")

#REst
@app.route('/temperature', methods = ['POST'])
def handle_temperature():
    data = request.json
    publish_to_mqtt(MQTT_TOPICS[0],data)
    print(f"received Rest:{data}")
    return jsonify({"status":"received"}), 200

#WebSocket
@sock.route('/heartrate')
def handle_heart_rate(ws):
    while True:
        message = ws.receive()
        if message:
            try:
                data = json.loads(message)
                print(f"received websocket:{data}")
                publish_to_mqtt(MQTT_TOPICS[2],data)
            except Exception as e:
                print(f"[WS ERROR] {e}")

#gRPC
class PressureSensor(sensor_pb2_grpc.SensorServiceServicer):
    def SendPressure(self, request, context):
        publish_to_mqtt(MQTT_TOPICS[1],MessageToJson(request))
        print(f"received gRPC:{request}")
        return sensor_pb2.Empty()
def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(PressureSensor(), server)
    server.add_insecure_port("[::]:7777")
    server.start()
    server.wait_for_termination()   

#MQTT
def connect_mqtt():
        try:
            gateway_client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT)
            print(f"MQTT connected  {MQTT_BROKER_ADDRESS}")
        except Exception as e:
            print(f"MQTT Error: {e}")

if __name__ == "__main__":
    time.sleep(2)
    mqtt_connected = connect_mqtt()
    if mqtt_connected:
        gateway_client.loop_start()

    grpc_thread = threading.Thread(target=serve_grpc)
    grpc_thread.daemon = True
    grpc_thread.start()
    
    app.run(host="0.0.0.0",port = 5000)
    #gateway_client.loop_start()

