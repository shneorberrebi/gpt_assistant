# web_browser_utils.py – פתיחה חכמה של אתרים עם Selenium + ניתוח תוכן

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def open_browser_and_wait(url, min_words=30, timeout=20, headless=False):
    """
    פותח את האתר בדפדפן כרום, ממתין שיהיה בו מספיק טקסט, ומחזיר את הטקסטים.
    :param url: כתובת האתר
    :param min_words: כמות מילים מינימלית כדי להיחשב כעמוד שנטען
    :param timeout: מקסימום זמן המתנה בשניות
    :param headless: האם לפתוח את כרום במצב ללא GUI
    :return: רשימת טקסטים מהאתר או [] אם נכשל
    """
    print(f"🌐 פותח את האתר: {url}")

    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")  # שקט ברקע
    options.add_experimental_option("detach", True)  # לא סוגר את הכרום אוטומטית

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    for second in range(timeout):
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        elements = soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'button', 'a', 'span', 'div'])
        texts = [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]

        if len(" ".join(texts).split()) >= min_words:
            print(f"✅ האתר נטען ({len(texts)} טקסטים)")
            driver.quit()
            return texts

        print(f"⏳ ממתין... ({second + 1}/{timeout})")
        time.sleep(1)

    driver.quit()
    print("❌ הזמן עבר – לא נמצא מספיק טקסט.")
    return []
