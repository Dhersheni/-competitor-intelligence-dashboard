import difflib
from typing import List

def unified_diff(old_text: str, new_text: str, context: int = 2) -> str:
    diff = difflib.unified_diff(
        old_text.splitlines(), new_text.splitlines(), lineterm="", n=context
    )
    return "\n".join(diff)

def extract_change_lines(diff_text: str) -> List[str]:
    out = []
    for line in diff_text.splitlines():
        if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
            continue
        if line.startswith('+') or line.startswith('-'):
            out.append(line)
    return out