
from pathlib import Path
from database import SessionLocal, init_db, Competitor
import json
from datetime import datetime

# Initialize DB
init_db()
db = SessionLocal()

# Fetch all competitors
competitors = db.query(Competitor).all()

# Convert to dict
data = {
    "competitors": [
        {
            "name": c.name,
            "website_update": c.website_update,
            "app_update": c.app_update,
            "social_update": c.social_update,
            "last_updated": c.last_updated.strftime("%Y-%m-%d %H:%M:%S") if c.last_updated else None
        }
        for c in competitors
    ]
}

# Use absolute path to project data/reports folder
project_root = Path(__file__).parent.parent.resolve()  # go up one folder from backend/
reports_folder = project_root / "data" / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)

# Save JSON
filename = reports_folder / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"✅ JSON report saved to {filename}")
