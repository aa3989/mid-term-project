
import math

from app.exceptions import ValidationError


class InputValidator:
    """Validate numerical input for calculator operations."""

    @staticmethod
    def validate_number(value, max_value=1000000):
        """Convert input to float and validate its range."""

        if isinstance(value, bool):
            raise ValidationError(
                "Boolean values are not valid numerical inputs."
            )

        try:
            number = float(value)
        except (ValueError, TypeError) as error:
            raise ValidationError(
                f"Invalid numerical input: {value}"
            ) from error

        if not math.isfinite(number):
            raise ValidationError(
                "Input must be a finite number."
            )

        if abs(number) > max_value:
            raise ValidationError(
                f"Input exceeds maximum allowed value: {max_value}"
            )

        return number

    @staticmethod
    def validate_operands(a, b, max_value=1000000):
        """Validate both operands."""

        first = InputValidator.validate_number(
            a, max_value
        )

        second = InputValidator.validate_number(
            b, max_value
        )

        return first, second
