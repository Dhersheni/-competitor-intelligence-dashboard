from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    website_update = Column(String)
    app_update = Column(String)
    social_update = Column(String)
    last_updated = Column(DateTime, default=datetime.datetime.now)
