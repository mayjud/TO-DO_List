from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.domain.exceptions import InvalidTaskDataError, TaskNotFoundError
from app.services.task_service import TaskService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_task_service(request: Request) -> TaskService:
    task_service = getattr(request.app.state, "task_service", None)
    if task_service is None:
        raise HTTPException(status_code=500, detail="Task service not configured.")
    return task_service


@router.get("/", response_class=HTMLResponse)
async def dashboard_view(request: Request, task_service: TaskService = Depends(get_task_service)) -> HTMLResponse:
    tasks = task_service.list_tasks()
    return request.app.state.templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tasks": tasks,
            "todo_tasks": [task for task in tasks if task.estado == "todo"],
            "doing_tasks": [task for task in tasks if task.estado == "doing"],
            "done_tasks": [task for task in tasks if task.estado == "done"],
        },
    )


@router.get("/tasks")
async def list_tasks(task_service: TaskService = Depends(get_task_service)) -> list[dict[str, Any]]:
    return [task.to_dict() for task in task_service.list_tasks()]


@router.post("/tasks")
async def create_task(
    title: str = Form(...),
    description: str = Form(""),
    estado: str = Form("todo"),
    task_service: TaskService = Depends(get_task_service),
) -> RedirectResponse:
    try:
        task_service.create_task(title=title, description=description, estado=estado)
    except InvalidTaskDataError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RedirectResponse(url="/", status_code=303)


@router.post("/tasks/{task_id}/move")
async def move_task(
    task_id: str,
    estado: str = Form(...),
    task_service: TaskService = Depends(get_task_service),
) -> RedirectResponse:
    try:
        task_service.move_task(task_id, estado)
    except (TaskNotFoundError, InvalidTaskDataError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RedirectResponse(url="/", status_code=303)


@router.post("/tasks/{task_id}/delete")
async def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> RedirectResponse:
    try:
        task_service.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url="/", status_code=303)


@router.get("/tasks/{task_id}")
async def get_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> dict[str, Any]:
    try:
        task = task_service.get_task(task_id)
        return task.to_dict()
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
