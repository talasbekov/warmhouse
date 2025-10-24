import logging
import os
import threading

from fastapi import FastAPI
from core.database import engine, Base, SessionLocal
from rabbitmq import RabbitMQConsumer
from routers.routers import router as telemetry_router
from schemas.schemas import TelemetryEvent
from services.services import TelemetryService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Telemetry Service",
    description="Микросервис для хранения истории телеметрии",
    version="1.0.0"
)

app.include_router(telemetry_router)


def process_telemetry_event(message: dict):
    db = SessionLocal()
    try:
        telemetry_event = TelemetryEvent(**message)

        TelemetryService.save_telemetry(db, telemetry_event)
        logger.info(f"Telemetry saved: {message.get('device_id')} - {message.get('metric_name')}")

    except Exception as e:
        logger.error(f"Error saving telemetry: {e}")
        raise
    finally:
        db.close()


def start_rabbitmq_consumer():
    rabbitmq_url = os.getenv(
        "RABBITMQ_URL",
        "amqp://admin:admin@smarthome-rabbitmq:5672/"
    )
    queue_name = "telemetry_events"

    consumer = RabbitMQConsumer(rabbitmq_url, queue_name)

    if consumer.connect():
        try:
            consumer.consume(process_telemetry_event)
        except KeyboardInterrupt:
            consumer.close()
            logger.info("Consumer stopped")


@app.on_event("startup")
def startup_event():
    consumer_thread = threading.Thread(target=start_rabbitmq_consumer, daemon=True)
    consumer_thread.start()
    logger.info("RabbitMQ consumer started in background")

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
