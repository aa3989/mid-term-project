
import pytest
from datetime import datetime
from unittest.mock import patch
from app.calculation import Calculation
from app.exceptions import OperationError


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("power", 2, 3, 8),
        ("root", 27, 3, 3),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 200, 12.5),
        ("abs_diff", 5, 10, 5),
    ]
)
def test_calculation_result(operation, a, b, expected):
    calculation = Calculation(operation, a, b)
    assert calculation.result == pytest.approx(expected)


def test_calculation_timestamp():
    calculation = Calculation("add", 10, 5)
    assert isinstance(calculation.timestamp, datetime)


def test_calculation_string():
    calculation = Calculation("add", 10, 5)

    assert str(calculation) == "10 add 5 = 15"


def test_calculation_to_dict():
    calculation = Calculation("add", 10, 5)
    data = calculation.to_dict()

    assert data["operation"] == "add"
    assert data["operand1"] == 10
    assert data["operand2"] == 5
    assert data["result"] == 15
    assert isinstance(data["timestamp"], str)


@pytest.mark.parametrize(
    "operation,a,b",
    [
        ("divide", 10, 0),
        ("root", -16, 2),
        ("unknown", 10, 5),
    ]
)
def test_calculation_errors(operation, a, b):
    with pytest.raises(OperationError):
        Calculation(operation, a, b)


def test_calculation_wraps_builtin_error():
    with patch(
        "app.calculation.OperationFactory.create_operation"
    ) as mock_factory:
        mock_factory.side_effect = ValueError("Invalid arithmetic")

        with pytest.raises(
            OperationError, match="Invalid arithmetic"
        ):
            Calculation("add", 10, 5)


def test_calculation_from_dict():
    original = Calculation("add", 10, 5)

    restored = Calculation.from_dict(original.to_dict())

    assert restored.operation == original.operation
    assert restored.operand1 == original.operand1
    assert restored.operand2 == original.operand2
    assert restored.result == original.result
    assert restored.timestamp == original.timestamp


def test_calculation_from_dict_invalid_data():
    invalid_data = {
        "operation": "add",
        "operand1": "invalid",
        "operand2": 5,
        "timestamp": "2026-01-01T12:00:00",
    }

    with pytest.raises(ValueError):
        Calculation.from_dict(invalid_data)
