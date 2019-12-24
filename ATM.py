
from tkinter import *
from tkinter import ttk
import mysql.connector
import re

class atm:
    
    def __init__(self,master):

        master.title('ATM Machine')

        master.iconbitmap(r'D:\My Stuff\VSCode\Python\atm-techno-talent-2019\money.ico')

        # ***** Frames *****

        self.mainFrame = Frame(master, width=500, height=500)
        self.mainFrame.pack(fill=BOTH)

        style = ttk.Style(mainWin)
        style.configure("TButton", font=('wasy10', 20), padding=10)     
        
        # ***** Menu *****

        menu = Menu(master)
        master.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label='Home', command=self.homePage)
        file.add_separator()
        file.add_command(label='Quit', command=master.destroy)
        menu.add_cascade(label='File', menu=file)

        # ***** Stuff for login *****

        self.clearFrame()
        self.comment1 = Label(self.mainFrame, justify=RIGHT, font='Helvetica 15', text='Account Number:')
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)
        
        self.name = ttk.Entry(self.mainFrame, justify=CENTER, font='Helvetica 15', width=13)
        self.name.grid(row=1, column=2, padx=5, pady=5)
        self.name.focus_set()
        
        self.comment2 = Label(self.mainFrame, justify=RIGHT, font='Helvetica 15', text='Account Pin:')
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)
        
        self.pin = ttk.Entry(self.mainFrame, justify=CENTER, font='Helvetica 15', show='*', width=13)
        self.pin.grid(row=2, column=2, padx=5, pady=5)

        self.comment3 = Label(self.mainFrame, justify=CENTER, font='Helvetica 10 bold', text='', foreground='red')
        self.comment3.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.login = ttk.Button(self.mainFrame, text='Login', style='TButton', command=self.auth)
        self.login.grid(row=4, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.lSpace = Label(self.mainFrame, width=12, height=10)
        self.lSpace.grid(row=0, column=0)

        self.rSpace = Label(self.mainFrame, width=10, height=10)
        self.rSpace.grid(row=5, column=3)

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
        mydb = mysql.connector.connect(host="localhost", user="hafiz", passwd="theboss", database="atm")
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
                print('acc does not exist')                                             #print
        else:
            self.comment3.config(text='Invalid credentials')
            print('enter numbers')                                                      #print
        if loggedPin != '':
            if eval(loggedPin) == correctPin:
                self.homePage()
                print('logged')                                                         #print
                mainWin.unbind('<Return>',bind_id)
            else:
                self.comment3.config(text='Invalid credentials')
                print('incorrect pass')                                                 #print
        
        
    def Deposit(self,*args):
        self.comment2 = Label(self.mainFrame, justify=CENTER, text='', font='Helvetica 15', foreground='green')
        self.comment2.grid(row=3, column=1, pady=5)

        amount = self.depositAmount.get()
        if amount != '' and self.isFloat(amount):
            mydb = mysql.connector.connect(host="localhost", user="hafiz", passwd="theboss", database="atm")
            cursor1 = mydb.cursor()
            cursor1.execute('select balance from user_info where uid = '+loggedAcc+';')
            amt = cursor1.fetchall()[0][0]
            if self.isFloat2d(amount):
                if len(str(amt + eval(amount))) < 20:
                    mydbs = mysql.connector.connect(host="localhost", user="hafiz", passwd="theboss", database="atm")
                    cursor2 = mydbs.cursor()
                    cursor2.execute('update user_info set balance = balance + '+amount+' where uid = '+loggedAcc+';')
                    mydbs.commit()
                    print('Deposited')                                                  #print
                    
                    mainWin.unbind('<Return>',bind_id)
                    self.comment2.grid_remove()
                    self.comment2 = Label(self.mainFrame, justify=CENTER, text=str(amount)+' Deposited!', font='Helvetica 15', foreground='green')
                    self.comment2.grid(row=3, column=1, pady=5)
                else:
                    self.comment2.grid_remove()
                    self.comment2 = Label(self.mainFrame, justify=CENTER, text='Enter a smaller amount', font='Helvetica 15', foreground='green')
                    self.comment2.grid(row=3, column=1, pady=5)
            else:
                self.comment2.grid_remove()
                self.comment2 = Label(self.mainFrame, justify=CENTER, text='Only two decimal places are allowed', font='Helvetica 15', foreground='green')
                self.comment2.grid(row=3, column=1, pady=5)
        else:
            self.comment2.grid_remove()
            self.comment2 = Label(self.mainFrame, justify=CENTER, text='Enter an amount to deposit', font='Helvetica 15', foreground='green')
            self.comment2.grid(row=3, column=1, pady=5)

    def Withdraw(self,*args):
        amount = self.withdrawAmount.get()
        if amount != '' and self.isFloat(amount):
            mydb = mysql.connector.connect(host="localhost", user="hafiz", passwd="theboss", database="atm")
            cursor1 = mydb.cursor()
            cursor1.execute('select balance from user_info where uid = '+loggedAcc+';')
            amt = cursor1.fetchall()[0][0]
            if self.isFloat2d(amount):
                if (amt-eval(amount)) > 1000:
                    mydbs = mysql.connector.connect(host="localhost", user="hafiz", passwd="theboss", database="atm")
                    cursor2 = mydbs.cursor()
                    cursor2.execute('update user_info set balance = balance - '+amount+' where uid = '+loggedAcc+';')
                    mydbs.commit()
                    print('Withdrawn')                                                  #print  
                    
                    mainWin.unbind('<Return>',bind_id)
                    self.comment2.grid_remove()
                    self.comment2 = Label(self.mainFrame, justify=CENTER, text=str(amount)+' Withdrawn!', font='Helvetica 15', foreground='green')
                    self.comment2.grid(row=3, column=1, pady=5)

                    self.lSpace.config(width=15)
                else:
                    self.comment2.grid_remove()
                    self.comment2 = Label(self.mainFrame, justify=CENTER, text='The entered amount is more than the available balance', font='Helvetica 15', foreground='green')
                    self.comment2.grid(row=3, column=1, pady=5)

                    self.ok.config(width=17)
                    self.withdrawAmount.config(width=17)
                    self.lSpace.config(width=0)  
            else:
                self.comment2.grid_remove()
                self.comment2 = Label(self.mainFrame, justify=CENTER, text='Only two decimal places are allowed', font='Helvetica 15', foreground='green')
                self.comment2.grid(row=3, column=1, pady=5)
                
                self.lSpace.config(width=15)
        else:
            self.comment2.grid_remove()
            self.comment2 = Label(self.mainFrame, justify=CENTER, text='Enter an amount to deposit', font='Helvetica 15', foreground='green')
            self.comment2.grid(row=3, column=1, pady=5)  

            self.lSpace.config(width=15)

    def changePin(self,*args):
        self.comment4 = Label(self.mainFrame, justify=CENTER, text='', font='Helvetica 15', foreground='red')
        self.comment4.grid(row=4, column=1, pady=5, sticky=W+E+N+S, columnspan=2)

        currentpin = self.currentPin.get()
        newpin = self.newPin.get()
        newpincheck = self.newPinCheck.get()

        mydb = mysql.connector.connect(host="localhost", user="hafiz", passwd="theboss", database="atm")
        cursor1 = mydb.cursor()
        cursor1.execute('select pin from user_info where uid = '+loggedAcc+';')
        oldpin = str(cursor1.fetchall()[0][0])
        print(oldpin)                                                                   #print
        mydbs = mysql.connector.connect(host="localhost", user="hafiz", passwd="theboss", database="atm")
        cursor2 = mydbs.cursor()
        
        if oldpin == currentpin:
            if newpin != '':
                if currentpin != newpin:
                    if len(newpin) == 4:
                        if newpin == newpincheck:
                            cursor2.execute('update user_info set pin = '+newpin+' where uid = '+loggedAcc+' ;')
                            mydbs.commit()
                            self.comment4.config(text='Account pin changed', foreground='green')
                            mainWin.unbind('<Return>',bind_id)
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
        
        self.lSpace = Label(self.mainFrame, width=13, height=4)
        self.lSpace.grid(row=0, column=0)

        self.rSpace = Label(self.mainFrame, width=10, height=10)
        self.rSpace.grid(row=6, column=2)
    
    def balancePage(self):
        self.clearFrame()

        mydb = mysql.connector.connect(host="localhost", user="hafiz", passwd="theboss", database="atm")
        cursor = mydb.cursor()
        cursor.execute('select balance from user_info where uid = '+loggedAcc+';')
        global amt
        amt = cursor.fetchall()[0][0]
        
        self.comment = Label(self.mainFrame, justify=CENTER, text='Current Balance', font='Helvetica 15')
        self.comment.grid(row=1, column=1, padx=5, pady=5)

        self.showBalance = Label(self.mainFrame, text=str(amt), font='Helvetica 20')
        self.showBalance.grid(row=2, column=1, padx=5, pady=5)

        self.deposit = ttk.Button(self.mainFrame, text='Deposit an Amount', style='TButton', command=self.depositPage)
        self.deposit.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.withdraw = ttk.Button(self.mainFrame, text='Withdraw an Amount', style='TButton', command=self.withdrawPage)
        self.withdraw.grid(row=4, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.back = ttk.Button(self.mainFrame, text='Back', style='TButton', command=self.homePage)
        self.back.grid(row=5, column=1, padx=5, pady=5, sticky=W+E+N+S)
        
        self.lSpace = Label(self.mainFrame, width=15, height=5)
        self.lSpace.grid(row=0, column=0)

        self.rSpace = Label(self.mainFrame, width=10, height=10)
        self.rSpace.grid(row=6, column=2)
    
    def depositPage(self):
        self.clearFrame()
        self.comment1 = Label(self.mainFrame, justify=CENTER, text='Enter the amount to deposit', font='Helvetica 15')
        self.comment1.grid(row=1, column=1, pady=5)

        self.depositAmount = ttk.Entry(self.mainFrame, justify=CENTER, font='Helvetica 20', width=10)
        self.depositAmount.grid(row=2, column=1, pady=5, sticky=W+E+N+S)
        self.depositAmount.focus_set()

        self.ok = ttk.Button(self.mainFrame, style='TButton', text='Deposit', command=self.Deposit)
        self.ok.grid(row=4,column=1, pady=5, sticky=W+E+N+S)

        self.back = ttk.Button(self.mainFrame, text='Back', style='TButton', command=self.homePage)
        self.back.grid(row=5, column=1, pady=5)
        
        self.lSpace = Label(self.mainFrame, width=17, height=8)
        self.lSpace.grid(row=0, column=0)

        self.rSpace = Label(self.mainFrame, width=10, height=10)
        self.rSpace.grid(row=6, column=2)

        global bind_id
        bind_id = mainWin.bind('<Return>',self.Deposit)

    def withdrawPage(self):
        self.clearFrame()
        self.comment1 = Label(self.mainFrame, justify=CENTER, text='Enter the amount to withdraw', font='Helvetica 15', pady=5)
        self.comment1.grid(row=1, column=1, pady=5)
        
        self.withdrawAmount = ttk.Entry(self.mainFrame, justify=CENTER, font='Helvetica 20', width=17)
        self.withdrawAmount.grid(row=2, column=1, pady=5)
        self.withdrawAmount.focus_set()
        
        self.ok = ttk.Button(self.mainFrame, text='Withdraw', style='TButton', command=self.Withdraw, width=17)
        self.ok.grid(row=4,column=1, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='TButton', command=self.homePage)
        self.back.grid(row=5, column=1, pady=5)
        
        self.lSpace = Label(self.mainFrame, width=15, height=8)
        self.lSpace.grid(row=0, column=0)

        self.rSpace = Label(self.mainFrame, width=10, height=10)
        self.rSpace.grid(row=6, column=2)

        global bind_id
        bind_id = mainWin.bind('<Return>',self.Withdraw)

    def pinChangePage(self):
        self.clearFrame()
        self.comment1 = Label(self.mainFrame, justify=RIGHT, font='Helvetica 15', text='Current Account Pin:')
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)

        self.currentPin = ttk.Entry(self.mainFrame, justify=LEFT, font='Helvetica 15', show='*', width =10)
        self.currentPin.grid(row=1, column=2, pady=5, sticky=W+E+N+S)
        self.currentPin.focus_set()
        
        self.comment2 = Label(self.mainFrame, justify=RIGHT, font='Helvetica 15', text='New Account Pin:')
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)

        self.newPin = ttk.Entry(self.mainFrame, justify=LEFT, font='Helvetica 15', show='*', width =10)
        self.newPin.grid(row=2, column=2, pady=5, sticky=W+E+N+S)
        
        self.comment3 = Label(self.mainFrame, justify=RIGHT, font='Helvetica 15', text='Repeat New Account Pin:')
        self.comment3.grid(row=3, column=1, sticky=W+E+N+S)

        self.newPinCheck = ttk.Entry(self.mainFrame, justify=LEFT, font='Helvetica 15', show='*', width =10)
        self.newPinCheck.grid(row=3, column=2, pady=5, sticky=W+E+N+S)

        self.ok = ttk.Button(self.mainFrame, style='TButton', text='Change Pin', command=self.changePin)
        self.ok.grid(row=5, column=1, pady=5, sticky=W+E+N+S, columnspan=2)

        self.back = ttk.Button(self.mainFrame, text='Back', style='TButton', command=self.homePage)
        self.back.grid(row=6, column=1, pady=5, columnspan=2)
        
        self.lSpace = Label(self.mainFrame, width=10, height=8)
        self.lSpace.grid(row=0, column=0)

        self.rSpace = Label(self.mainFrame, width=10, height=10)
        self.rSpace.grid(row=7, column=3)

        global bind_id
        bind_id = mainWin.bind('<Return>',self.changePin)

    def loginPage(self):
        self.clearFrame()

        global loggedAcc
        loggedAcc = ''
        global loggedPin
        loggedPin = ''

        self.comment1 = Label(self.mainFrame, justify=RIGHT, font='Helvetica 15', text='Account Number:')
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)
        
        self.name = ttk.Entry(self.mainFrame, justify=CENTER, font='Helvetica 15', width=13)
        self.name.grid(row=1, column=2, padx=5, pady=5)
        self.name.focus_set()
        
        self.comment2 = Label(self.mainFrame, justify=RIGHT, font='Helvetica 15', text='Account Pin:')
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)
        
        self.pin = ttk.Entry(self.mainFrame, justify=CENTER, font='Helvetica 15', show='*', width=13)
        self.pin.grid(row=2, column=2, padx=5, pady=5)

        self.comment3 = Label(self.mainFrame, justify=CENTER, font='Helvetica 10 bold', text='', foreground='red')
        self.comment3.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.login = ttk.Button(self.mainFrame, text='Login', style='TButton', command=self.auth)
        self.login.grid(row=4, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.lSpace = Label(self.mainFrame, width=12, height=10)
        self.lSpace.grid(row=0, column=0)

        self.rSpace = Label(self.mainFrame, width=10, height=10)
        self.rSpace.grid(row=5, column=3)

        global bind_id
        bind_id = mainWin.bind('<Return>',self.auth)

    

mainWin = Tk()
mainWin.resizable(False,False)
mainWin.maxsize(500,500)
mainWin.minsize(500,500)
atm(mainWin)
mainWin.mainloop()