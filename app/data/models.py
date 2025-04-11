from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

Base = declarative_base()

class HorairesEtablissement(Base):
    __tablename__ = 'horaires_etablissement'

    id = Column(Integer, primary_key=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
    jour = Column(String, nullable=False)
    heures_travaillees = Column(Float, nullable=False)
    heures_normales = Column(Float, nullable=False)
    heures_supplementaires = Column(Float, nullable=False)

class ReglesCalcul(Base):
    __tablename__ = 'regles_calcul'

    id = Column(Integer, primary_key=True)
    cle = Column(String, unique=True, nullable=False)
    valeur = Column(Float, nullable=False)
