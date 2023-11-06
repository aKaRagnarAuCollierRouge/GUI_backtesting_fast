import json
import string

import openpyxl
import pandas as pd
import os
from datetime import datetime, date

from openpyxl.styles import Font

def get_column_labels(num_cols):
    # Cette fonction génère des lettres de l'alphabet et les combine pour obtenir des étiquettes de colonne.
    labels = []
    alphabet = string.ascii_uppercase
    for i in range(num_cols):
        label = ""
        if i < 26:
            label = alphabet[i]
        else:
            first_letter = alphabet[i // 26 - 1]
            second_letter = alphabet[i % 26]
            label = first_letter + second_letter
        labels.append(label)
    return labels

def rename_screenshot_folder(dossier,Nb_screenshot_per_trade):

    # Obtenez la date d'aujourd'hui
    aujourd_hui = date.today()
    # Créez une liste pour stocker les fichiers datant d'aujourd'hui
    fichiers_aujourdhui = []
    # Parcourez les fichiers dans le dossier
    for fichier in os.listdir(dossier):
        chemin_fichier = os.path.join(dossier, fichier)
        print(chemin_fichier)
        # Vérifiez si le chemin est un fichier
        if os.path.isfile(chemin_fichier):
            # Obtenez la date de modification du fichier
            date_creation_timestamp = os.path.getctime(chemin_fichier)
            date_modification = date.fromtimestamp(os.path.getmtime(chemin_fichier))

            # Vérifiez si la date de modification est égale à aujourd'hui
            if date_modification == aujourd_hui:
                fichiers_aujourdhui.append((fichier, date_creation_timestamp))
    # Triez la liste de fichiers par date

    fichiers_aujourdhui.sort(key=lambda x: x[1])
    alphabet_majuscules = [chr(i) for i in range(65, 91)]
    combinaison=[]
    for lettre in alphabet_majuscules:
        grp_lettre="Z"+lettre
        combinaison.append(grp_lettre)

    alphabet_majuscules=alphabet_majuscules+combinaison
    nb_screenshot=0
    nb_lettre=0
    for fichier in fichiers_aujourdhui:
        lettre=alphabet_majuscules[nb_lettre]
        extension=fichier[0].split('.')[-1]
        name=f"{dossier}/{lettre} ({nb_screenshot+1}).{extension}"
        chemin_fichier=f"{dossier}/{fichier[0]}"
        os.rename(chemin_fichier, name)
        nb_screenshot += 1
        if nb_screenshot==Nb_screenshot_per_trade:
            nb_lettre+=1
            nb_screenshot=0


def Hyperlien_fast(File_hyperlien,dir_screenshot,liste_colonnes,nb_screenshot,num_first_line,name_sheet_screenshot):
    # Nom de votre fichier JSON
    nom_fichier_json = "données.json"
    with open(nom_fichier_json, "r") as fichier_json:
        data = json.load(fichier_json)
    liste_fichier_exclure = data["valeurs_defaults"]["words_exclure_backtesting"]

    Fichier_insert_hyperlien = rf"{os.path.normpath(File_hyperlien)}"
    path_dir_screenshot=rf"{os.path.normpath(dir_screenshot)}"






    liste = []
    nom_screenshot = ''
    liste_screenshot=[]
    for filename in os.listdir(path_dir_screenshot):
        # Vérifie que le fichier est un fichier (et pas un dossier)
        if filename in liste_fichier_exclure:
            pass

        elif os.path.isfile(os.path.join(path_dir_screenshot, filename)):
            name = ''
            for character in filename:

                if character == " ":
                    break
                else:
                    name += character
            if nom_screenshot == name:

                liste.append(filename)
            else:
                if len(liste)>0:
                    liste_screenshot.append(liste)
                liste = [filename]
                nom_screenshot = name

    liste_screenshot.append(liste)

    number_line=0


    # Ouvrir un fichier Excel existant
    workbook = openpyxl.load_workbook(Fichier_insert_hyperlien)
    #Donnez le nom de la feuille de calcul
    w= workbook[name_sheet_screenshot]

    for c in liste_screenshot:
        for i in range(len(c)):

            screen=path_dir_screenshot+f"\\{c[i]}"
            w[f"{liste_colonnes[i]}{num_first_line}"].value=screen
            w[f"{liste_colonnes[i]}{num_first_line}"].hyperlink=screen
            w[f"{liste_colonnes[i]}{num_first_line}"].font = Font(color='0563C1',size=32)
        num_first_line+=1
    workbook.save(Fichier_insert_hyperlien)

