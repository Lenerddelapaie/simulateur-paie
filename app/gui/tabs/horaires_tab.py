from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox
)


class HorairesTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

        self.inputs_travaillees = {}
        self.inputs_nuit = {}
        self.inputs_payees_normales = {}
        self.inputs_payees_majorees = {}
        self.inputs_payees_equiv = {}

        grid = QGridLayout()
        grid.addWidget(QLabel("Jour"), 0, 0)
        grid.addWidget(QLabel("Trav."), 0, 1)
        grid.addWidget(QLabel("Nuit"), 0, 2)
        grid.addWidget(QLabel("Norm."), 0, 3)
        grid.addWidget(QLabel("Major."), 0, 4)
        grid.addWidget(QLabel("Équiv. 25%"), 0, 5)

        for i, jour in enumerate(jours):
            grid.addWidget(QLabel(jour), i + 1, 0)

            self.inputs_travaillees[jour] = QLineEdit()
            grid.addWidget(self.inputs_travaillees[jour], i + 1, 1)

            self.inputs_nuit[jour] = QLineEdit()
            grid.addWidget(self.inputs_nuit[jour], i + 1, 2)

            self.inputs_payees_normales[jour] = QLineEdit()
            grid.addWidget(self.inputs_payees_normales[jour], i + 1, 3)

            self.inputs_payees_majorees[jour] = QLineEdit()
            grid.addWidget(self.inputs_payees_majorees[jour], i + 1, 4)

            self.inputs_payees_equiv[jour] = QLineEdit()
            grid.addWidget(self.inputs_payees_equiv[jour], i + 1, 5)

        layout.addLayout(grid)

        # Boutons de calcul
        boutons_layout = QHBoxLayout()

        btn_calc_payees = QPushButton("Calcul des heures payées")
        btn_calc_payees.clicked.connect(self.calcul_heures_payees)

        btn_calc_mensuelles = QPushButton("Calcul des heures mensuelles")
        btn_calc_mensuelles.clicked.connect(self.calcul_heures_mensuelles)

        boutons_layout.addWidget(btn_calc_payees)
        boutons_layout.addWidget(btn_calc_mensuelles)

        layout.addLayout(boutons_layout)

        self.setLayout(layout)

    def calcul_heures_payees(self):
        total = 0
        try:
            for jour in self.inputs_travaillees:
                heures = float(self.inputs_travaillees[jour].text() or 0)
                nuit = float(self.inputs_nuit[jour].text() or 0)
                normales = heures - nuit

                self.inputs_payees_normales[jour].setText(str(normales))
                self.inputs_payees_majorees[jour].setText(str(nuit))

                total += heures

            QMessageBox.information(self, "Calcul terminé", f"Total hebdomadaire travaillé : {total} h")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer uniquement des chiffres valides.")

    def calcul_heures_mensuelles(self):
        try:
            total_hebdos = sum(float(self.inputs_travaillees[jour].text() or 0) for jour in self.inputs_travaillees)
            total_mensuel = total_hebdos * 4.33

            QMessageBox.information(self, "Calcul terminé", f"Total mensuel moyen : {total_mensuel:.2f} h")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer uniquement des chiffres valides.")
