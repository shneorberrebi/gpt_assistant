# test_gpt_connection.py – בדיקת חיבור ל־GPT

import openai
import os
from dotenv import load_dotenv

# טוען משתני סביבה מקובץ .env
load_dotenv()

# טוען את המפתח מהמשתנה ENV
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "האם אתה מחובר?"},
        ],
        temperature=0.2,
        max_tokens=50
    )
    print("✅ הצליח להתחבר ל־GPT")
    print("תשובה:", response.choices[0].message["content"])
except Exception as e:
    print("❌ לא הצליח להתחבר ל־GPT")
    print(e)
