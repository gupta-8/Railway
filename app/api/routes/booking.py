from fastapi import APIRouter, HTTPException

from app.models.schemas import Booking, BookingCreate
from app.services.booking_service import create_booking, list_bookings

router = APIRouter()

@router.get("", response_model=list[Booking])
def get_bookings():
    return list_bookings()

@router.post("", response_model=Booking)
def book(payload: BookingCreate):
    try:
        return create_booking(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
