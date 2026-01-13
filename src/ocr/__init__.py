"""
OCR module for text extraction from images.
"""

from src.ocr.extraction import (
    load_image,
    extract_text_from_image,
    process_multiple_images,
    extract_table_transactions,
)

__all__ = [
    'load_image',
    'extract_text_from_image',
    'process_multiple_images',
    'extract_table_transactions',
]
