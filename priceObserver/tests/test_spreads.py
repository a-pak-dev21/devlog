snapshot_id = 1

def test_spreads(client):
    response = client.get(f"/spreads/{snapshot_id}")
    data = response.json()
    spread_set = {"abs_spread", "pct_spread", "best_buy_on", "best_sell_on"}

    assert response.status_code == 200
    assert isinstance(data, list)

    for item in data:
        assert spread_set.issubset(item)


invalid_snapshot_id = 999

def test_spreads_with_invalid_id(client):
    response = client.get(f"/spreads/{invalid_snapshot_id}")

    assert response.status_code == 404
    assert "detail" in response.json()