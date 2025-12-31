import re
import json
from typing import Dict, Any, Optional

def strip_markdown_fences(text: Optional[str]) -> str:
    t = (text or "").strip()
    t = re.sub(r"^```json\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^```\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()

def safe_json_loads(text: Optional[str]) -> Dict[str, Any]:
    cleaned = strip_markdown_fences(text)
    return json.loads(cleaned)

def month_key_from_iso(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return date_str[:7]
    return None