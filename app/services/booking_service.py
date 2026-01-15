from __future__ import annotations

from datetime import datetime, timezone
import secrets

from app.data.seed import get_trip
from app.models.schemas import Booking, BookingCreate

UTC = timezone.utc

_BOOKINGS: dict[str, Booking] = {}

def _now() -> datetime:
    return datetime.now(tz=UTC)

def _ticket_code() -> str:
    a = secrets.token_hex(2).upper()
    b = secrets.token_hex(2).upper()
    return f"RQ-{a}-{b} 🚆"

def create_booking(payload: BookingCreate) -> Booking:
    trip = get_trip(payload.trip_id)

    booking_id = f"B{secrets.randbelow(10**8):08d}"
    total_price = trip.base_fare * payload.seats

    booking = Booking(
        booking_id=booking_id,
        ticket_code=_ticket_code(),
        passenger_name=payload.passenger_name,
        trip=trip,
        seats=payload.seats,
        total_price=total_price,
        booked_at=_now(),
    )
    _BOOKINGS[booking_id] = booking
    return booking

def list_bookings() -> list[Booking]:
    return sorted(_BOOKINGS.values(), key=lambda b: b.booked_at, reverse=True)
