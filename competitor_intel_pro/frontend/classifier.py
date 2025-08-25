from typing import List, Dict

KEYWORDS = {
    "pricing": ["price", "pricing", "billed", "cost", "plan", "subscription", "per month", "per user"],
    "feature": ["new", "introduce", "launch", "support", "integration", "beta", "general availability", "ga", "feature"],
    "bugfix": ["fix", "resolved", "issue", "stability", "performance", "improve", "optimize"],
    "ui": ["ui", "design", "interface", "layout", "navigation", "button", "color", "theme", "ux"],
}

def classify_change_lines(lines: List[str]) -> Dict[str, List[str]]:
    buckets = {"Pricing Changes":[], "New Features":[], "Bug Fixes/Performance":[], "UI/UX":[], "Other":[]}
    for l in lines:
        raw = l[1:].lower()
        placed = False
        if any(k in raw for k in KEYWORDS["pricing"]):
            buckets["Pricing Changes"].append(l[1:].strip()); placed=True
        if any(k in raw for k in KEYWORDS["feature"]):
            buckets["New Features"].append(l[1:].strip()); placed=True
        if any(k in raw for k in KEYWORDS["bugfix"]):
            buckets["Bug Fixes/Performance"].append(l[1:].strip()); placed=True
        if any(k in raw for k in KEYWORDS["ui"]):
            buckets["UI/UX"].append(l[1:].strip()); placed=True
        if not placed:
            buckets["Other"].append(l[1:].strip())
    # dedupe
    for k in buckets:
        buckets[k] = list(dict.fromkeys(buckets[k]))
    return buckets