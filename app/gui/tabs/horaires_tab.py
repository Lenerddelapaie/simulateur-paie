from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from app.core.fiche_societe.horaires_travail import HorairesTravail
from app.data.database import Session
from app.data.models import HorairesEtablissement
from datetime import datetime

class HorairesTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

        self.inputs_travaillees = {}
        self.inputs_normales = {}
        self.inputs_sup = {}

        grid = QGridLayout()
        grid.addWidget(QLabel("Jour"), 0, 0)
        grid.addWidget(QLabel("Travaillées"), 0, 1)
        grid.addWidget(QLabel("Heures normales"), 0, 2)
        grid.addWidget(QLabel("Heures supp."), 0, 3)

        horaires_defaut = HorairesTravail().repartition_defaut

        for i, jour in enumerate(jours):
            grid.addWidget(QLabel(jour), i + 1, 0)

            input_trav = QLineEdit(str(horaires_defaut.get(jour, 0)))
            grid.addWidget(input_trav, i + 1, 1)
            self.inputs_travaillees[jour] = input_trav

            input_normales = QLineEdit()
            input_normales.setReadOnly(True)
            grid.addWidget(input_normales, i + 1, 2)
            self.inputs_normales[jour] = input_normales

            input_sup = QLineEdit()
            input_sup.setReadOnly(True)
            grid.addWidget(input_sup, i + 1, 3)
            self.inputs_sup[jour] = input_sup

        layout.addLayout(grid)

        btn_calc_payees = QPushButton("Calcul des heures payées")
        btn_calc_payees.clicked.connect(self.calcul_heures_payees)

        btn_calc_mensuelles = QPushButton("Calcul des heures mensuelles")
        btn_calc_mensuelles.clicked.connect(self.calcul_heures_mensuelles)

        layout.addWidget(btn_calc_payees)
        layout.addWidget(btn_calc_mensuelles)

        self.setLayout(layout)

    def calcul_heures_payees(self):
        session = Session()
        horaires = HorairesTravail()

        heures_travaillees = {}
        try:
            for jour, input_widget in self.inputs_travaillees.items():
                heures_travaillees[jour] = float(input_widget.text() or 0)

            resultat = horaires.calculer_heures(heures_travaillees)

            for jour, valeurs in resultat.items():
                self.inputs_normales[jour].setText(f"{valeurs['normales']:.4f}")
                self.inputs_sup[jour].setText(f"{valeurs['supplementaires']:.4f}")

                entree_db = HorairesEtablissement(
                    jour=jour,
                    heures_travaillees=valeurs['travaillees'],
                    heures_normales=valeurs['normales'],
                    heures_supplementaires=valeurs['supplementaires'],
                    date_creation=datetime.utcnow()
                )
                session.add(entree_db)

            session.commit()

            QMessageBox.information(self, "Succès", "Calcul effectué et sauvegardé en base.")

        except ValueError:
            session.rollback()
            QMessageBox.warning(self, "Erreur", "Veuillez saisir uniquement des chiffres valides.")
        finally:
            session.close()

    def calcul_heures_mensuelles(self):
        horaires = HorairesTravail()
        coeff_mensualisation = horaires.regles["coefficient_mensualisation"]

        heures_travaillees = {}
        total_normales = total_sup = 0

        try:
            for jour, input_widget in self.inputs_travaillees.items():
                heures_travaillees[jour] = float(input_widget.text() or 0)

            resultat = horaires.calculer_heures(heures_travaillees)

            for valeurs in resultat.values():
                total_normales += valeurs['normales']
                total_sup += valeurs['supplementaires']

            normales_mens = round(total_normales * coeff_mensualisation, 2)
            sup_mens = round(total_sup * coeff_mensualisation, 2)

            QMessageBox.information(
                self, "Heures mensualisées",
                f"Heures normales mensualisées : {normales_mens} h\n"
                f"Heures supplémentaires mensualisées : {sup_mens} h"
            )

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir uniquement des chiffres valides.")