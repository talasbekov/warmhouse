from sqlalchemy.orm import Session
from models.models import Device, DeviceStatus
from schemas.schemas import DeviceCreate, DeviceUpdate
from typing import List, Optional, Any
import uuid


class DeviceService:

    @staticmethod
    def create_device(db: Session, device_data: DeviceCreate) -> Device:
        db_device = Device(
            id=str(uuid.uuid4()),
            serial_number=device_data.serial_number,
            model=device_data.model,
            type=device_data.type,
            status=DeviceStatus.INACTIVE,
            owner_id=device_data.owner_id
        )
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device

    @staticmethod
    def get_device(db: Session, device_id: str) -> Optional[Device]:
        return db.query(Device).filter(Device.id == device_id).first()

    @staticmethod
    def get_devices(db: Session, skip: int = 0, limit: int = 100) -> list[type[Device]]:
        return db.query(Device).offset(skip).limit(limit).all()

    @staticmethod
    def update_device(db: Session, device_id: str, device_data: DeviceUpdate) -> type[Device] | None:
        db_device = db.query(Device).filter(Device.id == device_id).first()
        if not db_device:
            return None

        if device_data.model is not None:
            db_device.model = device_data.model
        if device_data.status is not None:
            db_device.status = device_data.status
        if device_data.owner_id is not None:
            db_device.owner_id = device_data.owner_id

        db.commit()
        db.refresh(db_device)
        return db_device

    @staticmethod
    def delete_device(db: Session, device_id: str) -> bool:
        db_device = db.query(Device).filter(Device.id == device_id).first()
        if not db_device:
            return False

        db.delete(db_device)
        db.commit()
        return True