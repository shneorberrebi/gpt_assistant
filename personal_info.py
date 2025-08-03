# personal_info.py – פרטים אישיים לעוזר האישי שלך 🧠
# העוזר לא יבצע תשלום – אלא אם תיתן אישור מפורש

import os
from dotenv import load_dotenv

load_dotenv()

def load_personal_info():
    return {
        "full_name": f"{os.getenv('PERSONAL_NAME', '')} {os.getenv('PERSONAL_LASTNAME', '')}".strip(),
        "email": os.getenv("PERSONAL_EMAIL", ""),
        "phone": os.getenv("PERSONAL_PHONE", ""),
        "city": os.getenv("PERSONAL_CITY", "כפר אדומים / ירושליים"),
        "address": os.getenv("PERSONAL_ADDRESS", "ישראל כפר אדומים משכנות הרועים 9"),
        "age": int(os.getenv("PERSONAL_AGE", "25")),
        "birth_date": os.getenv("PERSONAL_BIRTH_DATE", "2000-05-13"),
        "business_name": os.getenv("PERSONAL_BUSINESS", ""),
        "website": os.getenv("PERSONAL_WEBSITE", ""),
        "credit_card": None,
        "payment_policy": "תמיד להשתמש בפתרונות חינמיים. אם אין – לבקש אישור ממני."
    }
