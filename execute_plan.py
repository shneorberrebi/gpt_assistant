import time
import web_browser_utils
from screen_capture import take_screenshot
from screen_ocr import extract_text_from_image
from screen_context_filter import summarize_screen_for_gpt
from gpt_client import ask_gpt
from keyboard_typer import type_text
from smart_clicker import click_text_on_screen
from window_utils import focus_browser_window
from bs4 import BeautifulSoup
from video_editor import handle_video_editing
from video_editing_prompt_instructions import get_video_editing_prompt

import os
import json
from dotenv import load_dotenv
load_dotenv()

# 💾 פרטים אישיים מקובץ .env
personal_info = {
    "email": os.getenv("PERSONAL_EMAIL", ""),
    "שם": os.getenv("PERSONAL_NAME", ""),
    "טלפון": os.getenv("PERSONAL_PHONE", "")
}

# 🧠 זיכרון
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

def wait_and_click(target_text, max_wait=10):
    for _ in range(max_wait):
        if click_text_on_screen(target_text):
            return True
        time.sleep(1)
    print(f"⚠️ לא נמצא גם אחרי {max_wait} שניות: {target_text}")
    return False

def execute_plan(plan_lines):
    for line in plan_lines:
        print(f"\n🪪 {line}")

        norm = normalize_action(line)
        if norm in executed_actions:
            print("⏩ הפעולה כבר בוצעה. מדלג.")
            continue

        executed_actions.add(norm)
        save_memory()

        if "פתח אתר" in line or "תיכנס ל" in line or "תתחיל ב" in line:
            url = clean_url(line)
            if url:
                print(f"🌐 פותח: {url}")
                web_browser_utils.open_website(url)
                wait_until_page_has_text()
            else:
                print("❌ לא הצלחתי להוציא כתובת URL")
            continue

        if "כתוביות" in line or "ערוך סרטון" in line:
            prompt = get_video_editing_prompt(line)
            handle_video_editing(prompt)
            continue

        if "הקלד" in line or "מלא" in line:
            text = line.split("הקלד")[-1].strip().replace(":", "")
            if not text:
                text = summarize_screen_for_gpt()
            if "מייל" in line or "אימייל" in line:
                text = personal_info["email"]
            elif "שם" in line:
                text = personal_info["שם"]
            elif "טלפון" in line or "מספר" in line:
                text = personal_info["טלפון"]
            type_text(text)
            continue

        if not wait_and_click(line):
            print("❌ לא הצליח ללחוץ.")
