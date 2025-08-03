from web_browser_utils import open_website, wait_until_page_has_text
from window_utils import focus_browser_window
from screen_capture import take_screenshot
from screen_ocr import extract_texts_with_positions
from gpt_client import ask_gpt
from screen_context_filter import get_video_editing_prompt
from gpt_action_executor import execute_plan
from utils_url_completion import complete_url_if_needed

def handle_command(command):
    try:
        command = command.strip()
        print(f"\n🎯 פקודה: {command}")

        # פתיחה ישירה של אתר ללא GPT
        if any(k in command for k in ["פתח אתר", "תיכנס ל", "תתחיל ב", "תפתח את"]):
            site = command.replace("פתח אתר", "").replace("תיכנס ל", "").replace("תתחיל ב", "").replace("תפתח את", "").strip()
            url = complete_url_if_needed(site)
            if url.startswith("http"):
                open_website(url)
                wait_until_page_has_text()
                focus_browser_window()
            else:
                print("⚠️ לא זוהה URL תקין לפתיחה.")
            return

        # צילום מסך וקריאת טקסטים עם מיקומים
        image_path = take_screenshot()
        texts_with_positions = extract_texts_with_positions(image_path)
        context = "\n".join([f"{t['text']} @ ({t['x']},{t['y']})" for t in texts_with_positions])

        # יצירת פרומפט מותאם (עריכת וידאו או פעולה כללית)
        if "ערוך סרטון" in command:
            prompt = get_video_editing_prompt(command, context)
        else:
            prompt = f"""
אתה עוזר אינטליגנטי עם שליטה במחשב – מסוגל לפתוח אתרים, ללחוץ, להקליד, לצלם מסך ולבצע כל פעולה לפי ההקשר.  
המסך הנוכחי כולל את הטקסטים הבאים:

{context}

המשתמש ביקש:
{command}

🔁 החזר רק את הפעולות לביצוע, שורה לכל פעולה – בלי הסברים. פורמטים מותרים:

- פתח אתר <כתובת>
- תיכנס ל <כתובת>
- תתחיל ב <כתובת>
- תפתח את <כתובת>
- לחץ על <טקסט>
- הקלד את <שדה>
- צלם מסך
- קרא מהמסך
- ערוך סרטון <פרטים>

⚠️ אל תסביר, אל תדבר – רק שורות פעולה נקיות, אחת בכל שורה.
""".strip()

        print("\n📤 שולח ל-GPT:\n", prompt)
        plan = ask_gpt(prompt).strip()
        print("\n📥 תוכנית שהתקבלה:\n", plan)

        # ניקוי והשלמה אוטומטית לכל URL בשורות
        lines = plan.splitlines()
        updated_lines = [complete_url_if_needed(line) for line in lines]
        final_plan = "\n".join(updated_lines)

        if not any(kw in final_plan for kw in ["פתח אתר", "תיכנס ל", "תתחיל ב", "תפתח את", "לחץ על", "הקלד את", "צלם מסך", "קרא מהמסך", "ערוך סרטון"]):
            print("⚠️ לא נמצאה אף שורת פעולה – כנראה שהתשובה של GPT לא תקפה.")
            return

        # ביצוע בפועל
        execute_plan(final_plan)

    except Exception as e:
        print(f"❌ שגיאה כללית ב-handle_command: {e}")
