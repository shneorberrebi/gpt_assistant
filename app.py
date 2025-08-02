# app.py – לולאת הפעלה לעוזר האישי

from handle_command import handle_command

print("\n🤖 העוזר מוכן! כתוב פקודה חכמה (או 'יציאה' כדי לצאת):")

while True:
    try:
        user_input = input("\n💬 > ").strip()

        if user_input.lower() in ["exit", "quit", "יציאה"]:
            print("👋 נתראה בפעם הבאה!")
            break

        if not user_input:
            continue

        print("\n🧠 חושב איך לבצע את זה...")
        handle_command(user_input)

    except KeyboardInterrupt:
        print("\n⛔ הופסק על ידי המשתמש.")
        break

    except Exception as e:
        print(f"\n❌ שגיאה כללית: {e}")
