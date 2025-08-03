# keyboard_typer.py – הקלדה והדבקה חכמה עם תמיכה בעברית, אימוג'ים ותווים מורכבים

import time
import pyautogui
import pyperclip


def type_text(text, delay=0.04):
    """
    🧠 מקליד תו-אחר-תו או מדביק לפי הצורך:
    - תווים מיוחדים (עברית, אימוג'ים, יוניקוד, שורות) → הדבקה
    - טקסט פשוט וקצר → הקלדה רגילה
    """
    time.sleep(0.3)
    if not text:
        return

    try:
        if len(text) > 50 or contains_special_chars(text):
            paste_text(text)
        else:
            pyautogui.write(text, interval=delay)
    except Exception as e:
        print(f"[type_text] שגיאה: {e} – מנסה להדביק במקום להקליד")
        paste_text(text)


def paste_text(text):
    """
    📋 מדביק טקסט דרך הלוח (clipboard) – תומך בעברית, יוניקוד, אימוג'ים ושורות.
    """
    try:
        pyperclip.copy("")      # ניקוי ראשוני
        time.sleep(0.05)
        pyperclip.copy(text)
        time.sleep(0.15)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.15)
        pyperclip.copy("")      # ניקוי סופי
    except Exception as e:
        print(f"[paste_text] שגיאה בהדבקה: {e}")
        try:
            pyautogui.write(text)
        except Exception as inner_e:
            print(f"[paste_text] גם write נכשלה: {inner_e}")


def press_enter():
    """
    ⏎ לוחץ על Enter
    """
    try:
        pyautogui.press("enter")
        time.sleep(0.2)
    except Exception as e:
        print(f"[press_enter] שגיאה: {e}")


def clear_text():
    """
    ❌ מוחק את כל הטקסט משדה כתיבה (Ctrl+A ואז Backspace)
    """
    try:
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.1)
        pyautogui.press("backspace")
        time.sleep(0.1)
    except Exception as e:
        print(f"[clear_text] שגיאה: {e}")


def type_and_enter(text):
    """
    💬 מקליד טקסט ואז לוחץ Enter
    """
    type_text(text)
    press_enter()


def contains_special_chars(text):
    """
    🧐 בודק אם הטקסט מכיל תווים מיוחדים:
    עברית, אימוג'ים, תווי Unicode, שורות חדשות וכדומה.
    """
    if not text:
        return False

    return any(
        ord(c) > 127 or c in "§™©•✓—“”‘’🙂🙃😂😭😒😡😎😩😱😴😇׳״…–\n\t\r"
        for c in text
    )
