from fastapi import APIRouter

from app.models.schemas import Station
from app.data.network import STATIONS

router = APIRouter()

@router.get("", response_model=list[Station])
def list_stations():
    return sorted(STATIONS.values(), key=lambda s: s.code)
