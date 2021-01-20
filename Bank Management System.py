#Enter MySQL Info -- Line 37

#General alignment issues
#Proof read
#dont allow admin into homepage

from tkinter import ttk, BOTH, Menu, RIGHT, CENTER, LEFT, W, E, N, S, TclError, Listbox, END
from ttkthemes import ThemedTk

import mysql.connector
import random
import datetime
import re


class atm:
    
    def __init__(self, master):

        master.title('Bank Management System')

        master.iconbitmap('money.ico')

        # ***** Frames *****

        self.mainFrame = ttk.Frame(master, width=500, height=500)
        self.mainFrame.pack(fill=BOTH)

        # ***** Styles *****

        style = ttk.Style(mainWin)
        style.configure('TButton', font=('Helvetica', 20), padding=10)
        style.configure('S.TButton', font=('Helvetica', 17), padding=7)
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

        # ***** Admin Info *****

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select pin, uid from user_info where name = \'admin\';')
        self.adminUser, self.adminPass = cursor.fetchone()
        self.Admin = False

        # ***** Random Variables *****

        self.destroy = master.destroy

        # ***** Stuff for login *****

        self.clearFrame()
        self.signUpButton = ttk.Button(self.mainFrame, text='Sign Up', style='TButton', command=self.signUpPage, width=15)
        self.signUpButton.grid(row=1, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.loginButton = ttk.Button(self.mainFrame, text='Log in', style='TButton', command=self.loginPage, width=15)
        self.loginButton.grid(row=2, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.adminButton = ttk.Button(self.mainFrame, text='Admin Mode', style='TButton', command=lambda:[self.admin(), self.loginPage()], width=15)
        self.adminButton.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.quit = ttk.Button(self.mainFrame, text='Quit', style='S.TButton', command=master.destroy, width=4)
        self.quit.grid(row=4, column=1, padx=5, pady=20)

        self.lSpace = ttk.Label(self.mainFrame, width=8)
        self.lSpace.grid(row=0, column=0, pady=35)

        self.rSpace = ttk.Label(self.mainFrame, width=1)
        self.rSpace.grid(row=5, column=3, pady=0)

    # ***** Functions *****

    def isFloat(self, n):
        n = str(n)
        return bool(re.match(r'^-?\d+\.?(\d+)?$', n))

    def isFloat2d(self, n):
        n = str(n)
        return bool(re.match(r'^\d*\.?(\d\d?)?$', n))

    def monthsFromToday(self, date):
        today = datetime.date.today()

        date_loan = int(date.strftime('%d'))
        month_loan = int(date.strftime('%m'))
        year_loan = int(date.strftime('%y'))
        date_today = int(today.strftime('%d'))
        month_today = int(today.strftime('%m'))
        year_today = int(today.strftime('%y'))

        if year_loan == year_today:
            if date_today < date_loan:
                return month_today - month_loan - 1
            else:
                return month_today - month_loan
        else:
            if date_today < date_loan:
                return month_today - month_loan + 12*(year_today-year_loan) - 1
            else:
                return month_today - month_loan + 12*(year_today-year_loan)

    def clearFrame(self):
        for widget in self.mainFrame.winfo_children():
            widget.grid_remove()

    def resetAdmin(self):
        self.Admin = False

    def admin(self):
        self.Admin = True

    def addInterest(self):
        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor1 = mydb.cursor(buffered=True)
        cursor1.execute('select loans from user_info where uid = '+self.loggedAcc+';')
        loans = cursor1.fetchone()[0]
        if loans:
            cursor2 = mydb.cursor(buffered=True)
            cursor2.execute('select loan_date from user_info where uid = '+self.loggedAcc+';')
            loan_date = cursor2.fetchone()[0]
            
            cursor3 = mydb.cursor(buffered=True)
            cursor3.execute('select monthly_interest from user_info where uid = '+self.loggedAcc+';')
            monthly_interest = cursor3.fetchone()[0]

            months = self.monthsFromToday(loan_date)
            today = datetime.date.today()
            interest = monthly_interest * months

            cursor4 = mydb.cursor(buffered=True)
            cursor4.execute('update user_info set loans = loans + '+str(interest)+', loan_date = \''+str(today)+'\' where uid = '+self.loggedAcc+';')
            #mydb.commit()

    def signUp(self,*args):
        name = self.name.get()
        pin = self.pin.get()
        pinConfirm = self.pinConfirm.get()

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor1 = mydb.cursor(buffered=True)
        cursor1.execute('select name from user_info;')
        nameList = cursor1.fetchall()

        cursor2 = mydb.cursor(buffered=True)
        cursor2.execute('select name from user_requests;')
        pendingName = cursor2.fetchall()

        cursor3 = mydb.cursor(buffered=True)
        cursor3.execute('select uid from user_info;')
        existingUid = cursor3.fetchall()

        cursor4 = mydb.cursor(buffered=True)
        cursor4.execute('select uid from user_requests;')
        pendingUid = cursor4.fetchall()

        uid = random.randint(1000,9999)
        while (uid,) in existingUid or (uid,) in pendingUid:
            uid = random.randint(1000,9999)

        if name:
            if len(name) < 20:
                if (name,) not in nameList:
                    if (name,) not in pendingName:
                        if pin.isdigit() and pinConfirm.isdigit():
                            if len(pin) == 4 and len(pinConfirm) == 4:
                                if pin == pinConfirm:
                                    cursor5 = mydb.cursor(buffered=True)
                                    cursor5.execute('insert into user_requests values(\''+name+'\','+str(uid)+','+pin+');')
                                    mydb.commit()
                                    
                                    self.comment4.config(text='Your Account number is '+str(uid)+'.\nAccount Activation Pending', foreground='green')
                                else:
                                    self.comment4.config(text='Entered Account Pins do not match')
                            else:
                                self.comment4.config(text='Account Pin must consist 4 digits')
                        else:
                            self.comment4.config(text='Account Pin must be of numbers')
                    else:
                        self.comment4.config(text='Account Activation Pending')
                else:
                    self.comment4.config(text='Account Name already exists')
            else:
                self.comment4.config(text='Name Too Long')
        else:
            self.comment4.config(text='Enter Credintials')

    def authChoose(self,*args):
        if self.Admin:
            self.adminAuth()
        else:
            self.auth()

    def adminAuth(self):
        entAdmUid = self.name.get()
        entAdmPin = self.pin.get()

        if entAdmUid == str(self.adminUser):
            if entAdmPin == str(self.adminPass):
                self.adminPage()
            else:
                self.comment3.config(text='Invalid credentials')
        else:
            self.comment3.config(text='Invalid credentials')

    def auth(self):
        self.loggedAcc = self.name.get()
        self.loggedPin = self.pin.get()
        correctPin = None

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor1 = mydb.cursor(buffered=True)
        cursor1.execute('select * from user_info;')
        details = cursor1.fetchone()

        cursor2 = mydb.cursor(buffered=True)
        cursor2.execute('select uid from user_requests;')
        pendDetails = cursor2.fetchall()
        
        if self.loggedAcc.isdigit() and self.loggedPin.isdigit():
            for pendUser in pendDetails:
                if eval(self.loggedAcc) == pendUser[0]:
                    self.comment3.config(text='Account activation pending')
            else:
                while details is not None:
                    if eval(self.loggedAcc) == details[1]:
                        correctPin = details[2]
                        self.amt = details[3]
                        self.uName = details[0]
                        break
                    else:
                        details = cursor1.fetchone()
                else:
                    self.comment3.config(text='Invalid credentials')
        else:
            self.comment3.config(text='Invalid credentials')
        if self.loggedPin:
            if eval(self.loggedPin) == correctPin and self.loggedPin != self.adminPass:
                self.homePage()
            else:
                self.comment3.config(text='Invalid credentials')

    def Deposit(self,*args):
        amount = self.depositAmount.get()

        if amount != '' and self.isFloat(amount):
            mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
            cursor1 = mydb.cursor(buffered=True)
            cursor1.execute('select balance from user_info where uid = '+self.loggedAcc+';')
            self.amt = float(cursor1.fetchone()[0])

            if self.isFloat2d(amount):
                if len(str(self.amt + eval(amount))) < 20:
                    try:
                        cursor2 = mydb.cursor(buffered=True)
                        cursor2.execute('update user_info set balance = balance + '+amount+' where uid = '+self.loggedAcc+';')
                        mydb.commit()

                        self.comment2.config(text=str(amount)+' Deposited!', foreground='green')
                    except mysql.connector.errors.DataError:
                        self.comment2.config(text='Enter a smaller amount', foreground='red')
                else:
                    self.comment2.config(text='Enter a smaller amount', foreground='red')
            else:
                self.comment2.config(text='Only positive amounts with two\ndecimal places are allowed', foreground='red')
        else:
            self.comment2.config(text='Enter an amount to deposit', foreground='red')

    def Withdraw(self,*args):
        amount = self.withdrawAmount.get()

        if amount != '' and self.isFloat(amount):
            mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
            cursor1 = mydb.cursor(buffered=True)
            cursor1.execute('select balance from user_info where uid = '+self.loggedAcc+';')
            amt = float(cursor1.fetchone()[0])
            if self.isFloat2d(amount):
                if (amt-eval(amount)) > 1000:
                    try:
                        cursor2 = mydb.cursor(buffered=True)
                        cursor2.execute('update user_info set balance = balance - '+amount+' where uid = '+self.loggedAcc+';')
                        mydb.commit()
                        
                        self.comment2.config(text=str(amount)+' Withdrawn!', foreground='green')
                    except mysql.connector.errors.DataError:
                        self.comment2.config(text='The entered amount is more than\nthe available balance', foreground='red')
                else:
                    self.comment2.config(text='The entered amount is more than\nthe available balance', foreground='red')
            else:
                self.comment2.config(text='Only positive amounts with two\ndecimal places are allowed', foreground='red')
        else:
            self.comment2.config(text='Enter an amount to withdraw', foreground='red')

    def getLoan(self,*args):
        amount = self.loanAmount.get()

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor1 = mydb.cursor(buffered=True)
        cursor1.execute('select balance from user_info where uid = '+self.loggedAcc+';')
        try:
            balance = float(cursor1.fetchone()[0])
        except:
            balance = cursor1.fetchone()

        cursor2 = mydb.cursor(buffered=True)
        cursor2.execute('select loans from user_info where uid = '+self.loggedAcc+';')
        loans = cursor2.fetchone()[0]

        if amount != '' and self.isFloat(amount):
            if self.isFloat2d(amount):
                if not loans:
                    if balance > 10000:
                        cursor2 = mydb.cursor(buffered=True)
                        cursor2.execute('update user_info set loans = '+amount+', loan_date = \''+str(datetime.date.today())+'\', balance = balance + '+amount+', monthly_interest = '+str(float(amount)*0.005)+' where uid = '+self.loggedAcc+';')
                        mydb.commit()

                        self.comment2.config(text='The required amount has been credited', foreground='green')
                    else:
                        self.comment2.config(text='Current account balance does not meet\nthe required balance', foreground='red')
                else:
                    self.comment2.config(text='Multiple loans are not allowed', foreground='red')
            else:
                self.comment2.config(text='Only positive amounts with two\ndecimal places are allowed', foreground='red')
        else:
            self.comment2.config(text='Enter an amount', foreground='red')

    def repayLoan(self,*args):
        try:
            amount = eval(self.loanAmount.get())
        except:
            amount = self.loanAmount.get()

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor1 = mydb.cursor(buffered=True)
        cursor1.execute('select loans from user_info where uid = '+self.loggedAcc+';')
        try:
            loans = float(cursor1.fetchone()[0])
        except:
            loans = cursor1.fetchone()

        if amount != '' and self.isFloat(amount):
            if self.isFloat2d(amount):
                if loans:
                    if amount < loans:
                        cursor2 = mydb.cursor(buffered=True)
                        cursor2.execute('update user_info set loans = loans - '+str(amount)+' where uid = '+self.loggedAcc+';')
                        mydb.commit()

                        self.showBalance.config(text="%.2f" %(float(loans-amount)))
                        self.comment2.config(text=str(amount)+' repayed!', foreground='green')
                    elif amount == loans:
                        cursor2 = mydb.cursor(buffered=True)
                        cursor2.execute('update user_info set loans = null, loan_date = null, monthly_interest = null where uid = '+self.loggedAcc+';')
                        mydb.commit()

                        self.showBalance.config(text='None')
                        self.comment2.config(text=str(amount)+' repayed!', foreground='green')
                    else:
                        self.comment2.config(text='Entered amount is greater than the\nloan amount', foreground='red')
                else:
                    self.comment2.config(text='No current loans', foreground='red')
            else:
                self.comment2.config(text='Only positive amounts with two\ndecimal places are allowed', foreground='red')
        else:
            self.comment2.config(text='Enter an amount to withdraw', foreground='red')

    def changePin(self,*args):
        currentpin = self.currentPin.get()
        newpin = self.newPin.get()
        newpincheck = self.newPinCheck.get()

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor1 = mydb.cursor(buffered=True)
        cursor1.execute('select pin from user_info where uid = '+self.loggedAcc+';')
        oldpin = str(cursor1.fetchone()[0])
        
        if oldpin == currentpin:
            if newpin != '':
                if currentpin != newpin and newpin.isdigit():
                    if len(newpin) == 4:
                        if newpin == newpincheck:
                            cursor2 = mydb.cursor(buffered=True)
                            cursor2.execute('update user_info set pin = '+newpin+' where uid = '+self.loggedAcc+' ;')
                            mydb.commit()
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

    def newUser(self,*args):
        name = self.newName.get()
        uid = self.newAcc.get()
        pin = self.newPin.get()
        pinConfirm = self.newPinCheck.get()

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor1 = mydb.cursor(buffered=True)
        cursor1.execute('select name from user_info;')
        nameList = cursor1.fetchall()

        cursor2 = mydb.cursor(buffered=True)
        cursor2.execute('select name from user_requests;')
        pendingName = cursor2.fetchall()

        cursor3 = mydb.cursor(buffered=True)
        cursor3.execute('select uid from user_info;')
        existingUid = cursor3.fetchall()

        cursor4 = mydb.cursor(buffered=True)
        cursor4.execute('select uid from user_requests;')
        pendingUid = cursor4.fetchall()

        if name:
            if len(name) < 20:
                if (name,) not in nameList:
                    if (name,) not in pendingName:
                        if len(uid) == 4:
                            if (eval(uid),) not in existingUid:
                                if (eval(uid),) not in pendingUid:
                                    if pin.isdigit() and pinConfirm.isdigit():
                                        if len(pin) == 4 and len(pinConfirm) == 4:
                                            if pin == pinConfirm:
                                                cursor5 = mydb.cursor(buffered=True)
                                                cursor5.execute('insert into user_info (name,uid,pin,balance) values(\''+name+'\','+uid+','+pin+',1000);')
                                                mydb.commit()

                                                self.comment5.config(text='Account created!', foreground='green')
                                            else:
                                                self.comment5.config(text='Entered Account Pins do not match', foreground='red')
                                        else:
                                            self.comment5.config(text='Account Pin must consist 4 digits', foreground='red')
                                    else:
                                        self.comment5.config(text='Account Pin must be of numbers', foreground='red')
                                else:
                                    self.comment5.config(text='Account Number already exists\n(in Requests)', foreground='red')
                            else:
                                self.comment5.config(text='Account Number already exists', foreground='red')
                        else:
                            self.comment5.config(text='Account Number must consist 4 digits', foreground='red')
                    else:
                        self.comment5.config(text='Account Name already exists\n(in Requests)', foreground='red')
                else:
                    self.comment5.config(text='Account Name already exists', foreground='red')
            else:
                self.comment5.config(text='Name Too Long', foreground='red')
        else:
            self.comment5.config(text='Enter Credintials', foreground='red')

    def delUser(self):
        try:
            toDel = self.userList.get(self.userList.curselection())
            self.userList.delete(self.userList.curselection())

            mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
            cursor = mydb.cursor(buffered=True)
            cursor.execute('delete from user_info where name = \''+toDel+'\';')
            mydb.commit()

        except TclError:
            pass

    def accRequest(self):
        try:
            newUser = self.userList.get(self.userList.curselection())
            self.userList.delete(self.userList.curselection())

            mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
            cursor1 = mydb.cursor(buffered=True)
            cursor1.execute('select * from user_requests where name = \''+newUser+'\';')
            details = cursor1.fetchone()

            cursor2 = mydb.cursor(buffered=True)
            cursor2.execute('insert into user_info (name,uid,pin,balance) values(\''+details[0]+'\','+str(details[1])+','+str(details[2])+',1000);')

            cursor3 = mydb.cursor(buffered=True)
            cursor3.execute('delete from user_requests where name = \''+newUser+'\';')
            mydb.commit()

        except TclError:
            pass

    def rejRequest(self):
        try:
            rejUser = self.userList.get(self.userList.curselection())
            self.userList.delete(self.userList.curselection())

            mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
            cursor1 = mydb.cursor(buffered=True)
            cursor1.execute('delete from user_requests where name = \''+rejUser+'\';')
            mydb.commit()

        except TclError:
            pass

    # ***** Navigation Functions *****

    def signUpPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except (TclError,AttributeError):
            pass

        self.comment1 = ttk.Label(self.mainFrame, style='TLabel', text='Enter your Name:', anchor=E)
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)
        
        self.name = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, width=13)
        self.name.grid(row=1, column=2, padx=5, pady=5)
        self.name.focus_set()
        
        self.comment2 = ttk.Label(self.mainFrame, style='TLabel', text='Enter Account Pin:', anchor=E)
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)
        
        self.pin = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width=13)
        self.pin.grid(row=2, column=2, padx=5, pady=5)

        self.comment3 = ttk.Label(self.mainFrame, style='TLabel', text='Confirm Account Pin:', anchor=E)
        self.comment3.grid(row=3, column=1, sticky=W+E+N+S)

        self.pinConfirm = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width =13)
        self.pinConfirm.grid(row=3, column=2, pady=5)

        self.comment4 = ttk.Label(self.mainFrame, justify=CENTER, style='B.TLabel', text='', foreground='red', anchor=CENTER)
        self.comment4.grid(row=4, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.signUpButton = ttk.Button(self.mainFrame, text='Sign Up', style='TButton', command=self.signUp)
        self.signUpButton.grid(row=5, column=1, columnspan=2, sticky=N+S)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.menuPage, width=5)
        self.back.grid(row=6, column=1, columnspan=2, pady=10)

        self.lSpace = ttk.Label(self.mainFrame, width=1)
        self.lSpace.grid(row=0, column=0, pady=30)

        self.rSpace = ttk.Label(self.mainFrame, width=1)
        self.rSpace.grid(row=7, column=3, pady=0)

        self.bind_id = mainWin.bind('<Return>',self.signUp)

    def loginPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except (TclError,AttributeError):
            pass

        self.loggedAcc = ''
        self.loggedPin = ''

        self.comment1 = ttk.Label(self.mainFrame, style='TLabel', text='Enter Account Number:', anchor=E)
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)
        
        self.name = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, width=13)
        self.name.grid(row=1, column=2, padx=5, pady=5)
        self.name.focus_set()
        
        self.comment2 = ttk.Label(self.mainFrame, style='TLabel', text='Enter Account Pin:', anchor=E)
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)
        
        self.pin = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width=13)
        self.pin.grid(row=2, column=2, padx=5, pady=5)

        self.comment3 = ttk.Label(self.mainFrame, justify=CENTER, style='B.TLabel', text='', foreground='red', anchor=CENTER)
        self.comment3.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S, columnspan=2)

        self.login = ttk.Button(self.mainFrame, text='Login', style='TButton', command=self.authChoose, width=15)
        self.login.grid(row=4, column=1, padx=5, pady=5, sticky=N+S, columnspan=2)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=lambda:[self.resetAdmin(),self.menuPage()], width=5)
        self.back.grid(row=5, column=1, pady=10, columnspan=2)

        self.lSpace = ttk.Label(self.mainFrame, width=0)
        self.lSpace.grid(row=0, column=0,padx=5, pady=45)

        self.rSpace = ttk.Label(self.mainFrame, width=1)
        self.rSpace.grid(row=6, column=3, pady=0)

        self.bind_id = mainWin.bind('<Return>',self.authChoose)

    def homePage(self):
        self.clearFrame()
        self.addInterest()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.welcome = ttk.Label(self.mainFrame, text='Welcome '+self.uName.capitalize()+'!', style='TLabel', justify=CENTER, anchor=CENTER)
        self.welcome.grid(row=0, column=0, sticky=W+E+N+S, pady=10, columnspan=3)

        self.balance = ttk.Button(self.mainFrame, text='Check Account Balance', style='TButton', command=self.balancePage)
        self.balance.grid(row=2, column=1, sticky=W+E+N+S, pady=5)

        self.deposit = ttk.Button(self.mainFrame, text='Deposit an Amount', style='TButton', command=self.depositPage)
        self.deposit.grid(row=3, column=1, sticky=W+E+N+S, pady=5)

        self.withdraw = ttk.Button(self.mainFrame, text='Withdraw an Amount', style='TButton', command=self.withdrawPage)
        self.withdraw.grid(row=4, column=1, sticky=W+E+N+S, pady=5)

        self.loans = ttk.Button(self.mainFrame, text='Loans', style='TButton', command=self.loanPage)
        self.loans.grid(row=5, column=1, sticky=W+E+N+S, pady=5)

        self.chPin = ttk.Button(self.mainFrame, text='Change PIN Number', style='TButton', command=self.pinChangePage)
        self.chPin.grid(row=6, column=1, sticky=W+E+N+S, pady=5)

        self.logout = ttk.Button(self.mainFrame, text='Logout', style='S.TButton', command=self.loginPage, width=7)
        self.logout.grid(row=7, column=1, pady=25)

        self.lSpace = ttk.Label(self.mainFrame, width=5)
        self.lSpace.grid(row=0, column=0, pady=3, padx=7)

        self.rSpace = ttk.Label(self.mainFrame, width=5)
        self.rSpace.grid(row=8, column=2, pady=100)

    def balancePage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select balance from user_info where uid = '+self.loggedAcc+';')
        self.amt = cursor.fetchone()[0]

        self.comment = ttk.Label(self.mainFrame, justify=CENTER, text='Current Balance',  style='TLabel')
        self.comment.grid(row=1, column=1, padx=5, pady=5)

        self.showBalance = ttk.Label(self.mainFrame, text=str(self.amt), style='L.TLabel')
        self.showBalance.grid(row=2, column=1, padx=5, pady=5)

        self.deposit = ttk.Button(self.mainFrame, text='Deposit an Amount', style='TButton', command=self.depositPage)
        self.deposit.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.withdraw = ttk.Button(self.mainFrame, text='Withdraw an Amount', style='TButton', command=self.withdrawPage)
        self.withdraw.grid(row=4, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.homePage, width=5)
        self.back.grid(row=5, column=1, padx=5, pady=5)

        self.lSpace = ttk.Label(self.mainFrame, width=7)
        self.lSpace.grid(row=0, column=0, pady=20)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=6, column=2, pady=100)

    def depositPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.comment1 = ttk.Label(self.mainFrame, text='Enter the amount to deposit', style='TLabel', anchor=CENTER)
        self.comment1.grid(row=1, column=1, pady=5)

        self.depositAmount = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.Lfont, width=17)
        self.depositAmount.grid(row=2, column=1, pady=5)
        self.depositAmount.focus_set()

        self.comment2 = ttk.Label(self.mainFrame, text='', justify=CENTER, style='TLabel', foreground='red', anchor=CENTER)
        self.comment2.grid(row=3, column=0, pady=5, columnspan=3)

        self.ok = ttk.Button(self.mainFrame, style='TButton', text='Deposit', command=self.Deposit, width=17)
        self.ok.grid(row=4,column=1, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.homePage, width=5)
        self.back.grid(row=5, column=1, pady=5)
        
        self.lSpace = ttk.Label(self.mainFrame, width=5)
        self.lSpace.grid(row=0, column=0, pady=40)

        self.rSpace = ttk.Label(self.mainFrame, width=4)
        self.rSpace.grid(row=6, column=2, pady=100)

        self.bind_id = mainWin.bind('<Return>',self.Deposit)

    def withdrawPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.comment1 = ttk.Label(self.mainFrame, text='Enter the amount to withdraw', style='TLabel', anchor=CENTER)
        self.comment1.grid(row=1, column=1, pady=5)
        
        self.withdrawAmount = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.Lfont, width=17)
        self.withdrawAmount.grid(row=2, column=1, pady=5)
        self.withdrawAmount.focus_set()

        self.comment2 = ttk.Label(self.mainFrame, text='', justify=CENTER, style='TLabel', foreground='red', anchor=CENTER)
        self.comment2.grid(row=3, column=0, pady=5, columnspan=3)
        
        self.ok = ttk.Button(self.mainFrame, text='Withdraw', style='TButton', command=self.Withdraw, width=17)
        self.ok.grid(row=4,column=1, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.homePage, width=5)
        self.back.grid(row=5, column=1, pady=5)
        
        self.lSpace = ttk.Label(self.mainFrame, width=4)
        self.lSpace.grid(row=0, column=0, pady=40)

        self.rSpace = ttk.Label(self.mainFrame, width=4)
        self.rSpace.grid(row=6, column=2, pady=100)

        self.bind_id = mainWin.bind('<Return>',self.Withdraw)

    def loanPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.status = ttk.Button(self.mainFrame, text='Check Loan Status', style='TButton', command=self.loanStatusPage)
        self.status.grid(row=1, column=1, sticky=W+E+N+S, pady=5)

        self.get = ttk.Button(self.mainFrame, text='Get Loan', style='TButton', command=self.getLoanPage)
        self.get.grid(row=2, column=1, sticky=W+E+N+S, pady=5)

        self.repay = ttk.Button(self.mainFrame, text='Repay Loan', style='TButton', command=self.repayLoanPage)
        self.repay.grid(row=3, column=1, sticky=W+E+N+S, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.homePage, width=5)
        self.back.grid(row=4, column=1, pady=15)

        self.lSpace = ttk.Label(self.mainFrame, width=8)
        self.lSpace.grid(row=0, column=0, pady=35)

        self.rSpace = ttk.Label(self.mainFrame, width=5)
        self.rSpace.grid(row=5, column=2, pady=100)

    def loanStatusPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass
        
        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select loans from user_info where uid = '+self.loggedAcc+';')
        loan = cursor.fetchone()[0]

        self.comment = ttk.Label(self.mainFrame, justify=CENTER, text='Current Loan Status',  style='TLabel')
        self.comment.grid(row=1, column=1, padx=5, pady=5)

        self.showBalance = ttk.Label(self.mainFrame, text=str(loan), style='L.TLabel')
        self.showBalance.grid(row=2, column=1, padx=5, pady=5)

        self.get = ttk.Button(self.mainFrame, text='Get Loan', style='TButton', command=self.getLoanPage)
        self.get.grid(row=3, column=1, sticky=W+E+N+S, pady=5)

        self.repay = ttk.Button(self.mainFrame, text='Repay Loan', style='TButton', command=self.repayLoanPage)
        self.repay.grid(row=4, column=1, sticky=W+E+N+S, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.loanPage, width=5)
        self.back.grid(row=5, column=1, padx=5, pady=15)
        
        self.lSpace = ttk.Label(self.mainFrame, width=8)
        self.lSpace.grid(row=0, column=0, pady=25)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=6, column=2, pady=100)

    def getLoanPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.comment1 = ttk.Label(self.mainFrame, text='Enter the amount needed', style='TLabel', anchor=CENTER)
        self.comment1.grid(row=1, column=1, pady=5)
        
        self.loanAmount = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.Lfont, width=17)
        self.loanAmount.grid(row=2, column=1, pady=5)
        self.loanAmount.focus_set()

        self.comment2 = ttk.Label(self.mainFrame, text='', justify=CENTER, style='TLabel', foreground='red', anchor=CENTER)
        self.comment2.grid(row=3, column=0, columnspan=3, pady=5)
        
        self.ok = ttk.Button(self.mainFrame, text='Get Loan', style='TButton', command=self.getLoan, width=17)
        self.ok.grid(row=4,column=1, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.loanPage, width=5)
        self.back.grid(row=5, column=1, pady=5)
        
        self.lSpace = ttk.Label(self.mainFrame, width=7)
        self.lSpace.grid(row=0, column=0, pady=40)

        self.rSpace = ttk.Label(self.mainFrame, width=4)
        self.rSpace.grid(row=6, column=2, pady=100)

        self.bind_id = mainWin.bind('<Return>',self.getLoan)

    def repayLoanPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select loans from user_info where uid = '+self.loggedAcc+';')
        loan = cursor.fetchone()[0]

        self.comment1 = ttk.Label(self.mainFrame, justify=CENTER, text='Current Loan Status',  style='TLabel')
        self.comment1.grid(row=1, column=1, padx=5, pady=5)

        self.showBalance = ttk.Label(self.mainFrame, text=str(loan), style='L.TLabel')
        self.showBalance.grid(row=2, column=1, padx=5, pady=5)

        self.loanAmount = ttk.Entry(self.mainFrame, justify=CENTER, style='TEntry', font=self.Lfont, width=15)
        self.loanAmount.grid(row=3, column=1, pady=5)
        self.loanAmount.focus_set()

        self.comment2 = ttk.Label(self.mainFrame, text='', justify=CENTER, style='TLabel', foreground='red', anchor=CENTER)
        self.comment2.grid(row=4, column=0, padx=5, pady=5, columnspan=3)

        self.ok = ttk.Button(self.mainFrame, text='Repay Loan', style='TButton', command=self.repayLoan, width=15)
        self.ok.grid(row=5, column=1, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.loanPage, width=5)
        self.back.grid(row=6, column=1, pady=5)

        self.lSpace = ttk.Label(self.mainFrame, width=8)
        self.lSpace.grid(row=0, column=0, pady=10)

        self.rSpace = ttk.Label(self.mainFrame, width=7)
        self.rSpace.grid(row=7, column=2, pady=100)

        self.bind_id = mainWin.bind('<Return>',self.repayLoan)

    def pinChangePage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.comment1 = ttk.Label(self.mainFrame, style='TLabel', text='Current Account Pin:', anchor=E)
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S)

        self.currentPin = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width =10)
        self.currentPin.grid(row=1, column=2, pady=5)
        self.currentPin.focus_set()
        
        self.comment2 = ttk.Label(self.mainFrame, style='TLabel', text='New Account Pin:', anchor=E)
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S)

        self.newPin = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width=10)
        self.newPin.grid(row=2, column=2, pady=5)
        
        self.comment3 = ttk.Label(self.mainFrame, style='TLabel', text='Repeat New Account Pin:', anchor=E)
        self.comment3.grid(row=3, column=1, sticky=W+E+N+S)

        self.newPinCheck = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width =10)
        self.newPinCheck.grid(row=3, column=2, pady=5)

        self.comment4 = ttk.Label(self.mainFrame, text='', justify=RIGHT, style='TLabel', foreground='red', anchor=CENTER)
        self.comment4.grid(row=4, column=0, pady=5, sticky=W+E+N+S, columnspan=3)

        self.ok = ttk.Button(self.mainFrame, style='TButton', text='Change Pin', width=20, command=self.changePin)
        self.ok.grid(row=5, column=1, pady=5, columnspan=2)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.homePage, width=5)
        self.back.grid(row=6, column=1, pady=5, columnspan=2)
        
        self.lSpace = ttk.Label(self.mainFrame, width=1)
        self.lSpace.grid(row=0, column=0, pady=30)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=7, column=3, pady=100)

        self.bind_id = mainWin.bind('<Return>',self.changePin)

    def adminPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.pendingUser = ttk.Button(self.mainFrame, style='TButton', text='Pending User Requests', command=self.pendingUserPage)
        self.pendingUser.grid(row=1, column=1, sticky=W+E+N+S, pady=5)
        
        self.addUser = ttk.Button(self.mainFrame, style='TButton', text='Add New Users', command=self.addUserPage)
        self.addUser.grid(row=2, column=1, sticky=W+E+N+S, pady=5)

        self.removeUser = ttk.Button(self.mainFrame, style='TButton', text='Remove Existing Users', command=self.removeUserPage)
        self.removeUser.grid(row=3, column=1, sticky=W+E+N+S, pady=5)

        self.logout = ttk.Button(self.mainFrame, text='Logout', style='S.TButton', command=self.loginPage, width=7)
        self.logout.grid(row=4, column=1, pady=25)

        self.lSpace = ttk.Label(self.mainFrame, width=6)
        self.lSpace.grid(row=0, column=0, pady=30)

        self.rSpace = ttk.Label(self.mainFrame, width=5)
        self.rSpace.grid(row=5, column=3, pady=10)

    def pendingUserPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select name from user_requests;')
        pending = cursor.fetchone()

        self.userList = Listbox(self.mainFrame, justify=CENTER, font=self.font, height=7, foreground='grey')
        self.userList.grid(row=1, column=1, pady=5, columnspan=2)

        while pending is not None:
            self.userList.insert(END,pending[0])
            pending = cursor.fetchone()

        self.add = ttk.Button(self.mainFrame, text='Accept', style='TButton', command=self.accRequest)
        self.add.grid(row=2, column=1, pady=5)

        self.remove = ttk.Button(self.mainFrame, text='Reject', style='TButton', command=self.rejRequest)
        self.remove.grid(row=2, column=2, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.adminPage, width=5)
        self.back.grid(row=3, column=1, pady=15, columnspan=2)

        self.lSpace = ttk.Label(self.mainFrame, width=4)
        self.lSpace.grid(row=0, column=0, pady=27, padx=4)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=5, column=3, pady=100)

    def addUserPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.comment1 = ttk.Label(self.mainFrame, style='TLabel', text='Enter User\'s Name:', anchor=E)
        self.comment1.grid(row=1, column=1, sticky=W+E+N+S, pady=5, padx=5)

        self.newName = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, width =14)
        self.newName.grid(row=1, column=2, sticky=W+E+N+S, pady=5, padx=5)
        self.newName.focus_set()

        self.comment2 = ttk.Label(self.mainFrame, style='TLabel', text='New Account Number:', anchor=E)
        self.comment2.grid(row=2, column=1, sticky=W+E+N+S, pady=5, padx=5)

        self.newAcc = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, width =14)
        self.newAcc.grid(row=2, column=2, sticky=W+E+N+S, pady=5, padx=5)
        
        self.comment3 = ttk.Label(self.mainFrame, style='TLabel', text='New Account Pin:', anchor=E)
        self.comment3.grid(row=3, column=1, sticky=W+E+N+S, pady=5, padx=5)

        self.newPin = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width=14)
        self.newPin.grid(row=3, column=2, sticky=W+E+N+S, pady=5, padx=5)

        self.comment4 = ttk.Label(self.mainFrame, style='TLabel', text='Repeat Account Pin:', anchor=E)
        self.comment4.grid(row=4, column=1, sticky=W+E+N+S, pady=5, padx=5)

        self.newPinCheck = ttk.Entry(self.mainFrame, justify=LEFT, style='TEntry', font=self.font, show='*', width =14)
        self.newPinCheck.grid(row=4, column=2, sticky=W+E+N+S, pady=5, padx=5)

        self.comment5 = ttk.Label(self.mainFrame, text='', justify=CENTER, style='TLabel', foreground='red', anchor=CENTER)
        self.comment5.grid(row=5, column=1, pady=5, sticky=W+E+N+S, columnspan=3)

        self.ok = ttk.Button(self.mainFrame, text='Create Account', style='TButton', width=20, command=self.newUser)
        self.ok.grid(row=6, column=1, columnspan=2, sticky=N+S, pady=5, padx=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.adminPage, width=5)
        self.back.grid(row=7, column=1, columnspan=2, sticky=N+S, pady=15, padx=5)
        
        self.lSpace = ttk.Label(self.mainFrame, width=0)
        self.lSpace.grid(row=0, column=0, pady=10)

        self.rSpace = ttk.Label(self.mainFrame, width=0)
        self.rSpace.grid(row=8, column=3, pady=100)

        self.bind_id = mainWin.bind('<Return>',self.newUser)

    def removeUserPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select name from user_info;')
        uName = cursor.fetchone()

        self.userList = Listbox(self.mainFrame, justify=CENTER, font=self.font, height=8, foreground='grey')
        self.userList.grid(row=1, column=1, pady=5)

        while uName is not None and uName != 'admin':
            self.userList.insert(END,uName[0])
            uName = cursor.fetchone()

        self.remove = ttk.Button(self.mainFrame, text='Remove User', style='TButton', command=self.delUser)
        self.remove.grid(row=2, column=1, pady=5)

        self.back = ttk.Button(self.mainFrame, text='Back', style='S.TButton', command=self.adminPage, width=5)
        self.back.grid(row=3, column=1, pady=15)

        self.lSpace = ttk.Label(self.mainFrame, width=10)
        self.lSpace.grid(row=0, column=0, pady=23)

        self.rSpace = ttk.Label(self.mainFrame, width=10)
        self.rSpace.grid(row=5, column=2, pady=100)

    def menuPage(self):
        self.clearFrame()
        try:
            mainWin.unbind('<Return>',self.bind_id)
        except TclError:
            pass

        self.signUpButton = ttk.Button(self.mainFrame, text='Sign Up', style='TButton', command=self.signUpPage, width=15)
        self.signUpButton.grid(row=1, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.loginButton = ttk.Button(self.mainFrame, text='Log in', style='TButton', command=self.loginPage, width=15)
        self.loginButton.grid(row=2, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.adminButton = ttk.Button(self.mainFrame, text='Admin Mode', style='TButton', command=lambda:[self.admin(), self.loginPage()], width=15)
        self.adminButton.grid(row=3, column=1, padx=5, pady=5, sticky=W+E+N+S)

        self.quit = ttk.Button(self.mainFrame, text='Quit', style='S.TButton', command=self.destroy, width=4)
        self.quit.grid(row=4, column=1, padx=5, pady=20, sticky=N+S)

        self.lSpace = ttk.Label(self.mainFrame, width=8)
        self.lSpace.grid(row=0, column=0, pady=35)

        self.rSpace = ttk.Label(self.mainFrame, width=1)
        self.rSpace.grid(row=5, column=3, pady=0)

mainWin = ThemedTk(theme='arc')
mainWin.resizable(False,False)
mainWin.geometry('500x500+200+150')
atm(mainWin)
mainWin.mainloop()