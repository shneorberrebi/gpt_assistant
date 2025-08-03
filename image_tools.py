# image_tools.py – OCR חכם + סינון חוסך טוקנים

import pytesseract
from PIL import Image
import mss
import re

# 📍 נתיב ל־Tesseract OCR – תוודא שזה נכון אצלך
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🧠 מילות מפתח שכנראה מצביעות על טקסטים חשובים
IMPORTANT_KEYWORDS = [
    "הירשם", "הרשמה", "התחבר", "שלח", "שמור", "הבא", "המשך",
    "הקלד", "שם", "מייל", "דוא\"ל", "סיסמה",
    "login", "sign", "submit", "email", "password", "name", "next", "continue"
]

def take_screenshot():
    """
    מצלם את המסך המלא ומחזיר את האובייקט PIL Image.
    """
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img

def read_text_from_image(image=None):
    """
    קורא טקסט מתוך תמונה עם OCR. אם לא קיבל תמונה – יצלם בעצמו.
    """
    if image is None:
        image = take_screenshot()
    return pytesseract.image_to_string(image, lang='eng+heb')

def summarize_screen_for_gpt():
    """
    חכם: מחלץ טקסטים חשובים בלבד מתוך צילום מסך.
    אם אין שום טקסט חשוב – מחזיר ריק.
    """
    image = take_screenshot()
    raw_text = pytesseract.image_to_string(image, lang='eng+heb')
    lines = raw_text.split('\n')

    important_lines = []
    for line in lines:
        clean = line.strip()
        if len(clean) < 2:
            continue

        # שמור אם יש מילת מפתח
        if any(keyword.lower() in clean.lower() for keyword in IMPORTANT_KEYWORDS):
            important_lines.append(clean)
            continue

        # שמור אם זה משפט עם 3 מילים לפחות
        if len(re.findall(r'\w+', clean)) >= 3:
            important_lines.append(clean)

    summary = '\n'.join(important_lines).strip()
    if not summary:
        print("🧠 לא נמצא טקסט רלוונטי לשליחה ל-GPT")
    else:
        print("🧠 סיכום מסך חכם עבור GPT:\n", summary)
    return summary
