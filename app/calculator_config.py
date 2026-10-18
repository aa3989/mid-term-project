
import codecs
import math
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


load_dotenv()


def get_int_env(name, default):
    """Read an integer environment variable."""
    value = os.getenv(name, str(default))

    try:
        return int(value)
    except ValueError as error:
        raise ConfigurationError(
            f"{name} must be a valid integer."
        ) from error


def get_float_env(name, default):
    """Read a floating-point environment variable."""
    value = os.getenv(name, str(default))

    try:
        return float(value)
    except ValueError as error:
        raise ConfigurationError(
            f"{name} must be a valid number."
        ) from error


def get_bool_env(name, default):
    """Read and validate a boolean environment variable."""
    value = os.getenv(
        name,
        str(default).lower(),
    ).strip().lower()

    if value not in ("true", "false"):
        raise ConfigurationError(
            f"{name} must be true or false."
        )

    return value == "true"

@dataclass
class CalculatorConfig:
    """Manage calculator configuration settings."""

    log_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("CALCULATOR_LOG_DIR", "logs")
        )
    )

    history_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("CALCULATOR_HISTORY_DIR", "history")
        )
    )

    log_file: str = field(
        default_factory=lambda: os.getenv(
            "CALCULATOR_LOG_FILE", "calculator.log"
        )
    )

    history_file: str = field(
        default_factory=lambda: os.getenv(
            "CALCULATOR_HISTORY_FILE",
            "calculator_history.csv"
        )
    )


    max_history_size: int = field(
        default_factory=lambda: get_int_env(
            "CALCULATOR_MAX_HISTORY_SIZE", 100
        )
    )

    auto_save: bool = field(
        default_factory=lambda: get_bool_env(
            "CALCULATOR_AUTO_SAVE", True
        )
    )

    precision: int = field(
        default_factory=lambda: get_int_env(
            "CALCULATOR_PRECISION", 2
        )
    )

    max_input_value: float = field(
        default_factory=lambda: get_float_env(
            "CALCULATOR_MAX_INPUT_VALUE", 1000000
        )
    )


    default_encoding: str = field(
        default_factory=lambda: os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        )
    )



    def __post_init__(self):
        """Validate settings and create required directories."""
        try:
            self.log_dir = Path(self.log_dir)
            self.history_dir = Path(self.history_dir)

            # Validate maximum history size
            if not isinstance(self.max_history_size, int):
                raise ConfigurationError(
                    "Maximum history size must be an integer."
                )

            if self.max_history_size <= 0:
                raise ConfigurationError(
                    "Maximum history size must be positive."
                )

            # Validate precision
            if not isinstance(self.precision, int):
                raise ConfigurationError(
                    "Precision must be an integer."
                )

            if self.precision < 0:
                raise ConfigurationError(
                    "Precision cannot be negative."
                )

            # Validate maximum input value
            if not math.isfinite(self.max_input_value):
                raise ConfigurationError(
                    "Maximum input value must be finite."
                )

            if self.max_input_value <= 0:
                raise ConfigurationError(
                    "Maximum input value must be positive."
                )

            # Validate auto-save
            if not isinstance(self.auto_save, bool):
                raise ConfigurationError(
                    "Auto-save must be true or false."
                )

            # Validate filenames
            if not self.log_file or not self.history_file:
                raise ConfigurationError(
                    "Log and history filenames cannot be empty."
                )

            # Validate encoding
            codecs.lookup(self.default_encoding)

            # Create directories
            self.log_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.history_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

        except (OSError, LookupError, TypeError, ValueError) as error:
            raise ConfigurationError(
                f"Invalid calculator configuration: {error}"
            ) from error


    @property
    def log_file_path(self):
        return self.log_dir / self.log_file

    @property
    def history_file_path(self):
        return self.history_dir / self.history_file
