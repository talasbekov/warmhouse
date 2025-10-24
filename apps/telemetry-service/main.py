from fastapi import FastAPI
from core.database import engine, Base
from routers.routers import router as telemetry_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Telemetry Service",
    description="Микросервис для хранения истории телеметрии",
    version="1.0.0"
)

app.include_router(telemetry_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "telemetry-service"
    }

@app.get("/")
def root():
    return {
        "message": "Telemetry Service",
        "docs": "/docs"
    }
