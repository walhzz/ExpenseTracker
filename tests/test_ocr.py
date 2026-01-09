"""
Unit tests for parsing module.
"""

import pytest
import glob
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ocr.extraction import extract_table_transactions
from src.parsing.desjardins import parsing_extraction_pdf
# from src.parsers.desjardins import parsing_pdf_credit

 

if __name__ == "__main__":
    pdf_files = glob.glob("*.pdf")

    for pdf in pdf_files :
        try : 
            for i in extract_table_transactions(pdf):
                parsing_extraction_pdf(i)
    
        except Exception as e:
            print(f"ERREUR: {e}\n")