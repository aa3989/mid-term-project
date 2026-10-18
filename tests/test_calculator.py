
import pandas as pd
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


@pytest.fixture
def calculator(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=True,
    )

    return Calculator(config)


def test_calculate(calculator):
    result = calculator.calculate("add", 10, 5)

    assert result == 15
    assert len(calculator.history) == 1


def test_calculation_autosave(calculator):
    calculator.calculate("multiply", 4, 5)

    path = calculator.config.history_file_path

    assert path.exists()

    dataframe = pd.read_csv(path)

    assert dataframe.iloc[0]["result"] == 20


def test_calculation_logging(calculator):
    calculator.calculate("add", 10, 5)

    path = calculator.config.log_file_path

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Operation: add" in content
    assert "Result: 15" in content


def test_calculator_undo_redo(calculator):
    calculator.calculate("add", 10, 5)

    calculator.undo()
    assert len(calculator.history) == 0

    calculator.redo()
    assert len(calculator.history) == 1


def test_calculator_clear(calculator):
    calculator.calculate("add", 10, 5)

    calculator.clear()

    assert len(calculator.history) == 0


def test_invalid_calculator_input(calculator):
    with pytest.raises(ValidationError):
        calculator.calculate("add", "invalid", 5)


def test_remove_observer(calculator):
    observer = calculator.observers[0]

    calculator.remove_observer(observer)

    assert observer not in calculator.observers


def test_autosave_disabled(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )

    calculator = Calculator(config)
    calculator.calculate("add", 10, 5)

    assert not config.history_file_path.exists()


def test_load_history_from_csv(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=True,
    )

    original = Calculator(config)
    original.calculate("add", 10, 5)
    original.calculate("multiply", 4, 3)

    restored = Calculator(config)
    restored.load_history()

    assert len(restored.history) == 2
    assert restored.history[0].operation == "add"
    assert restored.history[0].result == 15.0
    assert restored.history[1].operation == "multiply"
    assert restored.history[1].result == 12.0
    assert (
        restored.history[0].timestamp
        == original.history[0].timestamp
    )


def test_load_history_when_file_missing(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )

    calculator = Calculator(config)
    calculator.load_history()

    assert calculator.history == []


def test_undo_updates_saved_history(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=True,
    )

    calculator = Calculator(config)
    calculator.calculate("add", 10, 5)
    calculator.calculate("multiply", 4, 3)
    calculator.undo()

    restored = Calculator(config)
    restored.load_history()

    assert len(restored.history) == 1
    assert restored.history[0].operation == "add"


def test_redo_updates_saved_history(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=True,
    )

    calculator = Calculator(config)
    calculator.calculate("add", 10, 5)
    calculator.undo()
    calculator.redo()

    restored = Calculator(config)
    restored.load_history()

    assert len(restored.history) == 1
    assert restored.history[0].result == 15.0


def test_clear_updates_saved_history(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=True,
    )

    calculator = Calculator(config)
    calculator.calculate("add", 10, 5)
    calculator.clear()

    restored = Calculator(config)
    restored.load_history()

    assert restored.history == []


def test_save_history_when_autosave_disabled(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )

    calculator = Calculator(config)
    calculator.save_history()

    assert not config.history_file_path.exists()
