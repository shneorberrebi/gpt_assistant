# screen_capture.py – צילום מסך חכם עם שמירה, תמונה, ו־debug

import mss
from PIL import Image
import time
import os


def take_screenshot(save_path=None, return_image=False, monitor_index=1, debug=True):
    """
    📸 מצלם את המסך הראשי או לפי index.
    - אם מוגדר save_path – שומר לשם.
    - אם return_image=True – מחזיר את אובייקט התמונה.
    - אחרת מחזיר את הנתיב או None.
    """
    try:
        with mss.mss() as sct:
            monitors = sct.monitors
            if len(monitors) <= monitor_index:
                monitor_index = 0  # fallback למסך ברירת מחדל

            monitor = monitors[monitor_index]
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            if save_path:
                img.save(save_path)
                if debug:
                    print(f"📸 צילום מסך נשמר ל: {save_path}")

            return img if return_image else save_path

    except Exception as e:
        print(f"❌ שגיאה בצילום המסך: {e}")
        return None


def take_screenshot_and_save(folder="screenshots", monitor_index=1, debug=True):
    """
    📂 שומר צילום מסך בתיקייה לפי שעה.
    מחזיר את הנתיב לתמונה או None.
    """
    try:
        os.makedirs(folder, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(folder, f"screenshot_{timestamp}.png")
        return take_screenshot(save_path=file_path, return_image=False, monitor_index=monitor_index, debug=debug)
    except Exception as e:
        print(f"❌ שגיאה בשמירת צילום המסך: {e}")
        return None
