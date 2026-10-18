
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
