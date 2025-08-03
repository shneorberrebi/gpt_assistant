import pyautogui
import time
from utils.image_tools import find_and_click

def open_capcut():
    print("🚀 מחפש את האייקון של CapCut...")
    time.sleep(1)

    found = find_and_click("capcut_icon", double_click=True, timeout=10)
    
    if found:
        print("✅ CapCut נפתח בהצלחה!")
        time.sleep(10)  # זמן פתיחה ממוצע
        return True
    else:
        print("❌ לא נמצא האייקון של CapCut על המסך.")
        return False
