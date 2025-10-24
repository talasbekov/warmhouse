from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.models import TelemetryHistory
from schemas.schemas import TelemetryEvent
from typing import List, Optional
from datetime import datetime
import uuid


class TelemetryService:

    @staticmethod
    def save_telemetry(db: Session, telemetry_data: TelemetryEvent) -> TelemetryHistory:
        db_telemetry = TelemetryHistory(
            id=str(uuid.uuid4()),
            device_id=telemetry_data.device_id,
            timestamp=telemetry_data.timestamp or datetime.utcnow(),
            metric_name=telemetry_data.metric_name,
            value=telemetry_data.value,
            unit=telemetry_data.unit
        )
        db.add(db_telemetry)
        db.commit()
        db.refresh(db_telemetry)
        return db_telemetry

    @staticmethod
    def get_telemetry_history(
        db: Session,
        device_id: str,
        metric_name: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[TelemetryHistory]:
        query = db.query(TelemetryHistory).filter(
            TelemetryHistory.device_id == device_id
        )

        if metric_name:
            query = query.filter(TelemetryHistory.metric_name == metric_name)

        if start_time:
            query = query.filter(TelemetryHistory.timestamp >= start_time)

        if end_time:
            query = query.filter(TelemetryHistory.timestamp <= end_time)

        query = query.order_by(TelemetryHistory.timestamp.desc())

        return query.limit(limit).all()

    @staticmethod
    def get_latest_telemetry(
        db: Session,
        device_id: str,
        metric_name: str
    ) -> Optional[TelemetryHistory]:
        return db.query(TelemetryHistory).filter(
            and_(
                TelemetryHistory.device_id == device_id,
                TelemetryHistory.metric_name == metric_name
            )
        ).order_by(TelemetryHistory.timestamp.desc()).first()
