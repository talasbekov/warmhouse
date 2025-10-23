import uuid
from enum import Enum
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from core import Base


class DeviceType(str, Enum):
    TEMPERATURE_SENSOR = "temperature_sensor"
    HUMIDITY_SENSOR = "humidity_sensor"
    LIGHT_RELAY = "light_relay"
    CAMERA = "camera"
    GATE_CONTROLLER = "gate_controller"


class DeviceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    serial_number = Column(String, unique=True, nullable=False, index=True)
    model = Column(String, nullable=False)
    type = Column(SQLEnum(DeviceType), nullable=False)
    status = Column(SQLEnum(DeviceStatus), nullable=False, default=DeviceStatus.INACTIVE)
    owner_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
