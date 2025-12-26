"""
Category management and expense categorization module.

Handles expense categorization with pattern matching and interactive learning.
"""

import sys
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

    print(f'!!!! LA DEPENSE: {expense_description}, n\'est pas dans la liste!!!! ')

    repeat = True
    save_it = 'YES'

    # Interactive category selection loop
    while repeat:
        print('if need context, \n ENTER : IDK ')
        element = input(f'entre une catergoie parmis: {categories}\n')

        if element in categories:
            if save_it == 'YES':
                category_file = get_category_file_path(element, categories_dir)
                patterns = load_json(category_file)
                if expense_description not in patterns:
                    patterns.append(expense_description)
                    save_json(category_file, patterns)
                    print('save it!')
            else:
                save_it = 'YES'
            repeat = False

        elif element == 'IDK':
            print('Detail :', expense_description, date, amount)
            while True:
                answer = input('Save in the Categorie? (YES/NO)')
                if answer in ['YES', 'NO']:
                    save_it = answer
                    break

        elif element == 'break':
            sys.exit()
        else:
            print(f'{element} est pas dans la liste ')

    return element


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
        print('Longureur database != id')
        sys.exit()

    try:
        index = categories.index(category_name)
        print(f"La valeur de {category_name} est BIEN dans le tableau de ID !")
        return ids[index]
    except ValueError:
        print(f"La valeur de {category_name} n'est pas dans le tableau de ID.")
        return None
