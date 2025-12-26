#----Importation --------------------------------------------------------

from PIL import Image
print("Pillow fonctionne !")
import pytesseract
from notion_client import Client
import os
import glob
import re
from datetime import datetime
import json
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import sys
import pandas as pd
from dotenv import load_dotenv

#-- Declaration des Fonctions et des procedures du programme----------------------------------------------------------------

def lire_tous_les_fichier_png(repertoire):

    chemin_png = glob.glob(os.path.join(repertoire, '*.jpeg'))

    if not chemin_png:
        print("Aucun fichier jpeg trouvé dans le répertoire.")
        return []
    
    print("Fichiers jpeg trouvés :")
    for fichier in chemin_png:
        print(fichier)
    
    return chemin_png

def retourner_image(image_path):
    return Image.open(image_path)

def lireTextImage(img) :
    texte = pytesseract.image_to_string(img, lang = 'eng')
    return texte

def supprimer_retours_de_ligne(texte):
 
    """
    Supprime les retours de ligne (\n) d'un texte et retourne un tableau avec les lignes sans retours.
    """
    # Divise le texte en lignes et supprime les lignes vides
    lignes = texte.splitlines()

    # Nettoie chaque ligne pour supprimer les espaces supplémentaires si nécessaire
    lignes_sans_retours = [ligne.strip() for ligne in lignes if ligne.strip()]
    print('!' + str(lignes_sans_retours))
    return lignes_sans_retours

def reperer_dates(texte):
    """
    Repère toutes les dates au format 'Mon DD' (ex: Jan 15, Dec 1) dans un texte
    et retourne une liste de tuples (mois, jour).
    """
    # Définition de l'expression régulière pour capturer le mois et le jour
    pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9][0-9]?)\b'
    
    matches = re.search(pattern, texte)
    
    if matches:
        # Si une date est trouvée, formater et retourner 'Mon DD'
        return f"{matches.group(1)} {matches.group(2)}"
    
    # Si aucune date n'est trouvée, retourner None
    return None

def retirer_date(texte):
    """
    Extrait une date au format 'Mon DD' (ex: Jan 12, Dec 16) d'une chaîne.
    Retourne la chaîne sans la date détectée.
    """
    # Définition de l'expression régulière pour capturer une date
    pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9][0-9]?)\b'
    
    # Recherche de la première correspondance
    match = re.search(pattern, texte)
    
    if match:
        # Supprimer la date trouvée de la chaîne
        texte_sans_date = re.sub(pattern, "", texte).strip()
        return texte_sans_date
    
    # Si aucune date n'est trouvée, retourner la chaîne originale
    return texte

def verifier_repertoire(repertoire):
    """
    Vérifie si un répertoire existe, lève une ValueError si ce n'est pas le cas.
    """
    if not os.path.isdir(repertoire):
        raise ValueError(f"Le chemin '{repertoire}' n'est pas un répertoire valide.")
    return f"Le répertoire '{repertoire}' est valide."

def essayer_avec_autre_repertoire(repertoires):
    """
    Tente de valider un répertoire parmi une liste.
    Si un répertoire est invalide, essaie avec le suivant.
    """
    for chemin in repertoires:
        try:
            resultat = verifier_repertoire(chemin)
            print(resultat)
            return chemin  # Retourne le chemin valide trouvé
        except ValueError as e:
            print(f"Erreur détectée : {e}")
    
    # Si aucun répertoire n'est valide, lever une exception
    raise ValueError("Aucun des répertoires fournis n'est valide.")

def nettoyer_colonne(dataframe, colonne):
    """
    Retire les éléments vides ("") ou None d'une colonne spécifique d'un DataFrame.
    
    Paramètres :
    - dataframe : le DataFrame pandas
    - colonne : le nom de la colonne à nettoyer (string)
    
    Retourne :
    - Une nouvelle série pandas sans les valeurs vides ou None.
    """
    # Filtrer les éléments non vides et non-None
    colonne_nettoyee = dataframe[colonne].dropna()  # Supprimer les valeurs None
    colonne_nettoyee = colonne_nettoyee[colonne_nettoyee != ""]  # Supprimer les valeurs vides ("")
    return colonne_nettoyee

