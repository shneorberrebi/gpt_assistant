# simple_assistant.py – עוזר מבצע פקודות בסיסיות דרך GPT

import pyautogui
import time
from openai import OpenAI

# 🛡️ שמור את המפתח כמשתנה סביבה או בקובץ נפרד אם תפרסם את הקוד
client = OpenAI(
    api_key="sk-proj-..."  # מומלץ להסתיר
)

def execute_command(command):
    try:
        if command.startswith("move:"):
            x, y = map(int, command.split(":")[1].split(","))
            pyautogui.moveTo(x, y, duration=0.5)
            print(f"✅ הזזנו את העכבר ל- X={x}, Y={y}")
        elif command == "click":
            pyautogui.click()
            print("🖱️ בוצע קליק")
        elif command.startswith("type:"):
            text = command.split(":", 1)[1]
            pyautogui.typewrite(text)
            print(f"⌨️ נכתב: {text}")
        else:
            print("❌ פקודה לא מוכרת:", command)
    except Exception as e:
        print(f"❌ שגיאה בביצוע הפקודה: {e}")

# 🔁 לולאה שמקבלת פקודה מהמשתמש -> GPT -> פעולה
while True:
    user_input = input("מה אתה רוצה שהעוזר יעשה? (או 'exit' כדי לצאת):\n")
    if user_input.lower() in ["exit", "יציאה"]:
        break

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "אתה עוזר אוטומציה. "
                        "אם המשתמש מבקש פעולה (כמו 'תלחץ על הכפתור', או 'תקליד היי'), "
                        "המר את זה לפקודה אחת מתוך: move:X,Y | click | type:טקסט. "
                        "תחזיר רק את הפקודה – בלי הסברים, בלי סימנים מיותרים."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        )
        command = response.choices[0].message.content.strip()
        print("🤖 פקודה שהתקבלה:", command)
        execute_command(command)

    except Exception as e:
        print("❌ שגיאה בתקשורת עם GPT:", e)
