from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Campus Social Network - Proof of Concept")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PostCreate(BaseModel):
    author: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)


class Post(PostCreate):
    id: str
    created_at: datetime


posts: list[Post] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/posts", response_model=Post, status_code=201)
def create_post(payload: PostCreate):
    post = Post(id=str(uuid4()), created_at=datetime.now(timezone.utc), **payload.model_dump())
    posts.append(post)
    return post


@app.get("/posts", response_model=list[Post])
def list_posts():
    return list(reversed(posts))
