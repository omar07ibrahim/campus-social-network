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


def test_whitespace_only_content_returns_422():
    res = client.post("/posts", json={"author": "Omar", "content": "   "})
    assert res.status_code == 422
    assert res.json()["detail"][0]["loc"] == ["body", "content"]
    assert posts == []


def test_content_over_1000_chars_returns_422():
    res = client.post("/posts", json={"author": "Omar", "content": "x" * 1001})
    assert res.status_code == 422
    assert res.json()["detail"][0]["type"] == "string_too_long"


def test_content_is_trimmed():
    res = client.post("/posts", json={"author": " Makar ", "content": "  hi  "})
    assert res.status_code == 201
    assert res.json()["author"] == "Makar"
    assert res.json()["content"] == "hi"


def test_list_posts_empty():
    res = client.get("/posts")
    assert res.status_code == 200
    assert res.json() == []


def test_list_posts_newest_first():
    client.post("/posts", json={"author": "Omar", "content": "one"})
    client.post("/posts", json={"author": "Salama", "content": "two"})
    res = client.get("/posts")
    assert res.status_code == 200
    contents = [p["content"] for p in res.json()]
    assert contents == ["two", "one"]
