
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError


def test_successful_calculation_is_logged(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )

    calculator = Calculator(config)
    calculator.calculate("add", 10, 5)

    log_content = config.log_file_path.read_text(
        encoding="utf-8"
    )

    assert "INFO" in log_content
    assert "Operation: add" in log_content
    assert "Result: 15" in log_content


def test_failed_calculation_is_logged(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )

    calculator = Calculator(config)

    with pytest.raises(OperationError):
        calculator.calculate("divide", 10, 0)

    log_content = config.log_file_path.read_text(
        encoding="utf-8"
    )

    assert "ERROR" in log_content
    assert "Calculation failed" in log_content
    assert "Cannot divide by zero" in log_content


def test_invalid_input_is_logged(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )

    calculator = Calculator(config)

    with pytest.raises(ValidationError):
        calculator.calculate("add", "invalid", 5)

    log_content = config.log_file_path.read_text(
        encoding="utf-8"
    )

    assert "ERROR" in log_content
    assert "Calculation failed" in log_content
