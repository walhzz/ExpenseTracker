"""
Desjardins bank statement parsing module.

Handles PDF credit statement parsing specific to Desjardins bank statements.
"""

<<<<<<< Updated upstream
import re
import os
=======
from typing import Any, Union
from datetime import datetime

>>>>>>> Stashed changes
import pandas as pd

<<<<<<< Updated upstream
#valide_sqc = {['Date de transaction\nJ M', "Date d'inscription\nJ M", 'Description', 'Remises', 'Montant'],}


def parsing_extraction_pdf(data):
    """Parse: FOR_LOOP > Page > Table"""
    pages = []
    
    for page_item in data:  # FOR_LOOP sur les pages
        page = {"tables": []}
        
        for table_item in page_item:  # Parcourir les tables
            page["tables"].append(table_item)
        
        pages.append(page)
        print(pages)
    #return pages
=======

def clean_date(date_str: str) -> str:
    """Convert a date string in 'DD MM' format to ISO 8601 format.

    Parses a date string where the day and month are separated by space
    (e.g., '15 01' for January 15th) and converts it to ISO format
    (YYYY-MM-DD). If the resulting date would be in the future, the
    previous year is used instead.

    Args:
        date_str: Date string in 'DD MM' format (e.g., '15 01' for Jan 15)

    Returns:
        ISO 8601 formatted date string (YYYY-MM-DD), or the original
        string if parsing fails
    """
    date_str = date_str.strip()

    # Month number to name mapping
    months: dict[str, str] = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }

    # Parse day and month
    parts = date_str.split()
    if len(parts) != 2:
        return date_str

    day, month = parts
    try:
        month_name = months[month]
    except KeyError:
        return date_str

    # Create date object and check if it's in the past
    current_date = datetime.now()
    current_year = current_date.year

    date_obj = datetime.strptime(f"{day} {month_name} {current_year}", "%d %b %Y")

    # If date is in the future, use previous year
    if date_obj > current_date:
        date_obj = datetime.strptime(f"{day} {month_name} {current_year - 1}", "%d %b %Y")

    return date_obj.strftime("%Y-%m-%d")


def parsing_desjardins_credit_statements_pdf(table_set: list[list[str]]) -> pd.DataFrame:
    """Parse Desjardins credit card statement tables into a DataFrame.

    Processes extracted PDF table data from Desjardins credit card statements,
    identifying transaction tables and extracting dates, descriptions, and
    amounts into a structured DataFrame.

    Args:
        table_set: List of table rows extracted from PDF files. Each row
            is a list of cell values.

    Returns:
        DataFrame with columns:
            - date_transaction: ISO formatted transaction date
            - description: Transaction description text
            - amount: Transaction amount (negative for expenses, positive for credits)
            - isValid: 1 if amount was successfully parsed, 0 otherwise
    """
    expenses: list[dict[str, Any]] = []

    for i in range(len(table_set) - 1):
        if detect_transaction_table(table_set[i]):
            i += 2

            date_index = 1
            description_index = 2
            amount_index = 4
        else:
            continue

        expense_table = table_set[i]

        if len(expense_table) < 5:
            continue

        dates = expense_table[date_index].split('\n')
        descriptions = expense_table[description_index].split('\n')
        amounts = expense_table[amount_index].split('\n')

        for date, description, amount in zip(dates, descriptions, amounts):
            has_cr = 'CR' in amount

            amount_clean: Union[float, str] = (
                amount.strip()
                .replace(',', '.')
                .replace(' ', '')
                .replace('%', '')
                .replace('$', '')
            )

            # Check if it's a valid float
            is_valid = 1
            try:
                if has_cr:
                    amount_clean = abs(float(amount_clean.strip().replace('CR', '')))
                else:
                    amount_clean = -abs(float(amount_clean))
            except ValueError:
                is_valid = 0

            try:
                expenses.append({
                    'date_transaction': clean_date(date),
                    'description': description.strip(),
                    'amount': amount_clean,
                    'isValid': is_valid
                })
            except ValueError:
                print(f"Error cleaning the data: '{amount_clean}'")
                continue

    df = pd.DataFrame(expenses)
    return df


def detect_transaction_table(table: list[Any]) -> bool:
    """Detect if a table row marks the start of a transaction table.

    Checks if the given table row is a header indicating the beginning
    of a transaction table section in a Desjardins credit card statement.

    Args:
        table: A table row (list of cell values) to check

    Returns:
        True if this row indicates the start of a transaction table,
        False otherwise
    """
    if not table or len(table) == 0:
        return False

    first_elem = table[0]

    if not isinstance(first_elem, str):
        return False

    return "Transactions effectuées" in first_elem
>>>>>>> Stashed changes
