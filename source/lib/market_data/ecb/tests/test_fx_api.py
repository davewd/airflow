"""Test module for ECB FX API functionality."""
import datetime

import pandas as pd
import pytest

from source.lib.market_data.ecb.fx_api import get_ecb_data_api


@pytest.fixture
def date_range() -> tuple[datetime.date, datetime.date]:
    """Fixture providing a test date range.

    Returns:
        tuple: (start_date, end_date) for testing
    """
    start_date = datetime.date(2025, 3, 1)
    end_date = datetime.date(2025, 3, 19)
    return start_date, end_date


def test_ecb_data_structure(date_range: tuple[datetime.date, datetime.date]) -> None:
    """Test the structure and content of ECB FX data.

    Args:
        date_range: Tuple of (start_date, end_date) for the query

    Tests:
        - Data is returned as a pandas DataFrame
        - Expected currencies are present
        - Data shape is correct for the date range
        - Values are numeric and valid
    """
    start_date, end_date = date_range
    data = get_ecb_data_api(start_date, end_date)

    # Test data type
    assert isinstance(data, pd.DataFrame), "Result should be a pandas DataFrame"

    # Test currencies
    expected_currencies = {"CHF", "USD", "GBP", "AUD"}
    actual_currencies = set(data.index.get_level_values('CURRENCY').unique())
    assert actual_currencies == expected_currencies, f"Expected currencies {expected_currencies}, got {actual_currencies}"

    # Test date range
    dates = pd.date_range(start_date, end_date, freq='B')  # Business days
    assert len(data) == len(dates) * len(expected_currencies), "Unexpected number of data points"

    # Test data validity
    assert data.notna().all().all(), "Data contains NaN values"
    assert (data > 0).all().all(), "Exchange rates should be positive"
