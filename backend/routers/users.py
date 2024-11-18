import sys
import os
from src.models import User, LoginUser
import asyncpg
from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()

@router.get("/users")
async def get_users():
    return {"message": "Hello World"}


@router.post("/users/register")
async def register_user(user: User):
    try:
        conn = await asyncpg.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            host=os.getenv("POSTGRES_HOST"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT"),
        )
        try:
            query = """
            INSERT INTO users (username, email, password)
            VALUES ($1, $2, $3)
            RETURNING id
            """
            user_id = await conn.fetchval(query, user.username, user.email, user.password)
            return {"message": "Пользователь успешно зарегистрирован", "user_id": user_id}
        finally:
            await conn.close()
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при регистрации пользователя: {str(error)}"
        )

@router.post("/users/login")
async def login_user(user: LoginUser):
    try:
        conn = await asyncpg.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            host=os.getenv("POSTGRES_HOST"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT"),
        )
        try:
            query = """
            SELECT id, email, password
            FROM users
            WHERE email = $1
            """
            user_data = await conn.fetchrow(query, user.email)
            if user_data:
                if user_data["password"] == user.password:
                    return {"message": "Пользователь успешно авторизован", "user_id": user_data["id"]}
            else:
                raise HTTPException(status_code=401, detail="Неверный email или пароль")
        finally:
            await conn.close()
    except asyncpg.PostgresError as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при авторизации пользователя: {str(error)}"
        )
