from bs4 import BeautifulSoup

def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "footer", "nav", "header"]):
        tag.decompose()
    texts = []
    for el in soup.find_all(["h1","h2","h3","h4","p","li"]):
        txt = " ".join(el.get_text(separator=" ", strip=True).split())
        if txt:
            texts.append(txt)
    return "\n".join(texts)