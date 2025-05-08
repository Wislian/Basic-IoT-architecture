import sys
from flask import Flask, request, jsonify
from flask_sock import Sock
import paho.mqtt.client as mqtt
import threading
import json
import sensor_pb2, sensor_pb2_grpc, grpc
from concurrent import futures

sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)
sock = Sock(app)

MQTT_BROKER_ADDRESS = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = ("temperature", "pressure", "heartRate")

#gateway_client = mqtt.Client("gateway_publisher")

def publish_to_mqtt(topic, data):
    gateway_client.publish(topic, json.dumps(data))
    print(f"[MQTT] Published: {data['sensor_id']}")
#REst
@app.route('/temperature', methods = ['POST'])
def handle_temperature():
    data = request.json
    #publish_to_mqtt(MQTT_TOPICS[0],data)
    print("received Rest")
    return jsonify({"status":"received"}), 200
#WebSocket
@sock.route('/heartrate')
def handle_heart_rate(ws):
    while True:
        message = ws.receive()
        if message:
            try:
                data = json.loads(message)
                print("received websocket")
                #publish_to_mqtt(MQTT_TOPICS[1],data)
            except Exception as e:
                print(f"[WS ERROR] {e}")

#gRPC
class PressureSensor(sensor_pb2_grpc.SensorServiceServicer):
    def SendPressure(self, request, context):
        #publish_to_mqtt(MQTT_TOPICS[2],request)
        print(request)
        return sensor_pb2.Empty()
def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(PressureSensor(), server)
    server.add_insecure_port("[::]:7777")
    server.start()
    server.wait_for_termination()   

if __name__ == "__main__":
    #gateway_client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT)
    grpc_thread = threading.Thread(target=serve_grpc)
    grpc_thread.start()
    
    app.run(host="0.0.0.0",port = 5000)
    #gateway_client.loop_start()

