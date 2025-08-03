# web_browser_analyzer.py – סורק דף ומדפיס כפתורים, קישורים ושדות לזיהוי חכם

import requests
from bs4 import BeautifulSoup

def fetch_and_analyze_page(url, max_items=25):
    """
    טוען דף אינטרנט ומחזיר רשימת טקסטים של כפתורים, קישורים ושדות קלט.
    שימושי לזיהוי והבנה חכמה של הדף.
    """
    try:
        print(f"🔗 טוען את הדף: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        return [f"❌ שגיאה בטעינת הדף: {e}"]

    elements = soup.find_all(['button', 'a', 'input', 'label', 'span', 'div'])

    found = set()
    results = []

    for el in elements:
        texts = [
            el.get_text(strip=True),
            el.get("value", ""),
            el.get("aria-label", ""),
            el.get("title", ""),
            el.get("placeholder", "")
        ]

        for text in texts:
            text = text.strip()
            if 2 < len(text) < 60 and text not in found:
                found.add(text)
                results.append(text)
                if len(results) >= max_items:
                    break

    print("🧠 פריטים שזוהו בדף:")
    for i, item in enumerate(results, 1):
        print(f"{i}. {item}")

    return results

# בדיקה עצמאית
if __name__ == "__main__":
    url = "https://www.wix.com/website/templates"
    fetch_and_analyze_page(url)
