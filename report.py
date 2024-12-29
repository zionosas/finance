import math
import csv
import tkinter as tk

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar
from datetime import datetime, date
from tkinter import RIDGE, Label, Tk, Frame, LabelFrame, Entry, ttk, HORIZONTAL, VERTICAL, BOTTOM, RIGHT, BOTH, \
    messagebox, simpledialog
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import mysql.connector

class Report:
    def __init__(self, root):
        self.root = root
        self.root.title("RCCG TURKEY MISSION SYSTEM")
        self.root.iconbitmap('RCCGpx.ico')
        self.root.geometry("1540x900")
        self.current_user = None
        Ltitle = Label(self.root, bd=20, relief=RIDGE, text="RCCG TURKEY FINANCIAL REPORTING SYSTEM", fg="red",
                       bg="white", font=("times new roman", 30, "bold"))
        Ltitle.pack(side='top', fill='x')
        Ititle2 = Label(self.root, bd=20, text="REPORT", fg="purple", bg="white",
                        font=("Arial Black", 20, "bold"))
        Ititle2.pack(side='top', fill='x')

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password@12",
            database="my_data"
        )
        self.cursor = self.db.cursor()

        self.Dataframe = Frame(self.root, bd=20, bg="white")
        self.Dataframe.place(x=0, y=180, width=1280, height=750)
        self.entries = {}

        self.create_frames()
        self.chest()
        self.converter()
        self.graphinfo()
        # self.incomeEntrySeach()

    def create_frames(self):
        # Create left frame
        self.DataframeLeft = LabelFrame(self.Dataframe, bd=2, relief=RIDGE,
                                        padx=10,
                                        font=("times new roman", 12, "bold"),
                                        text="SAFE     INCOME    &    EXPENDITURE Information")
        self.DataframeLeft.place(x=0, y=0, width=750, height=750)

        # Create right frame
        self.DataframeRight = LabelFrame(self.Dataframe, bd=2, relief=RIDGE,
                                         padx=10,
                                         font=("times new roman", 12, "bold"),
                                         text="GRAPH VIEW")
        self.DataframeRight.place(x=750, y=1, width=530, height=750)

        # Create Top Income Frame
        self.incomeFrame = LabelFrame(self.DataframeLeft, bd=2, relief=RIDGE,
                                        padx=20,
                                        font=("times new roman", 12, "bold"),
                                        text="  INCOME Information")
        self.incomeFrame.place(x=0, y=100, width=750, height=200)

        # Search Frame
        self.SearchFrame= Label(self.DataframeLeft)
        self.SearchFrame.place(x=0, y=300, width=750, height=40)

        # Create Bottom Expense Frame
        self.expenseFrame = LabelFrame(self.DataframeLeft, bd=2, relief=RIDGE,
                                      padx=20,
                                      font=("times new roman", 12, "bold"),
                                      text="  EXPENSE Information")
        self.expenseFrame.place(x=0, y=350, width=750, height=200)

        self.ESearchFrame = Label(self.DataframeLeft)
        self.ESearchFrame.place(x=0, y=550, width=750, height=40)

        self.safe = Label(self.DataframeLeft, text="SAFE", font=("times new roman",12,"bold") )
        self.safe.grid(row=1, column=0)

        self.lira = Label(self.DataframeLeft, text="LIRA", font=("times new roman",12,"bold"))
        self.lira.grid(row=0, column=1,padx=10, pady=10)

        self.dollar = Label(self.DataframeLeft, text="DOLLAR", font=("times new roman",12,"bold"))
        self.dollar.grid(row=0, column=2,padx=10, pady=10)

        self.euro = Label(self.DataframeLeft, text="EURO", font=("times new roman",12,"bold"))
        self.euro.grid(row=0, column=3,padx=10, pady=10)

        self.pound = Label(self.DataframeLeft, text="POUND", font=("times new roman",12,"bold"))
        self.pound.grid(row=0, column=4,padx=10, pady=10)

        self.lira_entry = Entry(self.DataframeLeft, width=10, font=("times new roman",15,"bold"))
        self.lira_entry.grid(row=1, column=1, padx=10, pady=10)

        self.dollar_entry = Entry(self.DataframeLeft, width=10, font=("times new roman",15,"bold"))
        self.dollar_entry.grid(row=1, column=2, padx=10, pady=10)

        self.euro_entry = Entry(self.DataframeLeft, width=10, font=("times new roman",15,"bold"))
        self.euro_entry.grid(row=1, column=3, padx=10, pady=10)

        self.pound_entry = Entry(self.DataframeLeft, width=10, font=("times new roman",15,"bold"))
        self.pound_entry.grid(row=1, column=4,sticky='w', padx=10, pady=10)

    def iesearch(self):
        self.Expense_fromDate = tk.Button(self.ESearchFrame, text="From Date", font=("times new roman", 12, "bold"),
                                  command=self.open_calendar3)
        self.Expense_fromDate.grid(row=0, column=0, padx=5, pady=5)
        self.Expense_startDate = Entry(self.ESearchFrame, font=("times new roman", 12, "bold"), width=10)
        self.Expense_startDate.grid(row=0, column=1, padx=5, pady=5)

        self.Expense_space = Label(self.ESearchFrame, text="--", font=("times new roman", 20, "bold"))
        self.Expense_space.grid(row=0, column=2, padx=10, pady=10)

        self.Expense_toDate = tk.Button(self.ESearchFrame, text="To Date", font=("times new roman", 12, "bold"),
                                command=self.open_calendar4)
        self.Expense_toDate.grid(row=0, column=3, padx=5, pady=5)
        self.Expense_endDate = Entry(self.ESearchFrame, width=10, font=("times new roman", 12, "bold"))
        self.Expense_endDate.grid(row=0, column=4, padx=5, pady=5)

        self.Expense_Search = tk.Button(self.ESearchFrame, text="SEARCH", bg="green", font=("times new roman", 12, "bold"),
                                 command=lambda:self.Expsearch(self.Expense_startDate.get(), self.Expense_startDate.get()))
        self.Expense_Search.grid(row=0, column=6, padx=10, pady=10)

        self.Expense_download = tk.Button(self.ESearchFrame, text="DOWNLOAD", font=("times new roman", 12, "bold"))
        self.Expense_download.grid(row=0, column=8, padx=10, pady=10)

    def incomesearch(self):
        self.fromDate=tk.Button(self.SearchFrame, text="From Date",font=("times new roman",12,"bold"),
                                command=self.open_calendar)
        self.fromDate.grid(row=0,column=0,padx=5, pady=5)
        self.startDate=Entry(self.SearchFrame,font=("times new roman", 12, "bold"), width=10)
        self.startDate.grid(row=0, column=1,padx=5, pady=5)

        self.space = Label(self.SearchFrame, text="--", font=("times new roman", 20, "bold"))
        self.space.grid(row=0, column=2, padx=10, pady=10)

        self.toDate = tk.Button(self.SearchFrame, text="To Date", font=("times new roman", 12, "bold"),command=self.open_calendar1)
        self.toDate.grid(row=0, column=4,padx=5, pady=5)
        self.endDate = Entry(self.SearchFrame, width=10,font=("times new roman", 12, "bold"))
        self.endDate.grid(row=0, column=5,padx=5, pady=5)

        self.fSearch = tk.Button(self.SearchFrame, text="SEARCH", bg="brown", font=("times new roman", 12, "bold"),
                                 command=lambda: self.search(self.startDate.get(), self.endDate.get()))
        self.fSearch.grid(row=0, column=6, padx=10, pady=10)

        self.download = tk.Button(self.SearchFrame, text="DOWNLOAD",font=("times new roman", 12, "bold"),command=self.incomeReport)
        self.download.grid(row=0, column=8, padx=10, pady=10)
