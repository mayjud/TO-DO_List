from __future__ import annotations

import logging
from typing import Literal

from app.domain.exceptions import InvalidTaskDataError, TaskNotFoundError
from app.domain.models import Task, TaskStatus
from app.repositories.base_repository import BaseTaskRepository

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, repository: BaseTaskRepository) -> None:
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        return self.repository.get_all()

    def create_task(self, title: str, description: str, estado: TaskStatus = "todo") -> Task:
        title = (title or "").strip()
        description = (description or "").strip()
        if not title:
            raise InvalidTaskDataError("El título es obligatorio.")
        if estado not in {"todo", "doing", "done"}:
            raise InvalidTaskDataError("Estado no válido.")

        task = Task(title=title, description=description, estado=estado)
        logger.info("Creando tarea %s", task.id)
        return self.repository.create(task)

    def get_task(self, task_id: str) -> Task:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} no encontrada.")
        return task

    def update_task(self, task_id: str, title: str, description: str, estado: TaskStatus) -> Task:
        task = self.get_task(task_id)
        title = (title or "").strip()
        description = (description or "").strip()
        if not title:
            raise InvalidTaskDataError("El título es obligatorio.")
        if estado not in {"todo", "doing", "done"}:
            raise InvalidTaskDataError("Estado no válido.")

        updated = Task(
            id=task.id,
            title=title,
            description=description,
            date_creacion=task.date_creacion,
            estado=estado,
        )
        logger.info("Actualizando tarea %s", task_id)
        return self.repository.update(task_id, updated)

    def delete_task(self, task_id: str) -> None:
        self.get_task(task_id)
        logger.info("Eliminando tarea %s", task_id)
        self.repository.delete(task_id)

    def move_task(self, task_id: str, next_state: TaskStatus) -> Task:
        if next_state not in {"todo", "doing", "done"}:
            raise InvalidTaskDataError("Estado no válido.")
        logger.info("Moviendo tarea %s a %s", task_id, next_state)
        return self.repository.move_to_state(task_id, next_state)
