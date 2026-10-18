
import logging

import pandas as pd
import pytest

from app.calculation import Calculation
from app.observers import LoggingObserver, AutoSaveObserver


def test_logging_observer(caplog):
    logger = logging.getLogger("test_observer")

    observer = LoggingObserver(logger)
    calculation = Calculation("add", 10, 5)

    with caplog.at_level(logging.INFO, logger="test_observer"):
        observer.update(calculation, [calculation])

    assert "Operation: add" in caplog.text
    assert "Result: 15" in caplog.text


def test_autosave_observer(tmp_path):
    file_path = tmp_path / "history.csv"

    observer = AutoSaveObserver(file_path)

    calculation = Calculation("multiply", 4, 5)

    observer.update(calculation, [calculation])

    assert file_path.exists()

    dataframe = pd.read_csv(file_path)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["operation"] == "multiply"
    assert dataframe.iloc[0]["result"] == 20


def test_autosave_multiple_calculations(tmp_path):
    file_path = tmp_path / "history.csv"

    observer = AutoSaveObserver(file_path)

    first = Calculation("add", 10, 5)
    second = Calculation("multiply", 2, 3)

    observer.update(second, [first, second])

    dataframe = pd.read_csv(file_path)

    assert len(dataframe) == 2
    assert list(dataframe["operation"]) == [
        "add",
        "multiply",
    ]


def test_autosave_creates_directory(tmp_path):
    file_path = tmp_path / "nested" / "history.csv"

    observer = AutoSaveObserver(file_path)

    calculation = Calculation("add", 1, 2)

    observer.update(calculation, [calculation])

    assert file_path.exists()
