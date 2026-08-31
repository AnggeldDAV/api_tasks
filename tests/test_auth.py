# test_auth.py
from core import security


def _create_user(client, name: str, password: str):
    response = client.post("/api/v1/users/", json={"name": name, "password": password})
    assert response.status_code == 201
    return response.json()


def _login(client, username: str, password: str):
    return client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )


# ------------------------------------------------------------
# POST /auth/login
# ------------------------------------------------------------

def test_login_success(client):

    _create_user(client, "authuser", "securepass")

    response = _login(client, "authuser", "securepass")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)



def test_login_user_not_found(client):

    response = _login(client, "nonexistent", "whatever")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_login_wrong_password(client):

    _create_user(client, "authuser2", "correctpass")


    response = _login(client, "authuser2", "wrongpass")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_login_invalid_data(client):

    response = client.post("/api/v1/auth/login", json={"username": "someuser"})
    assert response.status_code == 422

    response = client.post("/api/v1/auth/login", json={"password": "somepass"})
    assert response.status_code == 422


# ------------------------------------------------------------
#  Login -> Token -> Protected endpoint 
# ------------------------------------------------------------

def test_get_tasks_with_valid_token(client):

    _create_user(client, "tokenuser", "tokenpass")

    login_response = _login(client, "tokenuser", "tokenpass")
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]


    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/tasks/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_tasks_with_invalid_token(client):

    headers = {"Authorization": "Bearer invalidtoken123"}
    response = client.get("/api/v1/tasks/", headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not Authenticated"
    
def test_get_tasks_with_valid_token_nonexistent_user(client):

    token = security.signJWT(999)

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/tasks/", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not Authenticated"