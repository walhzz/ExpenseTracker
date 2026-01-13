"""
Unit tests for parsing module.
"""

import pytest
import glob
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ocr.extraction import extract_table_transactions
from src.parsing.desjardins import parsing_desjardins_statements_pdf
# from src.parsers.desjardins import parsing_pdf_credit

 

if __name__ == "__main__":
    pdf_files_path = glob.glob("*.pdf")
    table1 = []
    table2 = []
    print('[3]')
    table2.append([3])
    table1 += [3]

    
    print(parsing_desjardins_statements_pdf(extract_table_transactions(pdf_files_path)))


        #try : 
        #    for i in extract_table_transactions(pdf):
        #        print('-----------------page')
        #        parsing_desjardins_statements_pdf(i)
    
        #except Exception as e:
         #   print(f"ERREUR: {e}\n")