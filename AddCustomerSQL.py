import sqlite3
import tkinter
import main
import random
import datetime
import expressions
from TreeEntry import *




def CREATE_TABLES(self):
    conn = sqlite3.connect("customers.db")
    c = conn.cursor()
    tables = ["Appline", "Appointments", "Services", "customers"]

    sql0 = """CREATE TABLE IF NOT EXISTS AppLine(
    AppID INTEGER, ServiceID INTEGER)"""

    sql1 = """CREATE TABLE IF NOT EXISTS Appointments(
    AppID INTEGER PRIMARY KEY AUTOINCREMENT,
    ID TEXT,
    DateCreated TEXT,
    Date TEXT,
    Time TEXT,
    NumOfSlots INTEGER)"""

    sql2 = """CREATE TABLE IF NOT EXISTS Services(
    ServiceID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Service TEXT NOT NULL,
    Price INTEGER,
    NumOfSlots INTEGER)"""

    sql3 = """CREATE TABLE IF NOT EXISTS customers(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT,
    LastName TEXT,
    Telephone TEXT,
    HouseNumber INTEGER,
    PostCode TEXT,
    Email TEXT)"""

    c.execute(sql0)
    c.execute(sql1)
    c.execute(sql2)
    c.execute(sql3)
    conn.commit()
    

def delete_appointment(self):
    appID = self.AppID.get()
    conn = sqlite3.connect("customers.db")
    with conn:
        c = conn.cursor()
        sql = "DELETE FROM Appointments WHERE AppID = ?"
        c.execute(sql,(appID,))
    with conn:
        c = conn.cursor()
        sql = "DELETE FROM AppLine WHERE AppID = ?"
        c.execute(sql,(appID,))


def delete_customer(self):
    conn = sqlite3.connect("customers.db")
    IDD = str(self.selectedSurname.get())
    ID = IDD.split(" ")
    try:
        with conn:
            c = conn.cursor()
            sql = "SELECT AppID FROM Appointments WHERE ID=?"
            c.execute(sql,(ID[0],))
            aID = c.fetchone()
            print("The aID is",aID)
        with conn:
            c = conn.cursor()
            sql = "DELETE FROM customers WHERE ID=?"
            c.execute(sql,(ID[0],))
        with conn:
            c = conn.cursor()
            sql2 = "DELETE FROM Appointments WHERE ID=?"
            c.execute(sql2,(ID[0],))
        with conn:
            c = conn.cursor()
            sql3 = "DELETE FROM AppLine WHERE AppID=?"
            c.execute(sql3, (aID),)
    except:
        print("Didnt Have an Appointment")




def Add_Service(self):
    ServiceName = self.service.get()
    ServicePrice = self.ServicePrice.get()
    conn = sqlite3.connect("customers.db")
    x = 2
    with conn:
        c = conn.cursor()
        sql = "INSERT INTO Services (Service, Price, NumOfSlots) values(?,?,?)"
        c.execute(sql,(ServiceName, ServicePrice, x),)

def Delete_Service(self):
    Service = self.serviceSelected.get()
    conn =sqlite3.connect("customers.db")
    with conn:
        c = conn.cursor()
        sql = "DELETE FROM Services WHERE Service = ?"
        c.execute(sql,(Service,))

def GetServices(self):
    ServicesList = []
    conn = sqlite3.connect("customers.db")
    with conn:
        c = conn.cursor()
        sql = "SELECT Service FROM Services"
        c.execute(sql)
        for row in c.fetchall():
            ServicesList += tuple(row)
    return ServicesList


def Find_Surname(self):
    nameList = []
    value = self.ClientSurname.get()
    conn = sqlite3.connect("customers.db")
    with conn:
        c = conn.cursor()
        sql = "SELECT ID, FirstName, LastName FROM customers WHERE LastName LIKE ?"
        c.execute(sql,(value+"%",))
        All_surnames = c.fetchall()

    for name in All_surnames:
        nameList.append(str(name[0])+" "+name[1]+" "+name[2])

    if len(All_surnames)>0:
        self.surnameBox["values"]=tuple(nameList)

    print(nameList)

    self.surnameBox["values"]=tuple(nameList)
    self.surnameBox.grid(row=3,column=2)


###############################ALL FOR ADDING APPOINTMENTS#######################################        
def convert_service(self):
    try:
        Service = self.serviceSelected.get()
    except:
        Service = self.Service.get()
    conn = sqlite3.connect("customers.db")
    with conn:
        c = conn.cursor()
        sql = "SELECT ServiceID FROM Services WHERE Service = ?"
        c.execute(sql,(Service,))
        for row in c.fetchall():
            print(row)

    return str(row[0])



def add_appointment(self):
    CusID = str(self.selectedSurname.get())
    CusID = CusID.split(" ")
    Createdd = str(datetime.datetime.now())
    Created = Createdd[11:22]
    Time = self.AppointmentTime.get()
    try:
        timecheck = int(Time)
        Date = self.AppointmentDate.get()
        x = 2
        Service = convert_service(self)
        conn = sqlite3.connect("customers.db")
        if expressions.is_date(Date):
            if timecheck < 25 and timecheck >= 0:
                with conn:
                    c = conn.cursor()
                    sql ="INSERT INTO Appointments"\
                          " (ID, DateCreated, Date, Time, NumOfSlots)"\
                          " values(?,?,?,?,?)"
                    c.execute(sql,(CusID[0], Created, Date, Time, x,))
                with conn:
                    c = conn.cursor()
                    AppID = FindAppID(self)
                    sql2 = "INSERT INTO AppLine (AppID, ServiceID) values(?,?)"
                    c.execute(sql2,(AppID[0], Service))
                    return False
            else:
                print("Invalid Time")
                return True
        else:
            print("Invalid Date")
            return True
    except:
        return True


