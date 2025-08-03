# web_browser_utils.py – פתיחה יציבה של אתרים עם Selenium והמתנה חכמה

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time

browser = None  # שומר את הדפדפן הגלובלי

def is_browser_valid(driver):
    try:
        if driver is None:
            return False
        driver.title  # ניסיון גישה יזרוק שגיאה אם סגור
        return True
    except:
        return False

def get_browser():
    """
    מחזיר מופע דפדפן פעיל. אם לא קיים – יוצר חדש.
    """
    global browser
    if is_browser_valid(browser):
        return browser

    print("🌐 פותח דפדפן חדש...")
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_experimental_option("detach", True)  # משאיר את החלון פתוח
    # ❗ ללא Headless – חובה לעבודה גרפית
    # options.add_argument("--headless")  ← לא להשתמש בזה!

    try:
        browser = webdriver.Chrome(options=options)
        browser.maximize_window()  # מסך מלא – שיפור ל-OCR וכו'
    except Exception as e:
        print(f"❌ שגיאה בהפעלת כרום: {e}")
        return None

    return browser

def open_website(url):
    """
    טוען את האתר בדפדפן.
    """
    driver = get_browser()
    if driver:
        try:
            driver.get(url)
            print(f"🌐 טוען את: {url}")
        except WebDriverException as e:
            print(f"❌ שגיאה בטעינת האתר: {e}")
        except Exception as e:
            print(f"❌ שגיאה כללית: {e}")

def wait_until_page_has_text(min_words=30, timeout=20):
    """
    ממתין עד שטוענים מספיק טקסט בדף.
    """
    driver = get_browser()
    if not driver:
        return False

    for second in range(timeout):
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            texts = [el.get_text(strip=True) for el in soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'button', 'a', 'span', 'div']) if el.get_text(strip=True)]
            word_count = len(" ".join(texts).split())

            if word_count >= min_words:
                print(f"✅ הדף נטען ({word_count} מילים)")
                return True
        except Exception as e:
            print(f"⚠️ שגיאה בקריאת דף: {e}")
        time.sleep(1)

    print("⏰ לא נטען מספיק טקסט בזמן")
    return False

def close_tab():
    """
    סוגר את הלשונית הנוכחית.
    """
    driver = get_browser()
    if driver:
        try:
            driver.close()
            print("🗙 לשונית נסגרה")
        except Exception as e:
            print(f"❌ שגיאה בסגירת לשונית: {e}")
