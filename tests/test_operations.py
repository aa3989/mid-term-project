
import pytest

from app.exceptions import OperationError
from app.operations import OperationFactory
from app.operations import Operation

@pytest.mark.parametrize(
    "operation",
    ["divide", "modulus", "int_divide", "percent"],
)
def test_zero_denominator_raises_operation_error(operation):
    calculator_operation = OperationFactory.create_operation(
        operation
    )

    with pytest.raises(OperationError):
        calculator_operation.execute(10, 0)


@pytest.mark.parametrize(
    "a,b",
    [
        (16, 0),
        (-16, 2),
        (-16, 2.5),
        (0, -2),
    ],
)
def test_invalid_roots_raise_operation_error(a, b):
    root = OperationFactory.create_operation("root")

    with pytest.raises(OperationError):
        root.execute(a, b)


def test_invalid_power_raises_operation_error():
    power = OperationFactory.create_operation("power")

    with pytest.raises(OperationError):
        power.execute(0, -1)


def test_complex_power_raises_operation_error():
    power = OperationFactory.create_operation("power")

    with pytest.raises(OperationError):
        power.execute(-4, 0.5)


def test_invalid_operation_raises_operation_error():
    with pytest.raises(OperationError):
        OperationFactory.create_operation("unknown")


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

    with pytest.raises(OperationError):
        instance.execute(a, b)


def test_invalid_operation():
    with pytest.raises(OperationError):
        OperationFactory.create_operation("unknown")

def test_abstract_operation_execute():
    class TestOperation(Operation):
        def execute(self, a, b):
            return super().execute(a, b)

    operation = TestOperation()

    assert operation.execute(10, 5) is None
