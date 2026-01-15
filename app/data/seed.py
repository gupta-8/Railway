from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models.schemas import Trip

UTC = timezone.utc

_TRIPS: dict[str, Trip] = {}

def _now() -> datetime:
    return datetime.now(tz=UTC)

def _seed() -> None:
    if _TRIPS:
        return

    now = _now()
    sample = [
        ("T1001", "12951", "NDLS", "AGC", 2, 4, 250),
        ("T1002", "12137", "AGC", "BPL", 5, 12, 900),
        ("T1003", "22953", "JP", "ADI", 3, 10, 850),
        ("T1004", "12809", "BPL", "NGP", 1, 6, 700),
        ("T1005", "12860", "NGP", "HWH", 6, 20, 1500),
    ]

    for trip_id, train_no, a, b, dep_h, dur_h, base in sample:
        depart = now + timedelta(hours=dep_h)
        arrive = depart + timedelta(hours=dur_h)
        _TRIPS[trip_id] = Trip(
            trip_id=trip_id,
            train_no=train_no,
            from_station=a,
            to_station=b,
            depart_at=depart,
            arrive_at=arrive,
            base_fare=base,
        )

def list_trips() -> list[Trip]:
    _seed()
    return sorted(_TRIPS.values(), key=lambda t: t.depart_at)

def get_trip(trip_id: str) -> Trip:
    _seed()
    if trip_id not in _TRIPS:
        raise ValueError("Unknown trip_id.")
    return _TRIPS[trip_id]
