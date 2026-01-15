from app.services.routing_service import find_cheapest_route

def test_route_exists():
    res = find_cheapest_route("NDLS", "BPL")
    assert res.total_km > 0
    assert res.total_fare > 0
    assert len(res.legs) >= 1
    assert res.from_station == "NDLS"
    assert res.to_station == "BPL"

def test_invalid_station():
    try:
        find_cheapest_route("XXXX", "BPL")
        assert False, "Expected ValueError"
    except ValueError:
        assert True
