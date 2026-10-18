
from abc import ABC, abstractmethod
from collections import deque


class Command(ABC):
    """Abstract interface for executable commands."""

    @abstractmethod
    def execute(self):
        """Execute the command."""
        pass


class CalculationCommand(Command):
    """Encapsulate a calculator operation and its operands."""

    def __init__(self, calculator, operation, a, b):
        self.calculator = calculator
        self.operation = operation
        self.a = a
        self.b = b

    def execute(self):
        """Execute the stored calculation."""
        return self.calculator.calculate(
            self.operation,
            self.a,
            self.b,
        )


class CommandQueue:
    """Manage calculation commands in FIFO order."""

    def __init__(self):
        self._queue = deque()

    def add_command(self, command):
        """Add a command to the queue."""
        self._queue.append(command)

    def execute_all(self):
        """Execute queued commands in insertion order."""
        results = []

        while self._queue:
            command = self._queue.popleft()
            results.append(command.execute())

        return results

    def __len__(self):
        """Return the number of pending commands."""
        return len(self._queue)
