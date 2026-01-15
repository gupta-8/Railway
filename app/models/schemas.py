from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class Station(BaseModel):
    code: str = Field(..., examples=["NDLS"])
    name: str = Field(..., examples=["New Delhi"])


class Edge(BaseModel):
    to: str
    km: int
    line: str


class RouteLeg(BaseModel):
    frm: str = Field(..., alias="from")
    to: str
    km: int
    line: str
    fare: int

    class Config:
        populate_by_name = True


class RouteResponse(BaseModel):
    from_station: str
    to_station: str
    total_km: int
    total_fare: int
    legs: list[RouteLeg]


class Trip(BaseModel):
    trip_id: str
    train_no: str
    from_station: str
    to_station: str
    depart_at: datetime
    arrive_at: datetime
    base_fare: int


class BookingCreate(BaseModel):
    passenger_name: str = Field(..., min_length=1, max_length=60)
    trip_id: str
    seats: int = Field(1, ge=1, le=6)


class Booking(BaseModel):
    booking_id: str
    ticket_code: str
    passenger_name: str
    trip: Trip
    seats: int
    total_price: int
    booked_at: datetime
