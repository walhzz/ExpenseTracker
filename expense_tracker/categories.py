"""
Category management and user interaction module.

Handles expense categorization with pattern matching and interactive learning.
"""

import sys
from expense_tracker.file_utils import charger_tableau, sauvegarder_tableau, get_fichier


def categorie(Depense, Date, Montant, base_path):
    """
    Categorize an expense interactively with pattern matching and learning.

    Searches for the expense in existing category patterns.
    If not found, prompts user for category and optionally saves the pattern.

    Args:
        Depense: Expense description
        Date: Transaction date
        Montant: Amount
        base_path: Base directory containing category JSON files

    Returns:
        Category name assigned to the expense
    """
    tableau = charger_tableau(get_fichier('Database.json', base_path))

    # Search through all categories
    for i in tableau:
        fichier = get_fichier(i + '.json', base_path)
        for j in charger_tableau(fichier):

            if j == []:
                continue

            if Depense in j:
                return i

    print('!!!! LA DEPENSE: ' + Depense + ', n\'est pas dans la liste!!!! ')

    repeat = True
    save_it = 'YES'

    # Interactive category selection loop
    while repeat:
        print('if need context, \n ENTER : IDK ')
        element = input('entre une catergoie parmis: ' + str(tableau) + '\n')

        if element in tableau:
            if save_it == 'YES':
                vierge = charger_tableau(get_fichier(element + '.json', base_path))
                if Depense not in vierge:
                    vierge.append(Depense)
                    sauvegarder_tableau(get_fichier(element + '.json', base_path), vierge)
                    print('save it!')

            else:
                save_it = 'YES'
            repeat = False

        elif element == 'IDK':
            print('Detail :', Depense, Date, Montant)
            while True:
                answer = input('Save in the Categorie? (YES/NO)')
                if answer == 'YES' or answer == 'NO':
                    save_it = answer
                    break

        elif element == 'break':
            sys.exit()
        else:
            print(str(element) + ' est pas dans la liste ')

    return element


def fournir_id(cate, base_path):
    """
    Get Notion ID for a category name.

    Maps category name to its corresponding Notion page ID by looking up
    the index in Database.json and returning the matching ID from id.json.

    Args:
        cate: Category name
        base_path: Base directory containing Database.json and id.json

    Returns:
        Notion page ID for the category
    """
    x = charger_tableau(get_fichier('Database.json', base_path))
    y = charger_tableau(get_fichier('id.json', base_path))

    if len(x) != len(y):
        print('Longureur database != id')
        sys.exit()
    else:
        try:
            index = x.index(cate)
            print("La valeur de " + cate + " est BIEN dans le tableau de ID !")
            return y[index]
        except ValueError:
            print("La valeur de " + cate + " n'est pas dans le tableau de ID.")
            return None
