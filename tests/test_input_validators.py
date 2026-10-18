
import pytest

from app.exceptions import ValidationError
from app.input_validators import InputValidator


@pytest.mark.parametrize(
    "value",
    [True, False],
)
def test_reject_boolean_inputs(value):
    with pytest.raises(ValidationError):
        InputValidator.validate_number(value)


@pytest.mark.parametrize(
    "value",
    ["", "abc", None, float("nan"), float("inf")],
)
def test_reject_invalid_numerical_inputs(value):
    with pytest.raises(ValidationError):
        InputValidator.validate_number(value)


def test_reject_negative_value_outside_limit():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(-101, max_value=100)


def test_accept_value_at_maximum_limit():
    assert InputValidator.validate_number(
        100, max_value=100
    ) == 100.0


def test_validate_numeric_string_operands():
    first, second = InputValidator.validate_operands(
        "10.5", "2.5"
    )

    assert first == 10.5
    assert second == 2.5


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
