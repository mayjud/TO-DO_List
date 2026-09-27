from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.core.config import ROOT_DIR
from app.repositories.json_repository import JsonTaskRepository
from app.services.task_service import TaskService

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

app = FastAPI(title="Kanban To-Do", version="1.0.0")

app.state.task_service = TaskService(JsonTaskRepository())
app.state.templates = Jinja2Templates(directory=str(ROOT_DIR / "app" / "templates"))

app.mount("/static", StaticFiles(directory=str(ROOT_DIR / "app" / "static")), name="static")
app.include_router(router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": "kanban-api"}


@app.middleware("http")
async def inject_service(request: Request, call_next):
    request.state.task_service = app.state.task_service
    response = await call_next(request)
    return response
