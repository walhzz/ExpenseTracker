"""
Expense Tracker - Automated expense processing from bank statements.

A modular package for:
- OCR processing of bank statement images
- Parsing Desjardins transaction data
- Categorizing expenses with pattern matching and learning
- Uploading to Notion databases

Usage:
    python -m expense_tracker
"""

__version__ = '2.0.0'
__author__ = 'Walid'

# Expose main entry point
from expense_tracker.main import main

__all__ = ['main']
