import runpy
import subprocess
import sys
import warnings
from unittest.mock import patch

from app.repl import main
from colorama import Fore

def run_repl(commands, capsys):
    """Run the REPL with simulated user commands."""
    with patch("builtins.input", side_effect=commands):
        main()

    return capsys.readouterr().out


def test_repl_calculation(capsys):
    output = run_repl(
        ["add 10 5", "multiply 4 3", "exit"],
        capsys,
    )

    assert "Result: 15.0" in output
    assert "Result: 12.0" in output
    assert "Goodbye!" in output


def test_repl_help(capsys):
    output = run_repl(["help", "exit"], capsys)

    assert "Operations:" in output
    assert "history" in output


def test_repl_history_undo_redo(capsys):
    output = run_repl(
        ["add 10 5", "undo", "redo", "history", "exit"],
        capsys,
    )

    assert "Last history change undone." in output
    assert "Last history change redone." in output
    assert "10.0 add 5.0 = 15.0" in output


def test_repl_invalid_operation(capsys):
    output = run_repl(
        ["unknown 10 5", "exit"],
        capsys,
    )

    assert "Error:" in output
    assert "Invalid operation" in output


def test_repl_division_by_zero(capsys):
    output = run_repl(
        ["divide 10 0", "exit"],
        capsys,
    )

    assert "Cannot divide by zero" in output
    assert "Goodbye!" in output


def test_repl_clear(capsys):
    output = run_repl(
        ["add 10 5", "clear", "history", "exit"],
        capsys,
    )

    assert "Calculation history cleared." in output
    assert "No calculation history." in output


def test_repl_invalid_command_format(capsys):
    output = run_repl(
        ["add 10", "exit"],
        capsys,
    )

    assert "Invalid command" in output


def test_repl_empty_input(capsys):
    output = run_repl(["", "   ", "exit"], capsys)

    assert "Goodbye!" in output

def test_repl_eof_exits_cleanly(capsys):
    with patch("builtins.input", side_effect=EOFError):
        main()

    assert "Goodbye!" in capsys.readouterr().out

def test_repl_module_entry_point():
    result = subprocess.run(
        [sys.executable, "-m", "app.repl"],
        input="exit\n",
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Advanced Python Calculator" in result.stdout
    assert "Goodbye!" in result.stdout


def test_repl_entry_point_coverage(capsys):
    """Test the REPL entry point within the coverage process."""
    with patch("builtins.input", side_effect=["exit"]):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=r".*app\.repl.*found in sys\.modules.*",
                category=RuntimeWarning,
            )

            runpy.run_module(
                "app.repl",
                run_name="__main__",
            )

    output = capsys.readouterr().out

    assert "Advanced Python Calculator" in output
    assert "Goodbye!" in output

def test_repl_save_and_load_history(capsys, tmp_path):
    from app.calculator import Calculator
    from app.calculator_config import CalculatorConfig

    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )

    calculator = Calculator(config)

    with patch("app.repl.Calculator", return_value=Calculator(config)):
        output = run_repl(["add 10 5", "save", "clear", "load", "history", "exit"], capsys)

    assert "History saved." in output
    assert "History loaded." in output
    assert "10.0 add 5.0 = 15.0" in output


def test_repl_success_output_is_green(capsys):
    output = run_repl(["add 10 5", "exit"], capsys)

    assert Fore.GREEN + "Result: 15.0" in output

def test_repl_recovers_from_malformed_startup_history(capsys, tmp_path):
    from app.calculator import Calculator
    from app.calculator_config import CalculatorConfig

    config = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        auto_save=False,
    )
    config.history_file_path.write_text(
        "invalid,header\nx,y\n",
        encoding="utf-8",
    )
    calculator = Calculator(config)

    with patch("app.repl.Calculator", return_value=calculator):
        output = run_repl(["add 10 5", "exit"], capsys)

    assert "Error loading history:" in output
    assert "Result: 15.0" in output
    assert "Goodbye!" in output

def test_repl_rejects_extra_save_and_load_arguments(capsys):
    output = run_repl(["save extra", "load extra", "exit"], capsys)

    assert "Invalid save command" in output
    assert "Invalid load command" in output
    
def test_repl_error_output_is_red(capsys):
    output = run_repl(["divide 10 0", "exit"], capsys)

    assert Fore.RED + "Error:" in output


def test_repl_help_output_is_cyan(capsys):
    output = run_repl(["help", "exit"], capsys)

    assert Fore.CYAN + "Operations:" in output


def test_repl_queued_calculations(capsys):
    output = run_repl(
        [
            "queue add 10 5",
            "queue multiply 4 3",
            "run",
            "exit",
        ],
        capsys,
    )

    assert "Queued: add 10 5" in output
    assert "Queued: multiply 4 3" in output
    assert output.index("Result: 15.0") < output.index("Result: 12.0")


def test_repl_run_empty_queue(capsys):
    output = run_repl(["run", "exit"], capsys)

    assert "No queued calculations." in output


def test_repl_invalid_queue_format(capsys):
    output = run_repl(["queue add 10", "exit"], capsys)

    assert "Invalid queue command" in output


def test_repl_queued_calculation_error(capsys):
    output = run_repl(
        ["queue divide 10 0", "run", "exit"],
        capsys,
    )

    assert "Cannot divide by zero" in output
    assert "Goodbye!" in output