def traitementTextDesjardins(texteTab):

    data = {'Transaction': texteTab }
    df = pd.DataFrame(data)

    data2 =  df["Transaction"].apply(reperer_dates)
    tf = pd.DataFrame(data2)

    data3 = df["Transaction"].apply(extraire_depense)
    mt = pd.DataFrame(data3)

    df["Transaction"] = df["Transaction"].apply(retirer_date)
    df["Transaction"] = df["Transaction"].apply(retirer_depense)
    df["Transaction"] = df["Transaction"].astype(str).str.replace(">", "", regex=False)
    df["Transaction"] = df["Transaction"].str.lower()

    df = df[~df["Transaction"].str.startswith(("visa", "to", "with", "kk", "ak", "from 02","r4","n10","y4","GOUV.QUEBEC","Pre-authorized purchase /" ))]    
    df = df[~df["Transaction"].str.contains(r"8086|interac|0268907|gouv. quebec|pre-authorized purchase|direct deposit", case=False)]

    df = df[df['Transaction'].notna() & (df['Transaction'] != '')]
    df = df.reset_index(drop=True)

    tf = tf.dropna(subset=['Transaction'])
    tf = tf.reset_index(drop=True)

    mt = mt.dropna(subset=['Transaction'])
    mt = mt.reset_index(drop = True)

    df['ID'] = df.index
    tf['ID'] = tf.index
    mt['ID'] = mt.index

    df_merged = pd.merge(df, tf, on='ID', how='outer', suffixes=('_df', '_tf'))
    df_merged = pd.merge(df_merged,mt,on='ID', how='outer', suffixes=('_df', '_tf'))

    print(df_merged)

    rep = input('edit ?')

    while rep.upper() == 'YES':
        file_path = "temp_file.xlsx"
    
        # Écrire le fichier CSV avec un séparateur clair, par exemple une virgule
        #df_merged.to_csv(file_path, index=False, sep=';', encoding='utf-8')  # Notez sep=';'
    
        df_merged.to_excel(file_path, index=False, engine='openpyxl')

        print(f"File saved to {file_path}. Please edit the file and save your changes.")
        os.startfile(file_path)  # Ouvrir le fichier dans Excel (ou l'application par défaut pour .csv)
    
        input("Press Enter after you finish editing and save the file...")
    
        # Recharger le fichier modifié
        #df_merged = pd.read_csv(file_path, sep=',', encoding='utf-8')
        df_merged = pd.read_excel(file_path, engine='openpyxl')
        
        print("Updated DataFrame:")
        print(df_merged)
    
        # Supprimer le fichier temporaire
        os.remove(file_path)
        print("Temporary file deleted.")
    
        rep = input('Edit again? (YES/NO): ')


    A = df_merged["Transaction_df"].tolist()
    B = df_merged["Transaction_tf"].tolist()
    C = df_merged["Transaction"].tolist()

    return [A,B,C]

def extraire_depense(chaine):
    # Utiliser une expression régulière pour extraire le nom du magasin et le montant
    match = re.search(r"\s*([+-]?\$\d+\.\d{2})", chaine)
    
    if match:  # Récupère le nom du magasin, en retirant les espaces inutiles
        depense = match.group(1) # Récupère le montant de la dépense
        return f"{depense}"
    else:
        return None

def retirer_depense(chaine):
    pattern = r"\s*([+-]?\$\d+\.\d{2})"
    
    # Recherche de la première correspondance
    
    match = re.search(pattern, chaine)
    
    if match:
        # Supprimer la date trouvée de la chaîne
        texte_sans_depense = re.sub(pattern, "", chaine).strip()
        return texte_sans_depense
    
    # Si aucune date n'est trouvée, retourner la chaîne originale
    return chaine

def traitementArgent(tab):
    resultat = []
    for i in tab:
        # Si i est déjà un float, pas besoin de traitement
        if isinstance(i, float) or isinstance(i, int):
            resultat.append(float(i))
            continue

        original = i  # Pour debug
        try:
            # Nettoyage de texte si c'est une chaîne
            i = i.replace("$", "").replace(",", "").strip()
            nombre = float(i)
            resultat.append(nombre)
        except (ValueError, AttributeError):
            print(f"Impossible de convertir '{original}' en nombre.")
            resultat.append(None)
    return resultat



