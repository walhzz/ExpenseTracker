"""
Utilities module for Expense Tracker.

Provides configuration management and file operations.
"""

from src.utils.config import (
    init_config,
    get_config,
    set_valid_path,
    get_valid_path,
    get_tesseract_path,
    get_transaction_dirs,
    get_notion_token,
    get_expense_database_id,
    get_income_database_id,
    get_account_linking_id,
    get_data_dir,
    get_categories_dir,
    get_screenshots_dir,
)

from src.utils.file_handler import (
    find_jpeg_files,
    verify_directory,
    find_valid_directory,
    save_json,
    load_json,
    get_category_file_path,
    get_database_json_path,
    get_id_json_path,
)

__all__ = [
    # Config functions
    'init_config',
    'get_config',
    'set_valid_path',
    'get_valid_path',
    'get_tesseract_path',
    'get_transaction_dirs',
    'get_notion_token',
    'get_expense_database_id',
    'get_income_database_id',
    'get_account_linking_id',
    'get_data_dir',
    'get_categories_dir',
    'get_screenshots_dir',
    # File handler functions
    'find_jpeg_files',
    'verify_directory',
    'find_valid_directory',
    'save_json',
    'load_json',
    'get_category_file_path',
    'get_database_json_path',
    'get_id_json_path',
]
