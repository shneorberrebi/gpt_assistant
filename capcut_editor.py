import pyautogui
import time
import os

def edit_in_capcut(video_path, has_brolls):
    os.startfile("C:\\Program Files\\CapCut\\CapCut.exe")  # עדכן לפי מיקום CapCut במחשב שלך
    time.sleep(10)  # מחכה שהאפליקציה תיטען

    pyautogui.hotkey('ctrl', 'o')  # פתיחת קובץ חדש
    time.sleep(2)
    pyautogui.write(video_path)
    pyautogui.press('enter')
    time.sleep(5)

    print("🎞️ הסרטון נטען. מבצע חיתוכים, מוסיף מוזיקה ובירולים...")
    # כאן תוכל להוסיף תנועות עכבר או לחיצות ספציפיות לפי הצרכים שלך
    if has_brolls:
        print("🎥 מוסיף בירולים...")
    else:
        print("🎶 מוסיף רקע, מוזיקה וחיתוכים...")

    time.sleep(3)
    print("💾 מייצא את הסרטון מתוך CapCut...")
    pyautogui.hotkey('ctrl', 'm')  # export
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(10)