#Enter MySQL Info -- Line 37

from tkinter import ttk, BOTH, Menu, RIGHT, CENTER, LEFT, W, E, N, S, TclError
from ttkthemes import ThemedTk

import mysql.connector
import re


class atm:
    
    def __init__(self,master):

        master.title('ATM Machine')

        master.iconbitmap('money.ico')

        # ***** Frames *****

        self.mainFrame = ttk.Frame(master, width=500, height=500)
        self.mainFrame.pack(fill=BOTH)

        # ***** Styles *****

        style = ttk.Style(mainWin)
        style.configure('TButton', font=('Helvetica', 20), padding=10)
        style.configure('TEntry', padding=5)
        style.configure('TLabel', font=('Courier', 15), padding=10)
        style.configure('B.TLabel', font=('Courier', 15, 'bold'), padding=10)
        style.configure('L.TLabel', font=('Courier', 20), padding=10)

        self.font = 'Helvetica 15'
        self.Lfont = 'Helvetica 20'

        # ***** MySQL Info *****

        self.host = 'localhost'
        self.user = 'root'
        self.passwd = '123456'
        self.database = 'atm'

        # ***** Stuff for login *****

        self.clearFrame()
        self.comment1 = ttk.Label(self.mainFrame, justify=RIGHT, style='TLabel', text='Account Number:')
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)
        
        self.name = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.font, width=13)
        self.name.grid(row=1, column=2, padx=5, pady=5)
        self.name.focus_set()
        
        self.comment2 = ttk.Label(self.mainFrame, justify=RIGHT, style='TLabel', text='Account Pin:')
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)
        
        self.pin = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.font, show='*', width=13)
        self.pin.grid(row=2, column=2, padx=5, pady=5)

        self.comment3 = ttk.Label(self.mainFrame, justify=CENTER, style='B.TLabel', text='', foreground='red')
        self.comment3.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.login = ttk.Button(self.mainFrame, text='Login', style='TButton', command=self.auth)
        self.login.grid(row=4, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.lSpace = ttk.Label(self.mainFrame, width=4)
        self.lSpace.grid(row=0, column=0, pady=50)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=5, column=3, pady=100)

        global bind_id
        bind_id = mainWin.bind('<Return>',self.auth)

    # ***** Functions *****

    def isFloat(self,n):
        n = str(n)
        return bool(re.match(r'^-?\d+(\.\d+)?$', n))

    def isFloat2d(self,n):
        n = str(n)
        return bool(re.match(r'^-?\d+(\.\d\d)?$', n))

    def clearFrame(self):
        for widget in self.mainFrame.winfo_children():
            widget.grid_remove()

    def auth(self,*args):
        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = mydb.cursor()
        cursor.execute('select * from user_info;')
        details = cursor.fetchone()
        global loggedAcc
        loggedAcc = self.name.get()
        global loggedPin
        loggedPin = self.pin.get()
        if loggedAcc.isdigit() and loggedPin.isdigit():
            while details is not None:
                if eval(loggedAcc) == details[0]:
                    correctPin = details[1]
                    global amt
                    amt = details[2]
                    break
                else:
                    details = cursor.fetchone()
            else:
                self.comment3.config(text='Invalid credentials')
        else:
            self.comment3.config(text='Invalid credentials')
        if loggedPin != '':
            if eval(loggedPin) == correctPin:
                self.homePage()
            else:
                self.comment3.config(text='Invalid credentials')

    def Deposit(self,*args):
        self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text='', style='TLabel', foreground='green')
        self.comment2.grid(row=3, column=1, pady=5)

        amount = self.depositAmount.get()
        if amount != '' and self.isFloat(amount):
            mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
            cursor1 = mydb.cursor()
            cursor1.execute('select balance from user_info where uid = '+loggedAcc+';')
            amt = cursor1.fetchall()[0][0]
            if self.isFloat2d(amount):
                if len(str(amt + eval(amount))) < 20:
                    mydbs = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
                    cursor2 = mydbs.cursor()
                    cursor2.execute('update user_info set balance = balance + '+amount+' where uid = '+loggedAcc+';')
                    mydbs.commit()
                    
                    self.comment2.grid_remove()
                    self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text=str(amount)+' Deposited!', style='TLabel', foreground='green')
                    self.comment2.grid(row=3, column=1, pady=5)
                else:
                    self.comment2.grid_remove()
                    self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text='Enter a smaller amount', style='TLabel', foreground='green')
                    self.comment2.grid(row=3, column=1, pady=5)
            else:
                self.comment2.grid_remove()
                self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text='Only two decimal places are allowed', style='TLabel', foreground='green')
                self.comment2.grid(row=3, column=1, pady=5)
        else:
            self.comment2.grid_remove()
            self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text='Enter an amount to deposit', style='TLabel', foreground='green')
            self.comment2.grid(row=3, column=1, pady=5)

    def Withdraw(self,*args):
        amount = self.withdrawAmount.get()
        if amount != '' and self.isFloat(amount):
            mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
            cursor1 = mydb.cursor()
            cursor1.execute('select balance from user_info where uid = '+loggedAcc+';')
            amt = cursor1.fetchall()[0][0]
            if self.isFloat2d(amount):
                if (amt-eval(amount)) > 1000:
                    mydbs = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
                    cursor2 = mydbs.cursor()
                    cursor2.execute('update user_info set balance = balance - '+amount+' where uid = '+loggedAcc+';')
                    mydbs.commit()
                    
                    self.comment2.grid_remove()
                    self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text=str(amount)+' Withdrawn!', style='TLabel',foreground='green')
                    self.comment2.grid(row=3, column=1, pady=5)
                else:
                    self.comment2.grid_remove()
                    self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text='The entered amount is more\nthan the available balance', style='TLabel', foreground='green')
                    self.comment2.grid(row=3, column=1, pady=5)

                    self.ok.config(width=17)
                    self.withdrawAmount.config(width=17)
            else:
                self.comment2.grid_remove()
                self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text='Only two decimal places are allowed', style='TLabel', foreground='green')
                self.comment2.grid(row=3, column=1, pady=5)
        else:
            self.comment2.grid_remove()
            self.comment2 = ttk.Label(self.mainFrame, justify=CENTER, text='Enter an amount to withdraw', style='TLabel', foreground='green')
            self.comment2.grid(row=3, column=1, pady=5)

    def changePin(self,*args):
        self.comment4 = ttk.Label(self.mainFrame, text='', justify=RIGHT, style='TLabel', foreground='red')
        self.comment4.grid(row=4, column=1, pady=5, sticky=W+E+N+S, columnspan=2)

        currentpin = self.currentPin.get()
        newpin = self.newPin.get()
        newpincheck = self.newPinCheck.get()

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor1 = mydb.cursor()
        cursor1.execute('select pin from user_info where uid = '+loggedAcc+';')
        oldpin = str(cursor1.fetchall()[0][0])
        mydbs = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor2 = mydbs.cursor()
        
        if oldpin == currentpin:
            if newpin != '':
                if currentpin != newpin:
                    if len(newpin) == 4:
                        if newpin == newpincheck:
                            cursor2.execute('update user_info set pin = '+newpin+' where uid = '+loggedAcc+' ;')
                            mydbs.commit()
                            self.comment4.config(text='Account pin changed', foreground='green')
                        else:
                            self.comment4.config(text='New pin does not match')
                    else:
                        self.comment4.config(text='New pin should have 4 digits')
                else:
                    self.comment4.config(text='Enter a different pin')
            else:
                self.comment4.config(text='Enter a new pin')
        else:
            self.comment4.config(text='Old pin is incorrect')

    # ***** Navigation Functions *****

    def homePage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',bind_id)
        except TclError:
            pass

        self.balance = ttk.Button(self.mainFrame, text='Check Account Balance', style='TButton', command=self.balancePage)
        self.balance.grid(row=1, column=1, sticky=W+E+N+S, pady=5)

        self.deposit = ttk.Button(self.mainFrame, text='Deposit an Amount', style='TButton', command=self.depositPage)
        self.deposit.grid(row=2, column=1, sticky=W+E+N+S, pady=5)

        self.withdraw = ttk.Button(self.mainFrame, text='Withdraw an Amount', style='TButton', command=self.withdrawPage)
        self.withdraw.grid(row=3, column=1, sticky=W+E+N+S, pady=5)

        self.chPin = ttk.Button(self.mainFrame, text='Change PIN Number', style='TButton', command=self.pinChangePage)
        self.chPin.grid(row=4,column=1, sticky=W+E+N+S, pady=5)

        self.logout = ttk.Button(self.mainFrame, text='Logout', style='TButton', command=self.loginPage)
        self.logout.grid(row=5,column=1, pady=25)
        
        self.lSpace = ttk.Label(self.mainFrame, width=6)
        self.lSpace.grid(row=0, column=0, pady=15)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=6, column=2, pady=100)
    
    def balancePage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',bind_id)
        except TclError:
            pass

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = mydb.cursor()
        cursor.execute('select balance from user_info where uid = '+loggedAcc+';')
        global amt
        amt = cursor.fetchall()[0][0]
        
        self.comment = ttk.Label(self.mainFrame, justify=CENTER, text='Current Balance',  style='TLabel')
        self.comment.grid(row=1, column=1, padx=5, pady=5)

        self.showBalance = ttk.Label(self.mainFrame, text=str(amt), style='L.TLabel')
        self.showBalance.grid(row=2, column=1, padx=5, pady=5)

        self.deposit = ttk.Button(self.mainFrame, text='Deposit an Amount', style='TButton', command=self.depositPage)
        self.deposit.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.withdraw = ttk.Button(self.mainFrame, text='Withdraw an Amount', style='TButton', command=self.withdrawPage)
        self.withdraw.grid(row=4, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.back = ttk.Button(self.mainFrame, text='Back', style='TButton', command=self.homePage)
        self.back.grid(row=5, column=1, padx=5, pady=5, sticky=W+E+N+S)
        
        self.lSpace = ttk.Label(self.mainFrame, width=7)
        self.lSpace.grid(row=0, column=0, pady=20)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=6, column=2, pady=100)
    
    def depositPage(self):
        self.clearFrame()
        global bind_id
        try:
            mainWin.unbind('<Return>',bind_id)
        except TclError:
            pass

        self.comment1 = ttk.Label(self.mainFrame, justify=CENTER, text='Enter the amount to deposit', style='TLabel')
        self.comment1.grid(row=1, column=1, pady=5)

        self.depositAmount = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.Lfont, width=17)
        self.depositAmount.grid(row=2, column=1, pady=5)
        self.depositAmount.focus_set()

        self.ok = ttk.Button(self.mainFrame, style='TButton', text='Deposit', command=self.Deposit, width=17)
        self.ok.grid(row=4,column=1, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='TButton', command=self.homePage)
        self.back.grid(row=5, column=1, pady=5)
        
        self.lSpace = ttk.Label(self.mainFrame, width=5)
        self.lSpace.grid(row=0, column=0, pady=40)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=6, column=2, pady=100)

        bind_id = mainWin.bind('<Return>',self.Deposit)

    def withdrawPage(self):
        self.clearFrame()
        global bind_id
        try:
            mainWin.unbind('<Return>',bind_id)
        except TclError:
            pass

        self.comment1 = ttk.Label(self.mainFrame, justify=CENTER, text='Enter the amount to withdraw', style='TLabel')
        self.comment1.grid(row=1, column=1, pady=5)
        
        self.withdrawAmount = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.Lfont, width=17)
        self.withdrawAmount.grid(row=2, column=1, pady=5)
        self.withdrawAmount.focus_set()
        
        self.ok = ttk.Button(self.mainFrame, text='Withdraw', style='TButton', command=self.Withdraw, width=17)
        self.ok.grid(row=4,column=1, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='TButton', command=self.homePage)
        self.back.grid(row=5, column=1, pady=5)
        
        self.lSpace = ttk.Label(self.mainFrame, width=4)
        self.lSpace.grid(row=0, column=0, pady=40)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=6, column=2, pady=100)

        bind_id = mainWin.bind('<Return>',self.Withdraw)

    def pinChangePage(self):
        self.clearFrame()
        global bind_id
        try:
            mainWin.unbind('<Return>',bind_id)
        except TclError:
            pass

        self.comment1 = ttk.Label(self.mainFrame, justify=RIGHT, style='TLabel', text='Current Account Pin:')
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)

        self.currentPin = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width =10)
        self.currentPin.grid(row=1, column=2, pady=5, sticky=W+E+N+S)
        self.currentPin.focus_set()
        
        self.comment2 = ttk.Label(self.mainFrame, justify=RIGHT, style='TLabel', text='New Account Pin:')
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)

        self.newPin = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width=10)
        self.newPin.grid(row=2, column=2, pady=5, sticky=W+E+N+S)
        
        self.comment3 = ttk.Label(self.mainFrame, justify=RIGHT, style='TLabel', text='Repeat New Account Pin:')
        self.comment3.grid(row=3, column=1, sticky=W+E+N+S)

        self.newPinCheck = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width =10)
        self.newPinCheck.grid(row=3, column=2, pady=5, sticky=W+E+N+S)

        self.ok = ttk.Button(self.mainFrame, style='TButton', text='Change Pin', width=20, command=self.changePin)
        self.ok.grid(row=5, column=1, pady=5, columnspan=2)

        self.back = ttk.Button(self.mainFrame, text='Back', style='TButton', command=self.homePage)
        self.back.grid(row=6, column=1, pady=5, columnspan=2)
        
        self.lSpace = ttk.Label(self.mainFrame, width=1)
        self.lSpace.grid(row=0, column=0, pady=30)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=7, column=3, pady=100)

        bind_id = mainWin.bind('<Return>',self.changePin)

    def loginPage(self):
        self.clearFrame()
        global bind_id
        try:
            mainWin.unbind('<Return>',bind_id)
        except TclError:
            pass

        global loggedAcc
        loggedAcc = ''
        global loggedPin
        loggedPin = ''

        self.comment1 = ttk.Label(self.mainFrame, justify=RIGHT, style='TLabel', text='Account Number:')
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)
        
        self.name = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.font, width=13)
        self.name.grid(row=1, column=2, padx=5, pady=5)
        self.name.focus_set()
        
        self.comment2 = ttk.Label(self.mainFrame, justify=RIGHT, style='TLabel', text='Account Pin:')
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)
        
        self.pin = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.font, show='*', width=13)
        self.pin.grid(row=2, column=2, padx=5, pady=5)

        self.comment3 = ttk.Label(self.mainFrame, justify=CENTER, style='B.TLabel', text='', foreground='red')
        self.comment3.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.login = ttk.Button(self.mainFrame, text='Login', style='TButton', command=self.auth)
        self.login.grid(row=4, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.lSpace = ttk.Label(self.mainFrame, width=4)
        self.lSpace.grid(row=0, column=0, pady=50)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=5, column=3, pady=100)

        bind_id = mainWin.bind('<Return>',self.auth)

mainWin = ThemedTk(theme='arc')
mainWin.resizable(False,False)
mainWin.geometry('500x500+200+150')
atm(mainWin)
mainWin.mainloop()