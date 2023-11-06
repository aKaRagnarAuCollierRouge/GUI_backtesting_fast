import json
import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QScrollArea, QPushButton, QLineEdit, QComboBox, QLabel


class Change_value_default_window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("C:\\Users\\Baptiste\\Documents\\Web_Scrapping\\GUI_Backtesting_fast\\Snake4.jpg"))
        self.setWindowTitle("Change value defaults")

        #Telecharger datas:
        # Emplacement du répertoire du script Python
        emplacement_script = os.path.dirname(os.path.abspath(__file__))
        # Nom de votre fichier JSON
        nom_fichier_json = "données.json"
         # Construction du chemin relatif vers le répertoire parent
        self.chemin_json = os.path.join(emplacement_script, "..", nom_fichier_json)

        with open(self.chemin_json, "r") as fichier_json:
            data = json.load(fichier_json)
        screen_words = data["valeurs_defaults"]["words_screenshot_colonne"]
        backtesting_words=data["valeurs_defaults"]["words_exclure_backtesting"]

        #Mise en place des widgets
        self.setWindowTitle("Changer value default ")
        layout = QGridLayout()
        self.label_ajouter_word_screen=QLabel("Entrer un world screen à ajouter:")
        self.add_word_screen=QLineEdit()
        self.Btn_add_word_screen=QPushButton("Ajouter Word Screen")
        self.Btn_add_word_screen.clicked.connect(self.add_word)
        self.label_delete_word_screen=QLabel("Supprimer word screen")
        self.screen_words_list = QComboBox()
        self.Btn_delete_word_screen=QPushButton("Detruire word screen")
        self.Btn_delete_word_screen.clicked.connect(self.delete_word)
        self.screen_words_list.addItems(screen_words)

        layout.addWidget(self.label_ajouter_word_screen)
        layout.addWidget(self.add_word_screen)
        layout.addWidget(self.Btn_add_word_screen)
        layout.addWidget(self.label_delete_word_screen)
        layout.addWidget(self.screen_words_list)
        layout.addWidget(self.Btn_delete_word_screen)
        layout.addWidget(self.screen_words_list)



        self.label_ajouter_word_backtesting_exclure=QLabel("entrez un nom de fichier à exclure:")
        self.ajouter_word_backtesting_exclure=QLineEdit()
        self.Btn_ajouter_word_backtesting_exclure=QPushButton("Ajouter Word backtesting")
        self.Btn_ajouter_word_backtesting_exclure.clicked.connect(self.add_word)
        self.label_delete_word_backtesting=QLabel("Supprimer Word Backtesting")
        self.backtesting_word=QComboBox()
        self.backtesting_word.addItems(backtesting_words)
        self.Btn_delete_word_backtesting=QPushButton("Detruire word backtesting")
        self.Btn_delete_word_backtesting.clicked.connect(self.delete_word)

        layout.addWidget(self.label_ajouter_word_backtesting_exclure)
        layout.addWidget(self.ajouter_word_backtesting_exclure)
        layout.addWidget(self.Btn_ajouter_word_backtesting_exclure)
        layout.addWidget(self.label_delete_word_backtesting)
        layout.addWidget(self.backtesting_word)
        layout.addWidget(self.Btn_delete_word_backtesting)

        self.setLayout(layout)
        #Style
        liste_label=[self.label_delete_word_backtesting,self.label_delete_word_screen,self.label_delete_word_backtesting,
                     self.label_ajouter_word_screen]
        liste_btn_ajouter=[self.Btn_ajouter_word_backtesting_exclure,self.Btn_add_word_screen]
        liste_btn_delete=[self.Btn_delete_word_backtesting,self.Btn_delete_word_backtesting]

    def delete_word(self):
        with open(self.chemin_json, "r") as fichier_json:
            data = json.load(fichier_json)
        if self.sender()== self.Btn_delete_word_screen:
            mot_effacer=self.screen_words_list.currentText()
            data["valeurs_defaults"]["words_screenshot_colonne"].remove(mot_effacer)
            self.screen_words_list.clear()
            self.screen_words_list.addItems(data["valeurs_defaults"]["words_screenshot_colonne"])
        elif self.sender()==self.Btn_delete_word_backtesting:
            mot_effacer = self.backtesting_word.currentText()
            data["valeurs_defaults"]["words_exclure_backtesting"].remove(mot_effacer)

            self.backtesting_word.clear()
            self.backtesting_word.addItems(data["valeurs_defaults"]["words_exclure_backtesting"])

        # Sauvegarder les modifications dans le fichier JSON
        with open(self.chemin_json, "w") as fichier_json:
            json.dump(data, fichier_json, indent=4)

    def add_word(self):
        with open(self.chemin_json, "r") as fichier_json:
            data = json.load(fichier_json)
        if self.sender()==self.Btn_add_word_screen:
            mot_ajout=self.add_word_screen.text()
            data["valeurs_defaults"]["words_screenshot_colonne"].append(mot_ajout)
            self.screen_words_list.clear()
            self.screen_words_list.addItems(data["valeurs_defaults"]["words_screenshot_colonne"])
        elif self.sender()==self.Btn_ajouter_word_backtesting_exclure:
            mot_ajout=self.ajouter_word_backtesting_exclure.text()
            data["valeurs_defaults"]["words_exclure_backtesting"].append(mot_ajout)
            self.backtesting_word.clear()
            self.backtesting_word.addItems(data["valeurs_defaults"]["words_exclure_backtesting"])

        # Sauvegarder les modifications dans le fichier JSON
        with open(self.chemin_json, "w") as fichier_json:
            json.dump(data, fichier_json, indent=4)

