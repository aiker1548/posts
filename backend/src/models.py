from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict
from fastapi import WebSocket

class User(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

class Post(BaseModel):
    title: str
    content: str
    author_id: int
    post_tags: List[int]

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    image_url: str = None
    post_tags: List[int] = []

class TagCreate(BaseModel):
    name: str


