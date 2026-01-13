"""
Desjardins bank statement parsing module.

Handles text processing, date extraction, amount parsing, and transaction cleaning
specific to Desjardins bank statements.
"""

import re
import os
import sys

import pandas as pd
from datetime import datetime
import questionary




def remove_line_breaks(text):
    """
    Remove line breaks from text and return array of non-empty lines.

    Args:
        text: Raw text with line breaks

    Returns:
        List of non-empty lines with whitespace stripped
    """
    lines = text.splitlines()
    lines_without_breaks = [line.strip() for line in lines if line.strip()]
    print('!' + str(lines_without_breaks))
    return lines_without_breaks


def find_date(text):
    """
    Find dates in 'Mon DD' format (e.g., Jan 15, Dec 1) in text.

    Args:
        text: Text to search for dates

    Returns:
        Formatted date string 'Mon DD', or None if not found
    """
    pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9][0-9]?)\b'
    matches = re.search(pattern, text)

    if matches:
        return f"{matches.group(1)} {matches.group(2)}"
    return None


def remove_date(text):
    """
    Remove date in 'Mon DD' format from a string.

    Args:
        text: String containing a date

    Returns:
        String with date removed
    """
    pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9][0-9]?)\b'
    match = re.search(pattern, text)

    if match:
        return re.sub(pattern, "", text).strip()
    return text


def extract_amount(text):
    """
    Extract monetary amount from string using regex.

    Args:
        text: String containing amount

    Returns:
        Amount string (e.g., '+$10.50'), or None if not found
    """
    match = re.search(r"\s*([+-]?\$\d+\.\d{2})", text)
    if match:
        return match.group(1)
    return None


def remove_amount(text):
    """
    Remove monetary amount from string.

    Args:
        text: String containing amount

    Returns:
        String with amount removed
    """
    pattern = r"\s*([+-]?\$\d+\.\d{2})"
    match = re.search(pattern, text)

    if match:
        return re.sub(pattern, "", text).strip()
    return text


def clean_dataframe_column(dataframe, column):
    """
    Remove empty ("") or None elements from a DataFrame column.

    Args:
        dataframe: Pandas DataFrame
        column: Column name to clean (string)

    Returns:
        New pandas Series without empty or None values
    """
    cleaned_column = dataframe[column].dropna()
    cleaned_column = cleaned_column[cleaned_column != ""]
    return cleaned_column


def parse_desjardins_statement(text_lines):
    """
    Main text processing pipeline for Desjardins bank transactions.

    Processes transaction text to extract descriptions, dates, and amounts.
    Includes interactive Excel editing feature for user corrections.

    Args:
        text_lines: List of text lines from OCR

    Returns:
        List containing [descriptions, dates, amounts]
    """
    data = {'Transaction': text_lines}
    df = pd.DataFrame(data)

    data2 = df["Transaction"].apply(find_date)
    tf = pd.DataFrame(data2)

    data3 = df["Transaction"].apply(extract_amount)
    mt = pd.DataFrame(data3)

    df["Transaction"] = df["Transaction"].apply(remove_date)
    df["Transaction"] = df["Transaction"].apply(remove_amount)
    df["Transaction"] = df["Transaction"].astype(str).str.replace(">", "", regex=False)
    df["Transaction"] = df["Transaction"].str.lower()

    # Filter out specific Desjardins transaction types
    df = df[~df["Transaction"].str.startswith((
        "visa", "to", "with", "kk", "ak", "from 02", "r4", "n10", "y4",
        "GOUV.QUEBEC", "Pre-authorized purchase /"
    ))]
    df = df[~df["Transaction"].str.contains(
        r"8086|interac|0268907|gouv. quebec|pre-authorized purchase|direct deposit",
        case=False
    )]

    df = df[df['Transaction'].notna() & (df['Transaction'] != '')]
    df = df.reset_index(drop=True)

    tf = tf.dropna(subset=['Transaction'])
    tf = tf.reset_index(drop=True)

    mt = mt.dropna(subset=['Transaction'])
    mt = mt.reset_index(drop=True)

    df['ID'] = df.index
    tf['ID'] = tf.index
    mt['ID'] = mt.index

    df_merged = pd.merge(df, tf, on='ID', how='outer', suffixes=('_df', '_tf'))
    df_merged = pd.merge(df_merged, mt, on='ID', how='outer', suffixes=('_df', '_tf'))

    print(df_merged)

    # Interactive Excel editing loop
    edit_data = questionary.confirm(
        "Do you want to edit the transaction data in Excel?",
        default=False
    ).ask()

    while edit_data:
        file_path = "temp_file.xlsx"

        df_merged.to_excel(file_path, index=False, engine='openpyxl')

        print(f"File saved to {file_path}. Please edit the file and save your changes.")
        os.startfile(file_path)  # Windows-specific

        questionary.press_any_key_to_continue(
            "Press any key after you finish editing and save the file..."
        ).ask()

        df_merged = pd.read_excel(file_path, engine='openpyxl')

        print("Updated DataFrame:")
        print(df_merged)

        os.remove(file_path)
        print("Temporary file deleted.")

        edit_data = questionary.confirm(
            "Edit again?",
            default=False
        ).ask()

    A = df_merged["Transaction_df"].tolist()
    B = df_merged["Transaction_tf"].tolist()
    C = df_merged["Transaction"].tolist()

    return [A, B, C]


