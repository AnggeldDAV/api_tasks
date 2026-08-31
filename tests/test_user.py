# test_user.py
from types import SimpleNamespace

from main import app
from deps.deps import get_current_user


def _override_current_user(user_id: int):
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=user_id)


# ------------------------------------------------------------
# POST /
# ------------------------------------------------------------

def test_post_user_success(client):
    user_data = {
        "name": "test",
        "password": "test123"
    }
    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == user_data["name"]
    assert "id" in data


def test_post_user_fail(client):
    user_data = {
        "name": "test"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422 
    data = response.json()
    assert data["detail"][0]["msg"] == "Field required"
    
    user_data = {
        "password": "test"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422 
    data = response.json()
    assert data["detail"][0]["msg"] == "Field required"
    
    user_data = {}
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422

    user_data = {
        "name": "test",
        "password": 123
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422 
    data = response.json()
    assert data["detail"][0]["type"]  == "string_type"


def test_post_user_exists_fail(client):
    user_data = {
        "name": "test",
        "password": "test123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201

    user_data_exists = {
        "name": "test",
        "password": "test123"
    }
    response = client.post("/api/v1/users/", json=user_data_exists)
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "User already exists"


# ------------------------------------------------------------
# GET /{id}
# ------------------------------------------------------------

def test_get_user_success(client):
    # Crear usuario
    user_data = {"name": "testget", "password": "testpass"}
    resp = client.post("/api/v1/users/", json=user_data)
    user = resp.json()
    user_id = user["id"]

    _override_current_user(user_id)

    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]


def test_get_user_not_found(client):
    _override_current_user(1)
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_forbidden(client):
    user1 = client.post("/api/v1/users/", json={"name": "user1", "password": "pass1"}).json()
    user2 = client.post("/api/v1/users/", json={"name": "user2", "password": "pass2"}).json()


    _override_current_user(user2["id"])
    response = client.get(f"/api/v1/users/{user1['id']}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not Authorized"


# ------------------------------------------------------------
# GET / (listar usuarios)
# ------------------------------------------------------------

def test_get_users_list(client):
    client.post("/api/v1/users/", json={"name": "list1", "password": "pass1"})
    client.post("/api/v1/users/", json={"name": "list2", "password": "pass2"})

    _override_current_user(1)

    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json() 
    assert data  == [
	{
		"id": 1,
		"name": "list1"
	},
	{
		"id": 2,
		"name": "list2"
	}
    ]


# ------------------------------------------------------------
# PUT /{id}
# ------------------------------------------------------------

def test_put_user_success(client):
    user = client.post("/api/v1/users/", json={"name": "putuser", "password": "oldpass"}).json()
    user_id = user["id"]

    _override_current_user(user_id)

    update_data = {"name": "putuser_updated", "password": "newpass"}
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "putuser_updated"


def test_put_user_not_found(client):
    _override_current_user(1)
    update_data = {"name": "newname", "password": "newpass"}
    response = client.put("/api/v1/users/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_put_user_forbidden(client):
    user1 = client.post("/api/v1/users/", json={"name": "forbid1", "password": "pass1"}).json()
    user2 = client.post("/api/v1/users/", json={"name": "forbid2", "password": "pass2"}).json()

    _override_current_user(user2["id"])

    update_data = {"name": "hacked", "password": "hackedpass"}
    response = client.put(f"/api/v1/users/{user1['id']}", json=update_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not Authorized"


# ------------------------------------------------------------
# DELETE /{id}
# ------------------------------------------------------------

def test_delete_user_success(client):
    user = client.post("/api/v1/users/", json={"name": "deleteuser", "password": "pass"}).json()
    user_id = user["id"]

    _override_current_user(user_id)

    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "User removed correctly"}

    response_get = client.get(f"/api/v1/users/{user_id}")
    assert response_get.status_code == 404


def test_delete_user_not_found(client):
    _override_current_user(1)
    response = client.delete("/api/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_forbidden(client):
    user1 = client.post("/api/v1/users/", json={"name": "delforbid1", "password": "pass1"}).json()
    user2 = client.post("/api/v1/users/", json={"name": "delforbid2", "password": "pass2"}).json()

    _override_current_user(user2["id"])

    response = client.delete(f"/api/v1/users/{user1['id']}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not Authorized"