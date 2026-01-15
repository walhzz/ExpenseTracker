"""
Utilities module for Expense Tracker.

Provides configuration management and file operations.
"""

from src.utils.config import (
    init_config,
    set_valid_path,
    get_transaction_dirs,
    get_notion_token,
    get_expense_database_id,
    get_account_linking_id,
    get_categories_dir,
    get_pdf_dir
)

from src.utils.file_handler import (
    find_pdf_files,
    find_valid_directory,
    save_json,
    load_json,
    get_category_file_path,
    get_database_json_path,
    get_id_json_path,
    is_file_open,
    remove_file
)

__all__ = [
    # Config functions
    'init_config',
    'set_valid_path',
    'get_transaction_dirs',
    'get_notion_token',
    'get_expense_database_id',
    'get_account_linking_id',
    'get_categories_dir',
    'get_pdf_dir',
    # File handler functions
    'find_pdf_files',
    'find_valid_directory',
    'save_json',
    'load_json',
    'get_category_file_path',
    'get_database_json_path',
    'get_id_json_path',
    'is_file_open',
    'remove_file'
]
