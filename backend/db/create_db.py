import os
import logging
from dotenv import load_dotenv
from pathlib import Path
import asyncpg

# Получаем абсолютный путь к текущему файлу
current_file = Path(__file__).resolve()

# Получаем путь к корневой директории проекта (два уровня вверх)
project_root = current_file.parent.parent.parent

# Формируем путь к файлу .env
env_path = project_root / '.env'

# Загружаем переменные окружения
load_dotenv(dotenv_path=env_path)


async def create_tables():
    commands = (
        '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL REFERENCES users(id),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        '''
    )

    try:
        conn = await asyncpg.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        try:
            for command in commands:
                try:
                    async with conn.transaction():
                        await conn.execute(command)
                    logging.info(f"Команда выполнена: {command}")
                except asyncpg.PostgresError as error:
                    logging.error(f"Ошибка при выполнении команды: {command}")
                    logging.error(error)
            return True
        finally:
            await conn.close()
    except asyncpg.PostgresError as conn_error:
        logging.error("Ошибка подключения к базе данных")
        logging.error(conn_error)
        return False
