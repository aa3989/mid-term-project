
from app.calculator_memento import CalculatorMemento
from app.exceptions import HistoryError


class HistoryManager:
    """Manage calculation history using the Memento pattern."""

    def __init__(self, max_history_size=100):
        if max_history_size <= 0:
            raise HistoryError("Maximum history size must be positive.")

        self.max_history_size = max_history_size
        self._history = []
        self._undo_stack = []
        self._redo_stack = []

    @property
    def history(self):
        """Return a copy of calculation history."""
        return self._history.copy()

    def _save_state(self):
        """Save current history before modifying it."""
        self._undo_stack.append(
            CalculatorMemento.create(self._history)
        )
        self._redo_stack.clear()

    def add_calculation(self, calculation):
        """Add a new calculation to history."""
        self._save_state()
        self._history.append(calculation)

        if len(self._history) > self.max_history_size:
            self._history.pop(0)

    def undo(self):
        """Undo the last history modification."""
        if not self._undo_stack:
            raise HistoryError("Nothing to undo.")

        self._redo_stack.append(
            CalculatorMemento.create(self._history)
        )

        self._history = self._undo_stack.pop().restore()
        return self.history

    def redo(self):
        """Redo a previously undone modification."""
        if not self._redo_stack:
            raise HistoryError("Nothing to redo.")

        self._undo_stack.append(
            CalculatorMemento.create(self._history)
        )

        self._history = self._redo_stack.pop().restore()
        return self.history

    def clear(self):
        """Clear history while preserving undo support."""
        if self._history:
            self._save_state()
            self._history.clear()

    def replace_history(self, calculations):
        """Replace history with a collection of calculations."""
        calculations = list(calculations)
        self._save_state()
        self._history = calculations[-self.max_history_size:]

    def __len__(self):
        return len(self._history)
