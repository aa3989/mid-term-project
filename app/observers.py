
from abc import ABC, abstractmethod

import pandas as pd


class CalculatorObserver(ABC):
    """Abstract base class for calculator observers."""

    @abstractmethod
    def update(self, calculation, history):
        """Respond to a new calculation."""
        pass


class LoggingObserver(CalculatorObserver):
    """Log calculation details using a configured logger."""

    def __init__(self, logger):
        self.logger = logger

    def update(self, calculation, history):
        self.logger.info(
            "Operation: %s | Operand1: %s | "
            "Operand2: %s | Result: %s",
            calculation.operation,
            calculation.operand1,
            calculation.operand2,
            calculation.result,
        )


class AutoSaveObserver(CalculatorObserver):
    """Automatically save history to CSV using pandas."""

    def __init__(self, file_path, encoding="utf-8"):
        self.file_path = file_path
        self.encoding = encoding

    def update(self, calculation, history):
        data = [
            item.to_dict()
            for item in history
        ]

        dataframe = pd.DataFrame(
            data,
            columns=[
                "operation",
                "operand1",
                "operand2",
                "result",
                "timestamp",
            ],
        )

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_csv(
            self.file_path,
            index=False,
            encoding=self.encoding,
        )
