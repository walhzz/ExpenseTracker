"""
Desjardins bank statement parsing module.

Handles text processing, date extraction, amount parsing, and transaction cleaning
specific to Desjardins bank statements.
"""

import re
import os
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