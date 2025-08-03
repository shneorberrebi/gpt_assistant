import tkinter as tk
from commands import handle_command

def on_submit(event=None):
    user_input = text_box.get("1.0", tk.END).strip()
    if user_input:
        handle_command(user_input)
        text_box.delete("1.0", tk.END)

root = tk.Tk()
root.title("GPT Assistant")

text_box = tk.Text(root, height=4, width=50)
text_box.pack(padx=10, pady=10)
text_box.bind("<Return>", on_submit)

submit_button = tk.Button(root, text="שלח", command=on_submit)
submit_button.pack(pady=(0, 10))

root.mainloop()
