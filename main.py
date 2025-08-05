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

        for i in range(0,4):
            self.tableFrame.columnconfigure(i,weight=1)

        for column_heading, heading_text in enumerate(self.column_headings):
            self.table_headings = tk.Label(self.tableFrame, text=heading_text,font=('Times New Roman',16))
            self.table_headings.grid(row=0,column=column_heading,sticky="we")


        self.tableFrame.pack(fill='x')


        self.add_button = tk.Button(self.root,text="Add",font=('Arial',13))
        self.add_button.pack()

        self.root.mainloop()



MyGUI()