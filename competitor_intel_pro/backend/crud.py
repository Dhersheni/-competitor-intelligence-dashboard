from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .database import Competitor

def add_competitor(db: Session, name, website_update, app_update, social_update):
    existing = db.query(Competitor).filter(Competitor.name == name).first()
    if existing:
        existing.website_update = website_update
        existing.app_update = app_update
        existing.social_update = social_update
        existing.last_updated = datetime.now()
    else:
        comp = Competitor(
            name=name,
            website_update=website_update,
            app_update=app_update,
            social_update=social_update,
            last_updated=datetime.now()
        )
        db.add(comp)
    db.commit()

def cleanup_db(db: Session, days_old=30):
    cutoff = datetime.now() - timedelta(days=days_old)
    old_entries = db.query(Competitor).filter(Competitor.last_updated < cutoff).all()
    for entry in old_entries:
        db.delete(entry)
    db.commit()
