# smart_clicker.py – זיהוי טקסט מהמסך ולחיצה עליו (OCR + fuzzy matching)

import pytesseract
from PIL import Image
import pyautogui
import mss
import time
import re
from fuzzywuzzy import fuzz

# עדכון נתיב ברירת המחדל של Tesseract – ודא שהוא נכון אצלך
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_target_word(command):
    """
    מוציא את המילה הרלוונטית לפעולה מתוך פקודת המשתמש.
    """
    match = re.search(r"(כפתור|טקסט|המילה|על)?\s*(שלח לי|שלח|אישור|הבא|ביטול|[\wא-ת ]{2,})$", command.strip())
    if match:
        return match.group(2).strip()
    return command.strip()

def clean_text(text):
    """
    מנקה טקסט מהפרעות – תווים מיוחדים, רווחים כפולים וכו'.
    """
    return re.sub(r'[^א-תA-Za-z0-9 ]', '', text).strip().lower()

def click_text_on_screen(command, threshold=None, debug=True):
    """
    מאתר ולוחץ על טקסט במסך לפי פקודת המשתמש, גם אם יש טעות קטנה בזיהוי.
    """
    if not command or not command.strip():
        print("⚠️ פקודה ריקה – לא מתבצעת לחיצה.")
        return False

    threshold = threshold or 70
    target_text = extract_target_word(command)
    target_text_clean = clean_text(target_text)

    print(f"\n🎯 מחפש טקסט במסך: '{target_text}'")
    time.sleep(1.2)

    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
    except Exception as e:
        print("❌ שגיאה בצילום המסך:", e)
        return False

    try:
        data = pytesseract.image_to_data(img, lang='eng+heb', output_type=pytesseract.Output.DICT)
    except Exception as e:
        print("❌ שגיאה בהרצת OCR:", e)
        return False

    best_match = None
    best_score = 0
    found_texts = []

    for i in range(len(data['text'])):
        word = data['text'][i].strip()
        if not word or len(word) <= 1:
            continue

        word_clean = clean_text(word)
        score = fuzz.partial_ratio(target_text_clean, word_clean)

        if not isinstance(score, int):
            continue

        found_texts.append((word, score))

        if debug:
            print(f"🔎 '{word}' ⟶ {score}% התאמה ל־'{target_text}'")

        if score > best_score and score >= threshold:
            best_score = score
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            best_match = (x, y)

    if best_match:
        pyautogui.moveTo(best_match[0], best_match[1], duration=0.3)
        pyautogui.click()
        print(f"✅ נלחץ על '{target_text}' במיקום {best_match} (דיוק: {best_score}%)")
        return True
    else:
        print(f"❌ לא נמצא טקסט תואם: '{target_text}'")
        if debug:
            print("📋 טקסטים דומים במסך (TOP 10):")
            for word, score in sorted(found_texts, key=lambda x: x[1], reverse=True)[:10]:
                print(f"- {word} ({score}%)")
        return False
