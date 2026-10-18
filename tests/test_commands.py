
import pytest

from app.commands import Command, CalculationCommand, CommandQueue
from app.exceptions import OperationError


def test_calculation_command_execution(mocker_unused=None):
    """Verify a command delegates to its calculator."""

    class FakeCalculator:
        def calculate(self, operation, a, b):
            assert operation == "add"
            assert a == 10
            assert b == 5
            return 15

    command = CalculationCommand(FakeCalculator(), "add", 10, 5)

    assert command.execute() == 15


def test_command_queue_execution_order():
    """Verify commands execute in FIFO order."""
    execution_order = []

    class TestCommand(Command):
        def __init__(self, value):
            self.value = value

        def execute(self):
            execution_order.append(self.value)
            return self.value

    queue = CommandQueue()
    queue.add_command(TestCommand(1))
    queue.add_command(TestCommand(2))
    queue.add_command(TestCommand(3))

    assert len(queue) == 3
    assert queue.execute_all() == [1, 2, 3]
    assert execution_order == [1, 2, 3]
    assert len(queue) == 0


def test_empty_command_queue():
    """Verify executing an empty queue returns no results."""
    queue = CommandQueue()

    assert queue.execute_all() == []
    assert len(queue) == 0


def test_command_propagates_errors():
    """Verify calculation errors propagate to the caller."""

    class FakeCalculator:
        def calculate(self, operation, a, b):
            raise OperationError("Invalid operation")

    command = CalculationCommand(
        FakeCalculator(),
        "unknown",
        10,
        5,
    )

    with pytest.raises(OperationError):
        command.execute()


def test_abstract_command_execute():
    """Cover the abstract command's default implementation."""

    class TestCommand(Command):
        def execute(self):
            return super().execute()

    assert TestCommand().execute() is None
