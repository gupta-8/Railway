from __future__ import annotations

from app.models.schemas import Edge, Station

# Undirected-ish graph: we store both directions explicitly
GRAPH: dict[str, list[Edge]] = {
    "NDLS": [Edge(to="AGC", km=188, line="Red Line"), Edge(to="JP", km=308, line="Pink Line")],
    "AGC":  [Edge(to="NDLS", km=188, line="Red Line"), Edge(to="GWL", km=118, line="Red Line")],
    "GWL":  [Edge(to="AGC", km=118, line="Red Line"), Edge(to="BPL", km=422, line="Green Line")],
    "JP":   [Edge(to="NDLS", km=308, line="Pink Line"), Edge(to="ADI", km=540, line="Blue Line")],
    "BPL":  [Edge(to="GWL", km=422, line="Green Line"), Edge(to="NGP", km=350, line="Orange Line"), Edge(to="ADI", km=594, line="Silver Line")],
    "NGP":  [Edge(to="BPL", km=350, line="Orange Line"), Edge(to="HWH", km=967, line="Gold Line")],
    "ADI":  [Edge(to="JP", km=540, line="Blue Line"), Edge(to="BPL", km=594, line="Silver Line")],
    "HWH":  [Edge(to="NGP", km=967, line="Gold Line")],
}

STATIONS: dict[str, Station] = {
    "NDLS": Station(code="NDLS", name="New Delhi"),
    "AGC":  Station(code="AGC", name="Agra Cantt"),
    "GWL":  Station(code="GWL", name="Gwalior"),
    "JP":   Station(code="JP", name="Jaipur"),
    "BPL":  Station(code="BPL", name="Bhopal"),
    "NGP":  Station(code="NGP", name="Nagpur"),
    "ADI":  Station(code="ADI", name="Ahmedabad"),
    "HWH":  Station(code="HWH", name="Howrah (Kolkata)"),
}
