import time, requests, random, datetime

GATEWAY_URL = "http://gateway:5000/temperature"

def generate_temperature():
    return{
        "sensor_id":"Temp_001",
        "value":round(random.uniform(35,38), 2),
        "unit":"C",
        "date":datetime.datetime.now().isoformat()
    }

def main():
    while True:
        data = generate_temperature()
        try:
            response = requests.post(GATEWAY_URL, json=data)
            print(f"Sent REST data:{data}| Response:{response.status_code}")
        except Exception as e:
            print("REST Error:", e)
        time.sleep(10)

if __name__ == "__main__":
    main()