import runpy
import subprocess
import sys
import warnings
from unittest.mock import patch

from app.repl import main

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