def convert_to_currency(values):
    """
    Convert currency strings to float values.

    Args:
        values: List of currency values (strings, floats, or ints)

    Returns:
        List of float values (None for unconvertible values)
    """
    result = []
    for value in values:
        if isinstance(value, (float, int)):
            result.append(float(value))
            continue

        original = value
        try:
            cleaned = value.replace("$", "").replace(",", "").strip()
            number = float(cleaned)
            result.append(number)
        except (ValueError, AttributeError):
            print(f"Unable to convert '{original}' to number.")
            result.append(None)
    return result


def convert_to_iso_dates(dates):
    """
    Convert date strings in 'Mon DD' format to ISO 8601 format (YYYY-MM-DD).
    Handles year rollover by comparing with current date.

    Args:
        dates: List of date strings in 'Mon DD' format (e.g., 'Jan 15')

    Returns:
        List of ISO formatted date strings (YYYY-MM-DD)
    """
    results = []
    now = datetime.now()

    for date in dates:
        target_date = datetime.strptime(f"{now.year} {date}", "%Y %b %d")

        # If date is in the future, use previous year
        if target_date > now:
            target_date = datetime.strptime(f"{now.year - 1} {date}", "%Y %b %d")

        results.append(target_date.strftime("%Y-%m-%d"))

    return results


def clean_date(date_str: str) -> str:
    """Converts '01 12' to ISO 8601 date string, ensuring the date is in the past"""
    date_str = date_str.strip()

    # Dictionnaire mois
    months = {
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
    expenses = []
    for i in range(len(table_set) - 1):
        #if table_set[i] == ['Date', 'Code', 'Description', 'Frais', 'Retrait', 'Dépôt', 'Solde']:

        #    i += 1

        #    date_index = 0
        #    description_index = 2
        #    amount_index = 4

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


            amount_clean = (amount.strip()
                            .replace(',', '.')
                            .replace(' ', '')
                            .replace('%', '')
                            .replace('$', '')
                            )

            # Vérifier si c'est un float valide
            is_valid = 1
            try:


                if has_cr:
                    amount_clean = abs(float((amount_clean.strip().replace('CR', ''))))

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


def detect_transaction_table(table: list) -> bool:
    """Détecte si c'est une table de transactions"""

    if not table or len(table) == 0:
        return False
    
    first_elem = table[0]
    
    if not isinstance(first_elem, str):
        return False

    return "Transactions effectuées" in first_elem

