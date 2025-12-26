"""
Configuration management module for Expense Tracker.

Handles loading environment variables and managing global application state
without using classes (function-based approach).
"""

import os
from dotenv import load_dotenv

# Module-level private variables for global state
_config = {}
_chemin_valide = None


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


def set_chemin_valide(path):
    """
    Set the global valid directory path.

    Args:
        path: Valid directory path to store
    """
    global _chemin_valide
    _chemin_valide = path


def get_chemin_valide():
    """
    Get the global valid directory path.

    Returns:
        The stored valid directory path
    """
    return _chemin_valide


def get_tesseract_path():
    """
    Get the Tesseract OCR executable path.

    Returns:
        Path to Tesseract executable
    """
    return _config.get('tesseract_path')


def get_transaction_dirs():
    """
    Get the list of transaction directories.

    Returns:
        List of directory paths to search for transactions
    """
    dirs_str = _config.get('transaction_dirs', '')
    return [d.strip() for d in dirs_str.split(',')]


def get_notion_token():
    """
    Get the Notion API token.

    Returns:
        Notion API authentication token
    """
    return _config.get('notion_token')


def get_expense_database_id():
    """
    Get the Notion expense database ID.

    Returns:
        Notion expense database ID
    """
    return _config.get('expense_database_id')


def get_income_database_id():
    """
    Get the Notion income database ID.

    Returns:
        Notion income database ID
    """
    return _config.get('income_database_id')


def get_account_linking_id():
    """
    Get the Notion account linking ID.

    Returns:
        Notion account linking ID for database relations
    """
    return _config.get('account_linking_id')
