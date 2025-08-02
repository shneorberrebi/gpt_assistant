# action_center.py – עיבוד פקודות חכם כולל GPT, חיפוש, לחיצות ודפי נחיתה

import os
import subprocess
import json
import re
import asyncio

from web_browser_utils import perform_web_search
from web_reader import summarize_website
from website_generator import generate_landing_page
from web_browser_agent import browse_and_read
from gpt_client import ask_gpt
from screen_context_filter import summarize_screen_for_gpt
from gpt_action_executor import execute_gpt_plan

DATA_FILE = "user_data.json"

# טעינת פרטי משתמש
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# הרצת טסק אסינכרוני בצורה בטוחה
def run_async_task(task):
    try:
        asyncio.run(task)
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(task)

# עיבוד פקודה כללית
def handle_command(text):
    print(f"\n📥 קלט התקבל:\n{text}\n")
    data = load_data()

    # החלפת טקסטים אישיים
    replacements = {
        "האימייל שלי": data.get("email", ""),
        "הסיסמה שלי": data.get("password", ""),
        "הטלפון שלי": data.get("phone", ""),
        "השם שלי": data.get("name", ""),
        "שם המשפחה שלי": data.get("last_name", "")
    }
    for key, val in replacements.items():
        if val:
            text = text.replace(key, val)

    # 🖱️ לחיצה על כפתור
    if any(word in text for word in ["click", "תלחץ על", "לחץ על", "תלחצי על", "לחצי על"]):
        match = re.search(r"(click|תלחץ על|לחץ על|תלחצי על|לחצי על)?\s*(כפתור\s*)?(.*)", text.strip(), re.IGNORECASE)
        if match:
            target = match.group(3).strip()
            print(f"🖱️ מנסה ללחוץ על: {target}")
            try:
                subprocess.run(["python", "smart_clicker.py", target], shell=True)
                return f"מנסה ללחוץ על: {target}"
            except Exception as e:
                return f"שגיאה בהרצת smart_clicker.py: {e}"

    # 🔎 חיפוש בגוגל
    if "תחפש בגוגל" in text or "תמצא לי" in text:
        query = text.replace("תחפש בגוגל", "").replace("תמצא לי", "").strip()
        print(f"🔎 חיפוש בגוגל: {query}")
        perform_web_search(query)
        return f"חיפוש בגוגל על: {query}"

    # 📄 סיכום אתר לפי קישור
    url_match = re.search(r'https?://\S+', text)
    if url_match:
        url = url_match.group(0)
        print(f"🌐 סורק אתר: {url}")
        summary = summarize_website(url)
        return f"📄 סיכום ראשוני מתוך הדף:\n\n{summary}"

    # 🧱 יצירת דף נחיתה
    if "תכין דף נחיתה" in text:
        idea = text.replace("תכין דף נחיתה", "").strip()
        print(f"🌟 יוצר דף נחיתה בנושא: {idea}")
        return generate_landing_page(idea)

    # 🧠 שליחה ל־GPT אם לא זיהינו פעולה ספציפית
    print("🧠 לא זוהתה פעולה ברורה – שואל את GPT...")
    screen_context = summarize_screen_for_gpt()
    prompt = f"""המסך הנוכחי כולל את הטקסט הבא:

{screen_context}

המשתמש ביקש:
{text}

תכנן את הפעולות הדרושות כדי לבצע את הבקשה."""    
    gpt_plan = ask_gpt(prompt)
    if not gpt_plan:
        return "❌ לא התקבלה תוכנית פעולה מ־GPT."

    print("🚀 מבצע את תוכנית הפעולה...")
    execute_gpt_plan(gpt_plan)
    return f"בוצע לפי תוכנית:\n{gpt_plan}"