#################################################Repetion of Calendar###########################################################
    def open_calendar(self):
        dialog = tk.Toplevel(root)
        dialog.title("Select Date")

        cal = Calendar(dialog, selectmode='day', year=date.today().year, month=date.today().month,
                       day=date.today().day)
        cal.pack(padx=10, pady=10)

        def select_date():
            selected_date = cal.get_date()
            new_date = datetime.strptime(selected_date, '%m/%d/%y')
            dialog.destroy()
            date_updater(new_date)
        select_button = ttk.Button(dialog, text="Select", command=select_date)
        select_button.pack(pady=5)

        def date_updater(new_date):
            self.startDate.delete(0, tk.END)
            self.startDate.insert(0, new_date)

    def open_calendar1(self):
        dialog = tk.Toplevel(root)
        dialog.title("Select Date")

        cal = Calendar(dialog, selectmode='day', year=date.today().year, month=date.today().month,
                       day=date.today().day)
        cal.pack(padx=10, pady=10)

        def select_date():
            selected_date = cal.get_date()
            new_date1 = datetime.strptime(selected_date, '%m/%d/%y')
            dialog.destroy()
            date_updater1(new_date1)
        select_button = ttk.Button(dialog, text="Select", command=select_date)
        select_button.pack(pady=5)

        def date_updater1(new_date1):
            self.endDate.delete(0, tk.END)
            self.endDate.insert(0, new_date1)

    def open_calendar3(self):
        dialog = tk.Toplevel(root)
        dialog.title("Select Date")

        cal = Calendar(dialog, selectmode='day', year=date.today().year, month=date.today().month,
                       day=date.today().day)
        cal.pack(padx=10, pady=10)

        def select_date():
            selected_date = cal.get_date()
            new_date = datetime.strptime(selected_date, '%m/%d/%y')
            dialog.destroy()
            date_updater(new_date)
        select_button = ttk.Button(dialog, text="Select", command=select_date)
        select_button.pack(pady=5)

        def date_updater(new_date):
            self.Expense_startDate.delete(0, tk.END)
            self.Expense_startDate.insert(0, new_date)

    def open_calendar4(self):
        dialog = tk.Toplevel(root)
        dialog.title("Select Date")

        cal = Calendar(dialog, selectmode='day', year=date.today().year, month=date.today().month,
                       day=date.today().day)
        cal.pack(padx=10, pady=10)

        def select_date():
            selected_date = cal.get_date()
            new_date1 = datetime.strptime(selected_date, '%m/%d/%y')
            dialog.destroy()
            date_updater1(new_date1)
        select_button = ttk.Button(dialog, text="Select", command=select_date)
        select_button.pack(pady=5)

        def date_updater1(new_date1):
            self.Expense_endDate.delete(0, tk.END)
            self.Expense_endDate.insert(0, new_date1)
