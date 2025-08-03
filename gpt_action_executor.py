import time
import json
import os
from bs4 import BeautifulSoup
import pyautogui
import keyboard
from dotenv import load_dotenv

from smart_clicker import click_text_on_screen
from screen_capture import take_screenshot
from screen_ocr import extract_text_from_image
from keyboard_typer import type_text
import web_browser_utils
from window_utils import focus_browser_window
from video_editor import handle_video_editing

# 📦 טעינת משתנים מקובץ .env
load_dotenv()
personal_info = {
    "email": os.getenv("PERSONAL_EMAIL", ""),
    "מייל": os.getenv("PERSONAL_EMAIL", ""),
    "שם": os.getenv("PERSONAL_NAME", ""),
    "שם פרטי": os.getenv("PERSONAL_NAME", ""),
    "שם משפחה": os.getenv("PERSONAL_LASTNAME", ""),
    "טלפון": os.getenv("PERSONAL_PHONE", ""),
    "מספר טלפון": os.getenv("PERSONAL_PHONE", ""),
    "שם עסק": os.getenv("PERSONAL_BUSINESS", ""),
    "השם שלי": os.getenv("PERSONAL_NAME", ""),
    "המייל שלי": os.getenv("PERSONAL_EMAIL", ""),
    "הטלפון שלי": os.getenv("PERSONAL_PHONE", "")
}

executed_actions = set()

def load_memory():
    if os.path.exists("executed_memory.json"):
        try:
            with open("executed_memory.json", "r", encoding="utf-8") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_memory():
    with open("executed_memory.json", "w", encoding="utf-8") as f:
        json.dump(list(executed_actions), f, ensure_ascii=False, indent=2)

executed_actions = load_memory()

def normalize_action(line):
    return line.replace(" ", "").replace(":", "").lower()

def wait_and_click(target_text, max_wait=10):
    if not target_text.strip():
        print("⚠️ טקסט ריק – לא ניתן ללחוץ עליו.")
        return False
    for _ in range(max_wait):
        try:
            if click_text_on_screen(target_text):
                return True
        except Exception as e:
            print(f"⚠️ שגיאה בלחיצה: {e}")
        time.sleep(1)
    print(f"⚠️ לא נמצא על המסך: {target_text}")
    return False

def extract_fields(text):
    return [s.strip() for s in text.replace(" ו", ",").split(",") if s.strip()]

def clean_url(url):
    url = url.strip().lower()
    if not url:
        return None
    if not url.startswith("http"):
        url = "https://" + url
    return url

def execute_plan(plan_text):
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
            if any(x in line for x in ["פתח אתר", "תיכנס ל", "תתחיל ב", "תפתח את"]):
                parts = line.split()
                url = parts[-1].strip()
                cleaned = clean_url(url)
                if cleaned:
                    web_browser_utils.open_website(cleaned)
                    focus_browser_window()
                    web_browser_utils.wait_until_page_has_text()

            elif "לחץ על" in line:
                target = line.split("לחץ על")[-1].strip()
                wait_and_click(target)

            elif "הקלד את" in line:
                typed = line.split("הקלד את")[-1].strip()
                fields = extract_fields(typed)
                for item in fields:
                    val = personal_info.get(item, item)
                    type_text(val)
                    time.sleep(1)

            elif "צלם מסך" in line:
                take_screenshot()

            elif "קרא מהמסך" in line:
                img = take_screenshot()
                extract_text_from_image(img)

            elif "ערוך סרטון" in line:
                handle_video_editing(line)

            elif "סגור את" in line:
                web_browser_utils.close_tab()

            elif "שמור" in line:
                keyboard.press_and_release("ctrl+s")
            elif "העתק" in line:
                keyboard.press_and_release("ctrl+c")
            elif "הדבק" in line:
                keyboard.press_and_release("ctrl+v")
            elif "בחר הכל" in line:
                keyboard.press_and_release("ctrl+a")

            elif "גלול למטה" in line:
                pyautogui.scroll(-300)
            elif "גלול למעלה" in line:
                pyautogui.scroll(300)

            elif "המתן" in line:
                time.sleep(3)

        except Exception as e:
            print(f"❌ שגיאה בביצוע '{line}': {e}")

    save_memory()
