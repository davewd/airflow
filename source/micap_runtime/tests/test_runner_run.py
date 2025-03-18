"""Tests for the runner module functionality."""

from dataclasses import dataclass
from datetime import date
from micap_runtime.runner import main
from pytest import CaptureFixture
from typing import Protocol
import pytest


class RunnerArgs(Protocol):
    """Protocol defining the expected arguments for the runner."""
    job_module: str
    run_date: date
    log_level: str


@dataclass
class MockArgs:
    """Mock implementation of RunnerArgs for testing."""
    job_module: str = "data_aquisition.market_data.ecb.fx_api"
    run_date: date = date(2024, 1, 1)
    log_level: str = "ERROR"


@pytest.fixture
def mock_args() -> RunnerArgs:
    """Fixture providing mock command line arguments.

    Returns:
        RunnerArgs: Mock arguments object with job_module and run_date attributes.
    """
    return MockArgs()


def test_main_output(mock_args: RunnerArgs, capsys: CaptureFixture[str]) -> None:
    """Test that main function produces expected output."""
    main(mock_args)
    captured = capsys.readouterr()
    expected = f"DD 123 - test runner has worked.{mock_args.job_module} {mock_args.run_date}"
    assert captured.out.strip() == expected


def test_main_with_different_module(capsys: CaptureFixture[str]) -> None:
    """Test main function with a different job module."""
    args = MockArgs(job_module="different.module")
    main(args)
    captured = capsys.readouterr()
    expected = f"DD 123 - test runner has worked.{args.job_module} {args.run_date}"
    assert captured.out.strip() == expected


def test_main_with_different_date(capsys: CaptureFixture[str]) -> None:
    """Test main function with a different run date."""
    args = MockArgs(run_date=date(2024, 3, 17))
    main(args)
    captured = capsys.readouterr()
    expected = f"DD 123 - test runner has worked.{args.job_module} {args.run_date}"
    assert captured.out.strip() == expected


@pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "ERROR", "INVALID"])
def test_main_with_different_log_levels(capsys: CaptureFixture[str], log_level: str) -> None:
    """Test main function with different logging levels."""
    args = MockArgs(log_level=log_level)
    main(args)
    captured = capsys.readouterr()
    expected = f"DD 123 - test runner has worked.{args.job_module} {args.run_date}"
    assert captured.out.strip() == expected
