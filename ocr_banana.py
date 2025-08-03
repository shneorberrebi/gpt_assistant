from PIL import Image
import pytesseract

# מיקום התוכנה tesseract במחשב שלך
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# שם הקובץ של התמונה שנרצה לקרוא
image_path = "test_image.png"

# פתיחת התמונה
image = Image.open(image_path)

# הפעלת OCR (זיהוי טקסט)
text = pytesseract.image_to_string(image, lang='eng+heb')

# הדפסת הטקסט שזוהה
print("🔍 הטקסט שזוהה מהתמונה:\n")
print(text)
