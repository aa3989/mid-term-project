
class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class OperationError(CalculatorError):
    """Raised when a calculation operation fails."""
    pass


class ValidationError(CalculatorError):
    """Raised when user input is invalid."""
    pass


class HistoryError(CalculatorError):
    """Raised when calculation history cannot be managed."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when calculator configuration is invalid."""
    pass
