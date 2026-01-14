"""
Category management and expense categorization module.

Handles expense categorization with pattern matching and interactive learning.
"""

from typing import Any, Optional, TypedDict

import questionary
from src.utils import (
    load_json,
    save_json,
    get_database_json_path,
    get_categories_dir,
)


<<<<<<< Updated upstream
def categorize_expense(expense_description, date, amount):
    """
    Categorize an expense interactively with pattern matching and learning.

    Searches for the expense in existing category patterns.
    If not found, prompts user for category and optionally saves the pattern.

    Args:
        expense_description: Expense description
        date: Transaction date
        amount: Amount

    Returns:
        Category name assigned to the expense
    """
    categories_dir = get_categories_dir()
    database_path = get_database_json_path(categories_dir)
    categories = load_json(database_path)

    # Search through all categories
    for category in categories:
        category_file = get_category_file_path(category, categories_dir)
        patterns = load_json(category_file)

        for pattern in patterns:
            if pattern == []:
                continue

            if expense_description in pattern:
                return category

    print(f'!!!! EXPENSE: {expense_description}, is not in the list!!!! ')

    save_pattern = True

    # Interactive category selection with menu
    while True:
        # Create choices with categories plus special options
        choices = categories + ['─── Special Options ───', 'Show Details', 'Exit Program']

        selected = questionary.select(
            f'Select a category for: {expense_description[:50]}...',
            choices=choices,
            use_shortcuts=True,
            use_arrow_keys=True
        ).ask()

        # Handle special options
        if selected == 'Show Details':
            print('\n' + '=' * 60)
            print(f'Detail: {expense_description}')
            print(f'Date: {date}')
            print(f'Amount: {amount}')
            print('=' * 60 + '\n')

            save_pattern = questionary.confirm(
                'Save this expense pattern to the selected category?',
                default=True
            ).ask()
            continue  # Go back to category selection

        elif selected == 'Exit Program':
            print('Exiting program...')
            sys.exit()

        elif selected == '─── Special Options ───':
            continue  # Separator, go back to selection

        elif selected in categories:
            # Valid category selected
            if save_pattern:
                category_file = get_category_file_path(selected, categories_dir)
                patterns = load_json(category_file)
                if expense_description not in patterns:
                    patterns.append(expense_description)
                    save_json(category_file, patterns)
                    print(f'✓ Pattern saved to {selected}!')

            return selected

        else:
            print(f'{selected} is not in the list')
            continue


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
=======
class CategoryResult(TypedDict):
    """Type definition for category lookup/selection results."""
    id: str
    name: str
    expense: str


def get_expense_class_by_description(expense_description: str) -> Optional[CategoryResult]:
    """Find a category containing the given expense description.

    Searches through all categories in the database to find one that
    contains the exact expense description in its list of known expenses.

    Args:
        expense_description: The expense description text to search for

    Returns:
        A CategoryResult dict with id, name, and expense fields if found,
        or None if the expense is not in any category
    """
    categories_dir = get_categories_dir()
    database_path = get_database_json_path(categories_dir)
    categories: list[dict[str, Any]] = load_json(database_path)

    for category in categories:
        if expense_description in category["expenses"]:
            return {
                "id": category["id"],
                "name": category["name"],
                "expense": expense_description
            }

    return None


def add_expense_description_to_category(expense_description: str, category_name: str) -> None:
    """Add an expense description to a category's known expenses list.

    Loads the category database, finds the specified category by name,
    and adds the expense description to its list if not already present.
    Saves the updated database back to disk.

    Args:
        expense_description: The expense description text to add
        category_name: Name of the category to add the expense to

    Returns:
        None
    """
    categories_dir = get_categories_dir()
    database_path = get_database_json_path(categories_dir)
    categories: list[dict[str, Any]] = load_json(database_path)

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


def categorize_expense(expense_description: str, date: str, amount: float) -> CategoryResult:
    """Categorize an expense interactively with pattern matching and learning.

    First searches for the expense in existing category patterns. If not found,
    prompts the user to select a category from a list using an interactive menu.
    Optionally saves the new pattern for future automatic categorization.

    Args:
        expense_description: The expense description text to categorize
        date: Transaction date in ISO format (for display purposes)
        amount: Transaction amount (for display purposes)

    Returns:
        A CategoryResult dict containing:
            - id: The category's Notion page ID
            - name: The category name
            - expense: The original expense description

    Note:
        If the user selects "Exit" from the category menu, the program
        will terminate.
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
    categories: list[dict[str, Any]] = load_json(database_path)

    # Create list of category names for selection, with exit option
    category_choices: list[str] = [category['name'] for category in categories]
    category_choices.append("Exit")

    # Use questionary to select category
    selected_name: Optional[str] = questionary.select(
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
    save_pattern: Optional[bool] = questionary.confirm(
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
>>>>>>> Stashed changes
