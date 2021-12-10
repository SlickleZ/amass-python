import pymysql
from datetime import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox


def create_db():
    try:
        username = ent_user_name.get()
        pw = ent_user_pw.get()
        conn = pymysql.connect(host="localhost", user=username, passwd=pw)
        cs = conn.cursor()
        cs.execute("CREATE DATABASE Ledger")  # If you want to delete database "DROP" can help you
    except pymysql.err.OperationalError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
    except pymysql.err.ProgrammingError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
    except pymysql.err.InternalError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
    else:
        tk.messagebox.showinfo("Completed", "Created database successfully! :)")
        conn.close()
        cs.close()


def create_table():
    try:
        username = ent_user_name.get()
        pw = ent_user_pw.get()
        conn1 = pymysql.connect(host="localhost", user=username, passwd=pw, db='Ledger')
        cs1 = conn1.cursor()
        cs1.execute("""CREATE TABLE Ledger_Record (DateTime CHAR(60) COLLATE utf8_bin, 
                               Description CHAR(100) COLLATE utf8_bin,
                               Income INT(10) NOT NULL, Expenses INT(10) NOT NULL, Balance INT(10),
                               PRIMARY KEY(DateTime))""")
    except pymysql.err.OperationalError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :( ")
        
    except pymysql.err.ProgrammingError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
        
    except pymysql.err.InternalError:
        tk.messagebox.showerror("Error", "Oops!\nSomethings went wrong. :(")
        
    else:
        tk.messagebox.showinfo("Completed", "Created table successfully! :)")
        conn1.close()
        cs1.close()


def initial_val():
    try:
        username = ent_user_name.get()
        pw = ent_user_pw.get()
        conn1 = pymysql.connect(host="localhost", user=username, passwd=pw, db='Ledger')
        cs1 = conn1.cursor()
        now1 = datetime.now()
        dt1 = now1.strftime("%d %b, %Y / %H:%M:%S")
        cs1.execute("""INSERT INTO Ledger_Record(DateTime, Description, Income, Expenses, Balance)
                                                VALUES("%s", "Initial Values", 0, 0, 0)""" % dt1)
        conn1.commit()
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


def manage():
    gui.iconify()
    root = Toplevel()
    root.title('Amass')
    root.iconbitmap('icon.ico')
    width_of_window1 = 500
    height_of_window1 = 80
    screen_width1 = gui.winfo_screenwidth()
    screen_height1 = gui.winfo_screenheight()
    x_coordinate1 = (screen_width1 / 2) - (width_of_window1 / 2)
    y_coordinate1 = (screen_height1 / 2) - (height_of_window1 / 2)
    root.geometry('%dx%d+%d+%d' % (width_of_window1, height_of_window1, x_coordinate1, y_coordinate1))
    frm1 = ttk.LabelFrame(root, text='Choose the options')
    frm1.pack()
    btn1 = ttk.Button(frm1, text='Create database', command=create_db)
    btn1.grid(column=0, row=0, pady=5, padx=5, ipadx=5, ipady=5)
    btn2 = ttk.Button(frm1, text='Create table', command=create_table)
    btn2.grid(column=1, row=0, pady=5, padx=5, ipadx=15, ipady=5)
    btn3 = ttk.Button(frm1, text='Set initial values', command=initial_val)
    btn3.grid(column=2, row=0, pady=5, padx=5, ipadx=5, ipady=5)
    

gui = Tk()
gui.title('Amass')
gui.iconbitmap('icon.ico')
width_of_window = 240
height_of_window = 120
screen_width = gui.winfo_screenwidth()
screen_height = gui.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
gui.geometry('%dx%d+%d+%d' % (width_of_window, height_of_window, x_coordinate, y_coordinate))
frm = ttk.LabelFrame(gui, text='Log in to your database')
frm.pack()

lbl_id = ttk.Label(frm, text='Username : ')
lbl_id.grid(column=0, row=0)
lbl_pw = ttk.Label(frm, text='Password : ')
lbl_pw.grid(column=0, row=1)

ent_user_name = ttk.Entry(frm, width=23)
ent_user_name.grid(column=1, row=0, padx=5, pady=5, ipadx=5)
ent_user_pw = ttk.Entry(frm, show='*', width=23)
ent_user_pw.grid(column=1, row=1, padx=5, pady=5, ipadx=5)

btn = ttk.Button(frm, text='Login', command=manage)
btn.grid(column=1, row=2, pady=5)

gui.mainloop()
