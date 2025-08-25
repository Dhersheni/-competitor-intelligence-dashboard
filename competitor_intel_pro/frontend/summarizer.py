import os
from typing import List, Dict

def format_buckets(buckets: Dict[str, List[str]]) -> str:
    out = []
    for k, items in buckets.items():
        if not items: 
            continue
        out.append(f"{k}:")
        out.extend([f"- {it}" for it in items[:10]])
        if len(items) > 10:
            out.append(f"... (+{len(items)-10} more)")
        out.append("")
    return "\n".join(out).strip()

def fallback_summary(change_lines: List[str]) -> str:
    if not change_lines:
        return "No significant textual changes detected."
    # Group into buckets using basic rules
    from classifier import classify_change_lines
    buckets = classify_change_lines(change_lines)
    return format_buckets(buckets)

def ai_summary(change_lines: List[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return fallback_summary(change_lines)
    try:
        import openai
        openai.api_key = api_key
        change_blob = "\n".join(change_lines[:800])
        prompt = (
            "You are a senior product analyst. Read the added/removed lines from a website diff and "
            "produce a crisp executive summary grouped under: New Features, Pricing Changes, UI/UX, "
            "Bug Fixes/Performance, Other. Keep it short, factual, deduplicated, and avoid noise.\n\n"
            f"DIFF LINES:\n{change_blob}"
        )
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content": prompt}],
            temperature=0.2
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception:
        return fallback_summary(change_lines)