# Advanced Command-Line Calculator Application with Python

An interactive command-line calculator developed in Python for the NJIT IS601 midterm project.

The application supports ten mathematical operations, calculation history with undo and redo, configurable settings, CSV history persistence, logging, automated testing, and continuous integration.

## Features

- Ten mathematical operations
- Interactive command-line interface (REPL)
- Calculation history with undo, redo, and clear
- Automatic CSV history saving and loading
- Factory, Memento, and Observer design patterns
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
python -m app.repl
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

Example session:

```text
calculator> add 10 5
Result: 15.0

calculator> history
1. 10.0 add 5.0 = 15.0

calculator> undo
Last history change undone.

calculator> redo
Last history change redone.

calculator> clear
Calculation history cleared.

calculator> exit
Goodbye!
```

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
| `CALCULATOR_PRECISION` | `2` | Configured precision setting |
| `CALCULATOR_MAX_INPUT_VALUE` | `1000000` | Maximum permitted operand magnitude |
| `CALCULATOR_DEFAULT_ENCODING` | `utf-8` | File encoding |

Configuration values are validated when the calculator starts. Required directories are created automatically.

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

Saved calculations are reconstructed using `Calculation.from_dict()`, which recalculates results through the operation factory.

## Error Handling and Logging

The calculator validates numeric operands and handles invalid operations and calculation errors.

Examples include:

- Invalid operation names
- Division by zero
- Invalid numeric inputs
- Invalid configuration values
- Operands exceeding the configured maximum

Errors are displayed in the REPL without immediately terminating the interactive session.

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

- **147 passing tests**
- **100% statement coverage**
- **90% minimum coverage requirement**

Tests cover calculations, mathematical operations, configuration, history management, observers, logging, input validation, persistence, and the REPL.

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
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   ├── observers.py
│   ├── operations.py
│   └── repl.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

Runtime directories such as `logs/` and `history/` are created automatically.

## Repository

[Advanced Python Calculator — GitHub](https://github.com/aa3989/mid-term-project)

Developed for the NJIT IS601 midterm project.