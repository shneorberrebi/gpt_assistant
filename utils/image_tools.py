import pyautogui
import time

def find_and_click(image_name, double_click=False, timeout=10):
    """
    מחפש את האייקון על המסך לפי שם קובץ בתיקיית images ולוחץ עליו.
    """
    path = f"images/{image_name}.png"
    start_time = time.time()

    while time.time() - start_time < timeout:
        location = pyautogui.locateCenterOnScreen(path, confidence=0.8)
        if location:
            pyautogui.moveTo(location)
            if double_click:
                pyautogui.doubleClick()
            else:
                pyautogui.click()
            return True
        time.sleep(0.5)

    return False
