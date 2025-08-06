# class Info:
#     def __init__(self,name,address,email,phone):
#         self.name = name
#         self.address = address
#         self.email = email
#         self.phone = phone
#
#
# person1 = Info("Alex","Pahad ke piche","Alex@yahoo.com",999555666)
# print(person1.name)

import tkinter as tk
from tkinter import messagebox, Label


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

        # creating the headings
        for column_heading, heading_text in enumerate(self.column_headings):
            table_headings = tk.Label(self.tableFrame, text=heading_text,font=('Times New Roman',16),borderwidth=1,relief='solid')
            table_headings.grid(row=0,column=column_heading,padx=1,pady=1,sticky="we")
        self.tableFrame.pack(fill='x')

        # first creating a frame to hold the Entry
        self.EntryFrame = tk.Frame(self.root)

        # creating 4 entries
        for i, column_heading in enumerate(self.column_headings):
            self.entry_label = tk.Label(self.EntryFrame, text=column_heading,font=('Times New Roman',14))
            self.entry_label.grid(row = i,column=0,padx=1,pady=1,sticky="we")

            entry = tk.Entry(self.EntryFrame,borderwidth=1,relief='solid',width=30)
            entry.grid(row=i,column=1,padx=1,pady=1)
        self.EntryFrame.pack(side='bottom',fill='x',pady=20)

        self.addBtn = tk.Button(self.EntryFrame, text='Add', font=('Times New Roman',16))
        self.addBtn.grid(row=1,column=2,padx = 20)

        # creating the input fields

        

        self.root.mainloop()



MyGUI()