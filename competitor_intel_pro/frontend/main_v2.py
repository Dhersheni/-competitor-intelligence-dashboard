import os, yaml
from utils import url_to_key, ensure_dir, ts
from renderer import render_page
from parser import extract_text_from_html
from diff_tools import unified_diff, extract_change_lines
from summarizer import ai_summary
from visual_diff import image_diff_score
from classifier import classify_change_lines
from storage import init_db, get_or_create_page, last_snapshot_for, insert_snapshot, insert_change
from notifier import save_report, post_to_slack

def load_config(path: str = "config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run():
    cfg = load_config()
    ensure_dir("data/snapshots")
    ensure_dir("data/screens")
    ensure_dir("data/reports")
    init_db()

    report_sections = []
    any_changes = False
    for t in cfg.get("targets", []):
        name = t["name"]; url = t["url"]
        css_wait = t.get("css_wait")
        full_page = bool(cfg.get("screenshot_full_page", True))

        print(f"[*] Rendering: {name} ({url})")
        html_path, png_path = render_page(url, "data/snapshots", "data/screens", css_wait=css_wait, full_page=full_page)
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        text = extract_text_from_html(html)

        # store current snapshot
        page_id = get_or_create_page(name, url)
        snapshot_id = insert_snapshot(page_id, ts(), html_path.replace('data/',''), html_path.replace('data/',''), png_path.replace('data/',''))

        # compare to last snapshot (visual only)
        last = last_snapshot_for(page_id)
        visual_info = ""
        visual_score = 0.0
        diff_img_path_rel = None
        if last and last[2] and os.path.exists("data/" + last[2]):
            prev_png = "data/" + last[2]
            score, diff_img = image_diff_score(prev_png, png_path)
            visual_score = float(score)
            diff_img_path = f"data/screens/diff_{url_to_key(url)}.png"
            diff_img.save(diff_img_path)
            diff_img_path_rel = diff_img_path.replace('data/','')
            visual_info = f"Visual change score: {visual_score:.2f} (higher = more change)."
        else:
            visual_info = "First snapshot captured; no previous image to compare."

        # textual diff vs. previous text file (if any)
        # We read the immediate previous snapshot's HTML file (if exists) and diff text content.
        # For simplicity, we use the last snapshot's HTML path if it's not this snapshot.
        old_text = ""
        if last and last[1]:  # last ts exists; try opening the previous html path via DB lookup is skipped for brevity
            # naive: try a sibling snapshot with same page_id but previous id (already last)
            pass

        # Use stored snapshots directory to find a previous text content file for same URL key
        # (MVP: just skip if not present; first diff only from second run)
        # Compute diff if there's a previous text file with same name
        text_file = html_path.replace(".html", ".txt")
        with open(text_file, "w", encoding="utf-8") as tf:
            tf.write(text)

        prev_text_path = text_file + ".prev"
        if os.path.exists(prev_text_path):
            with open(prev_text_path, "r", encoding="utf-8") as pf:
                old_text = pf.read()

        diff = unified_diff(old_text, text, context=int(cfg.get("diff_context", 2)))
        change_lines = extract_change_lines(diff)

        # Summaries
        summary = ai_summary(change_lines)
        buckets = classify_change_lines(change_lines)

        # Persist change entry
        insert_change(page_id, ts(), diff, summary, visual_score, diff_img_path_rel or "")

        # Rotate prev pointer
        if os.path.exists(text_file):
            os.replace(text_file, prev_text_path)

        if change_lines or visual_score > 1.0:
            any_changes = True
            section = [f"### {name}", summary, visual_info]
            report_sections.append("\n".join(section) + "\n")
        else:
            report_sections.append(f"### {name}\nNo substantial changes detected.\n" + visual_info + "\n")

    # Final report
    header = "# Competitor Intelligence Report\n" + f"Generated: {ts()}\n\n"
    final_report = header + "\n".join(report_sections)
    path = save_report(final_report)
    print(f"[+] Report saved: {path}")
    status = post_to_slack(final_report)
    if status:
        print(f"[+] Slack post status: {status}")
    else:
        print("[i] Slack not configured.")

    if not any_changes:
        print("[i] No notable changes this run.")

if __name__ == "__main__":
    run()