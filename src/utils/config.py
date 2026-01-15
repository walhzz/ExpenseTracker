"""
Configuration management module.

Handles loading environment variables and managing global application state.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Module-level private variables for global state
_config: dict[str, Optional[str]] = {}


def init_config() -> None:
    """Initialize configuration by loading environment variables from .env file.

    Loads all required configuration values from environment variables into
    a module-level dictionary. Should be called once at application startup
    before accessing any configuration values.

    Returns:
        None
    """
    global _config
    load_dotenv()

    # Load all configuration into the module-level dict
    _config = {
        'transaction_dirs': os.getenv('TRANSACTION_DIRS', r'C:\Users\PC\iCloudDrive\Transaction,C:\Users\Walid\iCloudDrive\Transaction'),
        'notion_token': os.getenv('NOTION_API_TOKEN'),
        'expense_database_id': os.getenv('EXPENSE_DATABASE_ID'),
        'account_linking_id': os.getenv('ACCOUNT_LINKING_ID'),
    }


def set_valid_path(path: str) -> None:
    """Set the global valid directory path.

    This function is a no-op placeholder for backward compatibility.
    The valid path is no longer stored globally.

    Args:
        path: Valid directory path to store (ignored)

    Returns:
        None
    """
    pass


def get_transaction_dirs() -> list[str]:
    """Get the list of transaction directories.

    Retrieves the transaction directories from configuration and splits
    them into a list of individual directory paths.

    Returns:
        List of directory path strings where transactions may be found
    """
    dirs_str = _config.get('transaction_dirs', '')
    return [d.strip() for d in dirs_str.split(',')]


def get_notion_token() -> Optional[str]:
    """Get the Notion API token.

    Retrieves the Notion API authentication token from configuration.

    Returns:
        The Notion API token string, or None if not configured
    """
    return _config.get('notion_token')


def get_expense_database_id() -> Optional[str]:
    """Get the Notion expense database ID.

    Retrieves the Notion database ID for storing expense records.

    Returns:
        The expense database ID string, or None if not configured
    """
    return _config.get('expense_database_id')


def get_account_linking_id() -> Optional[str]:
    """Get the Notion account linking ID.

    Retrieves the Notion page ID used for linking expenses to accounts.

    Returns:
        The account linking ID string, or None if not configured
    """
    return _config.get('account_linking_id')


def get_data_dir() -> Path:
    """Get the data directory path.

    Calculates the path to the data directory relative to the project root.

    Returns:
        Path object pointing to the data directory
    """
    # Get project root (ExpenseTracker/)
    project_root = Path(__file__).parent.parent.parent
    return project_root / 'data'


def get_categories_dir() -> Path:
    """Get the categories data directory path.

    Returns the path to the directory containing category JSON files.

    Returns:
        Path object pointing to the categories directory
    """
    return get_data_dir() / 'categories'


def get_pdf_dir() -> Path:
    """Get the PDF files directory path.

    Returns the path to the directory containing PDF statement files.

    Returns:
        Path object pointing to the PDF directory
    """
    return get_data_dir() / 'pdf'
