from fastapi import FastAPI
from core.database import engine
from core import Base
from routers.routers import router as device_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Management Service",
    description="Микросервис для управления IoT устройствами",
    version="1.0.0"
)

app.include_router(device_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "device-service"
    }


@app.get("/")
def root():
    return {
        "message": "Device Management Service",
        "docs": "/docs"
    }