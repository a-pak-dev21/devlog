import os


def test_login(client):
    response = client.post("/auth/login",
                           data={
                               "username": "admin",
                               "password": os.getenv("ADMIN_TEST_PASSWORD")
                           })
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_invalid_login(client):
    response = client.post("auth/login",
                           data={
                               "username": "wrong_username",
                               "password": "invalid_password"
                           })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"