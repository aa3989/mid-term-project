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


def test_invalid_precision_environment(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "abc")

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_invalid_history_environment(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY_SIZE", "invalid"
    )

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_invalid_auto_save_environment(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE", "sometimes"
    )

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_invalid_max_input_environment(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_MAX_INPUT_VALUE", "hello"
    )

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_auto_save_false(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")

    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
    )

    assert config.auto_save is False


def test_invalid_encoding(tmp_path):
    with pytest.raises(ConfigurationError):
        CalculatorConfig(
            log_dir=tmp_path / "logs",
            history_dir=tmp_path / "history",
            default_encoding="invalid-encoding-name",
        )


def test_nonfinite_max_input(tmp_path):
    with pytest.raises(ConfigurationError):
        CalculatorConfig(
            log_dir=tmp_path / "logs",
            history_dir=tmp_path / "history",
            max_input_value=float("inf"),
        )

@pytest.mark.parametrize(
    "field,value,message",
    [
        ("max_history_size", "ten", "Maximum history size must be an integer"),
        ("precision", "two", "Precision must be an integer"),
        ("auto_save", "yes", "Auto-save must be true or false"),
        ("log_file", "", "Log and history filenames cannot be empty"),
        ("history_file", "", "Log and history filenames cannot be empty"),
    ],
)
def test_invalid_configuration_field_types(
    tmp_path, field, value, message
):
    config_values = {
        "log_dir": tmp_path / "logs",
        "history_dir": tmp_path / "history",
        field: value,
    }

    with pytest.raises(ConfigurationError, match=message):
        CalculatorConfig(**config_values)
