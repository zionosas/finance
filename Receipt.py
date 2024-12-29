from datetime import date, datetime
from tkinter import RIDGE, Label, Tk, Entry, Frame, LabelFrame, ttk, Button, HORIZONTAL, VERTICAL, BOTTOM, RIGHT, BOTH, \
    Text, END, StringVar, messagebox
import tkinter as tk
import mysql.connector
from tkcalendar import Calendar



class Income:
    def __init__(self, root):
        self.root = root
        self.root.title("RCCG TURKEY MISSION SYSTEM")
        self.root.iconbitmap('RCCGpx.ico')
        self.root.geometry("1540x900")

        Ltitle = Label(self.root, bd=20, relief=RIDGE, text="RCCG TURKEY FINANCIAL REPORTING SYSTEM", fg="red",
                       bg="white", font=("times new roman", 30, "bold"))
        Ltitle.pack(side='top', fill='x')
        Ititle2 = Label(self.root, bd=20, text="COLLECTIONS", fg="BLACK", bg="white",
                        font=("Arial Black", 15, "bold"))
        Ititle2.pack(side='top', fill='x')

        self.collection1 = StringVar()
        self.LIRA1 = StringVar()
        self.DOLLAR1 = StringVar()
        self.EURO1 = StringVar()
        self.POUND1 = StringVar()
        self.collection2 = StringVar()
        self.LIRA2 = StringVar()
        self.DOLLAR2 = StringVar()
        self.EURO2 = StringVar()
        self.POUND2 = StringVar()
        self.collection3 = StringVar()
        self.LIRA3 = StringVar()
        self.DOLLAR3 = StringVar()
        self.EURO3 = StringVar()
        self.POUND3 = StringVar()
        self.collection4 = StringVar()
        self.LIRA4 = StringVar()
        self.DOLLAR4 = StringVar()
        self.EURO4 = StringVar()
        self.POUND4 = StringVar()
        self.collection5 = StringVar()
        self.LIRA5 = StringVar()
        self.DOLLAR5 = StringVar()
        self.EURO5 = StringVar()
        self.POUND5 = StringVar()
        self.lIRA_TOTAL = StringVar()
        self.DOLLAR_TOTAL = StringVar()
        self.EURO_TOTAL = StringVar()
        self.POUND_TOTAL = StringVar()
        self.creation_date = StringVar()

        self.create_frames()
        self.incomeBase()
        self.widget()
        # self.open_calendar()

    def create_frames(self):
        self.Headerframe = Frame(self.root, bd=20)
        self.Headerframe.place(x=0, y=140, width=440, height=70)
        self.Dataframe = Frame(self.root, bd=20, relief=RIDGE)
        self.Dataframe.place(x=0, y=130, width=1530, height=400)
        self.DataframeLeft = LabelFrame(self.Dataframe, bd=10, relief=RIDGE, padx=10,
                                        font=("times new roman", 12, "bold"), text="Income Information")
        self.DataframeLeft.place(x=0, y=5, width=800, height=350)
        self.DataframeRight = LabelFrame(self.Dataframe, bd=10, bg="white", relief=RIDGE, padx=10,
                                         font=("times new roman", 12, "bold"), text="Summary Information")
        self.DataframeRight.place(x=800, y=5, width=440, height=350)
        ################################### BUTTONS FRAME ###################################################
        self.Buttonframe = Frame(self.root, bd=20, relief=RIDGE)
        self.Buttonframe.place(x=0, y=530, width=1270, height=70)
        ################################### DETAILS FRAME ###################################################
        self.Detailframe = Frame(self.root, bd=20, relief=RIDGE)
        self.Detailframe.place(x=0, y=600, width=1270, height=220)

    def incomeBase(self):
        Scroll_x = ttk.Scrollbar(self.Detailframe, orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(self.Detailframe, orient=VERTICAL)
        self.Income_table = ttk.Treeview(self.Detailframe, columns=(
            "Income_num", "COLLECTION1", "LIRA1", "DOLLAR1", "EURO1", "POUND1", "COLLECTION2", "LIRA2",
            "DOLLAR2", "EURO2",
            "POUND2", "COLLECTION3", "LIRA3",
            "DOLLAR3", "EURO3", "POUND3", "COLLECTION4", "LIRA4", "DOLLAR4", "EURO4", "POUND4",
            "COLLECTION5",
            "LIRA5", "DOLLAR5", "EURO5",
            "POUND5", "lIRA_TOTAL", "DOLLAR_TOTAL", "EURO_TOTAL", "POUND_TOTAL", "Creation_Date"),
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
        self.load()
        self.Income_table.bind("<ButtonRelease-1>", self.get_cursor)

    def open_calendar(self):
        dialog = tk.Toplevel(self.DataframeLeft)
        dialog.title("Select Date")

        cal = Calendar(dialog, selectmode='day', year=date.today().year, month=date.today().month,
                       day=date.today().day)
        cal.pack(padx=10, pady=10)

        def select_date():
            selected_date = cal.get_date()
            new_date = datetime.strptime(selected_date, '%m/%d/%y')
            dialog.destroy()
            self.date_updater(new_date)

        select_button = ttk.Button(dialog, text="Select", command=select_date)
        select_button.pack(pady=5)

    def date_updater(self, new_date):
        self.creation_date.delete(0, tk.END)
        self.creation_date.insert(0, new_date)

    def widget(self):
        Collection = Label(self.DataframeLeft, text="COLLECTION TYPE", font=("times new roman", 12, "bold"))
        Collection.grid(row=0, column=0, padx=10, pady=10)
        Lira = Label(self.DataframeLeft, text="LIRA", font=("times new roman", 12, "bold"))
        Lira.grid(row=0, column=1, padx=10, pady=10)
        Dollar = Label(self.DataframeLeft, text="DOLLAR", font=("times new roman", 12, "bold"))
        Dollar.grid(row=0, column=2, padx=10, pady=10)
        Euro = Label(self.DataframeLeft, text="EURO", font=("times new roman", 12, "bold"))
        Euro.grid(row=0, column=3, padx=10, pady=10)
        Pound = Label(self.DataframeLeft, text="POUND", font=("times new roman", 12, "bold"))
        Pound.grid(row=0, column=4, padx=10, pady=10)

        Rowfield1 = ttk.Combobox(self.DataframeLeft, textvariable=self.collection1,
                                 font=("times new roman", 12, "bold"),
                                 width=15)
        # Set a default value
        Rowfield1.set("Select One")
        Rowfield1["values"] = (
            "OFFERING", "GENERAL_TITHE", "MINISTERS_TITHE", "THANKSGIVING", "SEED_OFFERING", "REFUND", "FIRST_FRUIT",
            "MID_WEEK", "ExChange")
        Rowfield1.grid(row=1, column=0)

        self.LIRA1 = Entry(self.DataframeLeft, width=10, textvariable=self.LIRA1, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.LIRA1.insert(0, 0)
        self.LIRA1.grid(row=1, column=1, sticky='w', padx=10, pady=10)

        self.DOLLAR1 = Entry(self.DataframeLeft, width=10, textvariable=self.DOLLAR1,
                             font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.DOLLAR1.insert(1, 0)
        self.DOLLAR1.grid(row=1, column=2, sticky='w', padx=10, pady=10)

        self.EURO1 = Entry(self.DataframeLeft, width=10, textvariable=self.EURO1, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.EURO1.insert(1, 0)
        self.EURO1.grid(row=1, column=3, sticky='w', padx=10, pady=10)

        self.POUND1 = Entry(self.DataframeLeft, width=10, textvariable=self.POUND1,
                            font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.POUND1.insert(1, 0)
        self.POUND1.grid(row=1, column=4, sticky='w', padx=10, pady=10)

        self.creation_date = Entry(self.DataframeLeft, width=15, textvariable=self.creation_date,
                                   font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.creation_date.grid(row=0, column=5, sticky='w', padx=10, pady=10)
        select_date = ttk.Button(self.DataframeLeft, text="Date", command=self.open_calendar)
        select_date.grid(row=1, column=5, padx=20, pady=20)

        Rowfield2 = ttk.Combobox(self.DataframeLeft, textvariable=self.collection2,
                                 font=("times new roman", 12, "bold"),
                                 width=15)
        # Set a default value
        Rowfield2.set("Select One")
        Rowfield2["values"] = (
            "OFFERING", "GENERAL_TITHE", "MINISTERS_TITHE", "THANKSGIVING", "SEED_OFFERING", "REFUND", "FIRST_FRUIT",
            "MID_WEEK", "ExChange")
        Rowfield2.grid(row=2, column=0)

        self.LIRA2 = Entry(self.DataframeLeft, width=10, textvariable=self.LIRA2, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.LIRA2.insert(1, 0)
        self.LIRA2.grid(row=2, column=1, sticky='w', padx=10, pady=10)

        self.DOLLAR2 = Entry(self.DataframeLeft, width=10, textvariable=self.DOLLAR2,
                             font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.DOLLAR2.insert(1, 0)
        self.DOLLAR2.grid(row=2, column=2, sticky='w', padx=10, pady=10)

        self.EURO2 = Entry(self.DataframeLeft, width=10, textvariable=self.EURO2, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.EURO2.insert(1, 0)
        self.EURO2.grid(row=2, column=3, sticky='w', padx=10, pady=10)

        self.POUND2 = Entry(self.DataframeLeft, width=10, textvariable=self.POUND2,
                            font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.POUND2.insert(1, 0)
        self.POUND2.grid(row=2, column=4, sticky='w', padx=10, pady=10)

        Rowfield3 = ttk.Combobox(self.DataframeLeft, font=("times new roman", 12, "bold"),
                                 textvariable=self.collection3,
                                 width=15)
        # Set a default value
        Rowfield3.set("Select One")
        Rowfield3["values"] = (
            "OFFERING", "GENERAL_TITHE", "MINISTERS_TITHE", "THANKSGIVING", "SEED_OFFERING", "REFUND", "FIRST_FRUIT",
            "MID_WEEK", "ExChange")
        Rowfield3.grid(row=3, column=0)

        self.LIRA3 = Entry(self.DataframeLeft, width=10, textvariable=self.LIRA3, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.LIRA3.insert(1, 0)
        self.LIRA3.grid(row=3, column=1, sticky='w', padx=10, pady=10)

        # self.l3=float(self.get_lira3_value())
        # self.LIRA3_var = StringVar()
        # self.LIRA3 = Entry(DataframeLeft, textvariable=self.LIRA3_var)

        self.DOLLAR3 = Entry(self.DataframeLeft, width=10, textvariable=self.DOLLAR3,
                             font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.DOLLAR3.insert(1, 0)
        self.DOLLAR3.grid(row=3, column=2, sticky='w', padx=10, pady=10)

        self.EURO3 = Entry(self.DataframeLeft, width=10, textvariable=self.EURO3, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.EURO3.insert(1, 0)
        self.EURO3.grid(row=3, column=3, sticky='w', padx=10, pady=10)

        self.POUND3 = Entry(self.DataframeLeft, width=10, textvariable=self.POUND3,
                            font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.POUND3.insert(1, 0)
        self.POUND3.grid(row=3, column=4, sticky='w', padx=10, pady=10)

        Rowfield4 = ttk.Combobox(self.DataframeLeft, font=("times new roman", 12, "bold"),
                                 textvariable=self.collection4,
                                 width=15)
        # Set a default value
        Rowfield4.set("Select One")
        Rowfield4["values"] = (
            "OFFERING", "GENERAL_TITHE", "MINISTERS_TITHE", "THANKSGIVING", "SEED_OFFERING", "REFUND", "FIRST_FRUIT",
            "MID_WEEK", "ExChange")
        Rowfield4.grid(row=4, column=0)

        self.LIRA4 = Entry(self.DataframeLeft, width=10, textvariable=self.LIRA4, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.LIRA4.insert(1, 0)
        self.LIRA4.grid(row=4, column=1, sticky='w', padx=10, pady=10)

        self.DOLLAR4 = Entry(self.DataframeLeft, width=10, textvariable=self.DOLLAR4,
                             font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.DOLLAR4.insert(1, 0)
        self.DOLLAR4.grid(row=4, column=2, sticky='w', padx=10, pady=10)

        self.EURO4 = Entry(self.DataframeLeft, width=10, textvariable=self.EURO4, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.EURO4.insert(1, 0)
        self.EURO4.grid(row=4, column=3, sticky='w', padx=10, pady=10)

        self.POUND4 = Entry(self.DataframeLeft, width=10, textvariable=self.POUND4,
                            font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.POUND4.insert(1, 0)
        self.POUND4.grid(row=4, column=4, sticky='w', padx=10, pady=10)

        Rowfield5 = ttk.Combobox(self.DataframeLeft, font=("times new roman", 12, "bold"),
                                 textvariable=self.collection5,
                                 width=15)
        # Set a default value
        Rowfield5.set("Select One")
        Rowfield5["values"] = (
            "OFFERING", "GENERAL_TITHE", "MINISTERS_TITHE", "THANKSGIVING", "SEED_OFFERING", "REFUND", "FIRST_FRUIT",
            "MID_WEEK", "ExChange")
        Rowfield5.grid(row=5, column=0)

        self.LIRA5 = Entry(self.DataframeLeft, width=10, textvariable=self.LIRA5, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.LIRA5.insert(1, 0)
        self.LIRA5.grid(row=5, column=1, sticky='w', padx=10, pady=10)
        # def get_lira5_value(self):
        #     return self.lIRA5.get()
        #
        # self.l5 = float(get_lira5_value(self))
        # self.LIRA5_var = StringVar()
        # self.LIRA5 = Entry(DataframeLeft, textvariable=self.LIRA5_var)

        self.DOLLAR5 = Entry(self.DataframeLeft, width=10, textvariable=self.DOLLAR5,
                             font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.DOLLAR5.insert(0, 0)
        self.DOLLAR5.grid(row=5, column=2, sticky='w', padx=10, pady=10)

        self.EURO5 = Entry(self.DataframeLeft, width=10, textvariable=self.EURO5, font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.EURO5.insert(0, 0)
        self.EURO5.grid(row=5, column=3, sticky='w', padx=10, pady=10)

        self.POUND5 = Entry(self.DataframeLeft, width=10, textvariable=self.POUND5,
                            font=("times new roman", 12, "bold"))
        # default_value = "Enter text here"
        self.POUND5.insert(0, 0)
        self.POUND5.grid(row=5, column=4, sticky='w', padx=10, pady=10)
        collectionTitle = Label(self.DataframeRight, text="COLLECTION SUMMARY", bg="white",
                                font=("times new roman", 15, "bold"))
        collectionTitle.grid(row=0, column=0, padx=10, pady=10)
        LiraTotal = Label(self.DataframeRight, text="TOTAL LIRA :", bg="white", font=("times new roman", 15, "bold"))
        LiraTotal.grid(row=1, column=0, padx=10, pady=10)
        self.LiraTotalValues = Label(self.DataframeRight, text="0.00", bg="white", font=("times new roman", 15, "bold"))
        self.LiraTotalValues.grid(row=1, column=1, padx=10, pady=10)

        DollarTotal = Label(self.DataframeRight, text="TOTAL DOLLAR:", bg="white", font=("times new roman", 15, "bold"))
        DollarTotal.grid(row=2, column=0, padx=10, pady=10)
        self.DollarTotalValues = Label(self.DataframeRight, text="0.00", bg="white",
                                       font=("times new roman", 15, "bold"))
        self.DollarTotalValues.grid(row=2, column=1, padx=10, pady=10)

        EuroTotal = Label(self.DataframeRight, text="TOTAL EURO:", bg="white", font=("times new roman", 15, "bold"))
        EuroTotal.grid(row=3, column=0, padx=10, pady=10)
        self.EuroTotalValues = Label(self.DataframeRight, text="0.00", bg="white", font=("times new roman", 15, "bold"))
        self.EuroTotalValues.grid(row=3, column=1, padx=10, pady=10)

        PoundTotal = Label(self.DataframeRight, text="TOTAL POUND:", bg="white", font=("times new roman", 15, "bold"))
        PoundTotal.grid(row=4, column=0, padx=10, pady=10)
        self.PoundTotalValues = Label(self.DataframeRight, text="0.00", bg="white",
                                      font=("times new roman", 15, "bold"))
        self.PoundTotalValues.grid(row=4, column=1, padx=10, pady=10)
        ################################### BUTTONS FRAME ######################################################################
        btnSubmit = Button(self.Buttonframe, text="SUMMARY", command=self.summary, bg="green", fg="white",
                           font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=0)

        btnSubmit = Button(self.Buttonframe, text="SUBMIT", bg="GREEN", fg="white", command=self.SUBMIT,
                           font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=1)

        btnSubmit = Button(self.Buttonframe, text="UPDATE", bg="green", fg="white", font=("arial", 12, "bold"),
                           width=20)
        btnSubmit.grid(row=0, column=2)

        btnSubmit = Button(self.Buttonframe, text="NEW", command=lambda: self.clear_frame_widgets(self.DataframeLeft),
                           bg="green", fg="white", font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=3)

        btnSubmit = Button(self.Buttonframe, text="DELETE", bg="red", fg="white", font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=4)

        btnSubmit = Button(self.Buttonframe, text="EXIT", command=self.logout, bg="yellow", fg="white",
                           font=("arial", 12, "bold"), width=17)
        btnSubmit.grid(row=0, column=5)

    #################################################Function of Buttons#######################################################################

    def logout(self):
        self.root.destroy()

    def summary(self):
        self.l1 = float(self.LIRA1.get())
        self.l2 = float(self.LIRA2.get())
        self.l3 = float(self.LIRA3.get())
        self.l4 = float(self.LIRA4.get())
        self.l5 = float(self.LIRA5.get())
        self.D1 = float(self.DOLLAR1.get())
        self.D2 = float(self.DOLLAR2.get())
        self.D3 = float(self.DOLLAR3.get())
        self.D4 = float(self.DOLLAR4.get())
        self.D5 = float(self.DOLLAR5.get())
        self.E1 = float(self.EURO1.get())
        self.E2 = float(self.EURO2.get())
        self.E3 = float(self.EURO3.get())
        self.E4 = float(self.EURO4.get())
        self.E5 = float(self.EURO5.get())
        self.P1 = float(self.POUND1.get())
        self.P2 = float(self.POUND2.get())
        self.P3 = float(self.POUND3.get())
        self.P4 = float(self.POUND4.get())
        self.P5 = float(self.POUND5.get())

        self.LiraTotalValues.config(text=f'{(self.l1 + self.l2 + self.l3 + self.l4 + self.l5):.2f} TL')
        self.DollarTotalValues.config(text=f'{(self.D1 + self.D2 + self.D3 + self.D4 + self.D5):.2f} $')
        self.EuroTotalValues.config(text=f'{(self.E1 + self.E2 + self.E3 + self.E4 + self.E5):.2f} euro')
        self.PoundTotalValues.config(text=f'{(self.P1 + self.P2 + self.P3 + self.P4 + self.P5):.2f} £')

        def totals():
            self.lIRA_TOTAL = float(self.l1 + self.l2 + self.l3 + self.l4 + self.l5)
            self.DOLLAR_TOTAL = float(self.D1 + self.D2 + self.D3 + self.D4 + self.D5)
            self.EURO_TOTAL = float(self.E1 + self.E2 + self.E3 + self.E4 + self.E5)
            self.POUND_TOTAL = float(self.P1 + self.P2 + self.P3 + self.P4 + self.P5)
            return self.lIRA_TOTAL, self.DOLLAR_TOTAL, self.EURO_TOTAL, self.POUND_TOTAL

        self.Totals = totals()

    def SUBMIT(self):
        self.summary()
        if self.lIRA_TOTAL == " " or self.collection1 == "Select One":
            messagebox.showerror("Error", "At least first row fields must be entered")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                               database="my_data")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into my_data.income (collection1,Lira1,Dollar1,Euro1,Pound1,"
                                  "collection2,Lira2,Dollar2,Euro2,Pound2,collection3,Lira3,Dollar3,Euro3,Pound3,"
                                  "collection4,Lira4,Dollar4,Euro4,Pound4,"
                                  "collection5,Lira5,Dollar5,Euro5,Pound5,lIRA_TOTAL,DOLLAR_TOTAL, EURO_TOTAL, POUND_TOTAL,creation_date )"
                                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                                  "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                  (
                                      # self.INVOICE_NUM.get(),
                                      self.collection1.get(),
                                      self.LIRA1.get(),
                                      self.DOLLAR1.get(),
                                      self.EURO1.get(),
                                      self.POUND1.get(),
                                      self.collection2.get(),
                                      self.LIRA2.get(),
                                      self.DOLLAR2.get(),
                                      self.EURO2.get(),
                                      self.POUND2.get(),
                                      self.collection3.get(),
                                      self.LIRA3.get(),
                                      self.DOLLAR3.get(),
                                      self.EURO3.get(),
                                      self.POUND3.get(),
                                      self.collection4.get(),
                                      self.LIRA4.get(),
                                      self.DOLLAR4.get(),
                                      self.EURO4.get(),
                                      self.POUND4.get(),
                                      self.collection5.get(),
                                      self.LIRA5.get(),
                                      self.DOLLAR5.get(),
                                      self.EURO5.get(),
                                      self.POUND5.get(),
                                      self.lIRA_TOTAL,
                                      self.DOLLAR_TOTAL,
                                      self.EURO_TOTAL,
                                      self.POUND_TOTAL,
                                      self.creation_date.get()
                                  ))
                conn.commit()
                self.load()
                messagebox.showinfo("SUCCESS", "Record added SUCCESSFULLY")
                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"An error occurred: {err}")
            except Exception as e:
                messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

    def load(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                       database="my_data")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from my_data.income order by income.Income_num desc")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.Income_table.delete(*self.Income_table.get_children())
            for i in rows:
                self.Income_table.insert("", END, values=i)

            conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.Income_table.focus()
        content = self.Income_table.item(cursor_row)
        print(f"Row contents: {content}")
        row = content["values"]
        print(f"Values: {row}")
        self.collection1.set(row[1])
        self.LIRA1.set(row[2])
        self.DOLLAR1.set(row[3])
        self.EURO1.set(row[4])
        self.POUND1.set(row[5])
        self.collection2.set(row[5])
        self.LIRA2.set(row[6])
        self.DOLLAR2.set(row[7])
        self.EURO2.set(row[8])
        self.POUND2.set(row[9])
        self.collection3.set(row[10])
        self.LIRA3.set(row[11])
        self.DOLLAR3.set(row[12])
        self.EURO3.set(row[13])
        self.POUND3.set(row[14])
        self.collection4.set(row[15])
        self.LIRA4.set(row[16])
        self.DOLLAR4.set(row[17])
        self.EURO4.set(row[18])
        self.POUND4.set(row[19])
        self.collection5.set(row[20])
        self.LIRA5.set(row[21])
        self.DOLLAR5.set(row[22])
        self.EURO5.set(row[23])
        self.POUND5.set(row[24])
        self.creation_date(row[29])

    def clear_frame_widgets(self, frame):
        # Reset all widgets in the frame

        for widget in self.DataframeLeft.winfo_children():
            widget_type = widget.winfo_class()

            if widget_type == "Entry":
                widget.delete(0, 'end')  # Clear entry widget

            elif widget_type == "Text":
                widget.delete('0.00', 'end')  # Clear text widget

            elif widget_type == "Combobox":
                widget.set('NONE')  # Reset combobox selection

            elif widget_type == "Checkbutton":
                widget.deselect()  # Uncheck checkbutton

            elif widget_type == "Radiobutton":
                # Reset radio button selection by setting to default value
                widget.set(0)  # Assuming 0 is the default value

            elif widget_type == "Spinbox":
                widget.delete(0, "end")
                widget.insert(0, widget.cget("from"))  # Reset to minimum value

            elif widget_type == "Scale":
                widget.set(widget.cget("from"))  # Reset to minimum value

            elif widget_type == "Listbox":
                widget.selection_clear(0, 'end')  # Clear selection

            elif widget_type == "Treeview":
                widget.delete(*widget.get_children())  # Clear all items

    def summaryRefresh(self, frame1):

        for widget in self.DataframeRight.winfo_children():
            widget_type = widget.winfo_class()

            if widget_type == "Entry":
                widget.delete(0, 'end')  # Clear entry widget

            elif widget_type == "Text":
                widget.delete('0.00', 'end')  # Clear text widget

            elif widget_type == "Combobox":
                widget.set('NONE')  # Reset combobox selection

            elif widget_type == "Checkbutton":
                widget.deselect()  # Uncheck checkbutton

            elif widget_type == "Radiobutton":
                # Reset radio button selection by setting to default value
                widget.set(0)  # Assuming 0 is the default value

            elif widget_type == "Spinbox":
                widget.delete(0, "end")
                widget.insert(0, widget.cget("from"))  # Reset to minimum value

            elif widget_type == "Scale":
                widget.set(widget.cget("from"))  # Reset to minimum value

            elif widget_type == "Listbox":
                widget.selection_clear(0, 'end')  # Clear selection

            elif widget_type == "Treeview":
                widget.delete(*widget.get_children())  # Clear all items


root = Tk()
ob = Income(root)
root.mainloop()