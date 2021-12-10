from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime
import csv
import os


def calc():
    try:
        global pw
        global username
        pw = ent_pw.get()
        username = ent_id.get()
        conn = pymysql.connect(host="localhost", user=username, passwd=pw, db='Ledger')
        cs = conn.cursor()
        
        now = datetime.now()
        dt = now.strftime("%d %b, %Y / %H:%M:%S")
        des = ent_des.get()
        inc = int(ent_inc.get())
        out = int(ent_exp.get())

        cs.execute("SELECT * FROM Ledger_Record")
        data = cs.fetchall()
        bal = data[-1][4]  # data[-1][4] is the last Balance value

        cs.execute("""INSERT INTO Ledger_Record(DateTime, Description, Income, Expenses, Balance)
                    VALUES("%s", "%s", %d, %d, %d)""" % (dt, des, inc, out, bal))

        cs.execute("SELECT * FROM Ledger_Record")
        new_data = cs.fetchall()
        new_bal = bal + new_data[-1][2] - new_data[-1][3]

        cs.execute("""UPDATE Ledger_Record SET Balance = %d WHERE DateTime = '%s' """ % (new_bal, new_data[-1][0]))
        conn.commit()
        refresh_items()

    except pymysql.err.OperationalError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
    else:
        tk.messagebox.showinfo("Completed", "Data saved successfully :)")
        conn.close()
        cs.close()


def clear():
    entry_des.delete(0, END)
    entry_inc.delete(0, END)
    entry_exp.delete(0, END)


def refresh_items():
    for row in tv_table.get_children():
        tv_table.delete(row)
    pw1 = ent_pw.get()
    username1 = ent_id.get()
    conn = pymysql.connect(host="localhost", user=username1, passwd=pw1, db='Ledger')
    cs = conn.cursor()
    cs.execute("SELECT * FROM Ledger_Record")
    newest_data = cs.fetchall()
    for row in newest_data:
        data = [row[0], row[1], row[2], row[3], row[4]]
        tv_table.insert('', 'end', values=data)
    


def monthly():
    try:
        pw = ent_pw.get()
        username = ent_id.get()
        conn1 = pymysql.connect(host="localhost", user=username, passwd=pw, db='Ledger')
        cs1 = conn1.cursor()
        now1 = datetime.now()
        dt1 = now1.strftime("%d %b, %Y / %H:%M:%S")
        month = now1.strftime("%b")

        cs1.execute("SELECT * FROM Ledger_Record")
        data = cs1.fetchall()
        bal = data[-1][4]  # data[-1][4] is the last Balance value
        path = os.path.join(os.path.join(os.environ['USERPROFILE'], r'Desktop\Ledger Report\2020 Report\Report.csv'))
        with open(path, 'a', encoding="utf-8",newline="") as fileout:
            writer = csv.writer(fileout)
            writer.writerows(data)
        

        cs1.execute("""DROP TABLE IF EXISTS Ledger_Record""")
        cs1.execute("""CREATE TABLE Ledger_Record (DateTime CHAR(60) COLLATE utf8_bin, 
                               Description CHAR(100) COLLATE utf8_bin,
                               Income INT(10) NOT NULL, Expenses INT(10) NOT NULL, Balance INT(10),
                               PRIMARY KEY(DateTime))""")
        cs1.execute("""INSERT INTO Ledger_Record(DateTime, Description, Income, Expenses, Balance)
                                                VALUES("{}", "Initial Monthly Values", 0, 0, {})""".format(dt1, bal))
        conn1.commit()
        refresh_items()

    except pymysql.err.OperationalError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
    except pymysql.err.ProgrammingError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
    except pymysql.err.InternalError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
    else:
        tk.messagebox.showinfo("Completed", " success! :)")
        conn1.close()
        cs1.close()
        

def show_icon():
    root.destroy()
    gui.deiconify()

def login():
    if ent_pw.get() == 'MY_PASSWORD':
        amass()
    else:
        tk.messagebox.showerror("Error!", "Wrong password! :(")

