from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from models.models import Device
from schemas.schemas import DeviceCreate, DeviceUpdate, DeviceResponse
from services.services import DeviceService

router = APIRouter(
    prefix="/api/devices",
    tags=["devices"]
)


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
        device: DeviceCreate,
        db: Session = Depends(get_db)
):
    existing = db.query(Device).filter(Device.serial_number == device.serial_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Device with serial_number {device.serial_number} already exists"
        )

    return DeviceService.create_device(db, device)


@router.get("/", response_model=List[DeviceResponse])
def get_devices(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return DeviceService.get_devices(db, skip, limit)


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
        device_id: str,
        db: Session = Depends(get_db)
):
    device = DeviceService.get_device(db, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with id {device_id} not found"
        )
    return device


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
        device_id: str,
        device_data: DeviceUpdate,
        db: Session = Depends(get_db)
):
    device = DeviceService.update_device(db, device_id, device_data)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with id {device_id} not found"
        )
    return device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
        device_id: str,
        db: Session = Depends(get_db)
):
    success = DeviceService.delete_device(db, device_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with id {device_id} not found"
        )
