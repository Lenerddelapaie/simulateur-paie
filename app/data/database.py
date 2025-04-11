from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

DATABASE_URL = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'paie.db')}"

engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
