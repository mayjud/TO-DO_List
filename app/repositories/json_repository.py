from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from app.core.config import TASKS_FILE_PATH
from app.domain.exceptions import InvalidTaskDataError, TaskNotFoundError
from app.domain.models import Task
from app.repositories.base_repository import BaseTaskRepository

logger = logging.getLogger(__name__)


class JsonTaskRepository(BaseTaskRepository):
    def __init__(self, file_path: str | Path | None = None) -> None:
        self.file_path = Path(file_path) if file_path else TASKS_FILE_PATH
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _read_all(self) -> list[dict[str, Any]]:
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
            if not isinstance(payload, list):
                raise InvalidTaskDataError("El archivo de tareas no tiene un formato válido.")
            return payload
        except json.JSONDecodeError as exc:
            logger.exception("JSON inválido en %s", self.file_path)
            raise InvalidTaskDataError("El archivo de tareas está corrupto.") from exc

    def _write_all(self, tasks: list[dict[str, Any]]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)

    def get_all(self) -> list[Task]:
        items = self._read_all()
        return [Task.from_dict(task) for task in items]

    def get_by_id(self, task_id: str) -> Task | None:
        tasks = self.get_all()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def create(self, task: Task) -> Task:
        tasks = self.get_all()
        tasks.append(task)
        self._write_all([item.to_dict() for item in tasks])
        logger.info("Task creada: %s", task.id)
        return task

    def update(self, task_id: str, task: Task) -> Task:
        tasks = self.get_all()
        found = False
        for index, current in enumerate(tasks):
            if current.id == task_id:
                tasks[index] = task
                found = True
                break
        if not found:
            raise TaskNotFoundError(f"Task {task_id} no encontrada.")
        self._write_all([item.to_dict() for item in tasks])
        logger.info("Task actualizada: %s", task_id)
        return task

    def delete(self, task_id: str) -> None:
        tasks = self.get_all()
        filtered = [task for task in tasks if task.id != task_id]
        if len(filtered) == len(tasks):
            raise TaskNotFoundError(f"Task {task_id} no encontrada.")
        self._write_all([item.to_dict() for item in filtered])
        logger.info("Task eliminada: %s", task_id)

    def move_to_state(self, task_id: str, estado: str) -> Task:
        tasks = self.get_all()
        for task in tasks:
            if task.id == task_id:
                task.estado = estado
                self._write_all([item.to_dict() for item in tasks])
                logger.info("Task movida a %s: %s", estado, task_id)
                return task
        raise TaskNotFoundError(f"Task {task_id} no encontrada.")
