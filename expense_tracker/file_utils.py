"""
File operations and JSON persistence module.

Handles file system operations, directory validation, and JSON data storage.
"""

import os
import glob
import json
import sys


def lire_tous_les_fichier_png(repertoire):
    """
    Find all .jpeg files in a directory.
    Note: Function name says 'png' but searches for 'jpeg' files.

    Args:
        repertoire: Directory path to search

    Returns:
        List of paths to .jpeg files found
    """
    chemin_png = glob.glob(os.path.join(repertoire, '*.jpeg'))

    if not chemin_png:
        print("Aucun fichier jpeg trouvé dans le répertoire.")
        return []

    print("Fichiers jpeg trouvés :")
    for fichier in chemin_png:
        print(fichier)

    return chemin_png


def verifier_repertoire(repertoire):
    """
    Verify if a directory exists.

    Args:
        repertoire: Directory path to verify

    Returns:
        Success message if directory is valid

    Raises:
        ValueError: If directory doesn't exist
    """
    if not os.path.isdir(repertoire):
        raise ValueError(f"Le chemin '{repertoire}' n'est pas un répertoire valide.")
    return f"Le répertoire '{repertoire}' est valide."


def essayer_avec_autre_repertoire(repertoires):
    """
    Try to validate a directory from a list of candidates.
    Returns the first valid directory found.

    Args:
        repertoires: List of directory paths to try

    Returns:
        First valid directory path found

    Raises:
        ValueError: If none of the directories are valid
    """
    for chemin in repertoires:
        try:
            resultat = verifier_repertoire(chemin)
            print(resultat)
            return chemin  # Return the valid path found
        except ValueError as e:
            print(f"Erreur détectée : {e}")

    # If no valid directory found, raise exception
    raise ValueError("Aucun des répertoires fournis n'est valide.")


def sauvegarder_tableau(fichier, tableau):
    """
    Save an array to a JSON file.

    Args:
        fichier: Filename/path to save to
        tableau: List/array to save
    """
    with open(fichier, 'w') as f:
        json.dump(tableau, f)


def charger_tableau(fichier):
    """
    Load an array from a JSON file.

    Args:
        fichier: Filename/path to read from

    Returns:
        Loaded list/array, or empty list if file not found/corrupted
    """
    try:
        with open(fichier, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Le fichier n'existe pas, retourne une liste vide.")
        return []
    except json.JSONDecodeError:
        print("Le fichier est vide ou corrompu, retourne une liste vide.")
        return []


def get_fichier(nomFichier, base_path):
    """
    Construct full file path using a base directory.

    Refactored from original to accept base_path parameter instead
    of using global chemin_valide variable.

    Args:
        nomFichier: Name of the file
        base_path: Base directory path

    Returns:
        Full path to the file, or None if nomFichier is 'break'
    """
    if nomFichier == 'break':
        return None

    if isinstance(nomFichier, str):
        file = os.path.join(base_path, nomFichier)
        print('chemin chercher :')
        print(file)
        return file
    else:
        print("Erreur : La variable n'est pas une chaîne.")
        return None


def get_id(index, base_path):
    """
    Get Notion category ID by index from id.json.

    Args:
        index: Index position in the id array
        base_path: Base directory containing id.json

    Returns:
        Notion ID at the specified index
    """
    x = charger_tableau(get_fichier('id.json', base_path))
    return x[index]


def get_dataBase(index, base_path):
    """
    Get database category name by index from Database.json.

    Args:
        index: Index position in the Database array
        base_path: Base directory containing Database.json

    Returns:
        Category name at the specified index
    """
    x = charger_tableau(get_fichier('Database.json', base_path))
    return x[index]
