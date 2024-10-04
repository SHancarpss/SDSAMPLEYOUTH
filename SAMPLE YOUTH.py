import sqlite3
import random
import string
from tkinter import *
from tkinter import messagebox

# Initialize Tkinter window
root = Tk()
root.title("It's all about Youth!")
root.geometry("800x600")
root.configure(bg='black')

# Connect to SQLite Database or create it
conn = sqlite3.connect('youth_details.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                full_name TEXT NOT NULL,
                birthplace TEXT NOT NULL,
                birthday TEXT NOT NULL,
                address TEXT NOT NULL,
                favorite_color TEXT NOT NULL,
                favorite_food TEXT NOT NULL
            )''')

# Function to generate random codes
def generate_codes():
    codes = [''.join(random.choices(string.digits, k=6)) for _ in range(6)]
    return codes

# Function to validate answers
def validate_answers():
    if answer1.get() in ["Lovely May G. Ama", "Ma. Reanne M. Carnasa"] and answer2.get() == "July 2, 2020":
        # Show the last question
        question3_frame.pack(pady=10)
    else:
        messagebox.showerror("Error", "Incorrect answers. Please try again.")

# Function to check the last question and generate codes
def check_last_question():
    if answer3.get() != "":
        codes = generate_codes()
        messagebox.showinfo("Generated Codes", f"Your codes are: {', '.join(codes)}")
        # Here you can save the codes or use them as needed
    else:
        messagebox.showerror("Error", "Please answer the last question.")

# Function to save member information
def save_member():
    username = username_entry.get()
    full_name = full_name_entry.get()
    birthplace = birthplace_entry.get()
    birthday = birthday_entry.get()
    address = address_entry.get()
    favorite_color = favorite_color_entry.get()
    favorite_food = favorite_food_entry.get()

    if username and full_name and birthplace and birthday and address and favorite_color and favorite_food:
        c.execute("INSERT INTO members (username, full_name, birthplace, birthday, address, favorite_color, favorite_food) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (username, full_name, birthplace, birthday, address, favorite_color, favorite_food))
        conn.commit()
        messagebox.showinfo("Success", "Member information saved successfully")
        clear_entries()
        retrieve_members()
    else:
        messagebox.showerror("Error", "All fields are required")

# Function to retrieve and display members
def retrieve_members():
    members_listbox.delete(0, END)
    for row in c.execute("SELECT * FROM members"):
        members_listbox.insert(END, f"{row[1]} - {row[2]}")

def clear_entries():
    username_entry.delete(0, END)
    full_name_entry.delete(0, END)
    birthplace_entry.delete(0, END)
    birthday_entry.delete(0, END)
    address_entry.delete(0, END)
    favorite_color_entry.delete(0, END)
    favorite_food_entry.delete(0, END)

# UI Elements for login
login_frame = Frame(root, bg='black')
login_frame.pack(pady=20)

Label(login_frame, text="Enter Password:", bg='black', fg='white').pack()
password_entry = Entry(login_frame, show='*')
password_entry.pack()

def login():
    if password_entry.get() == "070220":  # Permanent code
        login_frame.pack_forget()
        setup_ui()
    else:
        messagebox.showerror("Error", "Incorrect password")

login_button = Button(login_frame, text="Login", command=login, bg='green', fg='white')
login_button.pack()

# UI Elements for questions
question_frame = Frame(root, bg='black')
question_frame.pack(pady=10)

Label(question_frame, text="Sino ang pasimuno ng Youth?", bg='blue', fg='white').pack()
answer1 = Entry(question_frame)
answer1.pack()

Label(question_frame, text="Anong exact date ginawa ang gc ng Youth?", bg='white', fg='black').pack()
answer2 = Entry(question_frame)
answer2.pack()

question3_frame = Frame(root, bg='black')

Label(question3_frame, text="Paano ka nakilala ni Lovely?", bg='black', fg='white').pack()
answer3 = Entry(question3_frame)
answer3.pack()

check_button = Button('question3_frame, text=Check Answers, command=check_last_question, bg='green', fg='white')
check_button.pack(pady=10)

# UI Elements for adding member information
def setup_ui():
    # Clear the previous frames
    question_frame.pack_forget()
    question3_frame.pack_forget()

    # Member information frame
    member_frame = Frame(root, bg='black')
    member_frame.pack(pady=20)

    Label(member_frame, text="Add Member Information", bg='black', fg='white', font=("Helvetica", 16)).pack()

    global username_entry, full_name_entry, birthplace_entry, birthday_entry, address_entry, favorite_color_entry, favorite_food_entry

    Label(member_frame, text="Username:", bg='black', fg='white').pack()
    username_entry = Entry(member_frame)
    username_entry.pack()

    Label(member_frame, text="Full Name:", bg='black', fg='white').pack()
    full_name_entry = Entry(member_frame)
    full_name_entry.pack()

    Label(member_frame, text="Birthplace:", bg='black', fg='white').pack()
    birthplace_entry = Entry(member_frame)
    birthplace_entry.pack()

    Label(member_frame, text="Birthday:", bg='black', fg='white').pack()
    birthday_entry = Entry(member_frame)
    birthday_entry.pack()

    Label(member_frame, text="Address:", bg='black', fg='white').pack()
    address_entry = Entry(member_frame)
    address_entry.pack()

    Label(member_frame, text="Favorite Color:", bg='black', fg='white').pack()
    favorite_color_entry = Entry(member_frame)
    favorite_color_entry.pack()

    Label(member_frame, text="Favorite Food:", bg='black', fg='white').pack()
    favorite_food_entry = Entry(member_frame)
    favorite_food_entry.pack()

    save_button = Button(member_frame, text="Save", command=save_member, bg='green', fg='white')
    save_button.pack(pady=5)

    delete_button = Button(member_frame, text="Delete", command=lambda: delete_member(), bg='red', fg='white')
    delete_button.pack(pady=5)

    duplicate_button = Button(member_frame, text="Duplicate", command=lambda: duplicate_member(), bg='blue', fg='white')
    duplicate_button.pack(pady=5)

    undo_button = Button(member_frame, text="Undo", command=lambda: undo_action(), bg='yellow', fg='black')
    undo_button.pack(pady=5)

    redo_button = Button(member_frame, text="Redo", command=lambda: redo_action(), bg='orange', fg='black')
    redo_button.pack(pady=5)

    global members_listbox
    members_listbox = Listbox(member_frame, width=50)
    members_listbox.pack(pady=10)
    retrieve_members()

def delete_member():
    selected_item = members_listbox.curselection()
    if selected_item:
        item_index = selected_item[0]
        item = members_listbox.get(item_index).split(" - ")[0]
        c.execute("DELETE FROM members WHERE username=?", (item,))
        conn.commit()
        messagebox.showinfo("Success", "Member deleted successfully")
        retrieve_members()
    else:
        messagebox.showerror("Error", "Please select a member to delete")

def duplicate_member():
    selected_item = members_listbox.curselection()
    if selected_item:
        item_index = selected_item[0]
        item = members_listbox.get(item_index).split(" - ")[0]
        # Fetch the member details
        c.execute("SELECT * FROM members WHERE username=?", (item,))
        member = c.fetchone()
        if member:
            c.execute("INSERT INTO members (username, full_name, birthplace, birthday, address, favorite_color, favorite_food) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (member[1], member[2], member[3], member[4], member[5], member[6], member[7]))
            conn.commit()
            messagebox.showinfo("Success", "Member duplicated successfully")
            retrieve_members()
    else:
        messagebox.showerror("Error", "Please select a member to duplicate")

def undo_action():
    # Implement undo functionality if needed
    messagebox.showinfo("Info", "Undo functionality not implemented yet.")

def redo_action():
    # Implement redo functionality if needed
    messagebox.showinfo("Info", "Redo functionality not implemented yet.")

# Start Tkinter event loop
root.mainloop()

# Close the database connection when the program exits
conn.close()

