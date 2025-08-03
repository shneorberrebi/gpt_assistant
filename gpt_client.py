# gpt_client.py – שליחה חכמה ל-GPT עם פרומפטים לפי הקשר

import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# 📋 פרומפט כללי למשימות מחשב
DEFAULT_SYSTEM_MESSAGE = """
אתה עוזר אינטליגנטי שפועל בתוך מחשב. כל פעולה שלך מבוצעת בפועל על המסך.
המטרה: לבצע משימות בצורה אוטונומית – בלי לדבר, בלי להסביר.

📌 פורמט:
- כל שורה היא פעולה אחת בלבד.
- דוגמאות: פתח אתר..., לחץ על..., הקלד את..., צלם מסך, קרא מהמסך, המתן עד שתופיע המילה...

🛑 אל תסביר. אל תשאל שאלות. החזר רק שורות פעולה לביצוע.
"""

# 🎬 פרומפט לעריכת וידאו
VIDEO_SYSTEM_MESSAGE = """
אתה עורך וידאו מקצועי שפועל לבד במחשב.
המטרה: לערוך סרטון ברמה גבוהה עם קצב מהיר, הוק חזק, כתוביות ויראליות, ומוזיקה סוחפת.

📌 פורמט:
- כל שורה היא פעולה כמו: פתח את CapCut, חתוך קטעים שקטים, הדגש את ההוק, הוסף כתוביות, פתח captions.ai, שמור סרטון...

🛑 אל תסביר. אל תשאל שאלות. החזר רק שורות פעולה.
"""

def ask_gpt(prompt, context="", personal_info=None, is_video_task=False, model="gpt-4o"):
    """
    שולח פקודה ל־GPT ומחזיר רק שורות פעולה לביצוע.
    """
    system_message = VIDEO_SYSTEM_MESSAGE if is_video_task else DEFAULT_SYSTEM_MESSAGE
    context_block = f"\n\n📺 תוכן המסך:\n{context.strip()}" if context else ""
    info_block = "\n\n🧾 פרטים אישיים:\n" + "\n".join(f"{k}: {v}" for k, v in personal_info.items()) if personal_info else ""

    full_prompt = prompt.strip() + context_block + info_block
    print("📤 שולח ל־GPT:\n", full_prompt[:300])

    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                api_key=API_KEY,
                messages=[
                    {"role": "system", "content": system_message.strip()},
                    {"role": "user", "content": full_prompt.strip()}
                ],
                temperature=0.2,
                max_tokens=1000,
            )

            reply = response.choices[0].message.content.strip()
            print("📥 תשובת GPT:\n", reply)

            # ✅ סינון שורות פעולה בלבד
            valid_prefixes = [
                "פתח", "כנס", "היכנס", "התחל", "טען",
                "לחץ", "הקלד", "העתק", "הדבק",
                "צלם", "קרא", "המתן", "שמור", "ערוך", "סגור"
            ]

            valid_lines = []
            for line in reply.split("\n"):
                line = line.strip("-–•➤> ").strip()
                if any(line.startswith(p) for p in valid_prefixes) and len(line.split()) > 1:
                    valid_lines.append(line)

            result = "\n".join(valid_lines).strip()
            if not result:
                print("⚠️ אין שורות פעולה תקפות.")
            return result

        except Exception as e:
            print(f"❌ ניסיון {attempt + 1} נכשל: {e}")
            time.sleep(1.5)

    print("⛔ לא התקבלה תשובה לאחר 3 ניסיונות.")
    return ""
