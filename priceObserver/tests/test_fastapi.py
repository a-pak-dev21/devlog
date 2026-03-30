from fastapi.testclient import TestClient
from app.api.fast_api import app_creator
from app.api.schemas import InputPairs

client = TestClient(app_creator())

def test_db_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_pairs():
    response = client.get("/pairs")
    assert response.status_code == 200
    data = response.json()
    if data:
        assert "pair" in data[0]

def test_pair_history():
    response = client.get(
        "/pairs/history",
        params={
            "base": "btc",
            "quote": "usdt",
            "start": "2026-03-01T00:00:00",
            "end": "2026-04-01T00:00:00",
            "exchange": "coinbase.com"
        }
        )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_pair_history_empty():
    response = client.get(
        "/pairs/history",
        params={
            "base": "trx",
            "quote": "udst",
            "end": "1999-01-01T00:00:00",
            "exchange": "bybit.com"
        }
    )
    assert response.status_code == 200
    assert response.json() == []

def test_pair_history_invalid_pair():
    response = client.get(
        "/pairs/history",
        params={
            "base": "btc",
            "quote": "btc"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The base and quote cannot be same"}

def test_pair_history_invalid_timeserie():
    response = client.get(
        "/pairs/history",
        params={
            "base": "btc",
            "quote": "usdt",
            "start": "2026-03-01T00:00:00",
            "end": "1900-03-01T00:00:00"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "starttime cannot be greater then endtime"}

def test_exchanges():
    response = client.get("/exchanges")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_spreads():
    response = client.get("/spreads/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_spreads_nonexisting_id():
    response = client.get("/spreads/99999")
    assert response.status_code == 200
    assert response.json() == []

def test_posting_snapshot():
    payload = InputPairs(pairs=[
        ("BTC", "USDT"), ("BNB","USDT"), ("ETH","USDT")
        ])
    response = client.post("/post-snapshot", json=payload.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

