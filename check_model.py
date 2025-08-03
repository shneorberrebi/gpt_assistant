import openai
from dotenv import load_dotenv
import os

# 📂 טוען משתנים מהקובץ .env
load_dotenv()

# 🔑 טוען את מפתח ה־API מהסביבה
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📦 מקבל את רשימת המודלים
models = openai.Model.list()

print("📦 המודלים שזמינים לך:")
for model in models.data:
    print("✅", model.id)
