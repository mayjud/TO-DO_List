from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from app.domain.models import Task


class BaseTaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Task]:
        """Return all tasks."""

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task | None:
        """Return a task by its id."""

    @abstractmethod
    def create(self, task: Task) -> Task:
        """Create a new task."""

    @abstractmethod
    def update(self, task_id: str, task: Task) -> Task:
        """Update a task by id."""

    @abstractmethod
    def delete(self, task_id: str) -> None:
        """Delete a task by id."""

    @abstractmethod
    def move_to_state(self, task_id: str, estado: str) -> Task:
        """Move a task to a new state."""
