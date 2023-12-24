from functools import wraps
from typing import Any, Callable


class GoogleApiAccessError(Exception):
    """Exception raised when an error occurs during API access."""

    pass


def error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise GoogleApiAccessError(f"An error occurred in {func.__name__}: {e}")

    return wrapper
