from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class HorairesEtablissement(Base):
    __tablename__ = 'horaires_etablissement'
    id = Column(Integer, primary_key=True)
    jour = Column(String, nullable=False)
    heures = Column(Float, nullable=False)

class ReglesCalcul(Base):
    __tablename__ = 'regles_calcul'
    id = Column(Integer, primary_key=True)
    cle = Column(String, unique=True, nullable=False)
    valeur = Column(Float, nullable=False)
