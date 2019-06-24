from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import datetime
import os
from database import Database
from tkUI import *

class MainMenu(Page):
    def __init__(self, master):
        super().__init__(master)

    def display(self):
        tablePane = ttk.Notebook(self.frame)
        tableViews = []
        for table in db.get_tables():
            tablePane.add(self.build_table_frame(table), text=table.name)
        tablePane.grid(row=1)

    def build_table_frame(self, table):
        tableFrame = Frame(self.frame)
        for columnIndex, header in enumerate(table.get_headers()):
            cell = Frame(tableFrame, relief=RAISED, borderwidth=1)
            Label(cell, text=header, font='Helvetica 9 bold').pack(padx=5, pady=5, anchor=W)
            cell.grid(row=0, column=columnIndex, sticky=NSEW)
        for rowIndex, record in enumerate(table.get_contents()):
            for columnIndex, field in enumerate(record):
                cell = Frame(tableFrame, relief=RAISED, borderwidth=2)
                Label(cell, text=field, font='Helvetica 9').pack(padx=5, pady=2, anchor=W)
                cell.grid(row=rowIndex + 2, column=columnIndex, sticky=NSEW)
        return tableFrame



class TableView(FrameStruct):
    def __init__(self, master, table, parent=None):
        super().__init__(master, parent)
        self.table = table

    def display(self):
        ttk.Separator(self.frame, orient=VERTICAL).grid(row=0, column=0, sticky="nsw")
        for columnIndex, header in enumerate(self.table.get_headers()):
            columnIndex += 1
            Label(self.frame, text=header).grid(row=0, column=columnIndex, padx=5)
            ttk.Separator(self.frame, orient=VERTICAL).grid(row=0, column=columnIndex + 1, sticky="nsw")
            ttk.Separator(self.frame, orient=HORIZONTAL).grid(row=1, column=columnIndex, sticky=EW)
        for rowIndex, record in enumerate(self.table.get_contents()):
            ttk.Separator(self.frame, orient=VERTICAL).grid(row=rowIndex + 2, column=0, sticky="nsw")
            for columnIndex, field in enumerate(record):
                columnIndex += 1
                Label(self.frame, text=field).grid(row=rowIndex + 2, column=columnIndex)
                ttk.Separator(self.frame, orient=VERTICAL).grid(row=rowIndex + 2, column=columnIndex + 1, sticky="nsw")

db = Database()
db.set_file("info.db")

initUI(MainMenu)