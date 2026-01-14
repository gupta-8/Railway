from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import RouteResponse
from app.services.routing_service import find_cheapest_route

router = APIRouter()

@router.get("", response_model=RouteResponse)
def route(
    from_station: str = Query(..., min_length=2, max_length=6),
    to_station: str = Query(..., min_length=2, max_length=6),
):
    try:
        return find_cheapest_route(from_station.upper(), to_station.upper())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
