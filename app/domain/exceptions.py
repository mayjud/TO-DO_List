class TaskError(Exception):
    """Base exception for task operations."""


class TaskNotFoundError(TaskError):
    """Raised when a task cannot be found."""


class InvalidTaskDataError(TaskError):
    """Raised when task payload is invalid."""
