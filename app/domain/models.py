from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

TaskStatus = Literal["todo", "doing", "done"]


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    date_creacion: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    estado: TaskStatus = "todo"

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_creacion": self.date_creacion,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, str]) -> "Task":
        return cls(
            id=payload.get("id") or str(uuid4()),
            title=payload.get("title", ""),
            description=payload.get("description", ""),
            date_creacion=payload.get("date_creacion") or datetime.now(timezone.utc).isoformat(),
            estado=payload.get("estado", "todo"),
        )
