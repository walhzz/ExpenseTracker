"""
OCR and image processing module.

Handles image loading and text extraction using Tesseract OCR.
"""

from PIL import Image
import pytesseract
import pdfplumber
import pandas as pd


def load_image(image_path):
    """
    Open and return a PIL Image object from a file path.

    Args:
        image_path: Path to the image file

    Returns:
        PIL Image object
    """
    return Image.open(image_path)


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
    tables_set = []

    for path in pdf_path:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                x = page.extract_tables()
                for j in x :
                    tables_set += j

    return tables_set
            
                    
