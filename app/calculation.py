
from dataclasses import dataclass, field
from datetime import datetime

from app.operations import OperationFactory
from app.exceptions import OperationError


@dataclass
class Calculation:
    """Represents a single calculator operation."""

    operation: str
    operand1: float
    operand2: float
    result: float = field(init=False)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Calculate the result after initialization."""
        try:
            operation_instance = OperationFactory.create_operation(
                self.operation
            )

            self.result = operation_instance.execute(
                self.operand1,
                self.operand2
            )

        except (ValueError, ZeroDivisionError, OverflowError) as error:
            raise OperationError(str(error)) from error

    def __str__(self):
        """Return a readable calculation description."""
        return (
            f"{self.operand1} {self.operation} "
            f"{self.operand2} = {self.result}"
        )

    def to_dict(self):
        """Convert the calculation into a dictionary."""
        return {
            "operation": self.operation,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "result": self.result,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a calculation from saved data."""
        calculation = cls(
            operation=data["operation"],
            operand1=float(data["operand1"]),
            operand2=float(data["operand2"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )

        return calculation
