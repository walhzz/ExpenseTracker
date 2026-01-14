"""
Unit tests for Notion API client module.
"""

import pytest
from unittest.mock import Mock
from src.notion_api.client import process


class TestProcess:
    """Tests for process function."""

    def test_process_skips_positive_amount(self):
        """Test that process skips positive amounts (income)."""
        mock_client = Mock()
        transaction_class = {"id": "123", "name": "Test", "expense": "Test expense"}

        # Should not raise any error
        process(mock_client, transaction_class, "db_id", "2024-01-01", 100.0, "account_id")

        # Verify no page was created (because amount is positive)
        mock_client.pages.create.assert_not_called()

    def test_process_handles_negative_amount(self):
        """Test that process creates expense for negative amounts."""
        mock_client = Mock()
        mock_client.pages.create.return_value = {"id": "new_page_id"}
        transaction_class = {"id": "cat_123", "name": "Food", "expense": "Grocery store"}

        process(mock_client, transaction_class, "expense_db_id", "2024-01-01", -50.0, "account_id")

        # Verify page was created
        mock_client.pages.create.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
