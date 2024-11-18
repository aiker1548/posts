import sys
import os
from src.models import Post, PostResponse
import asyncpg
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime

router = APIRouter()

async def get_db_connection():
    conn = await asyncpg.connect(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
    )
    try:
        yield conn
    finally:
        await conn.close()

@router.post("/posts/create", response_model=PostResponse)
async def create_post(post: Post, conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        created_at = datetime.utcnow()
        if post.post_tags:
            query = """
            WITH inserted AS (
                INSERT INTO posts (title, content, author_id, created_at)
                VALUES ($1, $2, $3, $4)
                RETURNING id
            )
            INSERT INTO post_tags (post_id, tag_id)
            SELECT (SELECT id FROM inserted), unnest($5::int[])
            RETURNING (SELECT id FROM inserted);
            """
            row = await conn.fetchrow(query, post.title, post.content, post.author_id, created_at, post.post_tags)
        else:
            query = """
            INSERT INTO posts (title, content, author_id, created_at)
            VALUES ($1, $2, $3, $4)
            RETURNING id;
            """
            row = await conn.fetchrow(query, post.title, post.content, post.author_id, created_at)

        # Проверка результата
        if row is None:
            print("Ошибка: вставка не удалась, row вернул None")

 
        
        return PostResponse(id=row[0], title=post.title, content=post.content, author_id=post.author_id, created_at=created_at, post_tags=post.post_tags)
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
        query = """
        SELECT p.id, p.title, p.content, p.author_id, p.created_at,
               ARRAY_AGG(t.name) AS tags
        FROM posts p
        LEFT JOIN post_tags pt ON p.id = pt.post_id
        LEFT JOIN tags t ON pt.tag_id = t.id
        WHERE p.id = $1
        GROUP BY p.id, p.title, p.content, p.author_id, p.created_at;
        """
        row = await conn.fetchrow(query, post_id)
        if row:
            return PostResponse(**dict(row))
        else:
            raise HTTPException(status_code=404, detail="Пост не найден")
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении поста: {str(error)}"
        )

@router.put("/posts/update/{post_id}", response_model=PostResponse)
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

@router.delete("/posts/delete/{post_id}")
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


@router.get("/posts/user/{user_id}", response_model=List[PostResponse])
async def get_posts_by_user(user_id: int, conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        query = "SELECT id, title, content, author_id, created_at FROM posts WHERE author_id = $1"
        rows = await conn.fetch(query, user_id)
        return [PostResponse(**dict(row)) for row in rows]
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении постов пользователя: {str(error)}"
        )
