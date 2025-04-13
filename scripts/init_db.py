from app.data.database import Session, engine
from app.data.models import Base, SmicHistorique, MajorationHS
from app.core.fiche_societe.regles import charger_regles
from datetime import datetime

Base.metadata.create_all(engine)
session = Session()
regles = charger_regles()

# Ajout SMIC Historique
for smic in regles['taux_horaire_smics']:
    entree_smic = SmicHistorique(
        date_effet=datetime.strptime(smic['date'], '%Y-%m-%d').date(),
        taux=smic['taux']
    )
    session.merge(entree_smic)

# Ajout Majorations HS
for majoration in regles['majorations_heures_sup']:
    seuil = majoration.get("jusqua", majoration.get("au_dela", 999))
    entree_majoration = MajorationHS(
        seuil=seuil,
        taux_majoration=majoration['taux']
    )
    session.merge(entree_majoration)

session.commit()
session.close()

print("✅ Base initialisée avec SMIC et majorations HS.")
