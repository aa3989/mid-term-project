
from dataclasses import dataclass
from typing import Tuple

from app.calculation import Calculation


@dataclass(frozen=True)
class CalculatorMemento:
    """Stores a snapshot of calculator history."""

    history: Tuple[Calculation, ...]

    @classmethod
    def create(cls, history):
        """Create a snapshot of the current history."""
        return cls(tuple(history))

    def restore(self):
        """Restore the saved history as a list."""
        return list(self.history)
