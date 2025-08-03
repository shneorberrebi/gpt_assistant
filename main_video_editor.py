import time
from capcut_editor import edit_in_capcut
from captions_editor import edit_in_captions
from utils import get_user_input, get_sender_name

def main():
    print("🎬 ברוך הבא לעורך הסרטונים החכם!")
    video_path = get_user_input("הזן את מיקום הסרטון במחשב:")
    sender_name = get_user_input("איך קוראים בערך לבן אדם ששלח את הסרטון?")
    has_brolls = get_user_input("האם שלחו לך בירולים? (כן/לא):").strip().lower() == "כן"

    print("\n🚀 מתחילים לערוך ב-CapCut...")
    edit_in_capcut(video_path, has_brolls)
    time.sleep(3)

    print("\n🧠 ממשיכים לעריכת כתוביות ב-Captions.ai...")
    edit_in_captions(sender_name)

    print("\n✅ הסרטון מוכן ונשמר! נשאר רק לשלוח אותו חזרה למי ששלח.")

if __name__ == "__main__":
    main()

