"""
Notion database integration module.

Handles creation of expense and income records in Notion databases.
"""

from expense_tracker.categories import categorie, fournir_id
from expense_tracker.config import get_chemin_valide


def new_expense_data(notion, database_id, text, date, totalAmount, Title, c, account_linking_id):
    """
    Create a new expense record in Notion database.

    Args:
        notion: Notion client instance
        database_id: Notion database ID for expenses
        text: Expense description text
        date: Transaction date in ISO format
        totalAmount: Amount of the expense
        Title: Title for the expense entry
        c: Category relation ID
        account_linking_id: Account page ID for linking

    Returns:
        Response from Notion API, or None if error
    """
    # Prepare new page data
    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Date": {
                "date": {
                    "start": date,  # ISO 8601 format
                    "end": None
                }
            },
            "Files & media": {
                "files": []  # Empty field
            },
            "Text": {
                "rich_text": [
                    {
                        "text": {
                            "content": text
                        }
                    }
                ]
            },
            "Total Amount": {
                "number": totalAmount  # Amount in dollars
            },
            "Expenses": {
                "title": [
                    {
                        "text": {
                            "content": Title
                        }
                    }
                ]
            },
            "Accounts": {
                "relation": [
                    {
                        "id": account_linking_id  # Account page ID for linking
                    }
                ]
            },
            "Categories": {
                "relation": [
                    {
                        "id": c  # Category page ID for linking
                    }
                ]
            }
        }
    }

    # Create new page
    try:
        response = notion.pages.create(**new_page_data)
        print("Nouvelle page créée :", response)
        return response
    except Exception as e:
        print("Erreur lors de la création de la page :", e)
        return None


def new_income_data(notion, income_database_id, typesDeDepense, dates, montant, account_linking_id):
    """
    Create a new income record in Notion database.

    Args:
        notion: Notion client instance
        income_database_id: Notion database ID for income
        typesDeDepense: Income description/type
        dates: Transaction date in ISO format
        montant: Amount of income
        account_linking_id: Account page ID for linking

    Returns:
        Response from Notion API, or None if error
    """
    new_page_data = {
        "parent": {"database_id": income_database_id},
        "properties": {
            "Date ( Deposite)": {
                "date": {
                    "start": dates,  # ISO 8601 format
                    "end": None
                }
            },
            "Notes": {
                "rich_text": [
                    {
                        "text": {
                            "content": typesDeDepense
                        }
                    }
                ]
            },
            "Amount": {
                "number": montant  # Amount in dollars
            },

            "Accounts": {
                "relation": [
                    {
                        "id": account_linking_id  # Account page ID for linking
                    }
                ]
            }
        }
    }

    # Create new page
    try:
        response = notion.pages.create(**new_page_data)
        print("Nouvelle page créée :", response)
        return response
    except Exception as e:
        print("Erreur lors de la création de la page :", e)
        return None


def action(expense_database_id, income_database_id, notion, typesDeDepense, dates, montant, account_linking_id):
    """
    Process all transactions and create Notion entries.

    Routes transactions to expense or income based on amount sign.
    Negative amounts are expenses, positive are income.

    Args:
        expense_database_id: Notion expense database ID
        income_database_id: Notion income database ID
        notion: Notion client instance
        typesDeDepense: List of transaction descriptions
        dates: List of transaction dates
        montant: List of transaction amounts
        account_linking_id: Account page ID for linking
    """
    if len(typesDeDepense) == len(dates) and len(typesDeDepense) == len(montant):
        for i in range(len(montant)):
            x = montant[i]
            if x == 0:
                continue
            elif x < 0:
                # Negative amount = expense
                base_path = get_chemin_valide()
                c = fournir_id(categorie(typesDeDepense[i], dates[i], montant[i], base_path), base_path)
                print(c)
                new_expense_data(
                    notion,
                    expense_database_id,
                    typesDeDepense[i],
                    dates[i],
                    montant[i] * -1,  # Convert to positive for display
                    typesDeDepense[i],
                    c,
                    account_linking_id
                )
            else:
                # Positive amount = income
                new_income_data(
                    notion,
                    income_database_id,
                    typesDeDepense[i],
                    dates[i],
                    montant[i],
                    account_linking_id
                )
    else:
        print("nombre de données sont inegales")
