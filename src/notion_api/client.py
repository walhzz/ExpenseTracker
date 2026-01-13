"""
Notion API client module.

Handles creation of expense and income records in Notion databases.
"""

from src.categorization import categorize_expense, get_notion_id_for_category

def page_creation_exception(notion_client, new_page_data):
    """
    Creates a new page in Notion using the provided client and page data.
    Handles any errors that may occur during the page creation process.

    Args:
        notion_client: Notion client instance
        new_page_data: Notion new data page template

    Returns:
        Response from Notion API, or None if error        
    """
    
    try:
        response = notion_client.pages.create(**new_page_data)
        print("New page created:", response)
        return response
    except Exception as e:
        print("Error creating page:", e)
        return None

def create_expense_record(notion_client, database_id, text, date, total_amount, title, category_id, account_id):
    """
    Create a new expense record in Notion database.

    Args:
        notion_client: Notion client instance
        database_id: Notion database ID for expenses
        text: Expense description text
        date: Transaction date in ISO format
        total_amount: Amount of the expense
        title: Title for the expense entry
        category_id: Category relation ID
        account_id: Account page ID for linking

    Returns:
        Response from Notion API, or None if error
    """
    new_page_data = {
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

    return page_creation_exception(notion_client,new_page_data)


def create_income_record(notion_client, database_id, description, date, amount, account_id):
    """
    Create a new income record in Notion database.

    Args:
        notion_client: Notion client instance
        database_id: Notion database ID for income
        description: Income description/type
        date: Transaction date in ISO format
        amount: Amount of income
        account_id: Account page ID for linking

    Returns:
        Response from Notion API, or None if error
    """
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


def process(notion_client: str,
            transaction_class: dict,
            expense_db_id: str,
            date: str,
            amount: float,
            account_id: str):
    # Skip if amount is not negative (income, not expense)
    if amount > 0:
        return

    description = transaction_class['expense']
    transaction_id = transaction_class["id"]

    try:
        # Process expense (negative amount)
        create_expense_record(
            notion_client,
            expense_db_id,
            description,
            date,
            abs(amount),
            description,
            transaction_id,
            account_id)
    except Exception as e:
        print(f"Error processing expense: {e}")


def process_transactions(notion_client, expense_db_id, descriptions, dates, amounts, account_id):
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
            if amount <= 0:
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
                continue

        except Exception as e:
            print(f"Error processing transaction '{description}' on {date}: {e}")
            continue