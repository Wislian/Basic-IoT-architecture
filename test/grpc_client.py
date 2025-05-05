import test_pb2, test_pb2_grpc, grpc
import time, random, datetime

def run():
    with grpc.insecure_channel("localhost:7777") as channel:
        stub = test_pb2_grpc.SensorServiceStub(channel)
        systolic = random.uniform(100,140)
        diastolic = random.uniform(60,90)
        data = test_pb2.PressureReading(
            sensor_id = "Press_001",
            systolic = round(systolic, 1),
            diastolic = round(diastolic, 1),
            unit = "mmHg",
            date = datetime.datetime.now().isoformat()
        )
        stub.SendPressure(data)
if __name__ == "__main__":
    run()