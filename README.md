# Advanced Command-Line Calculator Application with Python

An interactive command-line calculator developed in Python for the NJIT IS601 midterm project.

The application supports ten mathematical operations, calculation history with undo and redo, configurable settings, CSV history persistence, logging, automated testing, and continuous integration.

## Features

- Ten mathematical operations
- Interactive command-line interface (REPL)
- Calculation history with undo, redo, and clear
- CSV history persistence with automatic saving and manual save/load commands
- Factory, Memento, and Observer design patterns
- Dynamic help menu generated from registered operations
- Color-coded Outputs using Colorama for REPL
- Command queuing using Command Design Pattern
- Environment-based configuration using `python-dotenv`
- Input validation and error handling
- Calculation and error logging
- Unit tests using pytest
- Test coverage enforcement using pytest-cov
- GitHub Actions continuous integration

## Requirements

- Python 3.14
- pip
- Git

Python dependencies are listed in `requirements.txt`:

- pandas
- python-dotenv
- pytest
- pytest-cov
- colorama

## Installation

Clone the repository:

```bash
git clone https://github.com/aa3989/mid-term-project.git
cd mid-term-project
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Linux/macOS:

```bash
source venv/bin/activate
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```


## Running the Calculator

Start the interactive calculator from the project root:

```bash
python3 -m main.py
```
Alternatively, run it as a Python module:

```bash
python3 -m app.repl
```

The application displays:

```text
Advanced Python Calculator
Type 'help' for available commands.
calculator>
```

Enter a mathematical operation followed by two numbers:

```text
calculator> add 10 5
Result: 15.0

calculator> multiply 4 3
Result: 12.0

calculator> divide 10 2
Result: 5.0
```

Type `exit` or `quit` to close the application.

## Supported Operations

| Operation | Command | Description |
|---|---|---|
| Addition | `add` | Adds two numbers |
| Subtraction | `subtract` | Subtracts the second number from the first |
| Multiplication | `multiply` | Multiplies two numbers |
| Division | `divide` | Divides the first number by the second |
| Exponentiation | `power` | Raises the first number to the power of the second |
| Root | `root` | Calculates a root |
| Modulus | `modulus` | Calculates the remainder |
| Integer Division | `int_divide` | Performs integer division |
| Percentage | `percent` | Calculates a percentage |
| Absolute Difference | `abs_diff` | Calculates the absolute difference |

Command format:

```text
<operation> <number1> <number2>
```

Examples:

```text
add 10 5
subtract 10 5
multiply 4 3
divide 10 2
power 2 3
root 27 3
modulus 10 3
int_divide 10 3
percent 25 200
abs_diff 5 10
```

## REPL Commands

| Command | Description |
|---|---|
| `help` | Display available operations and commands |
| `history` | Display calculation history |
| `undo` | Undo the most recent history change |
| `redo` | Redo an undone history change |
| `clear` | Clear calculation history |
| `exit` | Exit the calculator |
| `quit` | Exit the calculator |
| `queue <operation> <number1> <number2>` | Add a calculation to the command queue |
| `save` | Save history to CSV, including when autosave is disabled |
| `load` | Replace current history with history from the CSV file |
| `run` | Execute queued calculations |

Example session:

With `CALCULATOR_AUTO_SAVE=false` and no existing saved history, this example demonstrates manually saving a calculation, clearing in-memory history, and loading it back from CSV.

```text
calculator> add 10 5
Result: 15.0

calculator> save
History saved.

calculator> clear
Calculation history cleared.

calculator> load
History loaded.

calculator> history
1. 10.0 add 5.0 = 15.0

calculator> exit
Goodbye!
```
### Queued Calculations

The calculator supports queuing multiple operations for later execution.

```text
calculator> queue add 10 5
Queued: add 10 5

calculator> queue multiply 4 3
Queued: multiply 4 3

