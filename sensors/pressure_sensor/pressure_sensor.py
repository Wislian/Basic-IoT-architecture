import grpc, time, random, datetime, sensor_pb2, sensor_pb2_grpc

def generate_pressure():
    systolic = random.uniform(100,140)
    diastolic = random.uniform(60,90)
    return sensor_pb2.SensorData(
        sensor_id = "Press_001",
        systolic = round(systolic, 1),
        diastolic = round(diastolic, 1),
        unit = "mmHg",
        date = datetime.datetime.now().isoformat()
    )

def run():
    try:
        with grpc.insecure_channel("localhost:7777") as channel:
            stub = sensor_pb2_grpc.SensorServiceStub(channel)
            print(f"[gRPC] Channel connected.")
            while True:
                pressure_data = generate_pressure()
                stub.SendPressure(pressure_data)
                print(f"[gRPC] Sent: \n{pressure_data}")
                time.sleep(10)
    except Exception as e:
        print(f"[gRPC] Error: {e}")
        

if __name__ == "__main__":
    run()