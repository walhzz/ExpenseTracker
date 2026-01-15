"""
PDF table extraction module.

Handles extraction of tables from PDF files using pdfplumber.
"""

from typing import Union
from pathlib import Path

import pdfplumber


def extract_table_transactions(pdf_paths: list[Union[str, Path]]) -> list[list[str]]:
    """Extract all table rows from multiple PDF files.

    Opens each PDF file, extracts all tables from every page, and combines
    them into a single list of table rows. Each table row is a list of
    cell values as strings.

    Args:
        pdf_paths: List of paths to PDF files to process

    Returns:
        List of table rows extracted from all PDFs. Each row is a list
        of cell values (strings). The rows are flattened from all tables
        across all pages of all PDFs.
    """
    tables_set: list[list[str]] = []

    for path in pdf_paths:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                for table in extracted_tables:
                    tables_set += table

    return tables_set
