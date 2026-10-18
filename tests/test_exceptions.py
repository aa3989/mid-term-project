
import pytest

from app.exceptions import (
    CalculatorError,
    OperationError,
    ValidationError,
    HistoryError,
    ConfigurationError,
)


@pytest.mark.parametrize(
    "exception_class",
    [
        OperationError,
        ValidationError,
        HistoryError,
        ConfigurationError,
    ]
)
def test_custom_exceptions(exception_class):
    with pytest.raises(CalculatorError):
        raise exception_class("Test error")


def test_exception_message():
    with pytest.raises(
        ValidationError,
        match="Invalid input"
    ):
        raise ValidationError("Invalid input")
