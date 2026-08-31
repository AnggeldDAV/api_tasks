# test_task.py
from types import SimpleNamespace

from main import app
from deps.deps import get_current_user


def _override_current_user(user_id: int):
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=user_id)


def _create_user(client, name="user", password="pass"):
    response = client.post("/api/v1/users/", json={"name": name, "password": password})
    assert response.status_code == 201
    return response.json()


def _create_task(client, user_id, title="Test task", description="Description",
                 state="pending", priority=False, date="2025-12-31T23:59:59"):
    _override_current_user(user_id)
    response = client.post("/api/v1/tasks/", json={
        "title": title,
        "description": description,
        "state": state,
        "priority": priority,
        "date": date
    })
    assert response.status_code == 201
    return response.json()


# ------------------------------------------------------------
# POST /
# ------------------------------------------------------------

def test_create_task_success(client):
    user = _create_user(client)
    task_data = {
        "title": "Mi tarea",
        "description": "Descripción de la tarea",
        "state": "in_progress",
        "priority": True,
        "date": "2025-12-31T23:59:59"
    }
    _override_current_user(user["id"])

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["state"] == task_data["state"]
    assert data["priority"] == task_data["priority"]

    assert "date" in data
    assert data["user_id"] == user["id"]
    assert "id" in data


def test_create_task_user_not_found(client):

    _override_current_user(999)
    response = client.post("/api/v1/tasks/", json={
        "title": "Tarea",
        "description": "Desc",
        "state": "pending",
        "priority": False,
        "date": "2025-12-31T23:59:59"
    })

    assert response.status_code == 400
    assert "detail" in response.json()


def test_create_task_validation_error(client):

    user = _create_user(client)
    _override_current_user(user["id"])

    response = client.post("/api/v1/tasks/", json={
        "title": "Falta state",
        "description": "Desc",
        "priority": False
    })
    assert response.status_code == 422


# ------------------------------------------------------------
# GET / 
# ------------------------------------------------------------

def test_get_tasks_list(client):
    user1 = _create_user(client, "user1", "pass1")
    user2 = _create_user(client, "user2", "pass2")
    
    _create_task(client, user1["id"], "Tarea 1", "Desc 1")
    _create_task(client, user1["id"], "Tarea 2", "Desc 2", state="done", priority=True)
    
    _create_task(client, user2["id"], "Tarea 3", "Desc 2", state="done", priority=True)

    _override_current_user(user1["id"])
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    tasks1 = response.json()
    assert len(tasks1) == 2
    titles1 = {t["title"] for t in tasks1}
    assert "Tarea 1" in titles1
    assert "Tarea 2" in titles1
    for t in tasks1:
        assert t["user_id"] == user1["id"]
    
    _override_current_user(user2["id"])
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    tasks2 = response.json()
    assert len(tasks2) == 1
    titles2 = {t["title"] for t in tasks2}
    assert "Tarea 3" in titles2
    for t in tasks2:
        assert t["user_id"] == user2["id"]



def test_get_tasks_list_empty(client):
    user = _create_user(client)
    _override_current_user(user["id"])
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert response.json() == []


# ------------------------------------------------------------
# GET /{id}
# ------------------------------------------------------------

def test_get_task_success(client):
    user = _create_user(client)
    task = _create_task(client, user["id"])

    _override_current_user(user["id"])
    response = client.get(f"/api/v1/tasks/{task['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task["id"]
    assert data["title"] == task["title"]
    assert data["state"] == task["state"]
    assert data["priority"] == task["priority"]
    assert "date" in data


def test_get_task_not_found(client):
    user = _create_user(client)
    _override_current_user(user["id"])
    response = client.get("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_task_forbidden(client):
    user1 = _create_user(client, "user1", "pass1")
    user2 = _create_user(client, "user2", "pass2")
    task = _create_task(client, user1["id"])

    _override_current_user(user2["id"])
    response = client.get(f"/api/v1/tasks/{task['id']}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not Authorized"


# ------------------------------------------------------------
# PUT /{id}
# ------------------------------------------------------------

def test_put_task_success(client):
    user = _create_user(client)
    task = _create_task(client, user["id"])

    _override_current_user(user["id"])
    update_data = {
        "title": "Tarea actualizada",
        "description": "Desc actualizada",
        "state": "done",
        "priority": True,
        "date": "2026-01-01T00:00:00"
    }
    response = client.put(f"/api/v1/tasks/{task['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Tarea actualizada"
    assert data["description"] == "Desc actualizada"
    assert data["state"] == "done"
    assert data["priority"] is True
    assert data["id"] == task["id"]


def test_put_task_not_found(client):
    user = _create_user(client)
    _override_current_user(user["id"])
    update_data = {
        "title": "Tarea",
        "description": "Desc",
        "state": "pending",
        "priority": False,
        "date": "2025-12-31T23:59:59"
    }
    response = client.put("/api/v1/tasks/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_put_task_forbidden(client):
    user1 = _create_user(client, "user1", "pass1")
    user2 = _create_user(client, "user2", "pass2")
    task = _create_task(client, user1["id"])

    _override_current_user(user2["id"])
    update_data = {
        "title": "Hacked",
        "description": "Hacked",
        "state": "pending",
        "priority": False,
        "date": "2025-12-31T23:59:59"
    }
    response = client.put(f"/api/v1/tasks/{task['id']}", json=update_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not Authorized"


# ------------------------------------------------------------
# DELETE /{id}
# ------------------------------------------------------------

def test_delete_task_success(client):
    user = _create_user(client)
    task = _create_task(client, user["id"])

    _override_current_user(user["id"])
    response = client.delete(f"/api/v1/tasks/{task['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task removed correctly"}

    response_get = client.get(f"/api/v1/tasks/{task['id']}")
    assert response_get.status_code == 404


def test_delete_task_not_found(client):
    user = _create_user(client)
    _override_current_user(user["id"])
    response = client.delete("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task_forbidden(client):
    user1 = _create_user(client, "user1", "pass1")
    user2 = _create_user(client, "user2", "pass2")
    task = _create_task(client, user1["id"])

    _override_current_user(user2["id"])
    response = client.delete(f"/api/v1/tasks/{task['id']}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not Authorized"