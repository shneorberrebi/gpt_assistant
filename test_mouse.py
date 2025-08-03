import pyautogui
import time

print("⌛ מחכה 5 שניות – תזיז את העכבר שלא יפריע...")

time.sleep(5)

# מיקום לבדיקה (אפשר לשנות)
x = 600
y = 300

pyautogui.moveTo(x, y, duration=0.5)  # זז למיקום תוך חצי שנייה
pyautogui.click()  # לוחץ קליק שמאלי

print(f"✅ זזנו ל־X={x}, Y={y} ולחצנו!")