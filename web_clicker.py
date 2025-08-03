# web_clicker.py – לחיצה חכמה על כפתורים מתוך HTML של אתר

import requests
from bs4 import BeautifulSoup
import time
from fuzzywuzzy import fuzz

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

# 🔑 מילות מפתח רלוונטיות ללחיצה (עברית + אנגלית)
CLICK_KEYWORDS = [
    "get started", "start", "create", "sign up", "register", "join", "open",
    "start now", "begin", "start for free", "try it", "try for free", "continue", "go",
    "בחר", "התחל", "צור", "צור חשבון", "הירשם", "התחל עכשיו", "התחל בחינם",
    "נסה", "נסה בחינם", "המשך", "קדימה", "לפתיחה", "ליצירה", "הפעל",
    "כניסה", "כניסת משתמש", "הרשמה", "הירשם עכשיו", "להתחיל", "כניסה לחשבון"
]

def extract_all_text_candidates(soup):
    """
    🔍 שולף טקסטים פוטנציאליים ללחיצה מתוך תגיות באתר.
    כולל aria-label, placeholder, alt, title, value ועוד.
    """
    tags = ["a", "button", "input", "label", "div", "span"]
    candidates = set()

    for el in soup.find_all(tags):
        texts = [
            el.get_text(strip=True),
            el.get("aria-label", ""),
            el.get("alt", ""),
            el.get("title", ""),
            el.get("placeholder", ""),
            el.get("value", "") if el.name == "input" else ""
        ]
        for t in texts:
            t = t.strip()
            if 2 < len(t) < 80 and t.lower() not in ["submit", "click here"]:
                candidates.add(t)

    return list(candidates)

def click_button_on_page(url, keywords=None, match_threshold=80):
    """
    🧠 מנסה לאתר כפתור לפי טקסט באתר ולבצע עליו לחיצה אוטומטית באמצעות Ctrl+F + Enter.
    """
    if keywords is None:
        keywords = CLICK_KEYWORDS

    print(f"🌍 טוען את האתר: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
    except Exception as e:
        return f"❌ שגיאה בטעינת הדף: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    candidates = extract_all_text_candidates(soup)
    print(f"🔍 נמצאו {len(candidates)} טקסטים פוטנציאליים ללחיצה")

    best_text, best_score, best_keyword = "", 0, ""

    for keyword in keywords:
        for text in candidates:
            score = fuzz.token_sort_ratio(keyword.lower(), text.lower())
            if score > best_score and score >= match_threshold:
                best_score = score
                best_text = text
                best_keyword = keyword

    if best_text:
        print(f"✅ טקסט תואם: '{best_text}' (התאמה ל־'{best_keyword}' – {best_score}%)")

        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.hotkey("ctrl", "f")
                time.sleep(0.4)
                pyautogui.typewrite(best_text[:50])
                time.sleep(0.6)
                pyautogui.press("esc")   # לסגור Ctrl+F
                time.sleep(0.3)
                pyautogui.press("enter") # ניסיון לחיצה
                return f"✅ בוצעה לחיצה על '{best_text}'"
            except Exception as e:
                return f"❌ שגיאה ב־pyautogui: {e}"
        else:
            return f"🔎 נמצא טקסט תואם: '{best_text}' (ללא ביצוע – pyautogui לא מותקן)"

    return "❌ לא נמצא כפתור מתאים 😞"
