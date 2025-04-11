import json
import os

def charger_regles():
    chemin = os.path.join(os.path.dirname(__file__), '../../config/regles.json')
    with open(chemin, 'r') as fichier:
        return json.load(fichier)
