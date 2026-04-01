import aiosqlite
from typing import AsyncGenerator
from contextlib import asynccontextmanager


# ========== Менеджер сессий (подключений) ==========
# Асинхронный контекстный менеджер для соединения с БД
@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Создаёт и возвращает соединение с БД, закрывая его после использования."""
    async with aiosqlite.connect("database.sqlite") as db:
        # Включаем поддержку внешних ключей (опционально)
        await db.execute("PRAGMA foreign_keys = ON")
        yield db


# FastAPI-зависимость, которую можно внедрять в эндпоинты
async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Зависимость FastAPI, предоставляющая сессию БД на время запроса."""
    async with get_db_connection() as db:
        yield db
