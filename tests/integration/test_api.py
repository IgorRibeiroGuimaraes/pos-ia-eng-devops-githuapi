def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_users_empty(client):
    r = client.get("/users")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_list_repositories_empty(client):
    r = client.get("/repositories")
    assert r.status_code == 200
    assert r.json()["total"] == 0


def test_statistics_empty(client):
    r = client.get("/statistics")
    assert r.status_code == 200
    data = r.json()
    assert data["total_users"] == 0
    assert data["total_repositories"] == 0


def test_get_user_not_found(client):
    r = client.get("/users/nonexistent_user_xyz")
    assert r.status_code == 404


def test_get_repository_not_found(client):
    r = client.get("/repositories/999999")
    assert r.status_code == 404


def test_admin_status_empty(client):
    r = client.get("/admin/status")
    assert r.status_code == 200


def test_user_repositories_not_found(client):
    r = client.get("/users/ghost_user_xyz/repositories")
    assert r.status_code == 404


def test_users_filter_params(client):
    r = client.get("/users?page=1&page_size=5&order_by=followers&order_dir=desc")
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["page_size"] == 5


def test_repositories_filter_params(client):
    r = client.get("/repositories?language=Python&min_stars=10&order_by=stars&order_dir=desc")
    assert r.status_code == 200
