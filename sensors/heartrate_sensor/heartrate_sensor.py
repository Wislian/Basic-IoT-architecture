import websockets
import asyncio
import random
import datetime
import json
import time
from zoneinfo import ZoneInfo


def generate_heart_rate():
    return {
        "sensor_id":f"Heart_00{random.randint(1,3)}",
        "person_id":random.randint(1,4),
        "value":random.randint(60,100),
        "unit":"bpm",
        "date":datetime.datetime.now(ZoneInfo("America/Bogota")).isoformat()
    }

async def send_data():
    uri = "ws://gateway:5000/heartrate"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[WS] connected to gateway")
            while True:
                data = generate_heart_rate()
                message = json.dumps(data)
                await websocket.send(message)
                await asyncio.sleep(10)
    except Exception as e:
        print(f"[WS] ERROR: {e}")

if __name__ == "__main__":
    time.sleep(5)
    asyncio.run(send_data())