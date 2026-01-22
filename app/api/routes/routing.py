import logging

from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import RouteResponse
from app.services.routing_service import find_cheapest_route

router = APIRouter()
logger = logging.getLogger("railway.routing")


@router.get("", response_model=RouteResponse)
def route(
    from_station: str = Query(..., min_length=2, max_length=6),
    to_station: str = Query(..., min_length=2, max_length=6),
):
    try:
        resp = find_cheapest_route(from_station.upper(), to_station.upper())
        logger.info(
            "route_found from=%s to=%s total_km=%s total_fare=%s legs=%s",
            resp.from_station,
            resp.to_station,
            resp.total_km,
            resp.total_fare,
            len(resp.legs),
        )
        return resp
    except ValueError as e:
        logger.warning(
            "route_failed from=%s to=%s error=%s",
            from_station.upper(),
            to_station.upper(),
            str(e),
        )
        raise HTTPException(status_code=400, detail=str(e))
