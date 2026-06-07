def test_last_snapshot(client):
    response = client.get("/last-snapshot")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)


def test_post_snapshot(client, auth_headers):
    response = client.post("/post-snapshot",
                           json={"pairs": [
                               ["btc", "usdt"],
                               ["bnb", "usdt"],
                               ["eth", "usdt"]
                           ]},
                           headers=auth_headers)
    
    assert response.status_code == 201
    assert "snapshot_id" in response.json()

def test_post_snapshot_unauthorized(client):
    response = client.post("/post-snapshot",
                           json={"pairs": [
                               ["btc", "usdt"],
                               ["bnb", "usdt"],
                               ["eth", "usdt"]
                           ]},
                           headers={
                               "Authorization": "Bearer invalid_token"
                           })
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication token"

def test_post_snapshot_no_token(client):
    response = client.post("/post-snapshot",
                           json={"pairs": [
                               ["btc", "usdt"],
                               ["bnb", "usdt"],
                               ["eth", "usdt"]
                           ]}
                           )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

    


# разобраться с тем как сейчас у меня и вообще в целом работает постгрес + докер 
# почему как только я запуская ПК он сразу знает что нужно запустить отдельный контейнер из компоуса 
# а другие контейнеры остаются лежать и как это связано (с пгАдмином или сам докер или как ?)
