"""
Main entry point for Expense Tracker CLI application.

Orchestrates the entire workflow:
1. Load configuration
2. Find transaction directory
3. Connect to Notion
4. Select input source (PDF Reader)
5. Process files based on selected source
6. Parse Desjardins transactions
7. Upload to Notion databases
"""

import sys
import os
from typing import Any

import pandas as pd
from notion_client import Client
import questionary

from src.utils import (
    init_config,
    get_transaction_dirs,
    set_valid_path,
    find_valid_directory,
    find_pdf_files,
    get_notion_token,
    get_expense_database_id,
    get_account_linking_id,
    get_pdf_dir,
    is_file_open,
    remove_file
)
from src.ocr import extract_table_transactions
from src.parsing import parsing_desjardins_credit_statements_pdf
from src.notion_api import process
from src.categorization import categorize_expense


def main() -> None:
    """Run the main Expense Tracker application workflow.

    Executes the complete expense tracking pipeline:
    1. Initializes configuration from environment variables
    2. Locates valid transaction directory
    3. Connects to Notion API
    4. Prompts user to select PDF input source
    5. Extracts and parses transactions from PDF statements
    6. Allows optional Excel editing of transaction data
    7. Categorizes and uploads transactions to Notion

    Returns:
        None

    Raises:
        SystemExit: On configuration errors, missing files, or user cancellation
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
    directories: list[str] = get_transaction_dirs()
    try:
        valid_directory: str = find_valid_directory(directories)
        set_valid_path(valid_directory)
        print(f"[OK] Valid directory found: {valid_directory}")
    except ValueError as e:
        print(f"[ERROR] Final error: {e}")
        sys.exit(1)

    # 3. Initialize Notion client
    print("[3/7] Connecting to Notion...")
    notion: Client = Client(auth=get_notion_token())
    expense_database_id: Any = get_expense_database_id()
    account_linking_id: Any = get_account_linking_id()
    print("[OK] Notion client initialized")

    # 4. Ask user for input source
    print("[4/7] Select input source...")
    input_source: Any = questionary.select(
        "Which input source do you want to use?",
        choices=["PDF Reader (PDF files)"]
    ).ask()

    if input_source is None:
        print("[ERROR] No input source selected. Exiting.")
        sys.exit(0)

    # Initialize variables for transaction data
    descriptions: list[str] = []
    dates: list[str] = []
    amounts: list[float] = []
    file_path: str = "temp_pdf_transactions.xlsx"

    # 5. Process based on selected input source
    if input_source == "PDF Reader (PDF files)":
        print("[5/7] Processing PDF files...")
        pdf_directory = get_pdf_dir()
        print(f"[OK] Using PDF directory: {pdf_directory}")
        pdf_paths: list[str] = find_pdf_files(pdf_directory)
        if not pdf_paths:
            print("[ERROR] No PDF files found in data/pdf. Exiting.")
            sys.exit(0)

        print(f"[OK] Found {len(pdf_paths)} PDF files")
        tables: list[list[str]] = extract_table_transactions(pdf_paths)
        print("[OK] Extracted tables from PDF files")

        # Parse Desjardins transactions from PDF tables
        print("[6/7] Parsing transactions...")
        df: pd.DataFrame = parsing_desjardins_credit_statements_pdf(tables)
        print(df)

        # Interactive Excel editing loop
        edit_data: Any = questionary.confirm(
            "Do you want to edit the transaction data in Excel?",
            default=False
        ).ask()

        while edit_data:
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
    continue_upload: Any = questionary.confirm(
        "Continue to upload transactions to Notion?",
        default=True
    ).ask()

    if not continue_upload:
        print('Shut Down!')
        sys.exit()

    # Upload to Notion
    print("\n[7/7] Uploading to Notion...")
    for description, date, amount in zip(descriptions, dates, amounts):
        transaction_category = categorize_expense(description, date, amount)

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
    temp_files: list[str] = ["temp_file.xlsx", "temp_pdf_transactions.xlsx"]
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"[CLEANUP] Deleted {temp_file}")


if __name__ == '__main__':
    main()
