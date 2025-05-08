import websockets
import asyncio
import random, datetime
import json


def generate_heart_rate():
    return {
        "sensor_id":"Heart_001",
        "value":random.randint(60,100),
        "unit":"bpm",
        "date":datetime.datetime.now().isoformat()
    }

async def send_data():
    uri = "ws://gateway:5000/heartrate"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[WS] connected to gateway")
            while True:
                data = generate_heart_rate()
                message = json.dumps(data)
                try:
                    await websocket.send(message)
                except Exception as e:
                    print(f"[WS] ERROR 1: {e}")
                await asyncio.sleep(7)
    except Exception as e:
        print(f"[WS] ERROR 2: {e}")

if __name__ == "__main__":
    asyncio.run(send_data())