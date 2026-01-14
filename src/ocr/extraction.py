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

<<<<<<< Updated upstream

def extract_text_from_image(img, lang='eng'):
    """
    Extract text from an image using Tesseract OCR.

    Args:
        img: PIL Image object
        lang: Language for OCR (default: 'eng')

    Returns:
        Extracted text as string
    """
    return pytesseract.image_to_string(img, lang=lang)


def process_multiple_images(image_paths):
    """
    Process multiple images and concatenate extracted text.

    Args:
        image_paths: List of image file paths

    Returns:
        Concatenated text from all images
    """
    text = ''
    for image_path in image_paths:
        img = load_image(image_path)
        text += ' ' + extract_text_from_image(img)
    return text


def extract_table_transactions(pdf_path):
    transactions_table = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            tables = page.extract_tables()
            transactions_table.append(tables)

    return transactions_table
            
                    
=======
    for path in pdf_paths:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                for table in extracted_tables:
                    tables_set += table

    return tables_set
>>>>>>> Stashed changes
