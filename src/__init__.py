"""
Expense Tracker - Automated expense processing from bank statements.

A modular package for:
- OCR processing of bank statement images
- Parsing Desjardins transaction data
- Categorizing expenses with pattern matching and learning
- Uploading to Notion databases

Package structure:
- ocr: Image processing and text extraction
- parsing: Text parsing and data transformation
- categorization: Expense categorization logic
- notion_api: Notion database operations
- utils: Configuration and file handling utilities
"""

__version__ = '2.0.0'
__author__ = 'Walid'

from src.main import main

__all__ = ['main']
