import re
from gpt_client import ask_gpt

KNOWN_SITES = {
    "קנבה": "https://www.canva.com",
    "canva": "https://www.canva.com",
    "ויקס": "https://www.wix.com",
    "wix": "https://www.wix.com",
    "durable": "https://www.durable.co",
    "דאראבל": "https://www.durable.co",
    "mailchimp": "https://www.mailchimp.com",
    "notion": "https://www.notion.so",
    "google": "https://www.google.com",
    "טיקטוק": "https://www.tiktok.com",
    "facebook": "https://www.facebook.com",
    "youtube": "https://www.youtube.com",
    "יוטיוב": "https://www.youtube.com"
}

def complete_url_if_needed(plan: str) -> str:
    """
    מזהה שורות כמו 'פתח את קנבה', ומשלים אותן ל-'פתח את https://www.canva.com'.
    אם האתר לא ברשימה – שואל את GPT.
    """
    lines = plan.splitlines()
    new_lines = []

    for line in lines:
        line_lower = line.lower()
        if "פתח" in line_lower or "כנס" in line_lower or "תתחיל" in line_lower:
            if "http" in line_lower:
                new_lines.append(line)
                continue

            matched = False
            for name, url in KNOWN_SITES.items():
                if name.lower() in line_lower:
                    line = re.sub(r"(פתח|כנס|התחל).*?" + re.escape(name), rf"פתח את {url}", line, flags=re.IGNORECASE)
                    matched = True
                    break

            if not matched:
                site_name = extract_site_name(line)
                if site_name:
                    gpt_url = ask_gpt(f"תן לי URL מדויק לאתר בשם '{site_name}'. רק כתובת מלאה כמו https://www... ללא הסברים.")
                    if gpt_url and "http" in gpt_url:
                        line = f"פתח את {gpt_url}"

        new_lines.append(line)

    return "\n".join(new_lines)


def extract_site_name(line: str) -> str:
    """
    מנסה לחלץ את שם האתר מתוך השורה.
    דוגמה: 'תתחיל עם אתר מיילצ'ימפ' -> mailchimp
    """
    words = line.replace("אתר", "").replace("האתר", "").replace("של", "").replace("עם", "").split()
    for word in reversed(words):
        clean = re.sub(r"[^\wא-ת]", "", word)
        if len(clean) > 3:
            return clean
    return ""
