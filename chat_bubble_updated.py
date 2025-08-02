# chat_bubble_updated.py – חלון צ'אט גרפי עם שליחה לעוזר
import tkinter as tk
import json
import os
import shutil
from tkinter import simpledialog, filedialog
from handle_command import handle_command

DATA_FILE = "user_data.json"
UPLOADS_DIR = "uploads"

def save_data(key, value):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[key] = value
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ נשמר: {key} = {value}")

def on_save_button_click():
    key = simpledialog.askstring("שמור פרטים", "הזן מפתח (למשל: email):")
    if key:
        value = simpledialog.askstring("שמור פרטים", f"הזן ערך עבור '{key}':")
        if value:
            save_data(key, value)

def upload_file():
    file_path = filedialog.askopenfilename(title="בחר קובץ להעלאה")
    if file_path:
        try:
            file_name = os.path.basename(file_path)
            os.makedirs(UPLOADS_DIR, exist_ok=True)
            shutil.copy(file_path, os.path.join(UPLOADS_DIR, file_name))
            text_box.insert(tk.END, f"📤 העלית קובץ: {file_name}\n")
        except Exception:
            text_box.insert(tk.END, f"❌ שגיאה בהעלאת הקובץ\n")

def on_submit(event=None):
    user_input = text_box.get("1.0", tk.END).strip()
    if user_input:
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, f"🧑‍💻 אתה: {user_input}\n")
        text_box.insert(tk.END, "🤖 העוזר מבצע את הפקודה...\n")
        try:
            handle_command(user_input)
        except Exception as e:
            text_box.insert(tk.END, f"❌ שגיאה: {str(e)}\n")

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")

def paste_from_clipboard(event=None):
    try:
        text = root.clipboard_get()
        text_box.insert(tk.INSERT, text)
    except Exception:
        pass

def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

root = tk.Tk()
root.title("GPT Assistant")
root.geometry("230x160+20+100")
root.attributes("-topmost", True)
root.overrideredirect(True)

frame = tk.Frame(root, bg="#f8f8f8", bd=2, relief="raised")
frame.pack(expand=True, fill="both")

frame.bind("<ButtonPress-1>", start_move)
frame.bind("<B1-Motion>", do_move)

text_box = tk.Text(frame, height=6, wrap="word", font=("Arial", 9))
text_box.pack(padx=4, pady=(4, 2), fill="both", expand=True)
text_box.bind("<Return>", lambda event: on_submit() if not event.state & 0x0001 else None)
text_box.bind("<Control-v>", paste_from_clipboard)
text_box.bind("<Control-V>", paste_from_clipboard)
text_box.bind("<Button-3>", show_context_menu)

context_menu = tk.Menu(text_box, tearoff=0)
context_menu.add_command(label="הדבק", command=paste_from_clipboard)

submit_button = tk.Button(frame, text="שלח", width=8, command=on_submit)
submit_button.pack(side="left", padx=(4, 2), pady=4)

save_button = tk.Button(frame, text="שמור פרטים", width=10, command=on_save_button_click)
save_button.pack(side="right", padx=(2, 4), pady=4)

upload_button = tk.Button(frame, text="העלה קובץ", width=20, command=upload_file)
upload_button.pack(side="bottom", padx=4, pady=(0, 4))

root.mainloop()
