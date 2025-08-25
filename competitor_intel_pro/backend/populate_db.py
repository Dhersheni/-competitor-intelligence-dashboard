import json
from pathlib import Path
from datetime import datetime

from backend.database import Competitor, SessionLocal, init_db
from backend.crud import add_competitor, cleanup_db


# Initialize DB
init_db()
db = SessionLocal()

# Reports directory
reports_dir = Path(__file__).parent.parent / "data" / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)

# Sample competitors
sample_competitors = [
    {
        "name": "Microsoft",
        "website_update": "New AI Copilot features announced",
        "app_update": "Microsoft Teams v2.5 released",
        "social_update": "Excited to push boundaries with AI at work!"
    },
    {
        "name": "Apple",
        "website_update": "iPhone 16 announced",
        "app_update": "App Store UI updated",
        "social_update": "Check out our latest innovations!"
    },
    {
        "name": "NVIDIA",
        "website_update": "RTX 5090 GPUs launch",
        "app_update": "GeForce Now updated",
        "social_update": "Gaming performance redefined!"
    },
]

# Add competitors to DB
for comp in sample_competitors:
    add_competitor(
        db,
        name=comp["name"],
        website_update=comp["website_update"],
        app_update=comp["app_update"],
        social_update=comp["social_update"]
    )

# Cleanup old entries
cleanup_db(db, days_old=30)

# Export DB to JSON
competitors = db.query(Competitor).all()
export_data = {"competitors": []}

for c in competitors:
    export_data["competitors"].append({
        "name": c.name,
        "website_update": c.website_update,
        "app_update": c.app_update,
        "social_update": c.social_update,
        "last_updated": c.last_updated.strftime("%Y-%m-%d %H:%M:%S")
    })

# Save report
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_file = reports_dir / f"report_{timestamp}.json"

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=4)

print(f"✅ DB populated and JSON exported: {json_file}")
