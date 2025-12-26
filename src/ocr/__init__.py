"""
OCR module for text extraction from images.
"""

from src.ocr.extraction import (
    load_image,
    extract_text_from_image,
    process_multiple_images,
)

__all__ = [
    'load_image',
    'extract_text_from_image',
    'process_multiple_images',
]
