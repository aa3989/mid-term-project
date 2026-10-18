import pandas as pd
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.history import HistoryManager
from app.input_validators import InputValidator
from app.logger import Logger
from app.observers import LoggingObserver, AutoSaveObserver


class Calculator:
    """Calculator with history and observer support."""

    def __init__(self, config=None):
        self.config = config or CalculatorConfig()

        self.history_manager = HistoryManager(
            max_history_size=self.config.max_history_size
        )

        self.observers = []

        self.logger = Logger(
            self.config.log_file_path
        ).get_logger()

        self.register_observer(
            LoggingObserver(self.logger)
        )

        if self.config.auto_save:
            self.register_observer(
                AutoSaveObserver(
                    self.config.history_file_path,
                    self.config.default_encoding,
                )
            )

    @property
    def history(self):
        """Return calculation history."""
        return self.history_manager.history

    def register_observer(self, observer):
        """Register a new observer."""
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """Remove an observer."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, calculation):
        """Notify observers of a new calculation."""
        for observer in self.observers:
            observer.update(calculation, self.history)
    
    def save_history(self):
        """Persist the current history to CSV."""
        if self.config.auto_save:
            for observer in self.observers:
                if isinstance(observer, AutoSaveObserver):
                    observer.update(None, self.history)

    
    def calculate(self, operation, a, b):
        """Perform a calculation and notify observers."""
        try:
            a, b = InputValidator.validate_operands(
                a,
                b,
                self.config.max_input_value,
            )

            calculation = Calculation(operation, a, b)

            self.history_manager.add_calculation(
                calculation
            )

            self.notify_observers(calculation)

            return calculation.result

        except Exception as error:
            self.logger.error(
                "Calculation failed | Operation: %s | "
                "Operand1: %s | Operand2: %s | Error: %s",
                operation,
                a,
                b,
                error,
            )
            raise

    def undo(self):
        """Undo the last history change."""
        history = self.history_manager.undo()
        self.save_history()
        return history

    def redo(self):
        """Redo the last undone change."""
        history = self.history_manager.redo()
        self.save_history()
        return history

    def clear(self):
        """Clear calculation history."""
        self.history_manager.clear()
        self.save_history()

    
    def load_history(self):
        """Load saved calculation history from CSV."""
        file_path = self.config.history_file_path

        if not file_path.exists():
            return

        dataframe = pd.read_csv(
            file_path,
            encoding=self.config.default_encoding,
        )

        calculations = [
            Calculation.from_dict(row)
            for row in dataframe.to_dict(orient="records")
        ]

        self.history_manager.replace_history(calculations)
