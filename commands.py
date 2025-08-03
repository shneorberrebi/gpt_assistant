from gpt_client import ask_gpt
from data_store import save_data

def handle_command(text):
    if "שמור" in text:
        key = "פרט"
        save_data(key, text)
        print("🟢 פרטים נשמרו!")
    else:
        answer = ask_gpt(text)
        print("🧠 תשובה מהעוזר:", answer)
