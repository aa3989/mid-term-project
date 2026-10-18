
import pytest

from app.operations import OperationFactory


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("power", 2, 3, 8),
        ("power", 2, -2, 0.25),
        ("root", 27, 3, 3),
        ("root", -27, 3, -3),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 200, 12.5),
        ("abs_diff", 5, 10, 5),
    ],
)
def test_operations(operation, a, b, expected):
    instance = OperationFactory.create_operation(operation)
    assert instance.execute(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "operation,a,b",
    [
        ("divide", 10, 0),
        ("modulus", 10, 0),
        ("int_divide", 10, 0),
        ("percent", 10, 0),
        ("root", 10, 0),
        ("root", -16, 2),
    ],
)
def test_invalid_inputs(operation, a, b):
    instance = OperationFactory.create_operation(operation)

    with pytest.raises(ValueError):
        instance.execute(a, b)


def test_invalid_operation():
    with pytest.raises(ValueError):
        OperationFactory.create_operation("unknown")
