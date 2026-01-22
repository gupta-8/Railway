from __future__ import annotations

import heapq
import logging
from typing import Dict, List, Tuple

from app.core.config import settings
from app.data.network import GRAPH
from app.models.schemas import RouteLeg, RouteResponse

logger = logging.getLogger("railway.routing_service")


def _dijkstra(start: str, goal: str) -> Tuple[int, List[Tuple[str, str]]]:
    if start not in GRAPH or goal not in GRAPH:
        raise ValueError("Unknown station code(s).")

    dist: Dict[str, float] = {node: float("inf") for node in GRAPH}
    prev: Dict[str, str | None] = {node: None for node in GRAPH}
    dist[start] = 0

    pq: list[tuple[float, str]] = [(0, start)]
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
    nodes: list[str] = []
    cur: str | None = goal
    while cur is not None:
        nodes.append(cur)
        cur = prev[cur]
    nodes.reverse()

    edges = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
    return int(dist[goal]), edges


def find_cheapest_route(from_station: str, to_station: str) -> RouteResponse:
    logger.info("route_compute_start from=%s to=%s", from_station, to_station)

    total_km, edges = _dijkstra(from_station, to_station)

    legs: list[RouteLeg] = []
    for u, v in edges:
        edge = next((e for e in GRAPH[u] if e.to == v), None)
        if edge is None:
            logger.error("graph_inconsistent missing_edge from=%s to=%s", u, v)
            raise RuntimeError("Graph inconsistent: missing edge.")
        fare = edge.km * settings.fare_per_km
        legs.append(RouteLeg(**{"from": u, "to": v, "km": edge.km, "line": edge.line, "fare": fare}))

    resp = RouteResponse(
        from_station=from_station,
        to_station=to_station,
        total_km=total_km,
        total_fare=total_km * settings.fare_per_km,
        legs=legs,
    )

    logger.info(
        "route_compute_done from=%s to=%s total_km=%s total_fare=%s legs=%s",
        from_station,
        to_station,
        total_km,
        resp.total_fare,
        len(legs),
    )
    return resp
