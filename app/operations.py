from abc import ABC, abstractmethod
from app.exceptions import OperationError

class Operation(ABC):
    """Abstract base class for calculator operations."""

    @abstractmethod
    def execute(self, a, b):
        """Perform an operation using two numbers."""
        pass


class Addition(Operation):
    def execute(self, a, b):
        return a + b


class Subtraction(Operation):
    def execute(self, a, b):
        return a - b


class Multiplication(Operation):
    def execute(self, a, b):
        return a * b



class Division(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    def execute(self, a, b):
        try:
            result = a ** b
        except (OverflowError, ZeroDivisionError, ValueError) as error:
            raise OperationError(
                f"Invalid power operation: {error}"
            ) from error

        if isinstance(result, complex):
            raise OperationError(
                "Power operation produced a complex result."
            )

        return result


class Root(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError(
                "Root degree cannot be zero."
            )

        if a == 0 and b < 0:
            raise OperationError(
                "Cannot take a negative-degree root of zero."
            )

        if a < 0:
            if not float(b).is_integer() or int(b) % 2 == 0:
                raise OperationError(
                    "Negative numbers require an odd integer root."
                )

            return -((-a) ** (1 / b))

        return a ** (1 / b)


class Modulus(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError(
                "Cannot calculate modulus by zero."
            )
        return a % b


class IntegerDivision(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return a // b


class Percentage(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Percentage denominator cannot be zero.")
        return (a / b) * 100


class AbsoluteDifference(Operation):
    def execute(self, a, b):
        return abs(a - b)


class OperationFactory:
    """Factory for creating calculator operations."""

    _operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntegerDivision,
        "percent": Percentage,
        "abs_diff": AbsoluteDifference,
    }

    @classmethod
    def create_operation(cls, operation_name):
        operation_class = cls._operations.get(operation_name)

        if operation_class is None:
            raise OperationError(
                f"Invalid operation: {operation_name}"
            )

        return operation_class()
