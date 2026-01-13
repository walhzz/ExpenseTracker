"""
Configuration management module.

Handles loading environment variables and managing global application state.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Module-level private variables for global state
_config = {}
_valid_path = None


def init_config():
    """
    Initialize configuration by loading environment variables from .env file.
    Should be called once at application startup.
    """
    global _config
    load_dotenv()

    # Load all configuration into the module-level dict
    _config = {
        'tesseract_path': os.getenv('TESSERACT_PATH', r'C:\Program Files\Tesseract-OCR\tesseract.exe'),
        'transaction_dirs': os.getenv('TRANSACTION_DIRS', r'C:\Users\PC\iCloudDrive\Transaction,C:\Users\Walid\iCloudDrive\Transaction'),
        'notion_token': os.getenv('NOTION_API_TOKEN'),
        'expense_database_id': os.getenv('EXPENSE_DATABASE_ID'),
        'income_database_id': os.getenv('INCOME_DATABASE_ID'),
        'account_linking_id': os.getenv('ACCOUNT_LINKING_ID'),
    }


def get_config(key, default=None):
    """
    Get a configuration value by key.

    Args:
        key: Configuration key
        default: Default value if key not found

    Returns:
        Configuration value or default
    """
    return _config.get(key, default)


def set_valid_path(path):
    """
    Set the global valid directory path.

    Args:
        path: Valid directory path to store
    """
    global _valid_path
    _valid_path = path


def get_valid_path():
    """
    Get the global valid directory path.

    Returns:
        The stored valid directory path
    """
    return _valid_path


def get_tesseract_path():
    """Get the Tesseract OCR executable path."""
    return _config.get('tesseract_path')


def get_transaction_dirs():
    """Get the list of transaction directories."""
    dirs_str = _config.get('transaction_dirs', '')
    return [d.strip() for d in dirs_str.split(',')]


def get_notion_token():
    """Get the Notion API token."""
    return _config.get('notion_token')


def get_expense_database_id():
    """Get the Notion expense database ID."""
    return _config.get('expense_database_id')


def get_income_database_id():
    """Get the Notion income database ID."""
    return _config.get('income_database_id')


def get_account_linking_id():
    """Get the Notion account linking ID."""
    return _config.get('account_linking_id')


def get_data_dir():
    """Get the data directory path."""
    # Get project root (ExpenseTracker/)
    project_root = Path(__file__).parent.parent.parent
    return project_root / 'data'


def get_categories_dir():
    """Get the categories data directory path."""
    return get_data_dir() / 'categories'


def get_screenshots_dir():
    """Get the screenshots directory path."""
    return get_data_dir() / 'screenshots'


def get_pdf_dir():
    """Get the PDF files directory path."""
    return get_data_dir() / 'pdf'