##########################################################################################################################################

    def chest(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                       database="my_data")

        my_cursor = conn.cursor()
        my_cursor.execute(" select * from my_data.vw_available_funds ")
        rows = my_cursor.fetchall()
        self.decimal_list=rows
        tuple_values = self.decimal_list[0]

        # # Access individual Decimal values from the tuple
        # self.first_value = tuple_values[0]  # Gets 216000.00
        # self.second_value = tuple_values[1]  # Gets 2020.00
        # self.third_value = tuple_values[2]  # Gets 850.00
        # self.fourth_value = tuple_values[3]  # Gets 890.00

        self.lira_entry.delete(0, tk.END)
        self.lira_entry.insert(0,tuple_values[0])
        self.lira_entry.config(state='readonly')

        self.dollar_entry.delete(0, tk.END)
        self.dollar_entry.insert(0, tuple_values[1])
        self.dollar_entry.config(state='readonly')

        self.euro_entry.delete(0, tk.END)
        self.euro_entry.insert(0, tuple_values[2])
        self.euro_entry.config(state='readonly')

        self.pound_entry.delete(0, tk.END)
        self.pound_entry.insert(0, tuple_values[3])
        self.pound_entry.config(state='readonly')
        self.incomeEntrySearch()
        self.expenseEntrySearch()
        return self.decimal_list


    def incomeEntrySearch(self):
        Scroll_x = ttk.Scrollbar(self.incomeFrame, orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(self.incomeFrame, orient=VERTICAL)
        self.Income_table = ttk.Treeview(self.incomeFrame, columns=(
             "ID","ENTRY DATE", "LIRA TOTAL", "DOLLAR TOTAL","EURO TOTAL","POUND TOTAL","TRANSACTION DATE"),
                                         xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)
        Scroll_x.pack(side=BOTTOM, fill='x')
        Scroll_y.pack(side=RIGHT, fill='y')

        Scroll_x.config(command=self.Income_table.xview)
        Scroll_y.config(command=self.Income_table.yview)
        for col in self.Income_table["columns"]:
            self.Income_table.heading(col, text=col.replace("_", " ").title())

        for col in self.Income_table["columns"]:
            self.Income_table.column(col, width=80)  # Adjust width as needed

        self.Income_table["show"] = "headings"
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        self.Income_table.pack(fill=BOTH, expand=1)
        self.incomesearch()
        self.load()

    def load(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                       database="my_data")
        my_cursor = conn.cursor()
        my_cursor.execute("select INCOME_REF_ID,ENTRY_DATE, Lira_Total, Dollar_Total,Euro_Total,Pound_Total,transaction_date from my_data.transaction where Type='Income'")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.Income_table.delete(*self.Income_table.get_children())
            for i in rows:
                self.Income_table.insert("", tk.END, values=i)

            conn.commit()
        conn.close()

    def expenseEntrySearch(self):
        Scroll_x = ttk.Scrollbar(self.expenseFrame, orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(self.expenseFrame, orient=VERTICAL)
        self.Expense_table = ttk.Treeview(self.expenseFrame, columns=("ENTRY DATE",
            "type1","Line_Amount1","type2","Line_Amount2","type3","Line_Amount3","type4","Line_Amount4","type5","Line_Amount5","TOTAL"),
                                         xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)
        Scroll_x.pack(side=BOTTOM, fill='x')
        Scroll_y.pack(side=RIGHT, fill='y')

        Scroll_x.config(command=self.Expense_table.xview)
        Scroll_y.config(command=self.Expense_table.yview)
        for col in self.Expense_table["columns"]:
            self.Expense_table.heading(col, text=col.replace("_", " ").title())

        for col in self.Expense_table["columns"]:
            self.Expense_table.column(col, width=80)  # Adjust width as needed

        self.Expense_table["show"] = "headings"
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        self.Expense_table.pack(fill=BOTH, expand=1)
        self.iesearch()
        self.voucherSummary()

    def voucherSummary(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                       database="my_data")
        my_cursor = conn.cursor()
        my_cursor.execute(
            "select creation_date, type1, Line_Amount1,type2, Line_Amount2,type3, Line_Amount3,type4, Line_Amount4,"
            "type5,Line_Amount5,TOTAL from voucher")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.Expense_table.delete(*self.Expense_table.get_children())
            for i in rows:
                self.Expense_table.insert("", tk.END, values=i)

            conn.commit()
        conn.close()

    def search(self,startDate, endDate):
        try:
            if startDate=="" or endDate =="":
                self.load()
                messagebox.showerror("Error", "Please fill both date feilds to make a search")
                return
            conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                           database="my_data")
            query = """
                    select income_ref_id,ENTRY_DATE, Lira_Total, Dollar_Total,Euro_Total,Pound_Total,transaction_date 
                    FROM my_data.Transaction 
                    WHERE Entry_Date between  %s AND %s
                    and Type='Income'
                """
            self.cursor.execute(query, (startDate, endDate))
            rows = self.cursor.fetchall()
            if len(rows) != 0:
                self.Income_table.delete(*self.Income_table.get_children())
                for i in rows:
                    self.Income_table.insert("", tk.END, values=i)
                conn.commit()
                print(rows[0][2])
            else:
                self.Income_table.delete(*self.Income_table.get_children())
                messagebox.showinfo("Information", f"No record(s) for the selected date range")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", "Database error: {err}")

    def Expsearch(self,Expense_startDate, Expense_endDate):
        try:
            if Expense_startDate == "" or Expense_endDate == "":
                messagebox.showerror("Error", "Please fill both date fields to make a search")
                return
            conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                           database="my_data")
            query = """
                    select creation_date, type1, Line_Amount1,type2, Line_Amount2,type3, Line_Amount3,type4, Line_Amount4,type5,Line_Amount5,TOTAL
                    from my_data.voucher
                    WHERE creation_date between  %s AND %s
                """
            self.cursor.execute(query, (Expense_startDate, Expense_endDate))
            rows = self.cursor.fetchall()
            if len(rows) != 0:
                self.Expense_table.delete(*self.Expense_table.get_children())
                for i in rows:
                    self.Expense_table.insert("", tk.END, values=i)
                conn.commit()
            else:
                self.Expense_table.delete(*self.Expense_table.get_children())
                messagebox.showinfo("Information", f"No record(s) for the selected date range")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", "Database error" )

    def converter(self):
        self.graphFrame=LabelFrame(self.Dataframe, bd=2, relief=RIDGE,
                                        padx=10,
                                        font=("times new roman", 12, "bold"),
                                        text="Graphical Information")
        self.graphFrame.place(x=750, y=1, width=530, height=350)

        self.ExchFrame = LabelFrame(self.Dataframe, bd=10, relief=RIDGE,
                                     padx=10,
                                     font=("times new roman", 12, "bold"),
                                     text="EXCHANGE  (e-DOVIS)")
        self.ExchFrame.place(x=750, y=350, width=530, height=750)
        self.exchDollar= Label(self.ExchFrame, text="DOLLAR", font=("times new roman",12,"bold"))
        self.exchDollar.grid(row=0, column=0, padx=5, pady=5)

        tuple_values = self.decimal_list[0]

        self.exchD_entry=Entry(self.ExchFrame,font=("times new roman",12,"bold"), width=10)
        self.exchD_entry.grid(row=1, column=0, pady=5, padx=5)
        self.exchD_entry.delete(0, tk.END)
        self.exchD_entry.insert(0, tuple_values[1])
        self.exchD_entry.config(state='readonly')


        self.exchEuro = Label(self.ExchFrame, text="EURO", font=("times new roman", 12, "bold"))
        self.exchEuro.grid(row=3, column=0, padx=5, pady=5)

        self.exchE_entry = Entry(self.ExchFrame, font=("times new roman", 12, "bold"), width=10)
        self.exchE_entry.grid(row=4, column=0, pady=5, padx=5)
        self.exchE_entry.delete(0, tk.END)
        self.exchE_entry.insert(0, tuple_values[2])
        self.exchE_entry.config(state='readonly')

        self.exchPound = Label(self.ExchFrame, text="POUND", font=("times new roman", 12, "bold"))
        self.exchPound.grid(row=5, column=0, padx=5, pady=5)

        self.exchP_entry = Entry(self.ExchFrame, font=("times new roman", 12, "bold"), width=10)
        self.exchP_entry.grid(row=6, column=0, pady=5, padx=5)
        self.exchP_entry.delete(0, tk.END)
        self.exchP_entry.insert(0, tuple_values[3])
        self.exchP_entry.config(state='readonly')

        self.checkbox1_var = tk.BooleanVar()
        self.checkbox1 = tk.Checkbutton(
            self.ExchFrame,
            text="Change",
            variable=self.checkbox1_var,
            command=self.toggle_entry
        )
        self.checkbox1.grid(row=1, column=1)

        self.checkbox2_var = tk.BooleanVar()
        self.checkbox2 = tk.Checkbutton(
            self.ExchFrame,
            text="Change",
            variable=self.checkbox2_var,
            command=self.toggle_entry
        )
        self.checkbox2.grid(row=4, column=1)

        self.checkbox3_var = tk.BooleanVar()
        self.checkbox3 = tk.Checkbutton(
            self.ExchFrame,
            text="Change",
            variable=self.checkbox3_var,
            command=self.toggle_entry
        )
        self.checkbox3.grid(row=6, column=1)

    def toggle_entry(self):
        if self.checkbox1_var.get():  # If checkbox is checked
            # Create and display entry field for Dollar
            self.exchAmt = Label(self.ExchFrame, text="Amount", font=("times new roman", 10, "bold"))
            self.exchAmt.grid(row=0, column=2, padx=5, pady=5)
            self.entry = tk.Entry(self.ExchFrame, width=10)
            self.entry.grid(row=1, column=2, padx=5, pady=5)
            self.change = tk.Button(self.ExchFrame, width=10, text="Change", command=self.submit)
            self.change.grid(row=1, column=3, padx=5, pady=5)
            self.entries['dynamic_entry'] = self.entry
            self.entries['dynamic_entry1' ]=self.exchAmt
            self.entries['dynamic_entry2'] = self.change
        elif self.checkbox2_var.get():
            # Create and display entry field for Euro
            self.exchAmt = Label(self.ExchFrame, text="Amount", font=("times new roman", 10, "bold"))
            self.exchAmt.grid(row=0, column=2, padx=5, pady=5)
            self.entry1 = tk.Entry(self.ExchFrame, width=10)
            self.entry1.grid(row=4, column=2, padx=5, pady=5)
            self.change1 = tk.Button(self.ExchFrame, width=10, text="Change",command=self.submit)
            self.change1.grid(row=4, column=3, padx=5, pady=5)
            self.entries['dynamic_entry'] = self.entry1
            self.entries['dynamic_entry1'] = self.exchAmt
            self.entries['dynamic_entry2'] = self.change1
        elif self.checkbox3_var.get():
            # Create and display entry field for Pound
            self.exchAmt = Label(self.ExchFrame, text="Amount", font=("times new roman", 10, "bold"))
            self.exchAmt.grid(row=0, column=2, padx=5, pady=5)
            self.entry2 = tk.Entry(self.ExchFrame, width=10)
            self.entry2.grid(row=6, column=2, padx=5, pady=5)
            self.change2 = tk.Button(self.ExchFrame, width=10, text="Change",command=self.submit)
            self.change2.grid(row=6, column=3, padx=5, pady=5)
            self.entries['dynamic_entry'] = self.entry2
            self.entries['dynamic_entry1'] = self.exchAmt
            self.entries['dynamic_entry2'] = self.change2
        else:
            # Remove entry field if it exists
            if 'dynamic_entry' in self.entries:
                self.entries['dynamic_entry'].destroy()
                self.entries['dynamic_entry1'].destroy()
                self.entries['dynamic_entry2'].destroy()
                # self.entries[1].destroy()
                del self.entries['dynamic_entry']
                del self.entries['dynamic_entry1']
                del self.entries['dynamic_entry2']

    def submit(self):
        if self.checkbox1_var.get():
            if float(self.entry.get()) > float(self.exchD_entry.get()) or float(self.entry.get()) < 0:
                messagebox.showerror("INFORMATION",
                                     "Entered amount cannot be greater than what you have in safe or less than 0 ")
                return
            else:
                try:
                    if self.entry.get() == "":
                        messagebox.showerror("INFO", "Please enter a value for amount")
                        return
                    self.Dollar_rate = float(simpledialog.askstring(title="Dollar Exchange rate", prompt="Cost of 1$ :"))
                    self.ExChanger = round((float(self.entry.get()) * self.Dollar_rate), 2)
                    self.ChAmt = -1 * float(self.entry.get())
                    query = """
                                INSERT INTO my_data.income
                                (collection1,Lira1,Dollar1,Euro1,Pound1,collection2,Lira2,Dollar2,Euro2,Pound2,collection3,Lira3,Dollar3,Euro3,Pound3,
                                                  collection4,Lira4,Dollar4,Euro4,Pound4,
                                                  collection5,Lira5,Dollar5,Euro5,Pound5,lIRA_TOTAL,DOLLAR_TOTAL, EURO_TOTAL, POUND_TOTAL,creation_date )
                                                  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                                  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """
                    self.cursor.execute(query,
                                        ('ExChange', f'{self.ExChanger}', 0.0, 0.0, 0.0, 'Select One', 0.0, 0.0, 0.0, 0.0,
                                         'Select One', 0.0, 0.0, 0.0, 0.0, 'Select One', 0.0, 0.0, 0.0, 0.0, 'Select One',
                                         0.0, 0.0, 0.0, 0.0,
                                         self.ExChanger, f'{self.ChAmt}', 0.0, 0.0, datetime.now()))
                    self.db.commit()
                    messagebox.showinfo("Success",
                                        "Transaction completed successfully \n The equivalent amount is:" f'{self.ExChanger} lira')
                    self.create_frames()
                    self.chest()
                    self.converter()
                    self.graphinfo()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Database error: {err}")
        elif self.checkbox2_var.get():
            if float(self.entry1.get()) > float(self.exchE_entry.get()) or float(self.entry1.get()) < 0:
                messagebox.showerror("INFORMATION",
                                     "Entered amount cannot be greater than what you have in safe or less than 0 ")
                return
            else:
                try:
                    if self.entry1.get() == "":
                        messagebox.showerror("INFO", "Please enter a value for amount")
                        return
                    self.Euro_rate = float(
                        simpledialog.askstring(title="Dollar Exchange rate", prompt="Cost of 1euro :"))
                    self.ExChanger = round((float(self.entry1.get()) * self.Euro_rate), 2)
                    self.ChAmt = -1 * float(self.entry1.get())
                    query = """
                                INSERT INTO my_data.income
                                (collection1,Lira1,Dollar1,Euro1,Pound1,collection2,Lira2,Dollar2,Euro2,Pound2,collection3,Lira3,Dollar3,Euro3,Pound3,
                                                  collection4,Lira4,Dollar4,Euro4,Pound4,
                                                  collection5,Lira5,Dollar5,Euro5,Pound5,lIRA_TOTAL,DOLLAR_TOTAL, EURO_TOTAL, POUND_TOTAL,creation_date )
                                                  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                                  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """
                    self.cursor.execute(query, (
                    'ExChange', f'{self.ExChanger}', 0.0, 0.0, 0.0, 'Select One', 0.0, 0.0, 0.0, 0.0,
                    'Select One', 0.0, 0.0, 0.0, 0.0, 'Select One', 0.0, 0.0, 0.0, 0.0, 'Select One', 0.0, 0.0, 0.0,
                    0.0,
                    self.ExChanger, 0.0, f'{self.ChAmt}', 0.0, datetime.now()))
                    self.db.commit()
                    messagebox.showinfo("Success",
                                        "Transaction completed successfully \n The equivalent amount is:" f'{self.ExChanger} lira')
                    self.create_frames()
                    self.chest()
                    self.converter()
                    self.graphinfo()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Database error: {err}")
        elif self.checkbox3_var.get():
            if float(self.entry2.get()) > float(self.exchP_entry.get()) or float(self.entry2.get()) < 0:
                messagebox.showerror("INFORMATION",
                                     "Entered amount cannot be greater than what you have in safe or less than 0 ")
                return
            else:
                try:
                    if self.entry2.get() == "":
                        messagebox.showerror("INFO", "Please enter a value for amount")
                        return
                    self.Dollar_rate = float(
                        simpledialog.askstring(title="Dollar Exchange rate", prompt="Cost of 1£ :"))
                    self.ExChanger = round((float(self.entry2.get()) * self.Dollar_rate), 2)
                    self.ChAmt = -1 * float(self.entry2.get())
                    query = """
                                INSERT INTO my_data.income
                                (collection1,Lira1,Dollar1,Euro1,Pound1,collection2,Lira2,Dollar2,Euro2,Pound2,collection3,Lira3,Dollar3,Euro3,Pound3,
                                                  collection4,Lira4,Dollar4,Euro4,Pound4,
                                                  collection5,Lira5,Dollar5,Euro5,Pound5,lIRA_TOTAL,DOLLAR_TOTAL, EURO_TOTAL, POUND_TOTAL,creation_date )
                                                  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                                  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """
                    self.cursor.execute(query, (
                    'ExChange', f'{self.ExChanger}', 0.0, 0.0, 0.0, 'Select One', 0.0, 0.0, 0.0, 0.0,
                    'Select One', 0.0, 0.0, 0.0, 0.0, 'Select One', 0.0, 0.0, 0.0, 0.0, 'Select One', 0.0, 0.0, 0.0,
                    0.0,
                    self.ExChanger, 0.0, 0.0, f'{self.ChAmt}', datetime.now()))
                    self.db.commit()
                    messagebox.showinfo("Success",
                                        "Transaction completed successfully \n The equivalent amount is:" f'{self.ExChanger} lira')
                    self.create_frames()
                    self.chest()
                    self.converter()
                    self.graphinfo()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Database error: {err}")
        else:
            messagebox.showerror("Error", "One Record at a time")
            return

    def incomeReport(self):
        try:
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if file_path:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)

                    # Write headers
                    headers = [self.Income_table.heading(column)['text'] for column in self.Income_table['columns']]
                    writer.writerow(headers)

                    # Write data rows
                    for item in self.Income_table.get_children():
                        values = self.Income_table.item(item)['values']
                        writer.writerow(values)

                messagebox.showinfo("Success", f"Data successfully downloaded to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download data: {str(e)}")

    def graphinfo(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                       database="my_data")
        my_cursor = conn.cursor()
        my_cursor.execute(
            """WITH combined_data AS (
                SELECT type1 as type, Line_Amount1 as amount FROM voucher
                UNION ALL
                SELECT type2, Line_Amount2 FROM voucher
                UNION ALL
                SELECT type3, Line_Amount3 FROM voucher
                UNION ALL
                SELECT type4, Line_Amount4 FROM voucher
                UNION ALL
                 SELECT type5, Line_Amount5 FROM voucher  )

                SELECT type,SUM(amount) as total_amount
                FROM combined_data
                WHERE type IN ("WELFARE", "REPAIR&MAINTENANCE", "UTILITY", "SUPPLIES", "REMITTANCE", "FURNITURE&FITTINGS", "TELECOMMUNICATION",
                               "CONSTRUCTION","LOAN","REFRESHMENT","TRANSPORTATION")
                GROUP BY type
                ORDER BY type """)
        rows = my_cursor.fetchall()
        self.label=[]
        self.value=[]
        for i in range(len(rows)):
            self.label.append(rows[i][0])
            self.value.append(rows[i][1])
        decimal_list=self.value
        new_name=self.label

        data= {
            'type':new_name,
            'value':decimal_list
        }
        df = pd.DataFrame(data)
        # Create figure and axis
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            df['value'],
            labels=df['type'],
            autopct='%1.1f%%',
            startangle=90
        )
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')

        # Add title
        ax.set_title('Expense Distribution')

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=self.graphFrame)
        canvas.draw()

        # Pack canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


root = Tk()
ob = Report(root)
root.mainloop()