def FindAppID(self):
    conn = sqlite3.connect("customers.db")
    with conn:
        c = conn.cursor()
        sql = "SELECT MAX(AppID) FROM Appointments"
        c.execute(sql)
        for row in c.fetchall():
            print(row)
    return row
####################################################################################################

def find_customer(self):
    user = []
    conn = sqlite3.connect("customers.db")
    cus_ID = str(self.selectedSurname.get())
    cus_ID = cus_ID.split(" ")
    print(cus_ID[0])
    with conn:
        c = conn.cursor()
        sql = "SELECT * FROM customers WHERE ID = ?"
        c.execute(sql, (cus_ID[0],))
        for row in c.fetchall():
            print(row)
            #user += row
    return row

def find_appointments(self):
    conn = sqlite3.connect("customers.db")
    ID = self.find_ID.get()
    with conn:
        c = conn.cursor()
        sql = """
          SELECT Time, Date, ServiceID
          FROM Appointments
          WHERE ID =?"""
        c.execute(sql,(ID,))
        for row in c.fetchall():
            print(row)
    return row
    conn.commit()
    conn.close()


###################################################################################################################        

def UpdateDetails(self):
    conn = sqlite3.connect("customers.db")
    try:
        IDD = str(self.selectedSurname.get())
        ID = IDD.split(" ")
        tryy = True
    except:
        ID = self.ClientID.get()
        print("except", ID)
        tryy = False
    FirstName = self.FirstName.get()
    LastName = self.LastName.get()
    CustomerPhone = self.CustomerTelephone.get()
    HouseNumber = self.CustomerHouseNumber.get()
    PostCode = self.CustomerPostCode.get()
    CustomerEmail = self.CustomerEmail.get()
    if AddCustomerCheck(self):
        with conn:
            c = conn.cursor()
            sql = "UPDATE customers SET FirstName=?, LastName=?, Telephone=?, HouseNumber=?, PostCode=?, Email=?"\
                  " WHERE ID = ?"
            if tryy:
                c.execute(sql,(FirstName, LastName, CustomerPhone, HouseNumber, PostCode, CustomerEmail, ID[0],))
            else:
                c.execute(sql,(FirstName, LastName, CustomerPhone, HouseNumber, PostCode, CustomerEmail, ID,))
            return False
    else:
        return True

def add_customer(self):
    conn = sqlite3.connect("customers.db")
    FirstName = self.CustomerNameFirst.get()
    LastName = self.CustomerNameLast.get()
    Telephone = self.CustomerTelephone.get()
    HouseNumber = self.CustomerHouseNumber.get()
    PostCode = self.CustomerPostCode.get()
    Email = self.CustomerEmail.get()

    if AddCustomerCheck(self):
        c = conn.cursor()
        sql = "INSERT INTO customers (FirstName, Lastname, Telephone, HouseNumber, PostCode, Email) values(?,?,?,?,?,?)"
        c.execute(sql, (FirstName, LastName, Telephone, HouseNumber, PostCode, Email),)
        conn.commit()
        conn.close()
        return False
    else:
        return True


def AddCustomerCheck(self):
    Telephone = self.CustomerTelephone.get()
    PostCode = self.CustomerPostCode.get()
    Email = self.CustomerEmail.get()
    print("Email",Email)
    print("PostCode",PostCode)
    if expressions.is_phone_number(Telephone) and expressions.is_postcode(PostCode):
        if expressions.is_email(Email):
            print("Valid")
            return True
        else:
            return False
    else:
        return False

def UpdateAppointment(self):
    Time = self.AppointmentTime.get()
    Date = self.AppointmentDate.get()
    with conn:
        c = conn.cursor()
        sql = "SELECT Date, Time FROM Appointments WHERE Date=? AND Time=?"
        c.execute(sql,(Date, Time, ))
        for row in c.fetchall():
            print("row", row)
        try:
            if row:
                print("It Exists")
                tkinter.messagebox.showinfo("Warning", "This Appointment time is already booked")
        except:
            print("It doesnt exist")
            UpdateApp(self)

def UpdateApps(self):
    appID = self.AppID.get()
    Date = self.Date.get()
    Time = self.Time.get()
    conn = sqlite3.connect("customers.db")
    with conn:
        c = conn.cursor()
        sql = "SELECT Date, Time FROM Appointments WHERE Date=? AND Time=?"
        c.execute(sql,(Date, Time, ))
        for row in c.fetchall():
            print("row", row)
        try:
            if row:
                tkinter.messagebox.showinfo("Warning", "This Appointment time is already booked")
        except:
            UpdateApp(self)
                

def UpdateApp(self):
    conn = sqlite3.connect("customers.db")
    appID = self.AppID.get()
    Time = self.Time.get()
    timecheck = int(Time)
    Date = self.Date.get()
    Service = convert_service(self)
    if expressions.is_date(Date):
        if timecheck < 25 and timecheck >= 0:
            with conn:
                c = conn.cursor()
                sql = "UPDATE Appointments SET Date=?, Time=? WHERE AppID=?"
                sql1 = "UPDATE AppLine SET ServiceID = ? WHERE AppID=?"
                c.execute(sql,(Date, Time, appID,))
                c.execute(sql1,(Service, appID,))

        else:
            tkinter.messagebox.showinfo("Warning", "Invalid Time")
    else:
        tkinter.messagebox.showinfo("Warning", "Invalid Date")
        

        
        




#conn.commit()
#c.execute("SELECT * FROM Customers WHERE Name='Oliver'")





#def add_customer(self):
