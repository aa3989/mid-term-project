
from functools import wraps

from app.operations import OperationFactory


def dynamic_operations(func):
    """Decorate a help function with registered operations."""

    @wraps(func)
    def wrapper():
        operations = ", ".join(OperationFactory._operations.keys())
        return f"Operations: {operations}\n{func()}"

    return wrapper


@dynamic_operations
def get_help_menu():
    """Return the calculator's basic help information."""
    return (
        "Usage: <operation> <number1> <number2>\n"
        "Commands: help, history, undo, redo, clear, queue, run, exit"
    )
