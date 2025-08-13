import sqlite3
import tkinter as tk
from tkinter import messagebox, Label

# import os
# print(os.path.abspath("records.db"))
class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Records")

        # centring the opening window
        self.centring_the_app()

        # connecting code to the database
        self.conn = sqlite3.connect("E:\Codes\Python\Basic DataBase\ records.db")  # make it so that it can create a new database in the same folder
        cursor = self.conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS records
               (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   phone TEXT UNIQUE,
                   residence TEXT,
                   email TEXT
               );'''
        )
        self.conn.commit()

        # creating a frame container
        self.tableFrame = tk.Frame(self.root)
        self.tableFrame.pack(fill='x')
        self.column_headings = ['S.No','Id', 'Name', 'Phone', 'Residence', 'Email']

        # creating 6 columns
        for i in range(0, 6):
            self.tableFrame.columnconfigure(i, weight=1)

        # creating the headings
        for column_number, heading_text in enumerate(self.column_headings):
            table_headings = tk.Label(self.tableFrame, text=heading_text, font=('Times New Roman', 16), borderwidth=1,
                                      relief='solid')
            table_headings.grid(row=0, column=column_number, padx=1, pady=1, sticky="we")

        self.number_of_rows = 1

        self.populate_the_ui()  # adding the data of the database

        # creating a frame to hold the Entry (input fields)
        self.EntryFrame = tk.Frame(self.root)
        self.EntryFrame.pack(side='bottom', fill='x', pady=20)

        # creating 4 entries
        self.input_fields = []
        self.input_labels = ['Name','Phone','Residence','Email']
        for i, labels in enumerate(self.input_labels):

            self.entry_label = tk.Label(self.EntryFrame, text=labels, font=('Times New Roman', 14))
            self.entry_label.grid(row=i, column=0, padx=1, pady=1, sticky="we")

            entry = tk.Entry(self.EntryFrame, borderwidth=1, relief='solid', width=30)
            self.input_fields.append(entry)  # storing the entry fields
            entry.grid(row=i, column=1, padx=1, pady=1)

        # adding a menubar
        # adding a menubar like the numerous tabs in notepad,excel etc
        self.menubar = tk.Menu(self.root)
        self.delete_menu = tk.Menu(self.menubar,tearoff=0)
        self.delete_menu.add_command(label='Delete',command=self.delete_entry)
        self.menubar.add_cascade(menu=self.delete_menu, label="File")  # adding the tabs to the menubar
        self.root.config(menu=self.menubar)  # adding the menubar to the root


        self.addBtn = tk.Button(self.EntryFrame, text='Add', font=('Times New Roman', 16), command=self.adding_inputs)
        self.addBtn.grid(row=1, column=2, padx=20)

        self.root.mainloop()
        self.conn.close()

    def centring_the_app(self):
        width = 800
        height = 600

        # get screen dimensions
        screen_width = self.root.winfo_screenwidth()  # Fixed method name
        screen_height = self.root.winfo_screenheight()  # Fixed method name

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")  # Fixed positioning

        label = tk.Label(self.root, text="Your Entries", font=('Times New Roman', 16))
        label.pack(padx=10, pady=10)

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

            # inserting the data into the database
            cursor = self.conn.cursor()
            values = [entry.get().strip() for entry in self.input_fields]
            cursor.execute('''
                           INSERT INTO records (name, phone, residence, email)
                           VALUES (?, ?, ?, ?)
                           ''', values)
            self.conn.commit()

            # get the ID of the newly inserted record
            new_id = cursor.lastrowid

            #   display the new record in the UI

            # adding the serial number
            serial_entry = tk.Label(self.tableFrame, text=self.number_of_rows,
                                font=('Times New Roman', 12),
                                borderwidth=1, relief='solid')
            serial_entry.grid(row=self.number_of_rows, column=0, padx=1, pady=1, sticky="we")

            #  adding the ID field updated entry
            id_entry = tk.Label(self.tableFrame, text=new_id,
                                font=('Times New Roman', 12),
                                borderwidth=1, relief='solid')
            id_entry.grid(row=self.number_of_rows, column=1, padx=1, pady=1, sticky="we")

            # pushing the rest info
            for i, entry in enumerate(self.input_fields):
                value = entry.get()
                new_entry = tk.Label(self.tableFrame, text=value, font=('Times New Roman', 12), borderwidth=1,
                                     relief='solid')
                new_entry.grid(row=self.number_of_rows, column=i + 2, padx=1, pady=1, sticky="we")
            self.number_of_rows = self.number_of_rows + 1

            # clearing all the fields
            for entry in self.input_fields:
                entry.delete(0, tk.END)

    def populate_the_ui(self):
        # loading the data in the database to the interface
        cursor = self.conn.cursor()
        cursor.execute('''
                       SELECT id, name, phone, residence, email
                       FROM records
                       ORDER BY id
                       ''')
        data = cursor.fetchall()

        # creating 6 columns
        # for i in range(0, 6):
        #     self.tableFrame.columnconfigure(i, weight=1)

        # # creating the headings
        # for column_number, heading_text in enumerate(self.column_headings):
        #     table_headings = tk.Label(self.tableFrame, text=heading_text, font=('Times New Roman', 16), borderwidth=1,
        #                               relief='solid')
        #     table_headings.grid(row=0, column=column_number+1, padx=1, pady=1, sticky="we")

        # self.number_of_rows = 1

        # filling the serial number first
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM records;
        ''')
        no_of_rows = cursor.fetchone()[0]

        for i in range(0,no_of_rows):
            serial_no = tk.Label(self.tableFrame,text=i+1,font=('Times New Roman',12),borderwidth=1,relief='solid')
            serial_no.grid(row=i+1,column=0,padx=1,pady=1,sticky="we")

        # adding the data from the database
        for row in data:
            for col_index, value in enumerate(row):
                new_entry = tk.Label(self.tableFrame, text=value,
                                     font=('Times New Roman', 12),
                                     borderwidth=1, relief='solid')
                new_entry.grid(row=self.number_of_rows, column=col_index+1,
                               padx=1, pady=1, sticky="we")
            self.number_of_rows += 1

    def delete_entry(self):
        """Function to open the custom dialog box."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Item")
        dialog.geometry("300x100")
        dialog.transient(self.root)  # Make the dialog a child of the main window
        dialog.grab_set()  # Make it modal

        # centring the dialog box
        # get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - 100) // 2
        y = (screen_height - 300) // 2

        dialog.geometry(f"{300}x{100}+{x}+{y}")  # Fixed positioning

        # Label and Entry widgets
        tk.Label(dialog, text="Enter the id of entry: ").pack(pady=5)
        entry = tk.Entry(dialog)
        entry.pack(pady=5)

        def on_ok():
            index_to_delete = entry.get().strip() # getting the id to delete
            if not index_to_delete.isdigit():
                messagebox.showerror("Error", "Please enter a valid numeric ID.")
                return

            id_to_delete = int(index_to_delete) # getting the id to delete
            cursor = self.conn.cursor()

            # check if the index exists before deleting
            cursor.execute("SELECT COUNT(*) FROM records WHERE id = ?", (id_to_delete,))
            if cursor.fetchone()[0] == 0:
                messagebox.showerror("Error", f"No record found with ID {id_to_delete}.")
                return
            
            # Delete the entry from the database
            cursor.execute("DELETE FROM records WHERE id = ?", (id_to_delete,))
            self.conn.commit()
    
            # Close the dialog
            dialog.destroy()

            # clearing the old widgets
            for widget in self.tableFrame.winfo_children():
                widget.destroy()

            # Reset the row counter
            self.number_of_rows = 1

            # Recreate the column configuration
            for i in range(0, 6):
                self.tableFrame.columnconfigure(i, weight=1)

            # Recreate the headings (fixed column indexing)
            for column_number, heading_text in enumerate(self.column_headings):
                table_headings = tk.Label(self.tableFrame, text=heading_text, font=('Times New Roman', 16), borderwidth=1,
                                          relief='solid')
                table_headings.grid(row=0, column=column_number, padx=1, pady=1, sticky="we")  # Fixed: removed +1

            # Repopulate with fresh data
            self.populate_the_ui()

            # Show success message
            #messagebox.showinfo("Success", f"Record with ID {id_to_delete} deleted successfully.")

            # creating the column headings
            # creating 6 columns
            # for i in range(0, 6):
            #     self.tableFrame.columnconfigure(i, weight=1)

            # # creating the headings
            # for column_number, heading_text in enumerate(self.column_headings):
            #     table_headings = tk.Label(self.tableFrame, text=heading_text, font=('Times New Roman', 16), borderwidth=1,
            #                               relief='solid')
            #     table_headings.grid(row=0, column=column_number+1, padx=1, pady=1, sticky="we")

            # self.populate_the_ui()
            # # Show success message
            # messagebox.showinfo("Success", f"Record with ID {id_to_delete} deleted successfully.")



            # dialog.destroy()

            # adding the new widgets
            #self.populate_the_ui()

            # Reset row count and repopulate the UI from the database
            # self.number_of_rows = 1
            # self.populate_the_ui()
            # dialog.destroy()

        def on_cancel():
            dialog.destroy()

        # OK and Cancel buttons
        tk.Button(dialog, text="OK", command=on_ok).pack(side='left', padx=10)
        tk.Button(dialog, text="Cancel", command=on_cancel).pack(side='right', padx=10)

        # Set focus on the entry field
        entry.focus_set()




MyGUI()