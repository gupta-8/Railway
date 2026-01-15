from fastapi import APIRouter

from app.models.schemas import Trip
from app.data.seed import list_trips

router = APIRouter()

@router.get("", response_model=list[Trip])
def get_trips():
    return list_trips()
