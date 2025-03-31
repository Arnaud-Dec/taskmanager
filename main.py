import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pytest


class TaskManager:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                due_date TEXT,
                status TEXT NOT NULL CHECK(status IN ('À faire', 'En cours', 'Terminé'))
            )
        ''')
        self.conn.commit()
    
    def add_task(self, description, due_date, status="À faire"):
        if not description:
            raise ValueError("La description ne peut pas être vide.")
        try:
            if due_date:
                datetime.strptime(due_date, "%Y-%m-%d")
            self.cursor.execute(
                '''INSERT INTO tasks (description, due_date, status) VALUES (?, ?, ?)''',
                (description, due_date, status)
            )
            self.conn.commit()
        except ValueError:
            raise ValueError("Le format de la date doit être YYYY-MM-DD")

    
    def get_tasks(self):
        self.cursor.execute("SELECT * FROM tasks ORDER BY due_date ASC")
        return self.cursor.fetchall()
    
    def update_task_status(self, task_id, new_status):
        self.cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        self.conn.commit()
    
    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
    
class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Gestionnaire de Tâches")
        self.create_widgets()
        self.load_tasks()
    
    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid(row=0, column=0)
        
        self.desc_label = ttk.Label(self.frame, text="Description:")
        self.desc_label.grid(row=0, column=0)
        self.desc_entry = ttk.Entry(self.frame, width=40)
        self.desc_entry.grid(row=0, column=1)
        
        self.date_label = ttk.Label(self.frame, text="Echéance (YYYY-MM-DD):")
        self.date_label.grid(row=1, column=0)
        self.date_entry = ttk.Entry(self.frame, width=20)
        self.date_entry.grid(row=1, column=1)
        
        self.add_button = ttk.Button(self.frame, text="Ajouter Tâche", command=self.add_task)
        self.add_button.grid(row=2, columnspan=2)
        
        self.task_list = ttk.Treeview(self.frame, columns=("ID", "Description", "Echéance", "Statut"), show="headings")
        self.task_list.heading("ID", text="ID")
        self.task_list.heading("Description", text="Description")
        self.task_list.heading("Echéance", text="Echéance")
        self.task_list.heading("Statut", text="Statut")
        self.task_list.grid(row=3, columnspan=2)
        
        self.complete_button = ttk.Button(self.frame, text="Marquer comme Terminé", command=self.complete_task)
        self.complete_button.grid(row=4, column=0)
        
        self.delete_button = ttk.Button(self.frame, text="Supprimer Tâche", command=self.delete_task)
        self.delete_button.grid(row=4, column=1)
    
    def add_task(self):
        desc = self.desc_entry.get()
        due_date = self.date_entry.get()
        try:
            if desc:
                self.manager.add_task(desc, due_date)
                self.load_tasks()
                self.desc_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Erreur", "La description ne peut pas être vide.")
        except ValueError:
            messagebox.showerror("Erreur", "Le format de la date est incorrect.")
    
    def load_tasks(self):
        for item in self.task_list.get_children():
            self.task_list.delete(item)
        for task in self.manager.get_tasks():
            self.task_list.insert("", tk.END, values=task)
    
    def complete_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            task_id = self.task_list.item(selected_item, "values")[0]
            self.manager.update_task_status(task_id, "Terminé")
            self.load_tasks()
        else:
            messagebox.showwarning("Erreur", "Sélectionnez une tâche.")
    
    def delete_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            task_id = self.task_list.item(selected_item, "values")[0]
            self.manager.delete_task(task_id)
            self.load_tasks()
        else:
            messagebox.showwarning("Erreur", "Sélectionnez une tâche.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()

