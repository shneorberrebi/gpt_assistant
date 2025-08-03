import tkinter as tk
import subprocess

def on_submit():
    command = entry.get()
    if command.strip() != "":
        subprocess.Popen(["python", "smart_assistant.py", command])

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")

# הגדרת חלון ראשי
root = tk.Tk()
root.title("עוזר אישי")
root.geometry("300x140")  # גודל קטן יותר
root.overrideredirect(True)  # בלי מסגרת
root.attributes("-topmost", True)  # תמיד למעלה

# אזור שאפשר לגרור ממנו
frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="raised")
frame.pack(fill="both", expand=True)

frame.bind("<Button-1>", start_move)
frame.bind("<B1-Motion>", do_move)

# כותרת
label = tk.Label(frame, text="מה תרצה שאעשה?", font=("Arial", 12), bg="#f0f0f0")
label.pack(pady=(10, 5))

# תיבת קלט
entry = tk.Entry(frame, font=("Arial", 11))
entry.pack(padx=10, pady=5, fill="x")

# כפתור שליחה
button = tk.Button(frame, text="שלח ✅", font=("Arial", 11), command=on_submit)
button.pack(pady=5)

root.mainloop()