def traitementDate(dates):
    resultats = []
    maintenant = datetime.now()  # Date actuelle

    for date in dates:
        # Tenter avec l'année courante
        date_cible = datetime.strptime(f"{maintenant.year} {date}", "%Y %b %d")
        
        # Si la date dépasse maintenant, prendre l'année précédente
        if date_cible > maintenant:
            date_cible = datetime.strptime(f"{maintenant.year - 1} {date}", "%Y %b %d")
        
        # Ajouter au résultat après conversion au format ISO
        resultats.append(date_cible.strftime("%Y-%m-%d"))
    
    return resultats

def new_expense_data(notion, database_id, text, date, totalAmount, Title,c):
    # Préparer les données de la nouvelle page
    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Date": {
                "date": {
                    "start": date,  # Date au format ISO 8601
                    "end": None
                }
            },
            "Files & media": {
                "files": []  # Champ vide
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
                "number": totalAmount  # Montant en dollars
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
                    "id": os.getenv("ACCOUNT_LINKING_ID")  # Remplacez account_page_id par l'ID de la page liée
                }
            ]
            },
            "Categories": {
                "relation": [
                    {
                    "id": c  # Remplacez account_page_id par l'ID de la page liée
                }
            ]
        }
    }
    }

    # Créer la nouvelle page
    try:
        response = notion.pages.create(**new_page_data)
        print("Nouvelle page créée :", response)
        return response
    except Exception as e:
        print("Erreur lors de la création de la page :", e)
        return None

