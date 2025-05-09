import grpc
import time
import random
import datetime
import sensor_pb2, sensor_pb2_grpc

def generate_pressure():
    return sensor_pb2.SensorData(
        sensor_id = f"Press_00{random.randint(1,3)}",
        person_id = random.randint(1,4),
        systolicPressure = random.randint(100,140),
        diastolicPressure = random.randint(60,90),
        unit = "mmHg",
        date = datetime.datetime.now().isoformat()
    )

def run():
    try:
        with grpc.insecure_channel("gateway:7777") as channel:
            stub = sensor_pb2_grpc.SensorDataServiceStub(channel)
            print(f"[gRPC] Channel connected.")
            while True:
                pressure_data = generate_pressure()
                stub.SendPressureReading(pressure_data)
                print(f"[gRPC] Sent: \n{pressure_data}")
                time.sleep(10)
    except Exception as e:
        print(f"[gRPC] Error: {e}")
        

if __name__ == "__main__":
    time.sleep(5)
    run()