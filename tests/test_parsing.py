"""
Unit tests for parsing module.
"""

import pytest
from src.parsing import (
    find_date,
    remove_date,
    extract_amount,
    remove_amount,
    convert_to_currency,
)


def test_find_date():
    """Test date extraction from text."""
    text = "Purchase /MAXI Oct 15 -$50.00"
    result = find_date(text)
    assert result == "Oct 15"


def test_find_date_no_match():
    """Test date extraction when no date present."""
    text = "No date here"
    result = find_date(text)
    assert result is None


def test_remove_date():
    """Test date removal from text."""
    text = "Purchase /MAXI Oct 15 -$50.00"
    result = remove_date(text)
    assert "Oct 15" not in result
    assert "Purchase /MAXI" in result


def test_extract_amount():
    """Test amount extraction."""
    text = "Purchase /MAXI Oct 15 -$50.00"
    result = extract_amount(text)
    assert result == "-$50.00"


def test_extract_amount_positive():
    """Test positive amount extraction."""
    text = "Payroll +$500.00"
    result = extract_amount(text)
    assert result == "+$500.00"


def test_remove_amount():
    """Test amount removal from text."""
    text = "Purchase /MAXI -$50.00"
    result = remove_amount(text)
    assert "$50.00" not in result
    assert "Purchase /MAXI" in result


def test_convert_to_currency():
    """Test currency string conversion to float."""
    values = ["-$50.00", "+$100.50", "$25.99"]
    result = convert_to_currency(values)
    assert result == [-50.00, 100.50, 25.99]


def test_convert_to_currency_with_floats():
    """Test currency conversion with mixed types."""
    values = [50.0, "-$25.00", 100]
    result = convert_to_currency(values)
    assert result == [50.0, -25.00, 100.0]


if __name__ == '__main__':
    pytest.main([__file__])
