from playwright.sync_api import sync_playwright
from utils import ensure_dir, safe_filename
import os, time

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

def render_page(url: str, out_dir_html: str, out_dir_png: str, css_wait: str = None, full_page: bool = True):
    ensure_dir(out_dir_html)
    ensure_dir(out_dir_png)
    png_path = None
    html_path = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=DEFAULT_UA, viewport={"width":1280, "height":2000})
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        if css_wait:
            try:
                page.wait_for_selector(css_wait, timeout=15000)
            except Exception:
                pass
        # small settle
        time.sleep(1.2)
        # HTML
        html = page.content()
        fname = safe_filename(url) + ".html"
        html_path = os.path.join(out_dir_html, fname)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        # Screenshot
        png_name = safe_filename(url) + ".png"
        png_path = os.path.join(out_dir_png, png_name)
        page.screenshot(path=png_path, full_page=full_page)
        context.close()
        browser.close()

    return html_path, png_path