def new_income_data(notion, income_database_id, typesDeDepense,dates,montant):
    new_page_data = {
        "parent": {"database_id": income_database_id},
        "properties": {
            "Date ( Deposite)": {
                "date": {
                    "start": dates,  # Date au format ISO 8601
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
                "number": montant  # Montant en dollars
            },
            
            "Accounts": {
                "relation": [
                    {
                    "id": os.getenv("ACCOUNT_LINKING_ID")  # Remplacez account_page_id par l'ID de la page liée
                }
            ]
        }
        }
    }

    # Créer la nouvelle page
    try:
        response = notion.pages.create(**new_page_data)
        print("Nouvelle page créée :", response)
        return response
    except Exception as e:
        print("Erreur lors de la création de la page :", e)
        return None

def traitementImage(cheminTab):
    text =''
    for i in cheminTab:
        img = retourner_image(i)
        text += ' '+ lireTextImage(img)
    return text

def action(expense_database_id,income_database_id,notion,typesDeDepense,dates,montant):

    if len(typesDeDepense) == len(dates) and len(typesDeDepense) == len(montant):
        for i in range(len(montant)):
            x = montant[i]
            if x == 0:
                continue
            elif x < 0:
                c = fournir_id(categorie(typesDeDepense[i],dates[i],montant[i]))
                print(c)
                new_expense_data(notion,expense_database_id, typesDeDepense[i],
                dates[i], montant[i]*-1, typesDeDepense[i],c)           
            else:
                new_income_data(notion, income_database_id, typesDeDepense[i],dates[i],montant[i])
    else: 
        print("nombre de données sont inegales")

def sauvegarder_tableau(fichier, tableau):
    """
    Sauvegarde un tableau dans un fichier au format JSON.

    Args:
        fichier (str): Nom du fichier pour sauvegarder les données.
        tableau (list): Le tableau à sauvegarder.
    """
    with open(fichier, 'w') as f:
        json.dump(tableau, f)

def charger_tableau(fichier):
    """
    Charge un tableau depuis un fichier JSON.

    Args:
        fichier (str): Nom du fichier à lire.

    Returns:
        list: Le tableau chargé depuis le fichier ou une liste vide si le fichier est vide ou introuvable.
    """
    try:
        with open(fichier, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print('Le fichier n\'existe pas, retourne une liste vide.')
        return []
    except json.JSONDecodeError:
        print('Le fichier est vide ou corrompu, retourne une liste vide.')
        return []

def categorie(Depense,Date,Montant): 

    tableau = charger_tableau(get_fichier('Database.json'))

    for i in tableau: 
        fichier = get_fichier(i + '.json')
        for j in charger_tableau(fichier):

            if j == []:
                continue

            if Depense in j :
                return i
    
    print('!!!! LA DEPENSE: ' + Depense + ', n\'est pas dans la liste!!!! ')

    repeat = True
    save_it = 'YES'

    while repeat:
        print('if need context, \n ENTER : IDK ')
        element = input('entre une catergoie parmis: ' + str(tableau) + '\n' )

        if element in tableau :
            if save_it == 'YES':
                vierge = charger_tableau(get_fichier(element +'.json'))
                if Depense not in vierge:
                    vierge.append(Depense)
                    sauvegarder_tableau(get_fichier(element +'.json'),vierge,)
                    print('save it!')

            else:
                save_it = 'YES'
            repeat = False
        elif element == 'IDK':
            print('Detail :', Depense, Date, Montant)
            while True:
                answer = input('Save in the Categorie? (YES/NO)' )
                if answer == 'YES' or answer == 'NO':
                    save_it = answer
                    break

        elif element == 'break':
            sys.exit()
        else:
            print(str(element) + ' est pas dans la liste ')

    return element

def on_select(event=None):
    """
    Vérifie si la sélection existe dans la liste. Si elle n'existe pas,
    demande à l'utilisateur de confirmer l'ajout d'une nouvelle option.
    """
    selection = selected_option.get()  # Récupère la valeur actuelle
    if selection not in options:  # Vérifie si l'élément est déjà dans la liste
        # Demande confirmation pour ajouter le nouvel élément
        reponse = simpledialog.askstring("Nouvelle option", f"L'élément '{selection}' n'existe pas. Voulez-vous l'ajouter ?")
        if reponse:  # Si l'utilisateur confirme l'ajout
            options.append(reponse)  # Ajoute le nouvel élément
            combo['values'] = options  # Met à jour la liste déroulante
            combo.set(reponse)  # Sélectionne automatiquement la nouvelle option
        else:
            combo.set(options[0])  # Réinitialise la sélection si l'utilisateur annule
    else:
        print(f"Option choisie : {selection}")  # Option existante

def get_fichier(nomFichier):
    repeat = True

    if nomFichier == 'break':
        return None 


    while repeat:
        if isinstance(nomFichier,str):
            file = chemin_valide + '\\'+ nomFichier
            repeat = False
            print('chemin chercher :')
            print(file)
            return file

        else: 
            print("Erreur : La variable n'est pas une chaîne.")

def get_id(index):
    x = charger_tableau(get_fichier('id.json'))
    return x[index]

def get_dataBase(index):
    x = charger_tableau(get_fichier('Database.json'))
    return x[index]

def fournir_id(cate):

    x = charger_tableau(get_fichier('Database.json'))
    y = charger_tableau(get_fichier('id.json'))

    if len(x) != len(y):
        print('Longureur database != id')
        sys.exit()
    else:
        try:
            index = x.index(cate)
            print("La valeur de " + cate + "est BIEN dans le tableau de ID !")
            return y[index]
        except ValueError:
            
            print("La valeur de " + cate + " n'est pas dans le tableau de ID.")

def get_options():
    """
    Retourne la liste actuelle des options sous forme de tableau.
    """
    return options

def afficher_liste():
    tableau_options = get_options()  # Récupère la liste complète
    print("Liste actuelle des options :", tableau_options)

# Modele de categorisation:

#--- Main procedure -----------------------------------------------------------
def main():

    # Load environment variables
    load_dotenv()

    # variable declaration
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", r'C:\Program Files\Tesseract-OCR\tesseract.exe')

    # Parse transaction directories from environment variable
    transaction_dirs_str = os.getenv("TRANSACTION_DIRS", r'C:\Users\PC\iCloudDrive\Transaction,C:\Users\Walid\iCloudDrive\Transaction')
    repertoires = [dir.strip() for dir in transaction_dirs_str.split(',')]

    # Notion DataBase
    notion = Client(auth=os.getenv("NOTION_API_TOKEN"))
    expense_database_id = os.getenv("EXPENSE_DATABASE_ID")
    income_database_id = os.getenv("INCOME_DATABASE_ID")

    global chemin_valide

    try:
        chemin_valide = essayer_avec_autre_repertoire(repertoires)
        print(f"Répertoire valide trouvé : {chemin_valide}")
    except ValueError as e:
        print(f"Erreur finale : {e}")
    
    text = traitementImage(lire_tous_les_fichier_png(chemin_valide))
    data = traitementTextDesjardins(supprimer_retours_de_ligne(text))
    
    rep = input ("continue ?(YES)")

    if rep != 'YES':
        print('Shut Down!')
        sys.exit()

    print("okay")
    
    typesDeDepense = data[0]
    dates = traitementDate(data[1])
    montant = traitementArgent(data[2])

    action(expense_database_id, income_database_id, notion, typesDeDepense, dates, montant)

main()