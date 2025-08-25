import os, datetime, requests
from typing import Optional

def save_report(text: str, out_dir: str = "data/reports") -> str:
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    path = os.path.join(out_dir, f"REPORT-{ts}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

def post_to_slack(text: str) -> Optional[int]:
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        return None
    try:
        resp = requests.post(webhook, json={"text": text}, timeout=15)
        return resp.status_code
    except Exception:
        return None