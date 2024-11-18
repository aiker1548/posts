import sys
import os
from src.models import TagCreate, PostResponse
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

async def create_tag(tag: TagCreate, conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        query = "INSERT INTO tags (name) VALUES ($1) ON CONFLICT DO NOTHING RETURNING name"
        result = await conn.fetch(query, tag.name)  # Изменено на fetch и передан tag.name
        return [row['name'] for row in result] if result else []  # Проверка на наличие результата
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tags/default")
async def create_default_tags(conn: asyncpg.Connection = Depends(get_db_connection)):
    default_tags = os.getenv("DEFAULT_TAGS").split(",")
    try:
        # Удаляем все существующие теги
        await conn.execute("DELETE FROM tags")
        
        # Создаем новые теги
        for tag in default_tags:
            await create_tag(TagCreate(name=tag), conn)
        
        return {"message": "Старые теги удалены, новые теги созданы"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении тегов: {str(e)}")

@router.get('/tags/all')
async def get_all_tags(conn: asyncpg.Connection = Depends(get_db_connection)):
    try:
        query = "SELECT name, id FROM tags"
        result = await conn.fetch(query)
        return [{"name": row['name'], "id": row['id']} for row in result]  # Изменен формат возвращаемых данных
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении тегов: {str(e)}")
