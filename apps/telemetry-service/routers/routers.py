from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core import get_db
from schemas.schemas import TelemetryEvent, TelemetryResponse
from services.services import TelemetryService

router = APIRouter(prefix="/api/telemetry", tags=["telemetry"])

@router.post("/", response_model=TelemetryResponse, status_code=201)
def save_telemetry(event: TelemetryEvent, db: Session = Depends(get_db)):
    return TelemetryService.save_telemetry(db, event)

@router.get("/history/{device_id}", response_model=List[TelemetryResponse])
def get_history(
    device_id: str,
    metric_name: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    return TelemetryService.get_telemetry_history(
        db, device_id, metric_name, start_time, end_time, limit
    )

@router.get("/latest/{device_id}/{metric_name}", response_model=TelemetryResponse)
def get_latest(device_id: str, metric_name: str, db: Session = Depends(get_db)):
    result = TelemetryService.get_latest_telemetry(db, device_id, metric_name)
    if not result:
        raise HTTPException(status_code=404, detail="Telemetry not found")
    return result