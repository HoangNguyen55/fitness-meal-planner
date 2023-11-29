import tkinter as tk
import mysql.connector
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
# IMPORTANT: make sure you download mysqlworkbench and make a new local connection to the server, save your user and
# password, user is usually root and password is whatever password you choose. execute the scripts to initilize the
# databse
# You need to pip install pillow, tkinter, mysql-connector-python Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Matthew@1499.",  # change to your password
    database="fitnessplanner"
)


# Function to add user details to the database
def input_metrics():
    try:
        cursor = db.cursor()
        query = ("INSERT INTO Users (Name, Weight, Height, MuscleMass, FitnessGoal, Preferences) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        data = (name_entry.get(), weight_entry.get(), height_entry.get(),
                muscle_mass_entry.get(), fitness_goal_entry.get(), preferences_entry.get())
        cursor.execute(query, data)
        db.commit()
        messagebox.showinfo("Success", "User data added successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    finally:
        cursor.close()


# Function to display meal recommendations
def display_meals():
    try:
        cursor = db.cursor()
        query = "SELECT Name, Calories, Protein, Carbs, Fats FROM Meals ORDER BY RAND() LIMIT 5"
        cursor.execute(query)
        result = cursor.fetchall()
        meals = "\n".join([f"{name} - Calories: {cal}, Protein: {prot}, Carbs: {carbs}, Fats: {fats}"
                           for name, cal, prot, carbs, fats in result])
        messagebox.showinfo("Meal Recommendations", meals)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    finally:
        cursor.close()


# Function to display exercise recommendations
def display_exercises():
    try:
        cursor = db.cursor()
        query = "SELECT Name, Difficulty, TargetMuscleGroup FROM Exercises ORDER BY RAND() LIMIT 5"
        cursor.execute(query)
        result = cursor.fetchall()
        exercises = "\n".join([f"{name} - Difficulty: {diff}, Target Muscle Group: {muscle}"
                               for name, diff, muscle in result])
        messagebox.showinfo("Exercise Recommendations", exercises)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    finally:
        cursor.close()


# Function to validate and submit user input
def submit_user_data():
    if not all([name_entry.get(), weight_entry.get(), height_entry.get()]):
        messagebox.showwarning("Warning", "Please fill all required fields")
        return
    input_metrics()


# Function to display data in a new window
def display_data(title, data):
    top = Toplevel()
    top.title(title)
    message = "\n".join(data)
    tk.Message(top, text=message, padx=20, pady=20).pack()


# Main application window
app = tk.Tk()
app.title("Personalized Fitness Planner")

# Using relative sizing instead of fixed size for responsiveness
app.geometry("400x300")
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1, uniform="row")
app.grid_rowconfigure(1, weight=1, uniform="row")
# ... [Configure weights for all rows] ...

# Set a background image that scales with the window size
def resize_background(event):
    image = Image.open("C:\\Users\mathe\PycharmProjects\\fitness-meal-planner\\UI\\fitness.png")  # change path the path you have
    image = image.resize((event.width, event.height), Image.Resampling.LANCZOS)

    background_image = ImageTk.PhotoImage(image)
    background_label.config(image=background_image)
    background_label.image = background_image  # Avoid garbage collection

background_label = tk.Label(app)
background_label.place(relwidth=1, relheight=1)
app.bind("<Configure>", resize_background)

# Styling for labels and entries
label_style = {"bg": "lightblue", "font": ("Arial", 12)}
entry_style = {"font": ("Arial", 12)}

# User input fields
tk.Label(app, text="Name", **label_style).grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(app, **entry_style)
name_entry.grid(row=0, column=1, sticky="e")

tk.Label(app, text="Weight (kg)", **label_style).grid(row=1, column=0, sticky="w")
weight_entry = tk.Entry(app, **entry_style)
weight_entry.grid(row=1, column=1, sticky="e")

tk.Label(app, text="Height (cm)", **label_style).grid(row=2, column=0, sticky="w")
height_entry = tk.Entry(app, **entry_style)
height_entry.grid(row=2, column=1, sticky="e")

tk.Label(app, text="Muscle Mass (%)", **label_style).grid(row=3, column=0, sticky="w")
muscle_mass_entry = tk.Entry(app, **entry_style)
muscle_mass_entry.grid(row=3, column=1, sticky="e")

tk.Label(app, text="Fitness Goal", **label_style).grid(row=4, column=0, sticky="w")
fitness_goal_entry = tk.Entry(app, **entry_style)
fitness_goal_entry.grid(row=4, column=1, sticky="e")

tk.Label(app, text="Preferences", **label_style).grid(row=5, column=0, sticky="w")
preferences_entry = tk.Entry(app, **entry_style)
preferences_entry.grid(row=5, column=1, sticky="e")


# Buttons for actions
submit_btn = tk.Button(app, text="Submit", command=submit_user_data, bg="green", fg="white")
submit_btn.grid(row=6, column=0, columnspan=2, pady=10)

meal_btn = tk.Button(app, text="Get Meal Recommendations", command=display_meals, bg="blue", fg="white")
meal_btn.grid(row=7, column=0, columnspan=2, pady=10)

exercise_btn = tk.Button(app, text="Get Exercise Recommendations", command=display_exercises, bg="purple", fg="white")
exercise_btn.grid(row=8, column=0, columnspan=2, pady=10)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        db.close()
        app.destroy()


app.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI
app.mainloop()
