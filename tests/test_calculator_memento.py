
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_create_and_restore():
    calculation = Calculation("add", 10, 5)
    history = [calculation]

    memento = CalculatorMemento.create(history)

    assert len(memento.history) == 1
    assert memento.restore() == history


def test_memento_snapshot_is_independent():
    history = [Calculation("add", 10, 5)]
    memento = CalculatorMemento.create(history)

    history.append(Calculation("multiply", 2, 3))

    assert len(memento.restore()) == 1


def test_memento_restore_returns_new_list():
    calculation = Calculation("add", 10, 5)
    memento = CalculatorMemento.create([calculation])

    restored = memento.restore()
    restored.clear()

    assert len(memento.restore()) == 1
