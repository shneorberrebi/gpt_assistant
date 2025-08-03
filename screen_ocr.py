# screen_ocr.py – OCR מדויק עם מיקום + ניקוי קבצים זמניים

from PIL import Image
import pytesseract
from mss import mss
import uuid
import os

# 🔧 נתיב ל־Tesseract – עדכן אם דרוש
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def take_screenshot_and_save(folder="screenshots"):
    """
    📸 מצלם את המסך ושומר לקובץ זמני בתיקייה.
    מחזיר את הנתיב לקובץ התמונה.
    """
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"screenshot_{uuid.uuid4().hex}.png")

    try:
        with mss() as sct:
            sct.shot(output=file_path)
        print(f"📸 צילום מסך נשמר: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ שגיאה בצילום מסך: {e}")
        return None

def extract_text_from_image(image_path, delete_after=True, debug=False):
    """
    🧠 OCR רגיל – מחזיר את כל הטקסט מהתמונה כטקסט אחד.
    """
    if not image_path or not os.path.exists(image_path):
        print("⚠️ אין קובץ תמונה לקריאה.")
        return ""

    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng+heb')
        cleaned = text.strip()
        if debug:
            print("📄 טקסט שזוהה:\n", cleaned or "[ללא טקסט]")
        return cleaned
    except Exception as e:
        print(f"❌ שגיאה בקריאת טקסט: {e}")
        return ""
    finally:
        if delete_after:
            safe_delete(image_path)

def extract_texts_with_positions(image_path, delete_after=True, debug=False):
    """
    🎯 OCR עם מיקום – מחזיר רשימת מילים עם קואורדינטות (x, y).
    מתאים לזיהוי ולחיצה חכמה על טקסטים במסך.
    """
    results = []

    if not image_path or not os.path.exists(image_path):
        print("⚠️ אין קובץ תמונה לניתוח.")
        return results

    try:
        image = Image.open(image_path)
        data = pytesseract.image_to_data(image, lang='eng+heb', output_type=pytesseract.Output.DICT)

        seen = set()
        for i in range(len(data['text'])):
            word = data['text'][i].strip()
            x = data['left'][i]
            y = data['top'][i]

            if not word or len(word) <= 1:
                continue
            if word in "|-–—=+*/><[].,{}()":
                continue

            key = (word.lower(), x, y)
            if key not in seen:
                results.append({'text': word, 'x': x, 'y': y})
                seen.add(key)

        if debug:
            print(f"🔍 זוהו {len(results)} מילים עם מיקום.")
        return results
    except Exception as e:
        print(f"❌ שגיאה ב־OCR עם מיקום: {e}")
        return []
    finally:
        if delete_after:
            safe_delete(image_path)

def safe_delete(path):
    """
    🧹 מוחק קובץ אם קיים, בשקט.
    """
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"⚠️ לא הצלחתי למחוק את הקובץ: {e}")
