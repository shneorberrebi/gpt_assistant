# brain.py – גרסה משודרגת עם הבנת הקשר חכמה ושמירה על פעולות

import time
import web_browser_utils
import web_reader
import web_clicker
import web_interactor

from video_editor import handle_video_editing
from smart_clicker import click_text_on_screen
from screen_capture import take_screenshot
from screen_ocr import extract_text_from_image, extract_texts_with_positions
from gpt_client import ask_gpt
from screen_context_filter import summarize_screen_for_gpt
from keyboard_typer import type_text
from window_utils import focus_browser_window
from bs4 import BeautifulSoup

from video_editing_prompt_instructions import get_video_editing_prompt

import json, os

# 💾 פרטים אישיים
personal_info = {
    "email": "lutya.co@gmail.com",
    "שם": "shneor",
    "טלפון": "0585333099"
}

# 🧠 זיכרון פעולות – כדי לא לחזור על אותן פעולות
executed_actions = set()
def load_memory():
    if os.path.exists("executed_memory.json"):
        with open("executed_memory.json", "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()
def save_memory():
    with open("executed_memory.json", "w", encoding="utf-8") as f:
        json.dump(list(executed_actions), f, ensure_ascii=False, indent=2)
executed_actions = load_memory()

def normalize_action(line):
    return line.replace(" ", "").replace(":", "").lower()

# 🖱️ לחיצה חכמה עם המתנה
def wait_and_click(target_text, max_wait=10):
    for _ in range(max_wait):
        if click_text_on_screen(target_text):
            return True
        time.sleep(1)
    print(f"⚠️ לא נמצא גם אחרי {max_wait} שניות: {target_text}")
    return False

# ⏳ המתנה עד שהעמוד יטען (לפי תוכן בפועל)
def wait_until_page_has_text(min_words=30, timeout=20):
    driver = web_browser_utils.get_browser()
    for _ in range(timeout):
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        texts = [el.get_text(strip=True) for el in soup.find_all(['h1','p','li','button','a']) if el.get_text(strip=True)]
        if len(" ".join(texts).split()) >= min_words:
            print("✅ העמוד נטען.")
            return True
        time.sleep(1)
    print("⏰ עבר הזמן – לא נטען מספיק טקסט.")
    return False

# 🌐 השלמת קישור חכמה
def clean_url(text):
    text = text.strip().lower()
    if text.startswith("http"):
        return text
    if "." in text:
        return "https://" + text
    try:
        print(f"🧠 שואל את GPT מה הקישור של: {text}")
        response = ask_gpt(f"השלם לי קישור אמיתי לאתר הבא רק בצורה של כתובת URL בלבד בלי טקסט נוסף: {text}")
        url = response.strip().split()[0]
        if url.startswith("http"):
            return url
    except Exception as e:
        print(f"⚠️ שגיאה בהשלמת קישור: {e}")
    return ""
# 🚀 הפעלת GPT על תוכנית פעולה
def execute_plan(plan_text):
    if not plan_text.strip():
        print("⚠️ אין תוכנית.")
        return
    lines = plan_text.strip().splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        normalized = normalize_action(line)
        if normalized in executed_actions:
            print(f"⏩ מדלג – כבר בוצע: {line}")
            continue
        executed_actions.add(normalized)
        print(f"➡️ מבצע: {line}")
        try:
            if "פתח אתר" in line:
                url = line.split("פתח אתר")[-1].strip()
                full_url = clean_url(url)
                if full_url:
                    web_browser_utils.open_website(full_url)
                    wait_until_page_has_text()
                    focus_browser_window()

            elif any(k in line for k in ["תיכנס ל", "תתחיל ב", "תפתח את"]):
                parts = line.split()
                url = parts[-1].strip() if len(parts) > 1 else ""
                if not url:
                    print(f"⚠️ לא נמצאה כתובת בתוך: {line}")
                    continue
                full_url = clean_url(url)
                if full_url:
                    web_browser_utils.open_website(full_url)
                    wait_until_page_has_text()
                    focus_browser_window()

            elif "לחץ על" in line:
                wait_and_click(line.split("לחץ על")[-1].strip())

            elif "צלם מסך" in line:
                take_screenshot()

            elif "קרא מהמסך" in line:
                img = take_screenshot()
                extract_text_from_image(img)

            elif "ערוך סרטון" in line:
                handle_video_editing(line)

            elif "הקלד את" in line:
                val = line.split("הקלד את")[-1].strip()
                type_text(personal_info.get(val, val))
                time.sleep(1)

        except Exception as e:
            print(f"❌ שגיאה בביצוע: {line} -> {e}")
    save_memory()

# 💬 פקודה רגילה מהצ'אט הראשי
def process_command(command):
    print(f"🧠 מבצע פקודה מהצ'אט: {command}")
    image_path = take_screenshot()
    screen_context = summarize_screen_for_gpt(image_path)
    plan = ask_gpt(command, screen_context)
    print("📥 תוכנית:\n", plan)
    execute_plan(plan)

# 💬 פקודה חכמה מהמסך – עם הבנת טקסטים
def handle_command(command):
    try:
        command = command.strip()
        print(f"\n🎯 פקודה: {command}")
        if any(k in command for k in ["פתח אתר", "תיכנס ל", "תתחיל ב", "תפתח את"]):
            site = command.replace("פתח אתר", "").replace("תיכנס ל", "").replace("תתחיל ב", "").replace("תפתח את", "").strip()
            url = clean_url(site)
            if url:
                web_browser_utils.open_website(url)
                wait_until_page_has_text()
                focus_browser_window()
            return

        image_path = take_screenshot()
        texts_with_positions = extract_texts_with_positions(image_path)
        context = "\n".join([f"{t['text']} @ ({t['x']},{t['y']})" for t in texts_with_positions])
        print("🖼️ טקסטים במסך:\n", context)

        if "ערוך סרטון" in command:
            prompt = get_video_editing_prompt(command, context)
        else:
            prompt = f"""
🧠 בקשה: הבן את הבקשה ובצע לפי מה שרואים במסך

פקודה:
{command}

טקסטים במסך:
{context}

החזר רק שורות פעולה:
- פתח אתר <כתובת>
- לחץ על <טקסט>
- הקלד את <שדה>
- צלם מסך
- קרא מהמסך
- ערוך סרטון
"""

        print("\n📤 שולח ל־GPT:\n", prompt)
        plan = ask_gpt(prompt)
        print("\n📥 תוכנית:\n", plan)
        execute_plan(plan)

    except Exception as e:
        print(f"❌ שגיאה כללית: {e}")