calculator> run
Result: 15.0
Result: 12.0
```

Queued calculations are executed in the order they were added. Successful calculations are recorded in history and saved to CSV when autosaving is enabled.

If a queued calculation fails, execution stops and the error is displayed. Remaining queued commands can be executed with another `run` command.

## Design Patterns

### Factory Pattern

The `OperationFactory` creates operation objects based on operation names. This separates operation selection from calculation execution.

### Memento Pattern

The `HistoryManager` uses `CalculatorMemento` to preserve previous calculation-history states, supporting undo and redo.

### Observer Pattern

The calculator notifies registered observers after a successful calculation.

- `LoggingObserver` records calculation activity.
- `AutoSaveObserver` saves calculation history to CSV.

The calculator also synchronizes CSV history after undo, redo, and clear operations when autosaving is enabled.

### Decorator Pattern

The `dynamic_operations` decorator in `app/help_menu.py` enhances the calculator's help menu.

It retrieves available operation names from `OperationFactory` whenever the help menu is displayed.

This ensures that newly registered operations automatically appear in the help menu without manually updating the REPL.

### Command Pattern

The Command Pattern is implemented in `app/commands.py`.

- `Command` defines the abstract command interface.
- `CalculationCommand` encapsulates a calculator operation and its operands.
- `CommandQueue` stores commands and executes them.

The REPL provides `queue` and `run` commands for queuing and executing calculations.

The Command Pattern delegates calculations to the existing `Calculator`, preserving input validation, history management, logging, and CSV persistence.

## Color-Coded Outputs

The interactive calculator uses `colorama` to improve readability.

| Color | Output |
|---|---|
| Green | Successful calculation results |
| Red | Errors and invalid commands |
| Cyan | Welcome messages, help, and confirmations |
| Yellow | Calculation history and empty-queue messages |

Colors are applied in `app/repl.py` without changing the calculator's underlying mathematical operations.

## Configuration

Configuration is managed by `CalculatorConfig` using environment variables loaded with `python-dotenv`.

Create a `.env` file in the project root if you want to customize the defaults:

```dotenv
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_FILE=calculator_history.csv
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

| Variable | Default | Purpose |
|---|---|---|
| `CALCULATOR_LOG_DIR` | `logs` | Directory for log files |
| `CALCULATOR_HISTORY_DIR` | `history` | Directory for saved history |
| `CALCULATOR_LOG_FILE` | `calculator.log` | Log filename |
| `CALCULATOR_HISTORY_FILE` | `calculator_history.csv` | History filename |
| `CALCULATOR_MAX_HISTORY_SIZE` | `100` | Maximum retained calculations |
| `CALCULATOR_AUTO_SAVE` | `true` | Enable or disable automatic CSV saving |
| `CALCULATOR_PRECISION` | `2` | Decimal places to round calculation results to |
| `CALCULATOR_MAX_INPUT_VALUE` | `1000000` | Maximum permitted operand magnitude |
| `CALCULATOR_DEFAULT_ENCODING` | `utf-8` | File encoding |

Configuration values are validated when the calculator starts. Required directories are created automatically.

### Calculation Precision

The `CALCULATOR_PRECISION` setting determines the number of decimal places used when rounding calculation results.

For example, with `CALCULATOR_PRECISION=2`:

```text
calculator> divide 10 3
Result: 3.33
```

The configured precision also applies when loading saved calculation history.

## History Persistence

Calculation history is stored in a CSV file, by default:

```text
history/calculator_history.csv
```

Each saved calculation includes:

- Operation name
- First operand
- Second operand
- Result
- Timestamp

When the REPL starts, it attempts to load previously saved history.

When autosaving is enabled, new calculations and history changes are written to the CSV file.

The `save` command writes the current history to the CSV even when autosaving is disabled. The `load` command replaces the current in-memory history with calculations from that file. Loaded results use the configured `CALCULATOR_PRECISION`.

Saved calculations are reconstructed using `Calculation.from_dict()`, which recalculates results through the operation factory.

If the history CSV file does not exist, the calculator continues normally with an empty history. Running the `load` command displays `No history file found.` instead of reporting a successful load.

Malformed or invalid history files are rejected without replacing the existing calculation history.

