import sys
import pandas as pd
import openpyxl
from PySide6.QtGui import QIcon, QAction, QBrush, QColor
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QTabWidget, QGridLayout, QWidget, QPushButton, \
    QLineEdit, QLabel, QComboBox, QSpinBox, QTableWidget, QTableWidgetItem

from Fonctions_complémentaires import rename_screenshot_folder, Hyperlien_fast, get_column_labels
from window_change_value_default.window_change_value_default import Change_value_default_window
from Style import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backtesting_fast Snakeman")
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QIcon("C:\\Users\\Baptiste\\Documents\\Web_Scrapping\\GUI_Backtesting_fast\\Snake4.jpg"))
        self.menuBar = self.menuBar()
        self.default_menu = self.menuBar.addMenu("&Changer valeurs defaults")
        self.change_default_value = QAction("Changer values defaults")
        self.default_menu.addAction(self.change_default_value)
        self.change_default_value.triggered.connect(self.fct_change_valeus_defaults)
        # creation widgets
        self.W_backtest_fast = QWidget()
        self.W_rename_screenshot=QWidget()
        layout_rename_screenshot=QGridLayout()
        layout_backtest_fast = QGridLayout()


        # Création table et différents onglets
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.East)

        #Création Widget rename_screenshot
        self.Btn_selection_dossier_rename_screenshot=QPushButton("Selectionne le dossier pour rename screen")
        self.Btn_selection_dossier_rename_screenshot.clicked.connect(self.select_folder)
        self.dossier_rename_screenshot=QLineEdit()
        self.dossier_rename_screenshot.setReadOnly(True)
        self.Label_nb_screenshot_rename=QLabel("Indiquez le nombre de screen par data:")
        self.nb_screenshot_rename=QSpinBox()
        self.Btn_rename_screenshots=QPushButton("Rename Screenshot")
        self.Btn_rename_screenshots.clicked.connect(self.rename_screenshot)
        layout_rename_screenshot.addWidget(self.Btn_selection_dossier_rename_screenshot)
        layout_rename_screenshot.addWidget(self.dossier_rename_screenshot)
        layout_rename_screenshot.addWidget(self.Label_nb_screenshot_rename)
        layout_rename_screenshot.addWidget(self.nb_screenshot_rename)
        layout_rename_screenshot.addWidget(self.Btn_rename_screenshots)

        #Création Widget backtest_fast
        self.Btn_selection_dossier_screenshot=QPushButton("Selection dossier screenshot")
        self.Btn_selection_dossier_screenshot.clicked.connect(self.select_folder)
        self.selection_dossier_screenshot=QLineEdit()
        self.selection_dossier_screenshot.setReadOnly(True)
        self.Btn_selection_fichier=QPushButton("Selection fichier insérer screen")
        self.Btn_selection_fichier.clicked.connect(self.showFileDialog)
        self.Btn_confirmation_selection_dossier_screenshot = QPushButton("Confirmer selection dossier")
        self.Btn_confirmation_selection_dossier_screenshot.clicked.connect(self.confirmer_select_folder)
        self.fichier_appliquer_data=QLineEdit()
        self.fichier_appliquer_data.setReadOnly(True)
        self.label_choisir_feuille=QLabel("Choisir feuille:")
        self.name_feuille=QComboBox()
        self.name_feuille.currentTextChanged.connect(self.change_feuille_combobox)
        self.label_number_screen=QLabel("Nombre de colonne screenshot où appliquer:")
        self.number_screen=QSpinBox()
        self.number_screen.setMinimum(0)
        self.label_colonne_screen=QLabel("Colonnes des screenshots(A,B,C....):")
        self.verification_bonne_colonne = QLineEdit()
        self.label_first_line=QLabel("Premiere ligne où appliquer screenshot:")
        self.first_line=QSpinBox()
        self.first_line.setMinimum(0)
        self.first_line.setMaximum(99999)
        self.Button_Appliquer_screen=QPushButton("Appliquer")
        self.Button_Appliquer_screen.clicked.connect(self.application_screenshot)

        # Creation Widget apercu_feuille
        self.Tab_apercu = QTableWidget()

        self.Tab_apercu.horizontalHeader().sectionClicked.connect(self.selectColumn)
        self.Tab_apercu.verticalHeader().sectionClicked.connect(self.handleRowSelection)
        self.Tab_apercu.setSelectionMode(QTableWidget.NoSelection)
        # Configuration de la sélection pour les colonnes (mode MultiSelection)
        self.selected_columns = set()  # Variable pour suivre les colonnes sélectionnées
        self.selected_columns_alpha = []

        layout_backtest_fast.addWidget(self.Btn_selection_dossier_screenshot)
        layout_backtest_fast.addWidget(self.selection_dossier_screenshot)
        layout_backtest_fast.addWidget(self.Btn_selection_fichier)
        layout_backtest_fast.addWidget(self.fichier_appliquer_data)
        layout_backtest_fast.addWidget(self.Btn_confirmation_selection_dossier_screenshot)
        layout_backtest_fast.addWidget(self.label_choisir_feuille)
        layout_backtest_fast.addWidget(self.name_feuille)
        layout_backtest_fast.addWidget(self.label_number_screen)
        layout_backtest_fast.addWidget(self.number_screen)
        layout_backtest_fast.addWidget(self.label_colonne_screen)
        layout_backtest_fast.addWidget(self.verification_bonne_colonne)
        layout_backtest_fast.addWidget(self.label_first_line)
        layout_backtest_fast.addWidget(self.first_line)
        layout_backtest_fast.addWidget(self.Button_Appliquer_screen)
        layout_backtest_fast.addWidget(self.Tab_apercu)


        #Creation_Widget_affichage feuille:
        self.W_rename_screenshot.setLayout(layout_rename_screenshot)
        self.W_backtest_fast.setLayout(layout_backtest_fast)
        self.tabs.addTab(self.W_rename_screenshot,"Rename Screenshot")
        self.tabs.addTab(self.W_backtest_fast,"Insertion screenshot")
        self.setCentralWidget(self.tabs)

        #Appliquer Style
        label=[self.label_first_line,self.label_colonne_screen,self.label_colonne_screen,self.label_choisir_feuille
            ,self.Label_nb_screenshot_rename,self.label_number_screen]
        Btn_confirmer=[self.Btn_selection_fichier,self.Btn_selection_dossier_screenshot,
            self.Btn_selection_dossier_screenshot,self.Btn_confirmation_selection_dossier_screenshot,self.Btn_selection_dossier_rename_screenshot]
        Btn_Appliquer=[self.Btn_rename_screenshots,self.Button_Appliquer_screen]

        for w in label:
            w.setStyleSheet(label_style)
        for w in Btn_confirmer:
            w.setStyleSheet(button_style_classique)
        for w in Btn_Appliquer:
            w.setStyleSheet(button_style_Appliquer)

    def handleRowSelection(self,logical_index):
        self.first_line.setValue(int(logical_index)+1)
    def selectColumn(self, logical_index):
        # Sélectionnez la colonne cliquée
        column_name = chr(ord('A') + logical_index)
        if logical_index not in self.selected_columns:
            self.selected_columns.add(logical_index)
            self.Tab_apercu.horizontalHeaderItem(logical_index).setBackground(
                QBrush(QColor(230, 230, 230)))  # Légèrement gris
            self.selected_columns_alpha.append(column_name)

        else:
            # Désélectionnez la colonne si elle est déjà sélectionnée
            self.selected_columns.remove(logical_index)
            self.selected_columns_alpha.remove(column_name)
            self.Tab_apercu.horizontalHeaderItem(logical_index).setBackground(
                QBrush(QColor(255, 255, 255)))  # Fond blanc
        self.number_screen.setValue(len(self.selected_columns_alpha))
        self.verification_bonne_colonne.setText("".join([f"{i} " for i in self.selected_columns_alpha]))

    def fct_change_valeus_defaults(self):

        self.w = Change_value_default_window()
        self.resize(300, 300)
        self.w.show()
    def rename_screenshot(self):
        dossier=self.dossier_rename_screenshot.text()
        Nb_screen_trade=int(self.nb_screenshot_rename.value())
        rename_screenshot_folder(dossier,Nb_screenshot_per_trade=Nb_screen_trade)

    def application_screenshot(self):
        file_hyperlien=self.fichier_appliquer_data.text()
        dir_screenshot=self.selection_dossier_screenshot.text()
        nb_screenshot=int(self.number_screen.value())
        num_first_line=int(self.first_line.value())
        name_sheet_screenshot=self.name_feuille.currentText()
        Hyperlien_fast(file_hyperlien,dir_screenshot,self.selected_columns_alpha,nb_screenshot,num_first_line,name_sheet_screenshot=name_sheet_screenshot)
        # Pour selectionner un dossier
    def confirmer_select_folder(self):
        chemin_file=self.fichier_appliquer_data.text()
        # Fonction pour prendre les feuilles et l'ajouter au Combobox
        workbook = openpyxl.load_workbook(chemin_file)
         # Récupérer les noms des feuilles
        sheet_names = workbook.sheetnames
        self.name_feuille.clear()
        self.name_feuille.addItems(sheet_names)


    def change_feuille_combobox(self):
        self.selected_columns_alpha=[]
        self.selected_columns=set()
        chemin=self.fichier_appliquer_data.text()
        name_feuille=self.name_feuille.currentText()
        df=pd.read_excel(chemin,sheet_name=name_feuille,engine="openpyxl")
        self.Tab_apercu.setRowCount(df.shape[0]+1)
        self.Tab_apercu.setColumnCount(df.shape[1])
        column_labels = get_column_labels(df.shape[1])
        self.Tab_apercu.setHorizontalHeaderLabels(column_labels)
        # Ajoutez les en-têtes de colonnes du DataFrame à la première ligne du tableau
        for j, column_name in enumerate(df.columns):
            item = QTableWidgetItem(column_name)
            self.Tab_apercu.setItem(0, j, item)

        # Remplissez le reste du tableau avec les données du DataFrame
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.Tab_apercu.setItem(i + 1, j, item)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner un Dossier", "/path/par/défaut")
        if self.sender()==self.Btn_selection_dossier_rename_screenshot:
            self.dossier_rename_screenshot.setText(folder)
        elif self.sender()==self.Btn_selection_dossier_screenshot:

            self.selection_dossier_screenshot.setText(folder)


        # Pour selectionner un fichier
    def showFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setOptions(options)

        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier", "", "Tous les fichiers (*)")
        if self.sender() == self.Btn_selection_fichier:
            if file_path:
                self.fichier_appliquer_data.setText(file_path)
            else:
                self.fichier_appliquer_data.setText("")





app = QApplication(sys.argv)
window = MainWindow()
window.resize(300, 250)
window.showMaximized()
window.show()
app.exec()
