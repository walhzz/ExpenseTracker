"""
Data transformation and validation module.

Handles conversion of currency strings to floats and date parsing.
"""

from datetime import datetime


def traitementArgent(tab):
    """
    Convert currency strings to float values.

    Args:
        tab: List of currency values (strings, floats, or ints)

    Returns:
        List of float values (None for unconvertible values)
    """
    resultat = []
    for i in tab:
        # If already a float or int, no conversion needed
        if isinstance(i, float) or isinstance(i, int):
            resultat.append(float(i))
            continue

        original = i  # For debugging
        try:
            # Clean text if it's a string
            i = i.replace("$", "").replace(",", "").strip()
            nombre = float(i)
            resultat.append(nombre)
        except (ValueError, AttributeError):
            print(f"Impossible de convertir '{original}' en nombre.")
            resultat.append(None)
    return resultat


def traitementDate(dates):
    """
    Convert date strings in 'Mon DD' format to ISO 8601 format (YYYY-MM-DD).
    Handles year rollover by comparing with current date.

    Args:
        dates: List of date strings in 'Mon DD' format (e.g., 'Jan 15')

    Returns:
        List of ISO formatted date strings (YYYY-MM-DD)
    """
    resultats = []
    maintenant = datetime.now()  # Current date

    for date in dates:
        # Try with current year
        date_cible = datetime.strptime(f"{maintenant.year} {date}", "%Y %b %d")

        # If date is in the future, use previous year
        if date_cible > maintenant:
            date_cible = datetime.strptime(f"{maintenant.year - 1} {date}", "%Y %b %d")

        # Add to result after converting to ISO format
        resultats.append(date_cible.strftime("%Y-%m-%d"))

    return resultats