### Auto-Save Configuration and Clear Behavior

Automatic history saving is controlled by the `CALCULATOR_AUTO_SAVE` environment variable.

- **`CALCULATOR_AUTO_SAVE=true` (default):** Automatically saves calculation history changes to the configured CSV file. Running `clear` also updates the CSV with the empty history. Therefore, previously saved calculations cannot be restored using `load` after clearing.
- **`CALCULATOR_AUTO_SAVE=false`:** Disables automatic saving. Users can manually save history using `save` and restore it using `load`. Running `clear` removes calculations from memory without overwriting the previously saved CSV file.

To test manual saving and loading, set:

```env
CALCULATOR_AUTO_SAVE=false
```

Restart the application and execute:

```text
calculator> add 100 50
Result: 150.0

calculator> multiply 7 8
Result: 56.0

calculator> save
History saved.

calculator> clear
Calculation history cleared.

calculator> load
History loaded.

calculator> history
1. 100.0 add 50.0 = 150.0
2. 7.0 multiply 8.0 = 56.0
```

For normal operation, `CALCULATOR_AUTO_SAVE=true` is recommended to automatically persist calculation history changes.

## Error Handling and Logging

The calculator validates numeric operands and handles invalid operations and calculation errors.

Examples include:

- Invalid operation names
- Division by zero
- Invalid numeric inputs
- Invalid configuration values
- Operands exceeding the configured maximum
- Non-finite calculation results (`NaN` or infinity)
- Invalid numeric values in saved CSV history
- Missing history files during manual loading
- Malformed or unreadable CSV history files
- End-of-file (EOF) during interactive input

Errors are displayed in the REPL without immediately terminating the interactive session.

If saved history is malformed or unreadable at startup, the REPL reports the error and continues with empty history. A failed manual load reports an error without replacing the current history. If input reaches EOF, the REPL prints “Goodbye!” and exits cleanly.

Calculation activity and calculation errors are recorded through the logging system.

The default log file is:

```text
logs/calculator.log
```

## Testing

The project uses pytest for automated testing.

Run the full test suite:

```bash
python -m pytest
```

Run tests with coverage reporting:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Enforce a minimum of 90% coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

At the time of documentation, the project has:

- **182 passing tests**
- **100% statement coverage**
- **90% minimum coverage requirement**

Tests cover calculations, mathematical operations, configuration, history management, observers, logging, input validation, persistence, the REPL, dynamic help generation, color-coded outputs, and command queuing.

## Continuous Integration

GitHub Actions automatically runs the test suite when changes are pushed to `main` or when pull requests target `main`.

The workflow is defined in:

```text
.github/workflows/python-app.yml
```

The CI process:

1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies from `requirements.txt`.
4. Runs pytest with coverage reporting.
5. Fails if test coverage is below 90%.

[View GitHub Actions](https://github.com/aa3989/mid-term-project/actions)

## Project Structure

```text
mid-term-project/
├── .github/
│   └── workflows/
│       └── python-app.yml
├── app/
│   ├── __init__.py
│   ├── calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── commands.py
│   ├── exceptions.py
│   ├── help_menu.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   ├── observers.py
│   ├── operations.py
│   └── repl.py
├── tests/
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_commands.py
│   ├── test_exceptions.py
│   ├── test_help_menu.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   ├── test_logger.py
│   ├── test_observers.py
│   ├── test_operations.py
│   └── test_repl.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

Runtime directories such as `logs/` and `history/` are created automatically.

The `app/` directory contains the calculator implementation, including the Factory, Memento, Observer, Decorator, and Command design patterns.

The `tests/` directory contains automated pytest tests covering calculator operations, configuration, history management, persistence, logging, input validation, interactive commands, and optional features.

The `.github/workflows/` directory contains the GitHub Actions workflow that runs automated tests and enforces a minimum of 90% statement coverage.


## Repository

[Advanced Command-Line Calculator Application with Python — GitHub](https://github.com/aa3989/mid-term-project)

Developed for the NJIT IS601 midterm project.