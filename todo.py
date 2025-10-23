import customtkinter as ctk
from tkinter import messagebox, simpledialog, Listbox, END
import json
import os

SAVE_FILE = "tasks.json"

ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Smart To-Do List 📝")

app.state("zoomed")   
app.resizable(True, True) 

tasks = []

def load_tasks():
    """Load tasks from a JSON file when the app starts."""
    global tasks
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                tasks = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            tasks = []
    update_listbox()

def save_tasks():
    """Save current tasks to JSON file."""
    with open(SAVE_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def update_listbox():
    task_box.delete(0, END)
    for task in tasks:
        task_box.insert(END, task)

def add_task():
    task = entry.get().strip()
    if task:
        tasks.append(task)
        save_tasks()
        update_listbox()
        entry.delete(0, "end")
    else:
        messagebox.showwarning("Empty Task", "Please enter a task before adding.")

def delete_task():
    try:
        selected = task_box.curselection()[0]
        del tasks[selected]
        save_tasks()
        update_listbox()
    except IndexError:
        messagebox.showinfo("No Selection", "Please select a task to delete.")

def edit_task():
    try:
        selected = task_box.curselection()[0]
        current_task = tasks[selected]
        new_task = simpledialog.askstring("Edit Task", "Modify your task:", initialvalue=current_task)
        if new_task:
            tasks[selected] = new_task.strip()
            save_tasks()
            update_listbox()
    except IndexError:
        messagebox.showinfo("No Selection", "Please select a task to edit.")

def clear_all():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
        tasks.clear()
        save_tasks()
        update_listbox()

title_label = ctk.CTkLabel(app, text="Smart To-Do List", font=("Poppins", 36, "bold"))
title_label.pack(pady=(30, 20))

entry_frame = ctk.CTkFrame(app, corner_radius=15)
entry_frame.pack(pady=10, padx=40, fill="x")

entry = ctk.CTkEntry(entry_frame, placeholder_text="Add a new task...", height=50, font=("Poppins", 16))
entry.pack(side="left", expand=True, fill="x", padx=20, pady=10)

add_button = ctk.CTkButton(entry_frame, text="+ Add", width=120, height=45, command=add_task)
add_button.pack(side="right", padx=20)

list_frame = ctk.CTkFrame(app, corner_radius=15)
list_frame.pack(pady=20, padx=40, fill="both", expand=True)

task_box = Listbox(list_frame, height=15, font=("Poppins", 16),
                   bg="#1e1e1e", fg="white", selectbackground="#00cc66",
                   selectforeground="black", bd=0, highlightthickness=0)
task_box.pack(padx=20, pady=20, fill="both", expand=True)

button_frame = ctk.CTkFrame(app, corner_radius=15)
button_frame.pack(pady=15, padx=40, fill="x")

edit_btn = ctk.CTkButton(button_frame, text="✏️ Edit", width=120, height=45, fg_color="#ff9933", command=edit_task)
edit_btn.pack(side="left", expand=True, padx=10, pady=10)

delete_btn = ctk.CTkButton(button_frame, text="🗑 Delete", width=120, height=45, fg_color="#ff4d4d", command=delete_task)
delete_btn.pack(side="left", expand=True, padx=10, pady=10)

clear_btn = ctk.CTkButton(button_frame, text="🚫 Clear All", width=120, height=45, fg_color="#6666ff", command=clear_all)
clear_btn.pack(side="left", expand=True, padx=10, pady=10)

footer = ctk.CTkLabel(app, text="✨ Tasks are auto-saved — Stay productive!", font=("Poppins", 14))
footer.pack(pady=20)

load_tasks()
app.mainloop()
