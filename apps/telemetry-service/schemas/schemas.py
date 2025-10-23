from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TelemetryEvent(BaseModel):
    device_id: str = Field(..., min_length=1)
    metric_name: str = Field(..., min_length=1)
    value: float
    unit: str
    timestamp: Optional[datetime] = None


class TelemetryResponse(BaseModel):
    id: str
    device_id: str
    timestamp: datetime
    metric_name: str
    value: float
    unit: str

    class Config:
        from_attributes = True