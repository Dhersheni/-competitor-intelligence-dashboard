import os, re, hashlib
from datetime import datetime

def url_to_key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_filename(name: str) -> str:
    name = re.sub(r'[^A-Za-z0-9_\-\.]+', '_', name).strip('_')
    return name[:96] or "file"