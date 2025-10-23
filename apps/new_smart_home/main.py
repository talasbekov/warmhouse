from fastapi import FastAPI, Query
from datetime import datetime
import random

app = FastAPI(title="Smart Home API")

SENSOR_LOCATIONS = {
    "1": "Living Room",
    "2": "Bedroom",
    "3": "Kitchen"
}

@app.get("/")
def root():
    return {"message": "Smart Home API is running!"}

@app.get("/temperature")
def get_temperature(
        location: str = Query(None),
        sensorId: str = Query(None)
        ):
    if not location and sensorId:
        location = SENSOR_LOCATIONS.get(sensorId, "Unknown")

    if not sensorId and location:
        for sid, loc in SENSOR_LOCATIONS.items():
            if loc == location:
                sensorId = sid
                break
            if not sensorId:
                sensorId = "0"

    if not location:
        location = "Unknown"
        sensorId = "0"

    temperature = round(random.uniform(18.0, 24.0), 1)

    return {
        "value": temperature,
        "unit": "°C",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": location,
        "status": "active",
        "sensor_id": sensorId,
        "sensor_type": "temperature",
        "description": f"Temperature reading from {location}"
    }

@app.get("/temperature/{sensor_id}")
def get_temperature_by_id(sensor_id: str):
    location = SENSOR_LOCATIONS.get(sensor_id, "Unknown")
    temperature = round(random.uniform(18.0, 25.0), 1)

    return {
        "value": temperature,
        "unit": "°C",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": location,
        "status": "active",
        "sensor_id": sensor_id,
        "sensor_type": "temperature",
        "description": f"Temperature reading from {location}"
    }
