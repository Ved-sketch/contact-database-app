import sqlite3
import tkinter as tk
from tkinter import messagebox, Label

from pyautogui import PRIMARY


class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Records")

        # centring the opening window
        width = 800
        height = 600

        # get screen dimensions
        screen_width = self.root.winfo_screenmmwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x+600}+{y}")

        self.label = tk.Label(self.root, text="Your Entries",font=('Times New Roman',16))
        self.label.pack(padx=10,pady=10)

        # creating a frame container
        self.tableFrame = tk.Frame(self.root)
        self.column_headings = ['Name','Phone','Residence','Email']

        # creating 4 columns
        for i in range(0,4):
            self.tableFrame.columnconfigure(i,weight=1)

        # connecting code to the database
        self.conn = sqlite3.connect("E:\Codes\Python\Basic DataBase\ records.db") # opening the connection to the database
        cursor = self.conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS records(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                residence TEXT,
                email TEXT
            );'''
        )
        self.conn.commit()

        # creating the headings
        for column_number, heading_text in enumerate(self.column_headings):
            table_headings = tk.Label(self.tableFrame, text=heading_text,font=('Times New Roman',16),borderwidth=1,relief='solid')
            table_headings.grid(row=0,column=column_number,padx=1,pady=1,sticky="we")
        self.tableFrame.pack(fill='x')

        self.number_of_rows = 1

        self.populate_the_ui() # adding the data of the database

        # creating a frame to hold the Entry (input fields)
        self.EntryFrame = tk.Frame(self.root)

        # creating 4 entries
        self.input_fields = []
        for i, column_heading in enumerate(self.column_headings):
            self.entry_label = tk.Label(self.EntryFrame, text=column_heading,font=('Times New Roman',14))
            self.entry_label.grid(row = i,column=0,padx=1,pady=1,sticky="we")

            entry = tk.Entry(self.EntryFrame,borderwidth=1,relief='solid',width=30)
            self.input_fields.append(entry) # storing the entry fields
            entry.grid(row=i,column=1,padx=1,pady=1)
        self.EntryFrame.pack(side='bottom',fill='x',pady=20)

        self.addBtn = tk.Button(self.EntryFrame, text='Add', font=('Times New Roman',16),command=self.adding_inputs)
        self.addBtn.grid(row=1,column=2,padx = 20)



        self.root.mainloop()
        self.conn.close()

    def empty_fields(self):
        for entry in self.input_fields:
            if entry.get().strip() == "":
                messagebox.showwarning(title="Warning", message="Please fill all the information")
                return True
        return False

    def adding_inputs(self):
        if self.empty_fields():
            return
        else:
            # push the info in the table
            temp = self.input_fields
            for i,entry in enumerate(temp):
                value = entry.get()
                new_entry = tk.Label(self.tableFrame,text=value,font=('Times New Roman',12),borderwidth=1,relief='solid')
                new_entry.grid(row=self.number_of_rows,column=i,padx=1,pady=1,sticky="we")
            self.number_of_rows = self.number_of_rows+1

            # adding inputs into the database
            cursor = self.conn.cursor()
            values = [entry.get().strip() for entry in self.input_fields]
            cursor.execute('''
                INSERT INTO records (name,phone,residence,email)
                VALUES (?,?,?,?)
            ''',values)
            self.conn.commit()

            # clearing all the fields
            for entry in self.input_fields:
                entry.delete(0, tk.END)

    def populate_the_ui(self):
        # loading the data in the database to the interface
        cursor = self.conn.cursor()
        cursor.execute('''
                       SELECT name, phone, residence, email
                       FROM records
                       ORDER BY id
                       ''')
        data = cursor.fetchall()

        for row in data:  # row = ("Alice", "123...", "Home", "email")
            for col_index, value in enumerate(row):
                new_entry = tk.Label(self.tableFrame, text=value,
                                     font=('Times New Roman', 12),
                                     borderwidth=1, relief='solid')
                new_entry.grid(row=self.number_of_rows, column=col_index,
                               padx=1, pady=1, sticky="we")
            self.number_of_rows += 1


MyGUI()