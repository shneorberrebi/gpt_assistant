# window_utils.py – זיהוי חלון דפדפן + פוקוס אוטומטי

import pygetwindow as gw
import time

def focus_browser_window():
    """
    🪟 מביא חלון של דפדפן לקדמת המסך (Chrome, Edge, Firefox, Brave, Opera).
    מחזיר True אם הצליח, אחרת False.
    """
    browser_keywords = ["chrome", "edge", "firefox", "brave", "opera"]
    try:
        windows = gw.getWindowsWithTitle("")
    except Exception as e:
        print(f"❌ שגיאה בשליפת חלונות: {e}")
        return False

    for window in windows:
        title = (window.title or "").lower().strip()

        if any(browser in title for browser in browser_keywords):
            try:
                if window.isMinimized:
                    window.restore()
                window.activate()
                window.maximize()
                print(f"🪟 הבאת לפוקוס את: {window.title}")
                time.sleep(0.8)
                return True
            except Exception as e:
                print(f"⚠️ לא הצלחתי להפעיל את החלון '{window.title}': {e}")

    print("❌ לא נמצא חלון דפדפן פעיל.")
    return False
