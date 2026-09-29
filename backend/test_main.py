from fastapi.testclient import TestClient

from main import app, posts

client = TestClient(app)


def setup_function():
    posts.clear()


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_post():
    res = client.post("/posts", json={"author": "Omar", "content": "first post"})
    assert res.status_code == 201
    body = res.json()
    assert body["author"] == "Omar"
    assert body["content"] == "first post"
    assert "id" in body
    assert "created_at" in body


def test_create_post_missing_content_returns_422():
    res = client.post("/posts", json={"author": "Omar"})
    assert res.status_code == 422
    assert res.json()["detail"][0]["loc"] == ["body", "content"]


def test_list_posts_newest_first():
    client.post("/posts", json={"author": "Omar", "content": "one"})
    client.post("/posts", json={"author": "Salama", "content": "two"})
    res = client.get("/posts")
    assert res.status_code == 200
    contents = [p["content"] for p in res.json()]
    assert contents == ["two", "one"]
