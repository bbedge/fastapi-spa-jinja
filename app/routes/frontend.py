"""Frontend routers"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=['Frontend'])
title = "FastAPI + SPA, пример."


# Подключение favicon
@router.get("/favicon.ico", include_in_schema=False, summary="Подключение иконки.")
async def favicon():
    response = FileResponse("app/static/images/favicon.ico")
    response.headers["Cache-Control"] = "public, max-age=31536000"
    return response


# Обработка корня
@router.get('/', include_in_schema=False, response_class=HTMLResponse, summary="Начальная страница.")
async def index(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      context={"request": request,
                                               "title": title})
