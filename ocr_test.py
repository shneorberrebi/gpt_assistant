# ocr_test.py – בדיקת OCR מהירה של צילום מסך

from screen_capture import capture_screen
from ocr_utils import get_text_elements

def test_ocr():
    print("📸 מבצע צילום מסך...")
    image = capture_screen()

    print("🔍 מפעיל OCR על התמונה...")
    text_elements = get_text_elements(image)

    if not text_elements:
        print("❌ לא נמצאו טקסטים בתמונה.")
        return

    print(f"✅ נמצאו {len(text_elements)} טקסטים:")
    for el in text_elements:
        print(f"📝 '{el['text']}' | מיקום: {el['box']}")

if __name__ == "__main__":
    test_ocr()
