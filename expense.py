import csv
from datetime import date, datetime
from tkinter import messagebox, Tk, Label, RIDGE, Entry, Frame, LabelFrame, ttk, Button, HORIZONTAL, VERTICAL, BOTTOM, \
    RIGHT, Y, BOTH, StringVar, END
import tkinter as tk
from tkinter import ttk
import messagebox
import mysql.connector
from tkcalendar import Calendar
from tkinter import filedialog

class Expense:
    def __init__(self, root):
        self.root = root
        self.root.title("RCCG TURKEY REPORTING SYSTEM")
        self.root.iconbitmap('RCCGpx.ico')
        self.root.geometry("1540x900")

        self.voucher_num = StringVar()
        self.item1 = StringVar()
        self.Type1 = StringVar()
        self.Description1 = StringVar()
        self.Quantity1 = StringVar()
        self.Unit_cost1 = StringVar()
        self.Line_Amount1 = StringVar()
        self.item2 = StringVar()
        self.Type2 = StringVar()
        self.Description2 = StringVar()
        self.Quantity2 = StringVar()
        self.Unit_cost2 = StringVar()
        self.Line_Amount2 = StringVar()
        self.item3 = StringVar()
        self.Type3 = StringVar()
        self.Description3 = StringVar()
        self.Quantity3 = StringVar()
        self.Unit_cost3 = StringVar()
        self.Line_Amount3 = StringVar()
        self.item4 = StringVar()
        self.Type4 = StringVar()
        self.Description4 = StringVar()
        self.Quantity4 = StringVar()
        self.Unit_cost4 = StringVar()
        self.Line_Amount4 = StringVar()
        self.item5 = StringVar()
        self.Type5 = StringVar()
        self.Description5 = StringVar()
        self.Quantity5 = StringVar()
        self.Unit_cost5 = StringVar()
        self.Line_Amount5 = StringVar()
        self.TOTAL = StringVar()
        self.Creation_Date = StringVar()

        Ltitle= Label(self.root, bd=20, relief=RIDGE,text="RCCG TURKEY FINANCIAL REPORTING SYSTEM", fg="red", bg="white",font=("times new roman", 30, "bold"))
        Ltitle.pack(side='top', fill='x')
        Ltitle1 = Label(self.root,bd=20, text="PAYMENT VOUCHER", fg="BLACK", bg="white", font=("times new roman", 20, "bold"))
        Ltitle1.pack(side='top', fill='x')

        # Headerframe = Frame(self.root, bd=20)
        # Headerframe.place(x=0, y=140, width=1280, height=70)

        self.create_frames()
        self.headInfo()
        self.entrywidget()
        self.autoSum()
        self.buttonsDesign()
        self.entriesDetails()

    def create_frames(self):
        self.Headerframe = Frame(self.root, bd=20)
        self.Headerframe.place(x=0, y=140, width=1280, height=70)

        ################################### INVOICE DATAFRAME#################################################
        self.Dataframe = Frame(self.root, bd=20, relief=RIDGE)
        self.Dataframe.place(x=0, y=200, width=1280, height=420)

        self.DataframeLeft = LabelFrame(self.Dataframe, bd=10, relief=RIDGE, padx=10,
                                   font=("times new roman", 12, "bold"), text="Voucher Information")
        self.DataframeLeft.place(x=0, y=0, width=1230, height=370)
        #############################Button Frame###################################################
        self.Buttonframe = Frame(self.root, bd=20, relief=RIDGE)
        self.Buttonframe.place(x=0, y=530, width=1270, height=70)
        ################################### DETAILS FRAME ###################################################
        self.Detailframe = Frame(self.root, bd=20, relief=RIDGE)
        self.Detailframe.place(x=0, y=600, width=1270, height=220)
        btnSubmit = Button(self.Buttonframe, text="EXIT", bg="yellow", fg="white",
                           font=("arial", 12, "bold"), width=17, command=self.logout)
        btnSubmit.grid(row=0, column=5)
    def headInfo(self):
        self.voucher_date = Entry(self.Headerframe, textvariable=self.Creation_Date, fg="BLACK",
                                  font=("times new roman", 15, "bold"))
        self.voucher_date.grid(row=0, column=2, padx=10, pady=10)

        def open_calendar():
            dialog = tk.Toplevel(self.Headerframe)
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

        select_date = tk.Button(self.Headerframe, text="Select Date", command=open_calendar)
        select_date.grid(row=0, column=1, padx=10, pady=10)

        def date_updater(new_date):
            self.voucher_date.delete(0, tk.END)
            self.voucher_date.insert(0, new_date)

    def entrywidget(self):
        ###################################Data FRAME Header Label ###################################################
        LineNum1 = Label(self.DataframeLeft, text="ITEM", font=("times new roman", 12, "bold"))
        LineNum1.grid(row=0, column=0)

        LineNum2 = Label(self.DataframeLeft, text="Type", font=("times new roman", 12, "bold"))
        LineNum2.grid(row=0, column=1)

        LineNum3 = Label(self.DataframeLeft, text="DESCRIPTION", font=("times new roman", 12, "bold"))
        LineNum3.grid(row=0, column=2, columnspan=9, sticky='ew', padx=10, pady=10)

        LineNum7 = Entry(self.DataframeLeft, width=8, font=("times new roman", 12, "bold"),textvariable=self.voucher_num)
        LineNum7.config(state='readonly')
        LineNum7.grid(row=6, column=2, padx=10, pady=10)

        LineNum4 = Label(self.DataframeLeft, text="QUANTITY", font=("times new roman", 12, "bold"))
        LineNum4.grid(row=0, column=13, padx=10, pady=10)

        LineNum5 = Label(self.DataframeLeft, text="UNIT COST", font=("times new roman", 12, "bold"))
        LineNum5.grid(row=0, column=14, padx=10, pady=10)

        LineNum6 = Label(self.DataframeLeft, text="AMOUNT", font=("times new roman", 12, "bold"))
        LineNum6.grid(row=0, column=15, padx=10, pady=10)

        LineNum5 = Label(self.DataframeLeft, text="TOTAL", font=("times new roman", 12, "bold"))
        LineNum5.grid(row=6, column=14, padx=10, pady=10)

        ###################################Data FRAME fields ###########################################################
        Rowfield1 = Entry(self.DataframeLeft, textvariable=self.item1, width=5)
        # default_value = "Enter text here"
        Rowfield1.insert(1, 1)
        Rowfield1.config(state='readonly')
        Rowfield1.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        Rowfield2 = ttk.Combobox(self.DataframeLeft, textvariable=self.Type1, font=("times new roman", 12, "bold"), width=13)
        # Set a default value
        Rowfield2.set("NONE")
        Rowfield2["values"] = (
        "WELFARE", "REPAIR&MAINTENANCE", "UTILITY", "MISSION HOUSE","SUPPLIES", "REMITTANCE", "FURNITURE&FITTINGS", "TELECOMMUNICATION",
        "CONSTRUCTION","LOAN","REFRESHMENT","TRANSPORTATION")
        Rowfield2.grid(row=1, column=1)

        Rowfield3 = Entry(self.DataframeLeft, textvariable=self.Description1, width=80, font=("times new roman", 12, "bold"))
        Rowfield3.insert(0, 'NULL')
        Rowfield3.grid(row=1, column=2, columnspan=10, sticky='ew', padx=10, pady=10)

        Rowfield4 = Entry(self.DataframeLeft, textvariable=self.Quantity1, width=5)
        Rowfield4.insert(0, 0)
        Rowfield4.grid(row=1, column=13, padx=10, pady=10)

        Rowfield5 = Entry(self.DataframeLeft, textvariable=self.Unit_cost1, width=10, font=("times new roman", 10, "bold"))
        Rowfield5.insert(0, 0.0)
        Rowfield5.grid(row=1, column=14, padx=10, pady=10)

        self.Rowfield6 = Entry(self.DataframeLeft, textvariable=self.Line_Amount1, width=15, bg='yellow', font=("times new roman", 10, "bold"))
        self.Rowfield6.insert(0, 0.0)
        self.Rowfield6.grid(row=1, column=15, padx=10, pady=10)

        Rowfield7 = Entry(self.DataframeLeft, textvariable=self.item2, width=5)
        Rowfield7.insert(1, 2)
        Rowfield7.config(state='readonly')
        Rowfield7.grid(row=2, column=0, sticky='w', padx=10, pady=10)

        Rowfield8 = ttk.Combobox(self.DataframeLeft, textvariable=self.Type2, font=("times new roman", 12, "bold"), width=13)

        Rowfield8["values"] = (
        "WELFARE", "REPAIR&MAINTENANCE", "UTILITY", "SUPPLIES", "REMITTANCE", "FURNITURE&FITTINGS", "TELECOMMUNICATION",
        "CONSTRUCTION","LOAN","REFRESHMENT","TRANSPORTATION")
        Rowfield8.grid(row=2, column=1)
        Rowfield8.set("NONE")
        Rowfield9 = Entry(self.DataframeLeft, textvariable=self.Description2, width=80, font=("times new roman", 12, "bold"))
        Rowfield9.insert(1, "NULL")
        Rowfield9.grid(row=2, column=2, columnspan=10, sticky='ew', padx=10, pady=10)

        Rowfield10 = Entry(self.DataframeLeft, textvariable=self.Quantity2, width=5)
        Rowfield10.insert(1, 0)
        Rowfield10.grid(row=2, column=13, padx=10, pady=10)

        Rowfield11 = Entry(self.DataframeLeft, textvariable=self.Unit_cost2, width=10, font=("times new roman", 10, "bold"))
        Rowfield11.insert(1, 0.0)
        Rowfield11.grid(row=2, column=14, padx=10, pady=10)

        self.Rowfield12 = Entry(self.DataframeLeft, textvariable=self.Line_Amount2, width=15,bg='yellow',
                           font=("times new roman", 10, "bold"))
        self.Rowfield12.insert(1, 0.0)
        self.Rowfield12.grid(row=2, column=15, padx=10, pady=10)

        Rowfield13 = Entry(self.DataframeLeft, textvariable=self.item3, width=5)
        Rowfield13.insert(1, 3)
        Rowfield13.config(state='readonly')
        Rowfield13.grid(row=3, column=0, sticky='w', padx=10, pady=10)

        Rowfield14 = ttk.Combobox(self.DataframeLeft, textvariable=self.Type3, font=("times new roman", 12, "bold"),
                                  width=13)
        Rowfield14["values"] = (
        "WELFARE", "REPAIR&MAINTENANCE", "UTILITY", "SUPPLIES", "REMITTANCE", "FURNITURE&FITTINGS", "TELECOMMUNICATION",
        "CONSTRUCTION","LOAN","REFRESHMENT","TRANSPORTATION")
        Rowfield14.set("NONE")
        Rowfield14.grid(row=3, column=1)

        Rowfield15 = Entry(self.DataframeLeft, textvariable=self.Description3, width=80,
                           font=("times new roman", 12, "bold"))
        Rowfield15.insert(1, "NULL")
        Rowfield15.grid(row=3, column=2, columnspan=10, sticky='ew', padx=10, pady=10)

        Rowfield16 = Entry(self.DataframeLeft, textvariable=self.Quantity3, width=5)
        Rowfield16.insert(1, 0)
        Rowfield16.grid(row=3, column=13, padx=10, pady=10)

        Rowfield17 = Entry(self.DataframeLeft, textvariable=self.Unit_cost3, width=10, font=("times new roman", 10, "bold"))
        Rowfield17.insert(1, 0.0)
        Rowfield17.grid(row=3, column=14, padx=10, pady=10)

        self.Rowfield18 = Entry(self.DataframeLeft, textvariable=self.Line_Amount3, width=15,bg='yellow',
                           font=("times new roman", 10, "bold"))
        self.Rowfield18.insert(1, 0.0)
        self.Rowfield18.grid(row=3, column=15, padx=10, pady=10)

        Rowfield19 = Entry(self.DataframeLeft, textvariable=self.item4, width=5)
        Rowfield19.insert(1, 4)
        Rowfield19.config(state='readonly')
        Rowfield19.grid(row=4, column=0, sticky='w', padx=10, pady=10)

        Rowfield20 = ttk.Combobox(self.DataframeLeft, textvariable=self.Type4, font=("times new roman", 12, "bold"),
                                  width=13)
        Rowfield20["values"] = (
        "WELFARE", "REPAIR&MAINTENANCE", "UTILITY", "SUPPLIES", "REMITTANCE", "FURNITURE&FITTINGS", "TELECOMMUNICATION",
        "CONSTRUCTION","LOAN","REFRESHMENT","TRANSPORTATION")
        Rowfield20.set("NONE")
        Rowfield20.grid(row=4, column=1)

        Rowfield21 = Entry(self.DataframeLeft, textvariable=self.Description4, width=80,
                           font=("times new roman", 12, "bold"))
        Rowfield21.insert(1, "NULL")
        Rowfield21.grid(row=4, column=2, columnspan=10, sticky='ew', padx=10, pady=10)

        Rowfield22 = Entry(self.DataframeLeft, textvariable=self.Quantity4, width=5)
        Rowfield22.insert(1, 0)
        Rowfield22.grid(row=4, column=13, padx=10, pady=10)

        Rowfield23 = Entry(self.DataframeLeft, width=10, textvariable=self.Unit_cost4, font=("times new roman", 10, "bold"))
        Rowfield23.insert(1, 0.0)
        Rowfield23.grid(row=4, column=14, padx=10, pady=10)

        self.Rowfield24 = Entry(self.DataframeLeft, textvariable=self.Line_Amount4, width=15,bg='yellow',
                           font=("times new roman", 10, "bold"))
        self.Rowfield24.insert(1, 0.0)
        self.Rowfield24.grid(row=4, column=15, padx=10, pady=10)

        Rowfield25 = Entry(self.DataframeLeft, textvariable=self.item5, width=5)
        Rowfield25.insert(1, 5)
        Rowfield25.config(state='readonly')
        Rowfield25.grid(row=5, column=0, sticky='w', padx=10, pady=10)

        Rowfield26 = ttk.Combobox(self.DataframeLeft, textvariable=self.Type5, font=("times new roman", 12, "bold"),
                                  width=13)
        Rowfield26["values"] = (
        "WELFARE", "REPAIR&MAINTENANCE", "UTILITY", "SUPPLIES", "REMITTANCE", "FURNITURE&FITTINGS", "TELECOMMUNICATION",
        "CONSTRUCTION","LOAN","REFRESHMENT","TRANSPORTATION")
        Rowfield26.set("NONE")
        Rowfield26.grid(row=5, column=1)

        Rowfield27 = Entry(self.DataframeLeft, textvariable=self.Description5, width=80,
                           font=("times new roman", 12, "bold"))
        Rowfield27.insert(1, "NULL")
        Rowfield27.grid(row=5, column=2, columnspan=10, sticky='ew', padx=10, pady=10)

        Rowfield28 = Entry(self.DataframeLeft, textvariable=self.Quantity5, width=5)
        Rowfield28.insert(1, 0)
        Rowfield28.grid(row=5, column=13, padx=10, pady=10)

        Rowfield29 = Entry(self.DataframeLeft, textvariable=self.Unit_cost5, width=10, font=("times new roman", 10, "bold"))
        Rowfield29.insert(1, 0.0)
        Rowfield29.grid(row=5, column=14, padx=10, pady=10)

        self.Rowfield30 = Entry(self.DataframeLeft, textvariable=self.Line_Amount5, width=15,bg='yellow',
                           font=("times new roman", 10, "bold"))
        self.Rowfield30.insert(1, 0.0)
        self.Rowfield30.grid(row=5, column=15, padx=10, pady=10)

        self.Total = Entry(self.DataframeLeft, textvariable=self.TOTAL, state='readonly', width=15,
                      font=("times new roman", 10, "bold"))
        self.Total.grid(row=6, column=15, padx=10, pady=10)

    def buttonsDesign(self):
        btnSubmit = Button(self.Buttonframe, text="SUBMIT", bg="green",  fg="white",command=self.submit,
                           font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=0)

        btnSubmit = Button(self.Buttonframe, text="CLEAR", command=lambda: self.summaryClear(self.DataframeLeft), bg="yellow", fg="white", font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=1)

        btnSubmit = Button(self.Buttonframe, text="UPDATE", command=self.update, bg="green", fg="white", font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=2)

        btnSubmit = Button(self.Buttonframe, text="DOWNLOAD", command=self.expenseReport, bg="green", fg="white", font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=3)

        btnSubmit = Button(self.Buttonframe, text="DELETE", command=self.delete, bg="red", fg="white", font=("arial", 12, "bold"), width=20)
        btnSubmit.grid(row=0, column=4)


    def update_sum(self,*args):
        try:
            value1 = float(self.Rowfield6.get()) if self.Rowfield6.get() else 0
            value2 = float(self.Rowfield12.get()) if self.Rowfield12.get() else 0
            value3 = float(self.Rowfield18.get()) if self.Rowfield18.get() else 0
            value4 = float(self.Rowfield24.get()) if self.Rowfield24.get() else 0
            value5 = float(self.Rowfield30.get()) if self.Rowfield30.get() else 0
            total = value1 + value2 + value3 + value4 + value5
            self.Total.config(state='normal')
            self.Total.delete(0, tk.END)
            self.Total.insert(0, f"{total:.2f}")
            self.Total.config(state='readonly')
        except ValueError:
            self.Total.config(state='normal')
            self.Total.delete(0, tk.END)
            self.Total.insert(0, "Invalid input")
            self.Total.config(state='readonly')

    def autoSum(self):
        self.update_sum()
        self.Line_Amount1 = StringVar()
        self.Line_Amount2 = StringVar()
        self.Line_Amount3 = StringVar()
        self.Line_Amount4 = StringVar()
        self.Line_Amount5 = StringVar()

        self.Rowfield6.config(textvariable=self.Line_Amount1)
        self.Rowfield12.config(textvariable=self.Line_Amount2)
        self.Rowfield18.config(textvariable=self.Line_Amount3)
        self.Rowfield24.config(textvariable=self.Line_Amount4)
        self.Rowfield30.config(textvariable=self.Line_Amount5)

        self.Line_Amount1.trace_add('write', self.update_sum)
        self.Line_Amount2.trace_add('write', self.update_sum)
        self.Line_Amount3.trace_add('write', self.update_sum)
        self.Line_Amount4.trace_add('write', self.update_sum)
        self.Line_Amount5.trace_add('write', self.update_sum)

    def entriesDetails(self):
        Scroll_x = ttk.Scrollbar(self.Detailframe, orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(self.Detailframe, orient=VERTICAL)
        self.voucher_table = ttk.Treeview(self.Detailframe, columns=(
            "item1", "Type1", "Description1", "Quantity1", "Unit_cost1", "Line_Amount1", "item2", "Type2",
            "Description2",
            "Quantity2", "Unit_cost2", "Line_Amount2",
            "item3", "Type3", "Description3", "Quantity3", "Unit_cost3", "Line_Amount3", "item4", "Type4",
            "Description4",
            "Quantity4", "Unit_cost4", "Line_Amount4",
            "item5", "Type5", "Description5", "Quantity5", "Unit_cost5", "Line_Amount5", "TOTAL", "Creation_Date","Voucher num"),
                                          xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)
        Scroll_x.pack(side=BOTTOM, fill='x')
        Scroll_y.pack(side=RIGHT, fill='y')

        Scroll_x.config(command=self.voucher_table.xview)
        Scroll_y.config(command=self.voucher_table.yview)

        for col in self.voucher_table["columns"]:
            self.voucher_table.heading(col, text=col.replace("_", " ").title())

        for col in self.voucher_table["columns"]:
            self.voucher_table.column(col, width=80)  # Adjust width as needed

        self.voucher_table["show"] = "headings"

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        self.voucher_table.pack(fill=BOTH, expand=1)
        self.load()
        self.voucher_table.bind("<ButtonRelease-1>", self.get_cursor)
    ######################################### Buttons Functions#######################################################

    def submit(self):
        if self.item1.get() == " " or self.Line_Amount1 == "":
            messagebox.showerror("Error", "At least first row fields must be entered")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                               database="my_data")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "insert into my_data.voucher (Item1,Type1,Description1,Quantity1,Unit_cost1,Line_Amount1,"
                    "Item2,Type2,Description2,Quantity2,Unit_cost2,Line_Amount2,"
                    "Item3,Type3,Description3,Quantity3,Unit_cost3,Line_Amount3,"
                    "Item4,Type4,Description4,Quantity4,Unit_cost4,Line_Amount4,"
                    "Item5,Type5,Description5,Quantity5,Unit_cost5,Line_Amount5,TOTAL,creation_date )"
                    "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        # self.INVOICE_NUM.get(),
                        self.item1.get(),
                        self.Type1.get(),
                        self.Description1.get(),
                        self.Quantity1.get(),
                        self.Unit_cost1.get(),
                        self.Line_Amount1.get(),
                        self.item2.get(),
                        self.Type2.get(),
                        self.Description2.get(),
                        self.Quantity2.get(),
                        self.Unit_cost2.get(),
                        self.Line_Amount2.get(),
                        self.item3.get(),
                        self.Type3.get(),
                        self.Description3.get(),
                        self.Quantity3.get(),
                        self.Unit_cost3.get(),
                        self.Line_Amount3.get(),
                        self.item4.get(),
                        self.Type4.get(),
                        self.Description4.get(),
                        self.Quantity4.get(),
                        self.Unit_cost4.get(),
                        self.Line_Amount4.get(),
                        self.item5.get(),
                        self.Type5.get(),
                        self.Description5.get(),
                        self.Quantity5.get(),
                        self.Unit_cost5.get(),
                        self.Line_Amount5.get(),
                        self.TOTAL.get(),
                        self.Creation_Date.get()
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
        my_cursor.execute("select Item1,Type1,Description1,Quantity1,Unit_cost1,Line_Amount1,"
                          "Item2,Type2,Description2,Quantity2,Unit_cost2,Line_Amount2,"
                          "Item3,Type3,Description3,Quantity3,Unit_cost3,Line_Amount3,"
                          "Item4,Type4,Description4,Quantity4,Unit_cost4,Line_Amount4,"
                          "Item5,Type5,Description5,Quantity5,Unit_cost5,Line_Amount5,TOTAL,creation_date,INVOICE_NUM from my_data.voucher order by voucher.Invoice_num desc")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.voucher_table.delete(*self.voucher_table.get_children())
            for i in rows:
                self.voucher_table.insert("", END, values=i)

            conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        try:
            cursor_row = self.voucher_table.focus()
            content = self.voucher_table.item(cursor_row)
            row = content["values"]


            # Use a loop to set values for items 1-5
            for i in range(1, 6):
                base_index = (i - 1) * 6
                # Get the corresponding StringVar variables
                getattr(self, f'item{i}').set(row[base_index])
                getattr(self, f'Type{i}').set(row[base_index + 1])
                getattr(self, f'Description{i}').set(row[base_index + 2])
                getattr(self, f'Quantity{i}').set(row[base_index + 3])
                getattr(self, f'Unit_cost{i}').set(row[base_index + 4])
                getattr(self, f'Line_Amount{i}').set(row[base_index + 5])

            # Set total and creation date
            self.TOTAL.set(row[30])
            self.Creation_Date.set(row[31])
            self.voucher_num.set(row[32])

        except IndexError:
            print("Error: Selected row does not contain all expected values.")
        except AttributeError as e:
            print(f"Error: StringVar variable not found - {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def update(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                       database="my_data")
        my_cursor = conn.cursor()
        my_cursor.execute("update my_data.voucher set item1=%s, type1=%s, Description1=%s, Quantity1=%s, Unit_cost1=%s,"
                          " Line_Amount1=%s, item2=%s, type2=%s, Description2=%s, Quantity2=%s, Unit_cost2=%s, Line_Amount2=%s,"
                          " item3=%s, type3=%s, Description3=%s, Quantity3=%s, Unit_cost3=%s, Line_Amount3=%s, item4=%s, type4=%s,"
                          " Description4=%s, Quantity4=%s, Unit_cost4=%s, Line_Amount4=%s, item5=%s, type5=%s, Description5=%s,"
                          " Quantity5=%s, Unit_cost5=%s, Line_Amount5=%s, TOTAL=%s where invoice_num=%s",(

                          self.item1.get(),
                          self.Type1.get(),
                          self.Description1.get(),
                          self.Quantity1.get(),
                          self.Unit_cost1.get(),
                          self.Line_Amount1.get(),
                          self.item2.get(),
                          self.Type2.get(),
                          self.Description2.get(),
                          self.Quantity2.get(),
                          self.Unit_cost2.get(),
                          self.Line_Amount2.get(),
                          self.item3.get(),
                          self.Type3.get(),
                          self.Description3.get(),
                          self.Quantity3.get(),
                          self.Unit_cost3.get(),
                          self.Line_Amount3.get(),
                          self.item4.get(),
                          self.Type4.get(),
                          self.Description4.get(),
                          self.Quantity4.get(),
                          self.Unit_cost4.get(),
                          self.Line_Amount4.get(),
                          self.item5.get(),
                          self.Type5.get(),
                          self.Description5.get(),
                          self.Quantity5.get(),
                          self.Unit_cost5.get(),
                          self.Line_Amount5.get(),
                          self.TOTAL.get(),
                          self.voucher_num.get()
                            ))
        conn.commit()
        messagebox.showinfo("SUCCESS", f"Record updated SUCCESSFULLY for voucher number {self.voucher_num.get()}")
        self.load()
        conn.close()

    def delete(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="password@12",
                                       database="my_data")
        my_cursor = conn.cursor()
        query = "delete from my_data.voucher where invoice_num=%s"
        value = (self.voucher_num.get(),)
        my_cursor.execute(query, value)

        conn.commit()
        conn.close()
        self.load()
        messagebox.showinfo("DELETE", f"Voucher record deleted successfully for voucher number {self.voucher_num.get()}")

    def clear_frame_widgets(self, frame):
        # Reset all widgets in the frame
        for widget in self.DataframeLeft.winfo_children():
            widget_type = widget.winfo_class()

            if widget_type == "Entry":
                widget.delete(0, 'end')  # Clear entry widget

            elif widget_type == "Text":
                widget.delete('NULL', 'end')  # Clear text widget

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

    def expenseReport(self):
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
                    headers = [self.voucher_table.heading(column)['text'] for column in self.voucher_table['columns']]
                    writer.writerow(headers)

                    # Write data rows
                    for item in self.voucher_table.get_children():
                        values = self.voucher_table.item(item)['values']
                        writer.writerow(values)

                messagebox.showinfo("Success", f"Data successfully downloaded to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download data: {str(e)}")

    def summaryClear(self, frame1):
        for widget in self.DataframeLeft.winfo_children():
            widget_type = widget.winfo_class()

            if widget_type == "Entry":
                widget.delete(0, 'end')  # Clear entry widget

            elif widget_type == "Text":
                widget.delete('0.00', 'end')  # Clear text widget


    def logout(self):
        self.root.destroy()

root = Tk()
ob = Expense(root)
root.mainloop()