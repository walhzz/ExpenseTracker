"""
Notion API client module.

Handles creation of expense records in Notion databases.
"""

from typing import Any, Optional, TypedDict
from notion_client import Client


class TransactionClass(TypedDict):
    """Type definition for transaction classification data."""
    id: str
    name: str
    expense: str


def _page_creation_exception(notion_client: Client, new_page_data: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Create a new page in Notion using the provided client and page data.

    Wraps the Notion API page creation call with error handling to ensure
    failures are logged but don't crash the application.

    Args:
        notion_client: Authenticated Notion client instance
        new_page_data: Dictionary containing the page structure conforming
            to Notion's page creation API schema

    Returns:
        The API response dictionary on success, or None if an error occurred
    """
    try:
        response = notion_client.pages.create(**new_page_data)
        print("New page created:", response)
        return response
    except Exception as e:
        print("Error creating page:", e)
        return None


def _create_expense_record(
    notion_client: Client,
    database_id: str,
    text: str,
    date: str,
    total_amount: float,
    title: str,
    category_id: str,
    account_id: str
) -> Optional[dict[str, Any]]:
    """Create a new expense record in a Notion database.

    Constructs the proper Notion page structure for an expense entry and
    creates it in the specified database.

    Args:
        notion_client: Authenticated Notion client instance
        database_id: ID of the Notion database to add the expense to
        text: Expense description text (stored in 'Text' rich_text field)
        date: Transaction date in ISO 8601 format (YYYY-MM-DD)
        total_amount: Amount of the expense as a positive number
        title: Title for the expense entry (stored in 'Expenses' title field)
        category_id: Notion page ID of the category to link this expense to
        account_id: Notion page ID of the account to link this expense to

    Returns:
        The API response dictionary on success, or None if an error occurred
    """
    new_page_data: dict[str, Any] = {
        "parent": {"database_id": database_id},
        "properties": {
            "Date": {
                "date": {
                    "start": date,
                    "end": None
                }
            },
            "Files & media": {
                "files": []
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
                "number": total_amount
            },
            "Expenses": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Accounts": {
                "relation": [
                    {
                        "id": account_id
                    }
                ]
            },
            "Categories": {
                "relation": [
                    {
                        "id": category_id
                    }
                ]
            }
        }
    }

    return _page_creation_exception(notion_client, new_page_data)


def process(
    notion_client: Client,
    transaction_class: TransactionClass,
    expense_db_id: str,
    date: str,
    amount: float,
    account_id: str
) -> None:
    """Process a single transaction and create a Notion expense entry.

    Takes a categorized transaction and creates a corresponding expense
    record in Notion. Only processes negative amounts (expenses); positive
    amounts (income) are skipped.

    Args:
        notion_client: Authenticated Notion client instance
        transaction_class: Dictionary containing categorization info with keys:
            - id: Category's Notion page ID
            - name: Category name
            - expense: Expense description text
        expense_db_id: ID of the Notion expense database
        date: Transaction date in ISO 8601 format (YYYY-MM-DD)
        amount: Transaction amount (negative for expenses)
        account_id: Notion page ID of the account to link this expense to

    Returns:
        None
    """
<<<<<<< Updated upstream
    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Date ( Deposite)": {
                "date": {
                    "start": date,
                    "end": None
                }
            },
            "Notes": {
                "rich_text": [
                    {
                        "text": {
                            "content": description
                        }
                    }
                ]
            },
            "Amount": {
                "number": amount
            },
            "Accounts": {
                "relation": [
                    {
                        "id": account_id
                    }
                ]
            }
        }
    }

    return page_creation_exception(notion_client,new_page_data)


def process_transactions(notion_client, expense_db_id, income_db_id, descriptions, dates, amounts, account_id):
    """
    Process all transactions and create Notion entries.

    Routes transactions to expense or income based on amount sign.
    Negative amounts are expenses, positive are income.

    Args:
        notion_client: Notion client instance
        expense_db_id: Notion expense database ID
        income_db_id: Notion income database ID
        descriptions: List of transaction descriptions
        dates: List of transaction dates
        amounts: List of transaction amounts
        account_id: Account page ID for linking
    
    Raises:
        ValueError: If input lists have unequal lengths
    """
    # Validate input lengths
    if not (len(descriptions) == len(dates) == len(amounts)):
        raise ValueError(
            f"Input lists have unequal lengths: "
            f"descriptions={len(descriptions)}, dates={len(dates)}, amounts={len(amounts)}"
        )

    # Process each transaction
    for description, date, amount in zip(descriptions, dates, amounts):
        
        # Skip zero amounts
        if amount == 0:
            continue
        
        try:
            if amount < 0:
                # Process expense (negative amount)
                category = categorize_expense(description, date, amount)
                category_id = get_notion_id_for_category(category)
                
                create_expense_record(
                    notion_client,
                    expense_db_id,
                    description,
                    date,
                    abs(amount),  # Convert to positive
                    description,
                    category_id,
                    account_id
                )
            else:
                # Process income (positive amount)
                create_income_record(
                    notion_client,
                    income_db_id,
                    description,
                    date,
                    amount,
                    account_id
                )
        except Exception as e:
            print(f"Error processing transaction '{description}' on {date}: {e}")
            continue
=======
    # Skip if amount is not negative (income, not expense)
    if amount > 0:
        return

    description = transaction_class['expense']
    transaction_id = transaction_class["id"]

    try:
        # Process expense (negative amount)
        _create_expense_record(
            notion_client,
            expense_db_id,
            description,
            date,
            abs(amount),
            description,
            transaction_id,
            account_id
        )
    except Exception as e:
        print(f"Error processing expense: {e}")
>>>>>>> Stashed changes
