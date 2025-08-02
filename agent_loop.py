# agent_loop.py – גרסה משודרגת: אינטליגנציה אמיתית

import time
from gpt_client import ask_gpt
from gpt_action_executor import execute_plan
from screen_context_filter import summarize_screen_for_gpt
from personal_info import load_personal_info
from brain import process_command

def run_loop(user_goal, max_steps=10):
    print("\n🎯 התחלת משימה:", user_goal)

    personal_info = load_personal_info()

    for step in range(max_steps):
        print(f"\n🔁 שלב {step+1} מתוך {max_steps}")

        try:
            # 🧠 שלב 1: ניתוח כוונת המשתמש
            context_prompt = f"""
אתה עוזר אישי חכם שמקבל בקשה ממשתמש:
"{user_goal}"

🔍 מה צריך לעשות כדי למלא את הבקשה הזו?

תענה רק בשלבים קצרים:
- אם צריך לברר משהו בגוגל – תגיד "חפש בגוגל על X"
- אם צריך לפתוח אתר מסוים – תגיד "פתח אתר X"
- אם צריך ללחוץ על כפתור – תגיד "חפש במסך ולחץ על Y"
- אם צריך למלא טופס – תגיד "מלא את שדה X עם Y"

אל תסביר – רק תחזיר תוכנית פעולה מדויקת לביצוע.
"""
            reasoning = ask_gpt(context_prompt, personal_info=personal_info)
            print("\n🤖 ניתוח משימה:\n", reasoning)

            # 🖥️ שלב 2: קבלת הקשר מהמסך
            screen_summary = summarize_screen_for_gpt()

            if not screen_summary or "לא זוהה" in screen_summary:
                print("⚠️ אין טקסטים רלוונטיים במסך. ממתין...")
                time.sleep(3)
                continue

            # 🛠️ שלב 3: בקשת תוכנית פעולה עם הבנה של מה שקורה במסך
            plan = ask_gpt(
                prompt=reasoning,
                context=screen_summary,
                personal_info=personal_info
            )

            print("\n📋 תוכנית לביצוע:\n", plan)

            # 🚀 שלב 4: ביצוע בפועל
            execute_plan(plan)
            time.sleep(2)

        except Exception as e:
            print(f"❌ שגיאה בשלב {step+1}: {e}")
            break

    print("\n✅ סיום הלולאה")


def run_agent(user_input):
    """
    🧠 מזהה אם צריך לולאה (משימה מורכבת) או פקודה פשוטה למסך הנוכחי
    """
    complex_keywords = ["תתחיל", "תעבור שלב", "תריץ לולאה", "שלבים", "תבצע את זה לבד", "תמצא", "תבדוק", "תעשה את כל", "תמצא לי", "תכתוב אפליקציה", "תתחיל פרויקט"]
    if any(kw in user_input.lower() for kw in complex_keywords):
        run_loop(user_input)
    else:
        process_command(user_input)
