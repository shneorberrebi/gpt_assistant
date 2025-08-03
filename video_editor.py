# video_editor.py – עריכת וידאו חכמה לפי קיומם של B-Rolls

import os
import time
import subprocess
import pyautogui
import cv2
import webbrowser

CAPCUT_PATH = r"C:\Program Files\CapCut\CapCut.exe"
CAPTIONS_URL = "https://app.captions.ai/projects"

def open_capcut():
    if not os.path.exists(CAPCUT_PATH):
        print("⚠️ CapCut לא נמצא – פתח ידנית")
        return
    subprocess.Popen(CAPCUT_PATH)
    time.sleep(10)
    print("✅ CapCut נפתח")

def import_video_to_capcut(video_path):
    print(f"📥 טוען לקאפקאט: {video_path}")
    open_capcut()
    pyautogui.hotkey('ctrl', 'o')
    time.sleep(2)
    pyautogui.write(video_path)
    pyautogui.press('enter')
    print("🎞️ הסרטון נטען לקאפקאט")

def analyze_video_basic(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    cap.release()
    print(f"🕒 אורך הסרטון: {duration:.1f} שניות")
    return duration

def open_captions():
    print("🌐 נפתח Captions.ai")
    webbrowser.open(CAPTIONS_URL)
    time.sleep(10)

def edit_video_automatically(video_path, has_b_rolls=False):
    duration = analyze_video_basic(video_path)

    if has_b_rolls:
        print("🎬 יש B-Roll – עורכים קודם בקאפקאט")
        import_video_to_capcut(video_path)
        print("⌛ מחכה לסיום עריכה ידנית בקאפקאט...")
        time.sleep(15)

    print("↪️ עכשיו עובר ל-Captions.ai לכתוביות (ותוך כדי עריכה אם אין B-Roll)")
    open_captions()

# 🧠 נקודת כניסה ראשית
def handle_video_editing(command_text):
    """
    מקבל שורת פקודה מ־GPT (למשל: 'ערוך סרטון בשם X ויש B-Roll')
    ומבצע תהליך אוטונומי לפי האם יש B-Roll.
    """
    print(f"🎬 התחלת עריכת וידאו לפי פקודה: {command_text}")
    has_b_rolls = "בירול" in command_text.lower() or "b-roll" in command_text.lower()
    video_path = extract_video_path_from_command(command_text)
    if video_path:
        edit_video_automatically(video_path, has_b_rolls)
    else:
        print("❌ לא נמצא נתיב לסרטון")

def extract_video_path_from_command(text):
    """
    מחלץ מסלול לקובץ מתוך פקודה של GPT (אם יש)
    לדוגמה: 'ערוך את הסרטון C:/Videos/test.mp4'
    """
    for word in text.split():
        if os.path.exists(word) and word.lower().endswith((".mp4", ".mov", ".mkv")):
            return word
    return ""
