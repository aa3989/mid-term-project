
import pytest

from app.input_validators import InputValidator
from app.exceptions import ValidationError


@pytest.mark.parametrize(
    "value,expected",
    [
        ("10", 10.0),
        ("-5", -5.0),
        ("3.14", 3.14),
        (100, 100.0),
        (0, 0.0),
    ],
)
def test_valid_numbers(value, expected):
    assert InputValidator.validate_number(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "hello",
        None,
        "10abc",
        "",
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_invalid_numbers(value):
    with pytest.raises(ValidationError):
        InputValidator.validate_number(value)


def test_number_exceeds_maximum():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(200, max_value=100)


def test_negative_number_exceeds_maximum():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(-200, max_value=100)


def test_valid_operands():
    a, b = InputValidator.validate_operands("10", "5")

    assert a == 10.0
    assert b == 5.0


def test_invalid_second_operand():
    with pytest.raises(ValidationError):
        InputValidator.validate_operands(10, "invalid")
