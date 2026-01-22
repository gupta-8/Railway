import logging

from fastapi import APIRouter, HTTPException

from app.models.schemas import Booking, BookingCreate
from app.services.booking_service import create_booking, list_bookings

router = APIRouter()
logger = logging.getLogger("railway.bookings")


@router.get("", response_model=list[Booking])
def get_bookings():
    logger.info("list_bookings")
    return list_bookings()


@router.post("", response_model=Booking)
def book(payload: BookingCreate):
    try:
        booking = create_booking(payload)
        logger.info(
            "booking_created booking_id=%s trip_id=%s seats=%s passenger_name=%s total_price=%s",
            booking.booking_id,
            payload.trip_id,
            payload.seats,
            payload.passenger_name,
            booking.total_price,
        )
        return booking
    except ValueError as e:
        logger.warning(
            "booking_failed trip_id=%s seats=%s passenger_name=%s error=%s",
            payload.trip_id,
            payload.seats,
            payload.passenger_name,
            str(e),
        )
        raise HTTPException(status_code=400, detail=str(e))
