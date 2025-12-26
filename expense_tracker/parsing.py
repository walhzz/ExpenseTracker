"""
Text parsing module for Desjardins bank statements.

Handles text processing, date extraction, amount parsing, and transaction cleaning.
"""

import re
import os
import pandas as pd


def supprimer_retours_de_ligne(texte):
    """
    Remove line breaks from text and return array of non-empty lines.

    Args:
        texte: Raw text with line breaks

    Returns:
        List of non-empty lines with whitespace stripped
    """
    # Split text into lines and remove empty ones
    lignes = texte.splitlines()

    # Clean each line to remove extra whitespace
    lignes_sans_retours = [ligne.strip() for ligne in lignes if ligne.strip()]
    print('!' + str(lignes_sans_retours))
    return lignes_sans_retours


def reperer_dates(texte):
    """
    Find dates in 'Mon DD' format (e.g., Jan 15, Dec 1) in text.

    Args:
        texte: Text to search for dates

    Returns:
        Formatted date string 'Mon DD', or None if not found
    """
    # Regular expression for month and day
    pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9][0-9]?)\b'

    matches = re.search(pattern, texte)

    if matches:
        # If date found, format and return 'Mon DD'
        return f"{matches.group(1)} {matches.group(2)}"

    # If no date found, return None
    return None


def retirer_date(texte):
    """
    Remove date in 'Mon DD' format from a string.

    Args:
        texte: String containing a date

    Returns:
        String with date removed
    """
    # Regular expression for date
    pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9][0-9]?)\b'

    # Search for first match
    match = re.search(pattern, texte)

    if match:
        # Remove found date from string
        texte_sans_date = re.sub(pattern, "", texte).strip()
        return texte_sans_date

    # If no date found, return original string
    return texte


def extraire_depense(chaine):
    """
    Extract monetary amount from string using regex.

    Args:
        chaine: String containing amount

    Returns:
        Amount string (e.g., '+$10.50'), or None if not found
    """
    # Regular expression to extract amount
    match = re.search(r"\s*([+-]?\$\d+\.\d{2})", chaine)

    if match:
        depense = match.group(1)  # Get the amount
        return f"{depense}"
    else:
        return None


def retirer_depense(chaine):
    """
    Remove monetary amount from string.

    Args:
        chaine: String containing amount

    Returns:
        String with amount removed
    """
    pattern = r"\s*([+-]?\$\d+\.\d{2})"

    # Search for first match
    match = re.search(pattern, chaine)

    if match:
        # Remove found amount from string
        texte_sans_depense = re.sub(pattern, "", chaine).strip()
        return texte_sans_depense

    # If no amount found, return original string
    return chaine


def nettoyer_colonne(dataframe, colonne):
    """
    Remove empty ("") or None elements from a DataFrame column.

    Args:
        dataframe: Pandas DataFrame
        colonne: Column name to clean (string)

    Returns:
        New pandas Series without empty or None values
    """
    # Filter non-empty and non-None elements
    colonne_nettoyee = dataframe[colonne].dropna()  # Remove None values
    colonne_nettoyee = colonne_nettoyee[colonne_nettoyee != ""]  # Remove empty strings
    return colonne_nettoyee


def traitementTextDesjardins(texteTab):
    """
    Main text processing pipeline for Desjardins bank transactions.

    Processes transaction text to extract descriptions, dates, and amounts.
    Includes interactive Excel editing feature for user corrections.

    Args:
        texteTab: List of text lines from OCR

    Returns:
        List containing [descriptions, dates, amounts]
    """
    data = {'Transaction': texteTab}
    df = pd.DataFrame(data)

    data2 = df["Transaction"].apply(reperer_dates)
    tf = pd.DataFrame(data2)

    data3 = df["Transaction"].apply(extraire_depense)
    mt = pd.DataFrame(data3)

    df["Transaction"] = df["Transaction"].apply(retirer_date)
    df["Transaction"] = df["Transaction"].apply(retirer_depense)
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

    rep = input('edit ?')

    # Interactive Excel editing loop
    while rep.upper() == 'YES':
        file_path = "temp_file.xlsx"

        # Write to Excel file
        df_merged.to_excel(file_path, index=False, engine='openpyxl')

        print(f"File saved to {file_path}. Please edit the file and save your changes.")
        os.startfile(file_path)  # Open file in Excel (Windows-specific)

        input("Press Enter after you finish editing and save the file...")

        # Reload modified file
        df_merged = pd.read_excel(file_path, engine='openpyxl')

        print("Updated DataFrame:")
        print(df_merged)

        # Delete temporary file
        os.remove(file_path)
        print("Temporary file deleted.")

        rep = input('Edit again? (YES/NO): ')

    A = df_merged["Transaction_df"].tolist()
    B = df_merged["Transaction_tf"].tolist()
    C = df_merged["Transaction"].tolist()

    return [A, B, C]
