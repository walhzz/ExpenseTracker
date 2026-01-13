"""
Main entry point for Expense Tracker CLI application.

Orchestrates the entire workflow:
1. Load configuration
2. Find transaction directory
3. Connect to Notion
4. Select input source (Image OCR or PDF Reader)
5. Process files based on selected source
6. Parse Desjardins transactions
7. Upload to Notion databases
"""

import sys
import os
import pytesseract
import pandas as pd
from notion_client import Client
import questionary
import time
import openpyxl

from src.utils import (
    init_config,
    get_tesseract_path,
    get_transaction_dirs,
    set_valid_path,
    find_valid_directory,
    find_jpeg_files,
    find_pdf_files,
    get_notion_token,
    get_expense_database_id,
    get_income_database_id,
    get_account_linking_id,
    get_pdf_dir,
    is_file_open,
    remove_file
)
from src.ocr import process_multiple_images, extract_table_transactions
from src.parsing import remove_line_breaks, parse_desjardins_statement, parsing_desjardins_credit_statements_pdf, convert_to_currency, convert_to_iso_dates
from src.notion_api import process
from src.categorization import categorize_expense


def main():
    """
    Main application workflow.
    """
    print("Pillow works!")
    print("=" * 50)
    print("Expense Tracker v2.0")
    print("=" * 50)

    # 1. Initialize configuration
    print("\n[1/7] Initializing configuration...")
    init_config()

    # 2. Find valid transaction directory
    print("[2/7] Finding transaction directory...")
    directories = get_transaction_dirs()
    try:
        valid_directory = find_valid_directory(directories)
        set_valid_path(valid_directory)
        print(f"[OK] Valid directory found: {valid_directory}")
    except ValueError as e:
        print(f"[ERROR] Final error: {e}")
        sys.exit(1)

    # 3. Initialize Notion client
    print("[3/7] Connecting to Notion...")
    notion = Client(auth=get_notion_token())
    expense_database_id = get_expense_database_id()
    income_database_id = get_income_database_id()
    account_linking_id = get_account_linking_id()
    print("[OK] Notion client initialized")

    # 4. Ask user for input source
    print("[4/7] Select input source...")
    input_source = questionary.select(
        "Which input source do you want to use?",
        choices=[
            "Image OCR (JPEG files)",
            "PDF Reader (PDF files)"
        ]
    ).ask()

    if input_source is None:
        print("[ERROR] No input source selected. Exiting.")
        sys.exit(0)

    # 5. Process based on selected input source
    if input_source == "Image OCR (JPEG files)":
        print("[5/7] Processing images with OCR...")
        pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()
        image_paths = find_jpeg_files(valid_directory)
        if not image_paths:
            print("[ERROR] No images found. Exiting.")
            sys.exit(0)

        print(f"[OK] Found {len(image_paths)} images")
        text = process_multiple_images(image_paths)
        print(f"[OK] Extracted text from all images")

        # Parse Desjardins transactions from OCR text
        print("[6/7] Parsing transactions...")
        text_lines = remove_line_breaks(text)
        data = parse_desjardins_statement(text_lines)

        # Transform data
        descriptions = data[0]
        dates = convert_to_iso_dates(data[1])
        amounts = convert_to_currency(data[2])

    else:  # PDF Reader
        print("[5/7] Processing PDF files...")
        pdf_directory = get_pdf_dir()
        print(f"[OK] Using PDF directory: {pdf_directory}")
        pdf_paths = find_pdf_files(pdf_directory)
        if not pdf_paths:
            print("[ERROR] No PDF files found in data/pdf. Exiting.")
            sys.exit(0)

        print(f"[OK] Found {len(pdf_paths)} PDF files")
        tables = extract_table_transactions(pdf_paths)
        print(f"[OK] Extracted tables from PDF files")

        # Parse Desjardins transactions from PDF tables
        print("[6/7] Parsing transactions...")
        df = parsing_desjardins_credit_statements_pdf(tables)
        print(df)

        # Interactive Excel editing loop
        edit_data = questionary.confirm(
            "Do you want to edit the transaction data in Excel?",
            default=False
        ).ask()

        while edit_data:
            file_path = "temp_pdf_transactions.xlsx"

            df.to_excel(file_path, index=False, engine='openpyxl')

            print(f"File saved to {file_path}. Please edit the file and save your changes.")
            os.startfile(file_path)

            questionary.press_any_key_to_continue(
                "Press any key after you finish editing and save the file..."
            ).ask()

            while is_file_open(file_path):
                print(" File is still open. Waiting...")

                questionary.press_any_key_to_continue(
                    "Please close the files and press any key..."
                ).ask()

            print(" File is closed")

            df = pd.read_excel(file_path, engine='openpyxl')

            print("Updated DataFrame:")
            print(df)

            edit_data = questionary.confirm(
                "Edit again?",
                default=False
            ).ask()

        # Transform data
        descriptions = df['description'].tolist()
        dates = df['date_transaction'].tolist()
        amounts = df['amount'].tolist()

        remove_file(file_path)

    print(f"[OK] Found {len(descriptions)} transactions")

    # 7. User confirmation to continue
    continue_upload = questionary.confirm(
        "Continue to upload transactions to Notion?",
        default=True
    ).ask()

    if not continue_upload:
        print('Shut Down!')
        sys.exit()

    # Upload to Notion
    print("\n[7/7] Uploading to Notion...")
    for description, date, amount in zip(descriptions, dates, amounts):
        transaction_category = categorize_expense(description,date,amount)



        process(
            notion,
            transaction_category,
            expense_database_id,
            date,
            amount,
            account_linking_id
        )

    print("\n" + "=" * 50)
    print("[OK] All transactions processed successfully!")
    print("=" * 50)

    # Cleanup temp Excel files
    temp_files = ["temp_file.xlsx", "temp_pdf_transactions.xlsx"]
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"[CLEANUP] Deleted {temp_file}")


if __name__ == '__main__':
    main()
