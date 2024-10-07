import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.src.models import Post, PostResponse
import asyncpg
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime

router = APIRouter()

async def get_db_connection():
    conn = await asyncpg.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
    )
    try:
        yield conn
    finally:
        await conn.close()

@router.post("/posts", response_model=PostResponse)
async def create_post(post: Post, conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        query = """
        INSERT INTO posts (title, content, author_id, created_at)
        VALUES ($1, $2, $3, $4)
        RETURNING id, title, content, author_id, created_at
        """
        created_at = datetime.utcnow()
        row = await conn.fetchrow(query, post.title, post.content, post.author_id, created_at)
        return PostResponse(**dict(row))
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при создании поста: {str(error)}"
        )

@router.get("/posts", response_model=List[PostResponse])
async def get_posts(conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        query = "SELECT id, title, content, author_id, created_at FROM posts ORDER BY created_at DESC"
        rows = await conn.fetch(query)
        return [PostResponse(**dict(row)) for row in rows]
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении постов: {str(error)}"
        )

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        query = "SELECT id, title, content, author_id, created_at FROM posts WHERE id = $1"
        row = await conn.fetchrow(query, post_id)
        if row:
            return PostResponse(**dict(row))
        else:
            raise HTTPException(status_code=404, detail="Пост не найден")
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении поста: {str(error)}"
        )

@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post: Post, conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        query = """
        UPDATE posts
        SET title = $1, content = $2
        WHERE id = $3 AND author_id = $4
        RETURNING id, title, content, author_id, created_at
        """
        row = await conn.fetchrow(query, post.title, post.content, post_id, post.author_id)
        if row:
            return PostResponse(**dict(row))
        else:
            raise HTTPException(status_code=404, detail="Пост не найден или у вас нет прав на его редактирование")
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обновлении поста: {str(error)}"
        )

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        query = "DELETE FROM posts WHERE id = $1"
        result = await conn.execute(query, post_id)
        if result == "DELETE 1":
            return {"message": "Пост успешно удален"}
        else:
            raise HTTPException(status_code=404, detail="Пост не найден или у вас нет прав на его удаление")
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при удалении поста: {str(error)}"
        )

