
import pytest
from datetime import datetime

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
