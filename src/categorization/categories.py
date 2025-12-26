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
