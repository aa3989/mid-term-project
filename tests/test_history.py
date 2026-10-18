
import pytest

from app.calculation import Calculation
from app.history import HistoryManager
from app.exceptions import HistoryError


@pytest.fixture
def manager():
    return HistoryManager(max_history_size=3)


def test_add_calculation(manager):
    calculation = Calculation("add", 10, 5)
    manager.add_calculation(calculation)

    assert len(manager) == 1
    assert manager.history[0].result == 15


def test_undo(manager):
    manager.add_calculation(Calculation("add", 10, 5))
    manager.add_calculation(Calculation("multiply", 2, 3))

    manager.undo()

    assert len(manager) == 1
    assert manager.history[0].result == 15


def test_redo(manager):
    manager.add_calculation(Calculation("add", 10, 5))
    manager.undo()
    manager.redo()

    assert len(manager) == 1


def test_undo_empty_history(manager):
    with pytest.raises(HistoryError, match="Nothing to undo"):
        manager.undo()


def test_redo_without_undo(manager):
    with pytest.raises(HistoryError, match="Nothing to redo"):
        manager.redo()


def test_new_calculation_clears_redo(manager):
    manager.add_calculation(Calculation("add", 10, 5))
    manager.undo()

    manager.add_calculation(Calculation("multiply", 2, 3))

    with pytest.raises(HistoryError):
        manager.redo()


def test_max_history_size(manager):
    for number in range(5):
        manager.add_calculation(
            Calculation("add", number, 1)
        )

    assert len(manager) == 3
    assert manager.history[0].operand1 == 2


def test_clear_history(manager):
    manager.add_calculation(Calculation("add", 10, 5))
    manager.clear()

    assert len(manager) == 0


def test_undo_clear(manager):
    manager.add_calculation(Calculation("add", 10, 5))
    manager.clear()
    manager.undo()

    assert len(manager) == 1


def test_replace_history(manager):
    calculations = [
        Calculation("add", 1, 1),
        Calculation("add", 2, 2),
    ]

    manager.replace_history(calculations)

    assert len(manager) == 2


def test_replace_history_respects_limit(manager):
    calculations = [
        Calculation("add", i, 1)
        for i in range(5)
    ]

    manager.replace_history(calculations)

    assert len(manager) == 3
    assert manager.history[0].operand1 == 2


def test_invalid_history_size():
    with pytest.raises(HistoryError):
        HistoryManager(max_history_size=0)


def test_history_property_returns_copy(manager):
    manager.add_calculation(Calculation("add", 10, 5))

    copied_history = manager.history
    copied_history.clear()

    assert len(manager) == 1
