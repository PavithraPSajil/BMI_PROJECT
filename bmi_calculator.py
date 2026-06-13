import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "bmi_data.csv"

# ---------------- BMI CATEGORY ---------------- #

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# ---------------- SAVE DATA ---------------- #

def save_data(name, weight, height, bmi, category):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Name", "Weight", "Height", "BMI", "Category"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            weight,
            height,
            round(bmi, 2),
            category
        ])

# ---------------- CALCULATE BMI ---------------- #

def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        # Validation
        if name == "":
            messagebox.showerror("Error", "Please enter name")
            return

        if weight <= 0 or weight > 300:
            messagebox.showerror("Error", "Enter valid weight")
            return

        if height_cm <= 50 or height_cm > 300:
            messagebox.showerror("Error", "Enter valid height in cm")
            return

        # Convert cm to meters
        height_m = height_cm / 100

        bmi = weight / (height_m ** 2)
        category = bmi_category(bmi)

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}"
        )

        save_data(name, weight, height_cm, bmi, category)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# ---------------- VIEW HISTORY ---------------- #

def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("700x400")
    history_window.configure(bg="#f0f8ff")

    tree = ttk.Treeview(history_window)

    tree["columns"] = (
        "Date",
        "Name",
        "Weight",
        "Height",
        "BMI",
        "Category"
    )

    tree.column("#0", width=0, stretch=tk.NO)

    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER, width=100)
        tree.heading(col, text=col)

    if os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for i, row in enumerate(reader):
                tree.insert(
                    parent="",
                    index="end",
                    iid=i,
                    values=row
                )

    tree.pack(fill="both", expand=True)

# ---------------- SHOW GRAPH ---------------- #

def show_graph():
    names = []
    bmi_values = []

    if not os.path.isfile(FILE_NAME):
        messagebox.showerror("Error", "No data available")
        return

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            names.append(row["Name"])
            bmi_values.append(float(row["BMI"]))

    if len(bmi_values) == 0:
        messagebox.showerror("Error", "No BMI records found")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(names, bmi_values, marker='o')
    plt.title("BMI Trend Analysis")
    plt.xlabel("Users")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.show()

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("500x600")
root.configure(bg="#1e1e2f")

title = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 24, "bold"),
    bg="#1e1e2f",
    fg="white"
)
title.pack(pady=20)

# Name

tk.Label(
    root,
    text="Enter Name",
    font=("Arial", 12),
    bg="#1e1e2f",
    fg="white"
).pack()

name_entry = tk.Entry(font=("Arial", 14), width=25)
name_entry.pack(pady=10)

# Weight

tk.Label(
    root,
    text="Weight (kg)",
    font=("Arial", 12),
    bg="#1e1e2f",
    fg="white"
).pack()

weight_entry = tk.Entry(font=("Arial", 14), width=25)
weight_entry.pack(pady=10)

# Height

tk.Label(
    root,
    text="Height (cm)",
    font=("Arial", 12),
    bg="#1e1e2f",
    fg="white"
).pack()

height_entry = tk.Entry(font=("Arial", 14), width=25)
height_entry.pack(pady=10)

# Calculate Button

calc_button = tk.Button(
    root,
    text="Calculate BMI",
    font=("Arial", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5,
    command=calculate_bmi
)
calc_button.pack(pady=20)

# Result Label

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 16, "bold"),
    bg="#1e1e2f",
    fg="#00ffcc"
)
result_label.pack(pady=20)

# History Button

history_button = tk.Button(
    root,
    text="View History",
    font=("Arial", 12, "bold"),
    bg="#2196F3",
    fg="white",
    command=view_history
)
history_button.pack(pady=10)

# Graph Button

graph_button = tk.Button(
    root,
    text="Show BMI Graph",
    font=("Arial", 12, "bold"),
    bg="#ff9800",
    fg="white",
    command=show_graph
)
graph_button.pack(pady=10)

# Exit Button

exit_button = tk.Button(
    root,
    text="Exit",
    font=("Arial", 12, "bold"),
    bg="#f44336",
    fg="white",
    command=root.quit
)
exit_button.pack(pady=20)

root.mainloop()