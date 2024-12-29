from tkinter import RIDGE, Label, Tk, Frame, LabelFrame, Entry, Button, ttk, messagebox
import tkinter as tk
import mysql.connector



class users:
    def __init__(self, root):
        self.root = root
        self.root.title("RCCG TURKEY MISSION SYSTEM")
        self.root.iconbitmap('RCCGpx.ico')
        self.root.geometry("1540x900")
        self.current_user = None
        Ltitle = Label(self.root, bd=20, relief=RIDGE, text="RCCG TURKEY FINANCIAL REPORTING SYSTEM", fg="red",
                       bg="white", font=("times new roman", 30, "bold"))
        Ltitle.pack(side='top', fill='x')
        Ititle2 = Label(self.root, bd=20, text="WELCOME", fg="BLACK", bg="white",
                        font=("Arial Black", 20, "bold"))
        Ititle2.pack(side='top', fill='x')

        self.Dataframe = Frame(self.root, bd=20, bg="green")
        self.Dataframe.place(x=0, y=180, width=1280, height=750)
        # Create left and right frames
        self.create_frames()
        self.show_login_page()
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password@12",
            database="my_data"
        )
        self.cursor = self.db.cursor()

    def create_frames(self):
        # Create left frame
        self.DataframeLeft = LabelFrame(self.Dataframe, bd=2, relief=RIDGE,
                                        padx=10,
                                        font=("times new roman", 12, "bold"),
                                        text="USER Information")
        self.DataframeLeft.place(x=0, y=0, width=620, height=750)

        # Create right frame
        self.DataframeRight = LabelFrame(self.Dataframe, bd=2, relief=RIDGE,
                                         padx=10, bg="white",
                                         font=("times new roman", 12, "bold"),
                                         text="Welcome Information")
        self.DataframeRight.place(x=620, y=1, width=630, height=750)
        self.show_login_page()

    def clear_frame(self):
        # Clear only the contents of the frames, not the frames themselves
        for widget in self.DataframeLeft.winfo_children():
            widget.destroy()
        for widget in self.DataframeRight.winfo_children():
            widget.destroy()

    def show_login_page(self):
        self.clear_frame()

        # Login form elements
        header = Label(self.DataframeLeft, text="LOGIN",
                       font=('Helvetica', 25), fg="green")
        header.grid(row=0, column=0, columnspan=2, pady=20)

        username_label = Label(self.DataframeLeft, text="Username:", font=('Helvetica', 15))
        username_label.grid(row=1, column=0, pady=5)
        self.username_entry = Entry(self.DataframeLeft, width=30)
        self.username_entry.grid(row=1, column=1, pady=5)

        password_label = Label(self.DataframeLeft, text="Password:",font=('Helvetica', 15))
        password_label.grid(row=2, column=0, pady=5)
        self.password_entry = Entry(self.DataframeLeft, show="*", width=30)
        self.password_entry.grid(row=2, column=1, pady=5)
        self.current_user = self.username_entry.get()
        print(self.current_user)

        login_button = Button(self.DataframeLeft, text="Login",font=('Helvetica', 10), bg="white", width=15,
                              command=lambda: self.login(self.username_entry.get(), self.password_entry.get()))
        login_button.grid(row=3, column=1, columnspan=2, pady=10)

        register_button = Button(self.DataframeLeft, text="Register", font=('Helvetica', 10), bg="white",width=15,
                                 command=self.show_register_page)
        register_button.grid(row=4, column=1, columnspan=2, pady=5)
    def show_register_page(self):
        self.clear_frame()

        # Registration form elements
        header = Label(self.DataframeLeft, text="Register",
                       font=('Helvetica', 30), fg="green")
        header.grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        Label(self.DataframeLeft, text="USERNAME:", font=('Helvetica', 15)).grid(row=1, column=0, pady=5)
        self.reg_username = Entry(self.DataframeLeft,  width=30)
        self.reg_username.grid(row=1, column=1, pady=5)

        # Surname
        Label(self.DataframeLeft, text="SURNAME:",font=('Helvetica', 15)).grid(row=2, column=0, pady=5)
        self.reg_surname = Entry(self.DataframeLeft, width=30)
        self.reg_surname.grid(row=2, column=1, pady=5)

        # Other name
        Label(self.DataframeLeft, text="OTHERNAME:",font=('Helvetica', 15)).grid(row=3, column=0, pady=5)
        self.reg_othername = Entry(self.DataframeLeft, width=30)
        self.reg_othername.grid(row=3, column=1, pady=5)

        # Password
        Label(self.DataframeLeft, text="Password:",font=('Helvetica', 15)).grid(row=4, column=0, pady=5)
        self.reg_password = Entry(self.DataframeLeft, show="*", width=30)
        self.reg_password.grid(row=4, column=1, pady=5)

        # Role selection
        Label(self.DataframeLeft, text="ROLE:",font=('Helvetica', 15)).grid(row=5, column=0, pady=5)
        self.reg_role = ttk.Combobox(self.DataframeLeft,
                                     values=['user', 'manager'], width=20)
        self.reg_role.set('user')
        self.reg_role.grid(row=5, column=1, pady=5)

        # Buttons
        Button(self.DataframeLeft, text="Register",width=20,font=('Helvetica', 15),bg="white",
               command=lambda: self.register(self.reg_username.get(),self.reg_surname.get(),
                                             self.reg_othername.get(),self.reg_password.get(),self.reg_role.get())).grid(row=6, column=1, columnspan=2, pady=10)

        Button(self.DataframeLeft, text="Back to Login", width=25,font=('Helvetica', 15),bg="white",
               command=self.show_login_page).grid(row=7, column=1,
                                                  columnspan=2, pady=5)

    def login(self, username, password):
        try:
            if not username.strip() or not password.strip():
                messagebox.showerror("Error", "Please fill in all fields")
                return

            query = """
                    SELECT id, username, role, status 
                    FROM my_data.users 
                    WHERE username=%s AND password=%s
                """
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()

            if not user:
                messagebox.showerror("Error", "Invalid credentials")
                return

            status = user[3]
            if status == 'pending':
                messagebox.showinfo("Info", "Your account is pending approval")
                return
            elif status == 'rejected':
                messagebox.showinfo("Info", "Your account has been rejected")
                return

            role = user[2]
            if role == 'admin':
                self.show_admin_page()
            elif role == 'manager':
                self.show_manager_page()
            else:
                self.current_user = username
                self.show_user_page()
                # self.show_user_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Login failed: {err}")

    def register(self, reg_username, reg_surname, reg_othername, reg_password, reg_role):
        try:
            if not all([reg_username.strip(), reg_surname.strip(), reg_othername.strip(), reg_password.strip()]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            query = """
                INSERT INTO my_data.users 
                (username, surname, othername, password, role, status, created_at)
                VALUES (%s, %s, %s, %s, %s, 'pending', NOW())
            """
            self.cursor.execute(query, (reg_username, reg_surname, reg_othername, reg_password, reg_role))
            self.db.commit()
            messagebox.showinfo("Success", "Registration successful! Please wait for admin approval")
            self.show_login_page()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Registration failed: {err}")

    def show_admin_page(self):
        self.clear_frame()
        try:
            # Create Treeview with scrollbar
            tree_frame = ttk.Frame(self.DataframeLeft)
            tree_frame.grid(row=1, column=0, columnspan=4, pady=10)

            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side='right', fill='y')

            columns = ('id', 'Username', 'OtherName', 'Role', 'Status', 'Created At')
            tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                yscrollcommand=scrollbar.set)
            scrollbar.config(command=tree.yview)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            tree.pack(expand=True, fill='both')

            # Fetch and display users
            self.cursor.execute("""
                SELECT id, Username, OtherName, Role, Status, created_at 
                FROM my_data.users 
                WHERE role != 'admin'
                ORDER BY created_at DESC
            """)
            for user in self.cursor.fetchall():
                tree.insert('', 'end', values=user)

            def approve_user():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Please select a user")
                    return

                user_id = tree.item(selected[0])['values'][0]
                self.cursor.execute("UPDATE my_data.users SET status='approved' WHERE id=%s", (user_id,))
                self.db.commit()
                self.show_admin_page()

            def reject_user():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Please select a user")
                    return

                user_id = tree.item(selected[0])['values'][0]
                self.cursor.execute("UPDATE my_data.users SET status='rejected' WHERE id=%s", (user_id,))
                self.db.commit()
                self.show_admin_page()

            ttk.Button(self.DataframeLeft, text="Approve", command=approve_user).grid(row=2, column=0, pady=10)
            ttk.Button(self.DataframeLeft, text="Reject", command=reject_user).grid(row=2, column=1, pady=10)
            ttk.Button(self.DataframeLeft, text="Refresh", command=self.show_admin_page).grid(row=2, column=2, pady=10)
            ttk.Button(self.DataframeLeft, text="Logout", command=self.show_login_page).grid(row=2, column=3, pady=10)
            Button(self.DataframeLeft, text="REPORTS", width=15,bg="green",fg="white",
                   command=self.open_report_window).grid(row=4, column=1, columnspan=2, pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load users: {err}")

    def show_user_page(self):
        self.clear_frame()

        ttk.Label(self.DataframeLeft, text="User Dashboard", font=('Helvetica', 16)).grid(row=0, column=0, pady=20)

        # # Check if user is approved
        username=self.current_user # You'll need to add this attribute during login
        print(username)
        self.cursor.execute("SELECT status FROM my_data.users WHERE username=%s", (username,))
        status = self.cursor.fetchone()[0]

        if status == 'approved':
            Button(self.DataframeLeft, text="Manage Expenses", width=15,
                       command=self.open_expense_window).grid(row=2, column=0, pady=5)
            Button(self.DataframeLeft, text="Manage Income", width=15,
                       command=self.open_income_window).grid(row=3, column=0, pady=5)
        else:
            Label(self.DataframeLeft, text="Your account needs approval to access these features",
                      font=('Helvetica', 12)).grid(row=2, column=0, pady=20)

        Button(self.DataframeLeft, text="Logout", width=20,
                   command=self.show_login_page).grid(row=5, column=0, pady=20)

    def open_expense_window(self):
        expense_window = tk.Toplevel(self.root)
        from expense import Expense
        expense_app = Expense(expense_window)

    def open_income_window(self):
        Receipt_window = tk.Toplevel(self.root)
        from Receipt import Income
        Receipt_app = Income(Receipt_window)

    def open_report_window(self):
        report_window = tk.Toplevel(self.root)
        from report import Report
        Report_app = Report(report_window)



root = Tk()
ob = users(root)
root.mainloop()