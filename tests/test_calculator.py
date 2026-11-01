
import pandas as pd
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError, OperationError


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

def test_calculate_honors_precision(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        precision=2,
    )
    calculator = Calculator(config)

    result = calculator.calculate("divide", 1, 3)

    assert result == 0.33
    assert calculator.history[0].result == 0.33


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

def test_load_history_honors_precision(tmp_path):
    history_dir = tmp_path / "history"
    source_config = CalculatorConfig(
        log_dir=tmp_path / "source-logs",
        history_dir=history_dir,
        precision=5,
    )
    Calculator(source_config).calculate("divide", 1, 3)

    restored_config = CalculatorConfig(
        log_dir=tmp_path / "restored-logs",
        history_dir=history_dir,
        precision=2,
    )
    restored = Calculator(restored_config)

    restored.load_history()

    assert restored.history[0].result == 0.33

def test_load_history_when_file_missing(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )

    calculator = Calculator(config)
    calculator.load_history()

    assert calculator.history == []

def test_load_malformed_history_preserves_current_history(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )
    calculator = Calculator(config)
    calculator.calculate("add", 10, 5)
    config.history_file_path.write_text(
        "invalid,header\nx,y\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing columns"):
        calculator.load_history()

    assert len(calculator.history) == 1
    assert calculator.history[0].result == 15.0

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

def test_forced_save_does_not_enable_autosaving(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )
    calculator = Calculator(config)
    calculator.calculate("add", 1, 2)

    calculator.save_history(force=True)
    calculator.calculate("add", 3, 4)

    dataframe = pd.read_csv(config.history_file_path)
    assert len(dataframe) == 1
    assert len(calculator.history) == 2

def test_save_history_logs_and_reraises_error(calculator, monkeypatch):
    def fail_save(self, calculation, history):
        raise OSError("disk full")

    monkeypatch.setattr(
        "app.calculator.AutoSaveObserver.update",
        fail_save,
    )

    with pytest.raises(OSError, match="disk full"):
        calculator.save_history()

    log_content = calculator.config.log_file_path.read_text(
        encoding="utf-8"
    )
    assert "History save failed" in log_content

def test_missing_history_returns_false(calculator):
    assert calculator.load_history() is False


def test_successful_history_load_returns_true(calculator):
    calculator.calculate("add", 10, 5)

    assert calculator.load_history() is True


def test_infinite_result_is_rejected(calculator):
    with pytest.raises(
        OperationError,
        match="finite number"
    ):
        calculator.calculate("percent", 1000000, 1e-320)

    assert calculator.history == []
