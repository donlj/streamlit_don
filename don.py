import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime
import re

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Wellness Dashboard")
        self.root.geometry("400x250")

        tk.Label(root, text="Mental Wellness Logger", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(root, text="Open Entry Logger", command=self.open_logger, width=30).pack(pady=10)
        tk.Button(root, text="Open Statistics", command=self.open_stats, width=30).pack(pady=10)
        tk.Button(root, text="Exit", command=root.destroy, width=30).pack(pady=10)

    def open_logger(self):
        LoggerWindow(tk.Toplevel(self.root))

    def open_stats(self):
        StatsWindow(tk.Toplevel(self.root))

class LoggerWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Entry Logger")
        self.window.geometry("800x600")

        self.entries = []
        self.file_name = "mental_wellness_entries.xlsx"

        tk.Label(window, text="Mental Wellness Entry Logger", font=("Arial", 16, "bold")).pack(pady=10)

        frame = tk.Frame(window)
        frame.pack(pady=10)

        self.entries_dict = {}
        fields = ["Student Name", "Wellness Activity", "Me-Time Activity", "Screen-Free Time (mins)", "Frequency(eg. 3x, 2 times)"]

        for idx, field in enumerate(fields):
            tk.Label(frame, text=field + ":").grid(row=idx, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame, width=40)
            entry.grid(row=idx, column=1, padx=5)
            self.entries_dict[field] = entry

        self.status_var = tk.StringVar()
        tk.Label(window, textvariable=self.status_var, font=("Arial", 12, "italic"), fg="blue").pack()

        button_frame = tk.Frame(window)
        button_frame.pack()

        tk.Button(button_frame, text="Add Entry", command=self.add_entry).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_entry).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_all).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Save to Excel", command=self.save_to_excel).grid(row=0, column=3, padx=5)

        self.tree = ttk.Treeview(window, columns=("Name", "Wellness", "Me-Time", "Screen-Free", "Frequency", "Status"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill='both', expand=True)

    def determine_status(self, screen_time, wellness, me_time):
        return "Healthy" if screen_time >= 60 and wellness and me_time else "Needs More Me-Time"

    def validate_inputs(self):
        name = self.entries_dict["Student Name"].get().strip()
        wellness = self.entries_dict["Wellness Activity"].get().strip()
        me_time = self.entries_dict["Me-Time Activity"].get().strip()
        screen_time = self.entries_dict["Screen-Free Time (mins)"].get().strip()
        frequency = self.entries_dict["Frequency(eg. 3x, 2 times)"].get().strip()

        if not name or not re.match("^[A-Za-z ]+$", name):
            messagebox.showerror("Input Error", "Student Name is required and should only contain letters and spaces.")
            return None
        if not wellness or not re.match("^[A-Za-z ]+$", wellness):
            messagebox.showerror("Input Error", "Wellness Activity is required and should only contain letters and spaces.")
            return None
        if not me_time or not re.match("^[A-Za-z ]+$", me_time):
            messagebox.showerror("Input Error", "Me-Time Activity is required and should only contain letters and spaces.")
            return None
        if not screen_time.isdigit() or int(screen_time) <= 0:
            messagebox.showerror("Input Error", "Screen-Free Time must be a positive integer.")
            return None
        if not frequency or not re.match("^[0-9]+(x| times| per week)?$", frequency):
            messagebox.showerror("Input Error", "Frequency is required and should be in a valid format like '3x' or '3 times'.")
            return None

        return name, wellness, me_time, int(screen_time), frequency

    def add_entry(self):
        validated_data = self.validate_inputs()
        if validated_data:
            name, wellness, me_time, screen_time, frequency = validated_data
            status = self.determine_status(screen_time, wellness, me_time)
            self.status_var.set(status)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.tree.insert('', 'end', values=(name, wellness, me_time, screen_time, frequency, status))

            messagebox.showinfo("Success", "Entry added!")

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an entry to delete.")
            return
        for sel in selected:
            self.tree.delete(sel)
        messagebox.showinfo("Deleted", "Selected entry deleted.")

    def clear_all(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        messagebox.showinfo("Cleared", "All entries cleared.")

    def save_to_excel(self):
        rows = [self.tree.item(child)["values"] for child in self.tree.get_children()]
        if not rows:
            messagebox.showerror("Error", "No entries to save.")
            return

        df = pd.DataFrame(rows, columns=["Student Name", "Wellness Activity", "Me-Time Activity", "Screen-Free Time (mins)", "Frequency", "Status"])
        df.to_excel(self.file_name, index=False)
        messagebox.showinfo("Saved", f"Entries saved to {self.file_name}.")

class StatsWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Statistics")
        self.window.geometry("400x250")

        file_name = "mental_wellness_entries.xlsx"
        if not os.path.exists(file_name):
            tk.Label(window, text="No data available. Please save entries first.").pack(pady=20)
            return

        df = pd.read_excel(file_name)
        healthy_count = df[df["Status"] == "Healthy"].shape[0]
        needs_more_count = df[df["Status"] == "Needs More Me-Time"].shape[0]

        tk.Label(window, text=f"Total Entries: {df.shape[0]}", font=("Arial", 12)).pack(pady=10)
        tk.Label(window, text=f"Healthy: {healthy_count}", font=("Arial", 12)).pack(pady=10)
        tk.Label(window, text=f"Needs More Me-Time: {needs_more_count}", font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
