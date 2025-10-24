from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from models.models import DeviceType, DeviceStatus


class DeviceCreate(BaseModel):
    serial_number: str = Field(..., min_length=5, max_length=100)
    model: str = Field(..., min_length=2, max_length=100)
    type: DeviceType
    owner_id: Optional[str] = None


class DeviceUpdate(BaseModel):
    model: Optional[str] = None
    status: Optional[DeviceStatus] = None
    owner_id: Optional[str] = None


class DeviceResponse(BaseModel):
    id: str
    serial_number: str
    model: str
    type: DeviceType
    status: DeviceStatus
    owner_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy