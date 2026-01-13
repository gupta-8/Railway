from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from models import Booking, BookingCreate, RouteResponse, Station, Trip
import store

app = FastAPI(
    title="Railway Quest 🚆",
    version="0.1.0",
    description="A mini railway network API: routes, trips, and bookings.",
)

# CORS (nice for future frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True, "service": "Railway Quest"}


@app.get("/stations", response_model=list[Station])
def stations():
    return store.list_stations()


@app.get("/route", response_model=RouteResponse)
def route(
    from_station: str = Query(..., min_length=2, max_length=6),
    to_station: str = Query(..., min_length=2, max_length=6),
):
    try:
        return store.find_route(from_station.upper(), to_station.upper())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/trips", response_model=list[Trip])
def trips():
    return store.list_trips()


@app.post("/bookings", response_model=Booking)
def book(payload: BookingCreate):
    try:
        return store.create_booking(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/bookings", response_model=list[Booking])
def bookings():
    return store.list_bookings()
