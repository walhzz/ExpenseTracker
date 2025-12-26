"""
Main entry point for Expense Tracker application.

Orchestrates the entire workflow:
1. Load configuration
2. Process images via OCR
3. Parse Desjardins transactions
4. Categorize expenses
5. Upload to Notion databases
"""

import sys
import pytesseract
from notion_client import Client

from expense_tracker import config
from expense_tracker import file_utils
from expense_tracker import ocr
from expense_tracker import parsing
from expense_tracker import validation
from expense_tracker import notion_api


def main():
    """
    Main application workflow.
    """
    print("Pillow fonctionne !")

    # 1. Initialize configuration
    config.init_config()

    # 2. Setup Tesseract OCR path
    pytesseract.pytesseract.tesseract_cmd = config.get_tesseract_path()

    # 3. Find valid transaction directory
    repertoires = config.get_transaction_dirs()
    try:
        chemin_valide = file_utils.essayer_avec_autre_repertoire(repertoires)
        config.set_chemin_valide(chemin_valide)
        print(f"Répertoire valide trouvé : {chemin_valide}")
    except ValueError as e:
        print(f"Erreur finale : {e}")
        sys.exit(1)

    # 4. Initialize Notion client
    notion = Client(auth=config.get_notion_token())
    expense_database_id = config.get_expense_database_id()
    income_database_id = config.get_income_database_id()
    account_linking_id = config.get_account_linking_id()

    # 5. Process images via OCR
    image_paths = file_utils.lire_tous_les_fichier_png(chemin_valide)
    text = ocr.traitementImage(image_paths)

    # 6. Parse Desjardins transactions
    text_lines = parsing.supprimer_retours_de_ligne(text)
    data = parsing.traitementTextDesjardins(text_lines)

    # 7. User confirmation to continue
    rep = input("continue ?(YES)")

    if rep != 'YES':
        print('Shut Down!')
        sys.exit()

    print("okay")

    # 8. Transform data
    typesDeDepense = data[0]
    dates = validation.traitementDate(data[1])
    montant = validation.traitementArgent(data[2])

    # 9. Upload to Notion
    notion_api.action(
        expense_database_id,
        income_database_id,
        notion,
        typesDeDepense,
        dates,
        montant,
        account_linking_id
    )


if __name__ == '__main__':
    main()
