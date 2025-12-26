"""
OCR and image processing module.

Handles image loading and text extraction using Tesseract OCR.
"""

from PIL import Image
import pytesseract


def retourner_image(image_path):
    """
    Open and return a PIL Image object from a file path.

    Args:
        image_path: Path to the image file

    Returns:
        PIL Image object
    """
    return Image.open(image_path)


def lireTextImage(img):
    """
    Extract text from an image using Tesseract OCR.

    Args:
        img: PIL Image object

    Returns:
        Extracted text as string
    """
    texte = pytesseract.image_to_string(img, lang='eng')
    return texte


def traitementImage(cheminTab):
    """
    Process multiple images and concatenate extracted text.

    Args:
        cheminTab: List of image file paths

    Returns:
        Concatenated text from all images
    """
    text = ''
    for i in cheminTab:
        img = retourner_image(i)
        text += ' ' + lireTextImage(img)
    return text
