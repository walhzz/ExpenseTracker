"""
Main entry point for Expense Tracker CLI application.

Orchestrates the entire workflow:
1. Load configuration
2. Process images via OCR
3. Parse Desjardins transactions
4. Categorize expenses
5. Upload to Notion databases
"""

import sys
import pytesseract
from notion_client import Client
import questionary

from src.utils import (
    init_config,
    get_tesseract_path,
    get_transaction_dirs,
    set_valid_path,
    find_valid_directory,
    find_jpeg_files,
    get_notion_token,
    get_expense_database_id,
    get_income_database_id,
    get_account_linking_id,
)
from src.ocr import process_multiple_images
from src.parsing import remove_line_breaks, parse_desjardins_statement, convert_to_currency, convert_to_iso_dates
from src.notion_api import process_transactions


def main():
    """
    Main application workflow.
    """
    print("Pillow works!")
    print("=" * 50)
    print("Expense Tracker v2.0")
    print("=" * 50)

    # 1. Initialize configuration
    print("\n[1/6] Initializing configuration...")
    init_config()

    # 2. Setup Tesseract OCR path
    print("[2/6] Setting up Tesseract OCR...")
    pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

    # 3. Find valid transaction directory
    print("[3/6] Finding transaction directory...")
    directories = get_transaction_dirs()
    try:
        valid_directory = find_valid_directory(directories)
        set_valid_path(valid_directory)
        print(f"[OK] Valid directory found: {valid_directory}")
    except ValueError as e:
        print(f"[ERROR] Final error: {e}")
        sys.exit(1)

    # 4. Initialize Notion client
    print("[4/6] Connecting to Notion...")
    notion = Client(auth=get_notion_token())
    expense_database_id = get_expense_database_id()
    income_database_id = get_income_database_id()
    account_linking_id = get_account_linking_id()
    print("[OK] Notion client initialized")

    # 5. Process images via OCR
    print("[5/6] Processing images with OCR...")
    image_paths = find_jpeg_files(valid_directory)
    if not image_paths:
        print("[ERROR] No images found. Exiting.")
        sys.exit(0)

    print(f"[OK] Found {len(image_paths)} images")
    text = process_multiple_images(image_paths)
    print(f"[OK] Extracted text from all images")

    # 6. Parse Desjardins transactions
    print("[6/6] Parsing transactions...")
    text_lines = remove_line_breaks(text)
    data = parse_desjardins_statement(text_lines)

    # 7. User confirmation to continue
    continue_upload = questionary.confirm(
        "Continue to upload transactions to Notion?",
        default=True
    ).ask()

    if not continue_upload:
        print('Shut Down!')
        sys.exit()

    print("\n[OK] Processing transactions...")

    # 8. Transform data
    descriptions = data[0]
    dates = convert_to_iso_dates(data[1])
    amounts = convert_to_currency(data[2])

    print(f"[OK] Found {len(descriptions)} transactions")

    # 9. Upload to Notion
    print("\n[UPLOAD] Uploading to Notion...")
    process_transactions(
        notion,
        expense_database_id,
        income_database_id,
        descriptions,
        dates,
        amounts,
        account_linking_id
    )

    print("\n" + "=" * 50)
    print("[OK] All transactions processed successfully!")
    print("=" * 50)


if __name__ == '__main__':
    main()
