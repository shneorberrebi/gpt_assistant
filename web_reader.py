# web_reader.py – סורק אתרי אינטרנט ומסכם מידע חשוב לעוזר

import requests
from bs4 import BeautifulSoup

def summarize_website(url, max_items=25):
    """
    📄 מסכם אתר אינטרנט: כותרת, טקסטים עיקריים, כפתורים, שדות, קישורים – בצורה שקל ל־GPT להבין.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
    except Exception as e:
        return f"❌ שגיאה בטעינת האתר: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "אין כותרת"

    def clean(text):
        return text.strip().replace("\n", " ").replace("\r", " ").replace("  ", " ").strip()

    def extract_unique_text(elements, attrs=None):
        seen = set()
        results = []
        for el in elements:
            texts = []
            if attrs:
                for attr in attrs:
                    val = el.get(attr, '')
                    if val:
                        texts.append(val)
            else:
                texts.append(el.get_text())

            for t in texts:
                t = clean(t or "")
                if 2 < len(t) < 140 and t.lower() not in seen:
                    seen.add(t.lower())
                    results.append(t)

        return results[:max_items]

    # חילוץ רכיבים רלוונטיים
    headings = extract_unique_text(soup.find_all(['h1', 'h2', 'h3', 'p', 'strong']))
    buttons = extract_unique_text(soup.find_all('button'))
    inputs = extract_unique_text(soup.find_all('input'), ["placeholder", "name", "id", "aria-label", "title", "value"])
    textareas = extract_unique_text(soup.find_all('textarea'), ["placeholder", "name", "id"])
    links = extract_unique_text(soup.find_all('a'), ["href", "aria-label", "title"])
    labels = extract_unique_text(soup.find_all('label'))

    # הרכבת סיכום קריא ל־GPT
    parts = [f"📄 כותרת העמוד: {title}"]

    if headings:
        parts.append("🧠 טקסטים עיקריים:\n" + "\n".join(f"- {t}" for t in headings))
    if buttons:
        parts.append("🔘 כפתורים:\n" + "\n".join(f"- {b}" for b in buttons))
    if inputs or textareas:
        parts.append("📥 שדות קלט:\n" + "\n".join(f"- {i}" for i in inputs + textareas))
    if links:
        parts.append("🔗 קישורים:\n" + "\n".join(f"- {l}" for l in links))
    if labels:
        parts.append("🏷️ תוויות:\n" + "\n".join(f"- {l}" for l in labels))

    return "\n\n".join(parts).strip()


# בדיקה ישירה
if __name__ == "__main__":
    test_url = "https://www.wix.com/website/templates"
    print(summarize_website(test_url))
