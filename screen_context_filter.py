# screen_context_filter.py – זיהוי טקסטים מהמסך + סיכום חכם ל־GPT

import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab

# צילום מסך רגיל
def take_screenshot():
    image = ImageGrab.grab()
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# זיהוי טקסטים עם מיקומים
def extract_texts_with_positions(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        data = pytesseract.image_to_data(gray, lang="eng+heb", output_type=pytesseract.Output.DICT)

        results = []
        for i in range(len(data["text"])):
            text = data["text"][i]
            if text and text.strip():
                x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
                results.append({
                    "text": text.strip(),
                    "position": (x + w // 2, y + h // 2)
                })
        return results
    except Exception as e:
        print(f"❌ שגיאה ב־extract_texts_with_positions: {e}")
        return []

# זיהוי טקסט פשוט בלי מיקומים
def extract_text_from_image(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang="eng+heb")
        return text
    except Exception as e:
        print(f"❌ שגיאה ב־extract_text_from_image: {e}")
        return ""

# ✅ פונקציית סיכום למסך – עבור GPT
def summarize_screen_for_gpt(texts):
    """
    מקבל רשימת טקסטים עם מיקומים ומחזיר סיכום שמתאר את מה שנראה על המסך.
    """
    if not texts:
        return "לא זוהו טקסטים על המסך."

    visible_items = [t["text"] for t in texts if t.get("text")]
    limited_items = visible_items[:30]  # לא נשלח יותר מדי
    summary = "המסך כרגע כולל את הטקסטים הבאים:\n- " + "\n- ".join(limited_items)
    return summary
def get_video_editing_prompt(file_info, user_notes=""):
    """
    ⚙️ יוצר פרומפט חכם לעריכת וידאו לפי שם הקובץ, תוכן ידוע, והערות משתמש.
    """
    video_name = file_info.get("name", "הסרטון")
    source = file_info.get("source", "מקור לא ידוע")
    sender = file_info.get("sender", "לקוח")
    insights = file_info.get("insights", "")

    prompt = f"""
אתה עורך וידאו מקצועי שמבין בשיווק, קצב, טרנדים ויצירת תוכן ויראלי.
ערוך את הסרטון בשם "{video_name}" בצורה כזו:
- פתח ב'הוק' חזק שיגרום לאנשים להישאר
- חתוך קטעים איטיים או מיותרים
- הוסף כתוביות צבעוניות (עדיף בעברית) בסגנון טיקטוק
- שמור על קצב מהיר, מעברים חדים
- אם נאמרו דברים חשובים – הדגש אותם בטקסט או בזום
- אם הסרטון נשלח מ־{source} על ידי {sender}, התחשב בכך
- {f"💡 תובנות מהסרטון: {insights}" if insights else ""}
- {f"📝 הערות משתמש: {user_notes}" if user_notes else ""}
החזר רק את שלבי העריכה או תיאור מדויק של מה לעשות. אל תענה הסברים.
""".strip()

    return prompt
