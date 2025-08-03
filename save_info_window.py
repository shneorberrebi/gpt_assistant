import tkinter as tk
import json
import os

FILE_NAME = "user_info.json"

def save_user_info(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("🎉 הפרטים נשמרו בהצלחה!")

def open_save_window():
    win = tk.Toplevel()
    win.title("שמור פרטים")
    win.geometry("300x250")

    fields = {
        "אימייל": tk.StringVar(),
        "סיסמה": tk.StringVar(),
        "שם מלא": tk.StringVar(),
        "טלפון": tk.StringVar(),
    }

    row = 0
    for label_text, var in fields.items():
        label = tk.Label(win, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(win, textvariable=var, show="*" if "סיסמה" in label_text else "")
        entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1

    def on_save():
        data = {key: var.get() for key, var in fields.items()}
        save_user_info(data)
        win.destroy()

    save_btn = tk.Button(win, text="שמור ✅", command=on_save)
    save_btn.grid(row=row, column=0, columnspan=2, pady=10)
