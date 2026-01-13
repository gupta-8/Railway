from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import heapq
import secrets
from typing import Dict, List, Tuple

from models import Booking, BookingCreate, Edge, RouteLeg, RouteResponse, Station, Trip

# --- Fake "railway network" graph (undirected) ---
# Each edge has distance (km) + line name (for vibes)
GRAPH: Dict[str, List[Edge]] = {
    "NDLS": [Edge(to="AGC", km=188, line="Red Line"), Edge(to="JP", km=308, line="Pink Line")],
    "AGC":  [Edge(to="NDLS", km=188, line="Red Line"), Edge(to="GWL", km=118, line="Red Line")],
    "GWL":  [Edge(to="AGC", km=118, line="Red Line"), Edge(to="BPL", km=422, line="Green Line")],
    "JP":   [Edge(to="NDLS", km=308, line="Pink Line"), Edge(to="ADI", km=540, line="Blue Line")],
    "BPL":  [Edge(to="GWL", km=422, line="Green Line"), Edge(to="NGP", km=350, line="Orange Line")],
    "NGP":  [Edge(to="BPL", km=350, line="Orange Line"), Edge(to="HWH", km=967, line="Gold Line")],
    "ADI":  [Edge(to="JP", km=540, line="Blue Line"), Edge(to="BPL", km=594, line="Silver Line")],
    "HWH":  [Edge(to="NGP", km=967, line="Gold Line")],
}

STATIONS: Dict[str, Station] = {
    "NDLS": Station(code="NDLS", name="New Delhi"),
    "AGC":  Station(code="AGC", name="Agra Cantt"),
    "GWL":  Station(code="GWL", name="Gwalior"),
    "JP":   Station(code="JP", name="Jaipur"),
    "BPL":  Station(code="BPL", name="Bhopal"),
    "NGP":  Station(code="NGP", name="Nagpur"),
    "ADI":  Station(code="ADI", name="Ahmedabad"),
    "HWH":  Station(code="HWH", name="Howrah (Kolkata)"),
}

FARE_PER_KM = 2  # super simple pricing


def list_stations() -> List[Station]:
    return sorted(STATIONS.values(), key=lambda s: s.code)


def _dijkstra(start: str, goal: str) -> Tuple[int, List[Tuple[str, str]]]:
    """
    Returns (total_km, path_edges) where path_edges = [(u,v), ...]
    """
    if start not in GRAPH or goal not in GRAPH:
        raise ValueError("Unknown station code(s).")

    dist = {node: float("inf") for node in GRAPH}
    prev = {node: None for node in GRAPH}  # store predecessor
    dist[start] = 0

    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == goal:
            break
        for e in GRAPH[u]:
            nd = d + e.km
            if nd < dist[e.to]:
                dist[e.to] = nd
                prev[e.to] = u
                heapq.heappush(pq, (nd, e.to))

    if dist[goal] == float("inf"):
        raise ValueError("No route found between these stations.")

    # rebuild path nodes
    nodes = []
    cur = goal
    while cur is not None:
        nodes.append(cur)
        cur = prev[cur]
    nodes.reverse()

    # convert nodes -> edges
    edges = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
    return int(dist[goal]), edges


def find_route(from_station: str, to_station: str) -> RouteResponse:
    total_km, edges = _dijkstra(from_station, to_station)

    legs: List[RouteLeg] = []
    for u, v in edges:
        edge = next((e for e in GRAPH[u] if e.to == v), None)
        if edge is None:
            # should never happen if graph is consistent
            raise RuntimeError("Graph is inconsistent.")
        fare = edge.km * FARE_PER_KM
        legs.append(RouteLeg(**{"from": u, "to": v, "km": edge.km, "line": edge.line, "fare": fare}))

    total_fare = total_km * FARE_PER_KM
    return RouteResponse(
        from_station=from_station,
        to_station=to_station,
        total_km=total_km,
        total_fare=total_fare,
        legs=legs,
    )


# --- Trips + bookings (in-memory) ---
UTC = timezone.utc


def _now() -> datetime:
    return datetime.now(tz=UTC)


TRIPS: Dict[str, Trip] = {}
BOOKINGS: Dict[str, Booking] = {}


def seed_trips() -> None:
    if TRIPS:
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
        TRIPS[trip_id] = Trip(
            trip_id=trip_id,
            train_no=train_no,
            from_station=a,
            to_station=b,
            depart_at=depart,
            arrive_at=arrive,
            base_fare=base,
        )


def list_trips() -> List[Trip]:
    seed_trips()
    return sorted(TRIPS.values(), key=lambda t: t.depart_at)


def get_trip(trip_id: str) -> Trip:
    seed_trips()
    if trip_id not in TRIPS:
        raise ValueError("Unknown trip_id.")
    return TRIPS[trip_id]


def _ticket_code() -> str:
    # fun little code, like: RQ-7F2A-9C1B 🚆
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
    BOOKINGS[booking_id] = booking
    return booking


def list_bookings() -> List[Booking]:
    return sorted(BOOKINGS.values(), key=lambda b: b.booked_at, reverse=True)
