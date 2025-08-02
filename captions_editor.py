import pyautogui
import time
import webbrowser

def edit_in_captions(sender_name):
    webbrowser.open("https://desktop.captions.ai/projects")
    time.sleep(10)

    print(f"🔍 מחפש את הפרויקט של {sender_name} ומתחיל לערוך...")
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write(sender_name)
    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.press('tab')  # מעבר לרשימה
    pyautogui.press('enter')  # כניסה לפרויקט
    time.sleep(5)

    print("📝 עורך כתוביות ובודק שגיאות...")
    # כאן תוכל להוסיף תנועות עכבר ללחיצה על 'Edit Subtitles'
    time.sleep(10)
    print("⬇️ מוריד את הסרטון המוכן...")