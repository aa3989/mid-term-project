
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_default_configuration(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_LOG_DIR", str(tmp_path / "logs")
    )
    monkeypatch.setenv(
        "CALCULATOR_HISTORY_DIR", str(tmp_path / "history")
    )
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "100")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")

    config = CalculatorConfig()

    assert config.precision == 2
    assert config.max_history_size == 100
    assert config.max_input_value == 1000000
    assert config.log_dir.exists()
    assert config.history_dir.exists()


def test_invalid_history_size(tmp_path):
    with pytest.raises(ConfigurationError):
        CalculatorConfig(
            log_dir=tmp_path / "logs",
            history_dir=tmp_path / "history",
            max_history_size=0,
        )


def test_invalid_precision(tmp_path):
    with pytest.raises(ConfigurationError):
        CalculatorConfig(
            log_dir=tmp_path / "logs",
            history_dir=tmp_path / "history",
            precision=-1,
        )


def test_invalid_max_input(tmp_path):
    with pytest.raises(ConfigurationError):
        CalculatorConfig(
            log_dir=tmp_path / "logs",
            history_dir=tmp_path / "history",
            max_input_value=-100,
        )


def test_configuration_file_paths(tmp_path):
    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
    )

    assert config.log_file_path == tmp_path / "logs" / "calculator.log"
    assert (
        config.history_file_path
        == tmp_path / "history" / "calculator_history.csv"
    )
