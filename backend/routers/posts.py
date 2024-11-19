import sys
import os
from src.models import Post, PostResponse
import asyncpg
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from typing import List
from datetime import datetime
import shutil
from fastapi.responses import FileResponse

UPLOAD_FOLDER = "uploads/images"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author_id: int = Form(...),
    image: UploadFile = File(...),  # Обработка изображения
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    try:
        # Сохранение изображения
        image_path = os.path.join(f'{UPLOAD_FOLDER}', image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        created_at = datetime.utcnow()
        
        # Вставка поста в базу данных
        query = """
        INSERT INTO posts (title, content, author_id, created_at, image_path)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, title, content, author_id, created_at, image_path;
        """
        image_url = f"{UPLOAD_FOLDER}/{image.filename}"  # Ссылка на изображение
        row = await conn.fetchrow(query, title, content, author_id, created_at, image_url)

        # Возврат ответа с данными
        if row:
            return PostResponse(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                author_id=row["author_id"],
                created_at=row["created_at"].strftime('%Y-%m-%d %H:%M:%S'),
                image_url=row["image_path"]
            )
        else:
            raise HTTPException(status_code=400, detail="Ошибка при создании поста.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке запроса: {str(e)}")
    

@router.get("/posts", response_model=List[PostResponse])
async def get_posts(conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        # URL сервера (замените на ваш хост)
        base_url = os.getenv("BASE_URL")

        query = """
        SELECT id, title, content, author_id, created_at, image_path
        FROM posts
        ORDER BY created_at DESC
        """
        rows = await conn.fetch(query)
        
        # Формируем список постов с ссылкой на изображение
        posts = [
            PostResponse(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                author_id=row["author_id"],
                created_at=row["created_at"],
                image_url=f"{base_url}/posts/{row['id']}/download_image" if row["image_path"] else None
            )
            for row in rows
        ]
        return posts
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении постов: {str(error)}"
        )
    
@router.get("/posts/{post_id}/download_image")
async def download_image(post_id: int, conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        # Запрос для получения пути к изображению
        query = "SELECT image_path FROM posts WHERE id = $1"
        row = await conn.fetchrow(query, post_id)
        print(row)
        if row and row["image_path"]:
            image_path = row["image_path"]
            print(image_path)
            if os.path.exists(image_path):
                return FileResponse(path=image_path, media_type="image/jpeg", filename=os.path.basename(image_path))
            else:
                raise HTTPException(status_code=404, detail="Изображение не найдено")
        else:
            raise HTTPException(status_code=404, detail="Пост или изображение не найдено")
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при скачивании изображения: {str(error)}"
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
        # URL сервера (замените на ваш хост)
        base_url = os.getenv("BASE_URL")

        query = """
        SELECT id, title, content, author_id, created_at, image_path
        FROM posts
        WHERE author_id = $1
        ORDER BY created_at DESC
        """
        rows = await conn.fetch(query, user_id)

        # Формируем список постов с ссылкой на изображение
        posts = [
            PostResponse(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                author_id=row["author_id"],
                created_at=row["created_at"],
                image_url=f"{base_url}/posts/{row['id']}/download_image" if row["image_path"] else None
            )
            for row in rows
        ]
        return posts
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении постов пользователя: {str(error)}"
        )
