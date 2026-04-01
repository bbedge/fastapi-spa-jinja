import uvicorn
from loguru import logger
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import get_db_connection
from routes.api import router as api_routes
from routes.frontend import router as fronted_routes


@asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:   # if the 'app' parameter is used
async def lifespan(_: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""

    # Создаём таблицу при старте (миграции для примера)
    async with get_db_connection() as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        await db.commit()
    yield
    # Здесь можно закрыть пулы соединений, если есть
    # В данном случае aiosqlite закроет соединения автоматически
    # logger.info("Завершение работы приложения...")


# Регистрация приложения
app = FastAPI(lifespan=lifespan)

# Подключение статики
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Обработка ошибки 404
@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse("app/templates/404.html")


# Настройка CORS- В примере не используется ORM и пул соединений.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,    # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Регистрация маршрутов
app.include_router(api_routes)  # api
app.include_router(fronted_routes)  # fronted


if __name__ == "__main__":
    logger.info(f"Сервер стартован.")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
