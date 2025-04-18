from .regles import charger_regles

class HorairesTravail:
    def __init__(self):
        self.regles = charger_regles()  # stocker les règles ici clairement
        self.duree_legale = self.regles["duree_legale_travail"]
        self.repartition_defaut = self.regles["repartition_heures_par_defaut"]

    def calculer_heures(self, heures_travaillees):
        total_semaine = sum(heures_travaillees.values())
        resultat = {}

        if total_semaine <= self.duree_legale:
            for jour, heures in heures_travaillees.items():
                resultat[jour] = {
                    "travaillees": heures,
                    "normales": heures,
                    "supplementaires": 0
                }
        else:
            for jour, heures in heures_travaillees.items():
                normales = heures * self.duree_legale / total_semaine
                supplementaires = heures - normales
                resultat[jour] = {
                    "travaillees": heures,
                    "normales": round(normales, 4),
                    "supplementaires": round(supplementaires, 4)
                }

        return resultat
