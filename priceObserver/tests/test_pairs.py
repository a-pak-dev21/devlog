def test_all_pairs(client):
    response = client.get("/pairs")
    data = response.json()
    
    assert response.status_code == 200
    assert isinstance(data, list)

    for item in data:
        assert isinstance(item, dict)
        assert "base" in item
        assert "quote" in item

#order_by; sort_dir; limit; offset; | 

def test_pair_history_basic(client):
    # Using only required parameters such as base & quote 
    response = client.get("pairs/history",
                          params={
                              "base": "BTC",
                              "quote": "USDT"
                          })
    assert response.status_code == 200
    assert isinstance(response.json(), list)
     

def test_pair_invalid_pair(client):
    response = client.get("pairs/history",
                          params={
                              "base": "BTC",
                              "quote": "BTC"
                          })
    
    assert response.status_code == 422
    assert "detail" in response.json()


def test_pair_invalid_time_range(client):
    response = client.get("pairs/history",
                          params={
                              "base": "BTC",
                              "quote": "USDT",
                              "start": "2026-06-27",
                              "end": "2026-05-01"
                          })
    
    assert response.status_code == 422
    assert "detail" in response.json()
    


