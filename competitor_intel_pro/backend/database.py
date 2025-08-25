from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Competitor(Base):
    __tablename__ = "competitors"

    name = Column(String, primary_key=True)
    website_update = Column(String)
    app_update = Column(String)
    social_update = Column(String)
    last_updated = Column(DateTime, default=datetime.now)

# SQLite database
engine = create_engine("sqlite:///competitors.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
