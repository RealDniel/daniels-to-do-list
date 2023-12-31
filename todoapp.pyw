#imports
import tkinter as tk
import pandas as pd
import pygame

#Creating the window using tkinter
root = tk.Tk()
root.title("Daniel's To-Do List")
root.geometry("900x700")
root.configure(bg="#293132")
label = tk.Label(root, text="To-Do List", font=("Georgia", 22), bg="#293132", fg="#9FB1BC")
label.pack()

#initializing pygame stuff for sound effects
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("yay.mp3")

#Main list of tasks using incomplete_tasks.csv - Contents of the list are added in line 84
task_listbox = tk.Listbox(root, width=60, height=700, bg="#4F5165", fg="#9FB1BC", font=("Georgia", 12))
task_listbox.pack(side=tk.LEFT, padx=10, pady=10)

#Frame for the menu - Buttons must be added later so they can utilize the functions (line 87)
menu = tk.Frame(root, bg="#293132")
menu.pack(expand=True, padx=10, pady=10)

title_entry = tk.Entry(menu, width=30, font=("Georgia", 12))
title_entry.pack(fill=tk.X, padx=5, pady=5)

desc_entry = tk.Text(menu, width=30, height=15, font=("Georgia", 12))
desc_entry.pack(fill=tk.X, padx=5, pady=5)

#Creating the task class - Telling the code what a "task" is.
class Task:
    def __init__(self, title, desc, status='Incomplete'):
        self.title = title
        self.desc = desc
        self.status = status

#Functions that save/load tasks to/from the csv files
def save_tasks(unsaved_tasks, file_to_save):
    data_to_save = {
        'Title': [task.title for task in unsaved_tasks],
        'Description': [task.desc for task in unsaved_tasks],
        'Status': [task.status for task in unsaved_tasks]
    }
    df = pd.DataFrame(data_to_save)
    df.to_csv(file_to_save, index=False)

def load_tasks(file_to_read):
    df = pd.read_csv(file_to_read)
    tasks = []
    for index, row in df.iterrows():
        tasks.append(Task(row['Title'], row['Description'], row['Status']))
    return tasks

def refresh_tasks():
    task_listbox.delete(0, tk.END)
    for task in loaded_tasks:
        task_listbox.insert(tk.END, f"{task.title} --- {task.desc}")

#Making a Loaded Tasks list that will display in the GUI
loaded_tasks = load_tasks("incomplete_tasks.csv")

#Adding functions that manipulate tasks. Correspond to their buttons.
def add_task(title, desc):
    if title and desc:
        new_task = Task(title, desc)
        loaded_tasks.append(new_task)
        refresh_tasks()
        title_entry.delete(0, tk.END)
        desc_entry.delete("1.0", tk.END)
        title_entry.focus_set()

def remove_task():
    selected_index = task_listbox.curselection()
    if selected_index:
        index_to_delete = selected_index[0]
        del loaded_tasks[index_to_delete]
        refresh_tasks()
        title_entry.focus_set()
        pygame.mixer.music.play()

#Initial contents for the list box
refresh_tasks()    

#Buttons for menu
add_task_button = tk.Button(menu, text="Submit New Task", command=lambda: add_task(title_entry.get(), desc_entry.get("1.0", tk.END).strip()))
add_task_button.pack(fill=tk.X, padx=5, pady=(5, 100))

del_task_button = tk.Button(menu, text="Complete Selected Task", command=lambda: remove_task())
del_task_button.pack(fill=tk.X, padx=5, pady=5)

#When window is closed, data saves to incomplete_tasks.csv
def close_window(unsaved_tasks, file_to_save):
    save_tasks(unsaved_tasks, file_to_save)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", lambda: close_window(loaded_tasks, "incomplete_tasks.csv"))

#Run Tkinter main loop - keeps the window open and ready to receive user input
root.mainloop()