def amass():
    gui.withdraw()
    global root
    global ent_des
    global ent_exp
    global ent_inc
    global entry_des
    global entry_exp
    global entry_inc

    root = Toplevel()
    root.title('Amass')
    root.iconbitmap('icon.ico')
    width_of_window1 = 1280
    height_of_window1 = 650
    screen_width1 = root.winfo_screenwidth()
    screen_height1 = root.winfo_screenheight()
    x_coordinate1 = (screen_width1 / 2) - (width_of_window1 / 2)
    y_coordinate1 = (screen_height1 / 2) - (height_of_window1 / 2)
    root.geometry('%dx%d+%d+%d' % (width_of_window1, height_of_window1, x_coordinate1, y_coordinate1))

    #  -------------------------Descriptions------------------------------------
    ttk.Label(root, text='Enter description', font=('TH Sarabun New', 14)).grid(row=1, column=0, padx=10,
                                                                                pady=10)
    ent_des = StringVar()
    entry_des = ttk.Entry(root, textvariable=ent_des, width=20)
    entry_des.grid(row=1, column=1, ipadx=50, ipady=1)

    #  -------------------------------Income------------------------------------
    ttk.Label(root, text='Enter your income', font=('TH Sarabun New', 14)).grid(row=2, column=0, padx=10,
                                                                                pady=10)
    ent_inc = StringVar()
    entry_inc = ttk.Entry(root, textvariable=ent_inc)
    entry_inc.grid(row=2, column=1, ipadx=10, ipady=1)

    #  -------------------------------Expense------------------------------------
    ttk.Label(root, text='Enter your expense', font=('TH Sarabun New', 14)).grid(row=3, column=0, padx=10,
                                                                                 pady=10)
    ent_exp = StringVar()
    entry_exp = ttk.Entry(root, textvariable=ent_exp)
    entry_exp.grid(row=3, column=1, ipadx=10, ipady=1)

    # ===================================Button===================================
    ttk.Button(root, text='Add', command=calc).grid(column=1, row=4, padx=15, pady=15, ipadx=5, ipady=5)
    ttk.Button(root, text='Clear', command=clear).grid(column=1, row=5, padx=15, pady=15, ipadx=5, ipady=5)

    # ===============================Tree View====================================
    ttk.Label(root, text='Your History Ledger', font=('TH Sarabun New', 16)).grid(row=6, column=1, padx=10,
                                                                                  pady=10)
    global tv_table
    tv_list = ['DateTime', 'Description', 'Incomes', 'Expenses', 'Balances']
    tv_table = ttk.Treeview(root, column=tv_list, show='headings', height=10)
    for i in tv_list:
        tv_table.heading(i, text=i.title())
    tv_table.grid(column=1, row=7, ipadx=1, ipady=5)
    ttk.Style().configure("Treeview", font=('TH Sarabun New', 16), anchor="s")
    ttk.Style().configure("Treeview.Heading", font=('TH Sarabun New', 14))
    vsb = ttk.Scrollbar(root, orient="vertical", command=tv_table.yview)
    vsb.grid(column=2, row=7, ipadx=10, ipady=100)

    tv_table.configure(yscrollcommand=vsb.set)

    ttk.Button(root, text='Refresh', command=refresh_items).grid(column=0, row=8, padx=5, pady=5, ipadx=5, ipady=5)
    ttk.Button(root, text='Exit', command=show_icon).grid(column=1, row=8, padx=5, pady=5, ipadx=5, ipady=5)
    btn4 = ttk.Button(root, text='Report', command=monthly)
    btn4.grid(column=2, row=8, pady=5, padx=5, ipadx=5, ipady=5)


def pri_win():
    global ent_pw
    global ent_id
    global gui
    gui = Tk()
    gui.title('Amass')
    gui.iconbitmap('icon.ico')
    width_of_window = 300
    height_of_window = 170
    screen_width = gui.winfo_screenwidth()
    screen_height = gui.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    gui.geometry('%dx%d+%d+%d' % (width_of_window, height_of_window, x_coordinate, y_coordinate))
    frm = ttk.LabelFrame(gui, text='Log in to your database')
    frm.pack()
    #  -------------------------Log-in------------------------------------
    lbl_id = ttk.Label(frm, text='Username :', font=('TH Sarabun New', 14))
    lbl_id.grid(column=0, row=0, padx=10, pady=10)

    ent_id = StringVar()
    entry_id = ttk.Entry(frm, textvariable=ent_id, width=25)
    entry_id.grid(row=0, column=1, ipady=1, padx=10)

    label_pw = ttk.Label(frm, text='Password :', font=('TH Sarabun New', 14))
    label_pw.grid(row=1, column=0, padx=10, pady=10)

    ent_pw = StringVar()
    entry_pw = ttk.Entry(frm, textvariable=ent_pw, show="*", width=25)
    entry_pw.grid(row=1, column=1, ipady=1, padx=10)

    btn = ttk.Button(frm, text='Log In', command=login)
    btn.grid(column=1, row=2, padx=10, pady=5, ipadx=5, ipady=5)

    btn1 = ttk.Button(frm, text='Exit', command=gui.destroy)
    btn1.grid(column=0, row=2, padx=10, pady=5, ipadx=1, ipady=1)
    gui.mainloop()


pri_win()
