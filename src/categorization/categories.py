"""
Category management and expense categorization module.

Handles expense categorization with pattern matching and interactive learning.
"""

import sys
import questionary
from src.utils import (
    load_json,
    save_json,
    get_category_file_path,
    get_database_json_path,
    get_id_json_path,
    get_categories_dir,
)


def get_expense_class_by_description(expense_description: str) -> dict:
    """
    Find a category and expense by description/name
    Returns a dict with category id and expense name
    """
    categories_dir = get_categories_dir()
    database_path = get_database_json_path(categories_dir)
    categories = load_json(database_path)


    for category in categories:
        if expense_description in category["expenses"]:
            return {
                "id": category["id"],
                "name": category["name"],
                "expense": expense_description
            }

    return None  # Not found


def add_expense_description_to_category(expense_description: str, category_name: str):
    categories_dir = get_categories_dir()
    database_path = get_database_json_path(categories_dir)
    categories = load_json(database_path)

    for category in categories:
        if category_name == category["name"]:
            # Check if expense already exists
            if expense_description not in category["expenses"]:
                category["expenses"].append(expense_description)
            else:
                print(f"'{expense_description}' already exists in {category_name}")
            break

    # Save the updated data
    save_json(database_path, categories)


def categorize_expense(expense_description: str, date: str, amount: float) -> dict:
    """
    Categorize an expense interactively with pattern matching and learning.
    Searches for the expense in existing category patterns. If not found,
    prompts user for category selection from a list.

    Args:
        expense_description: Expense description
        date: Transaction date
        amount: Amount

    Returns:
        Dict with category id, name, and expense
    """

    # First, try to find the expense in existing patterns
    result = get_expense_class_by_description(expense_description)

    if result:
        # Found a matching expense
        print(f"✓ Matched: '{expense_description}' → {result['name']}")
        return result

    # Not found, prompt user to select a category
    print(f"\n$ Categorizing: {expense_description} (${amount} on {date})")

    categories_dir = get_categories_dir()
    database_path = get_database_json_path(categories_dir)
    categories = load_json(database_path)

    # Create list of category names for selection, with exit option
    category_choices = [category['name'] for category in categories]
    category_choices.append("Exit")

    # Use questionary to select category
    selected_name = questionary.select(
        "Select category:",
        choices=category_choices
    ).ask()

    # Check if user selected exit
    if selected_name == "Exit":
        print("Exiting program...")
        exit()

    # Find the full category dict
    selected_category = next(cat for cat in categories if cat['name'] == selected_name)

    # Ask if user wants to save this pattern for future use
    save_pattern = questionary.confirm(
        f"Save '{expense_description}' to '{selected_category['name']}' for future use?"
    ).ask()

    if save_pattern:
        add_expense_description_to_category(expense_description, selected_category["name"])
        print(f"✓ Pattern saved: '{expense_description}' → {selected_category['name']}")

    # Return the full category dict
    return {
        "id": selected_category["id"],
        "name": selected_category["name"],
        "expense": expense_description
    }

def categorize1_expense(expense_description: str, date: str, amount: float) -> str:
    """
    Categorize an expense interactively with pattern matching and learning.

    Searches for the expense in existing category patterns. If not found,
    prompts user for category and optionally saves the pattern.

    Args:
        expense_description: Expense description
        date: Transaction date
        amount: Amount

    Returns:
        Category name assigned to the expense
    """

    # First, try to find the expense in existing patterns
    result = get_expense_class_by_description(expense_description)

    if result:
        # Found a matching expense
        print(f"✓ Matched: '{expense_description}' → {result['name']}")
        return result["name"]

    # Not found, prompt user to select a category
    print(f"\n$ Categorizing: {expense_description} (${amount} on {date})")

    categories_dir = get_categories_dir()
    database_path = get_database_json_path(categories_dir)
    categories = load_json(database_path)

    # Display available categories
    print("\nAvailable categories:")
    for i, category in enumerate(categories, 1):
        print(f"  {i}. {category['name']}")

    # Get user input
    while True:
        try:
            choice = int(input("\nSelect category (number): "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]["name"]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    # Ask if user wants to save this pattern for future use
    save_pattern = input(f"\nSave '{expense_description}' to '{selected_category}' for future use? (y/n): ").lower()

    if save_pattern == 'y':
        add_expense_description_to_category(expense_description, selected_category)
        print(f"✓ Pattern saved: '{expense_description}' → {selected_category}")

    return selected_category


def get_notion_id_for_category(category_name):
    """
    Get Notion ID for a category name.

    Maps category name to its corresponding Notion page ID by looking up
    the index in Database.json and returning the matching ID from id.json.

    Args:
        category_name: Category name

    Returns:
        Notion page ID for the category
    """
    categories_dir = get_categories_dir()
    database_path = get_database_json_path(categories_dir)
    id_path = get_id_json_path(categories_dir)

    categories = load_json(database_path)
    ids = load_json(id_path)

    if len(categories) != len(ids):
        print('Length database != id')
        sys.exit()

    try:
        index = categories.index(category_name)
        print(f"The value of {category_name} is in the ID array!")
        return ids[index]
    except ValueError:
        print(f"The value of {category_name} is not in the ID array.")
        return None
