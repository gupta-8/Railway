from fastapi import APIRouter

from .health import router as health_router
from .stations import router as stations_router
from .routing import router as routing_router
from .trips import router as trips_router
from .bookings import router as bookings_router

router = APIRouter()

router.include_router(health_router, tags=["health"])
router.include_router(stations_router, prefix="/stations", tags=["stations"])
router.include_router(routing_router, prefix="/route", tags=["routing"])
router.include_router(trips_router, prefix="/trips", tags=["trips"])
router.include_router(bookings_router, prefix="/bookings", tags=["bookings"])
