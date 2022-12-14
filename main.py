from tkinter import *
import tkinter as tk
from tkinter.ttk import Combobox,Treeview,Scrollbar
from AddCustomerSQL import *
from sqlite3 import *
from tkinter import messagebox
import datetime
from expressions import *
from TreeEntry import *
import re
from smtpEmail import *
from tkinter.scrolledtext import ScrolledText
import time

#def isLeapYear(year):
#    if(Year % 4 == 0 and year %100 !=0) or(year%400 == 0):
#        return True
#    else:
#        return False



class MainMenu:
    def __init__(self, master):
        CREATE_TABLES(self)
        self.master = master
        self.master.geometry("1280x700")
        self.master.title("Doggie Barber Shop")
        self.master.config(bg="#E3E3E3")
        ######################CLOCK###############################
        self.digitalClock = Label(self.master, text="", font=("Courier", 16))
        self.digitalClock.place(x=1000,y=10)
        self.tick()
        self.dateL = Label(self.master, text="", font=("Courier", 10))
        self.dateL.place(x=1010, y=40)
        self.tickdate()
        

            

        ##########################################################

        self.welcomeLabel = Label(self.master, text="Doggie Barber Shop Database", font=("Courier", 13))
        self.addCustomer = Button(self.master, text="Add Customer", command=self.addCustomer)
        self.deleteCustomer = Button(self.master, text="Update/Delete", command=self.deleteCustomer)
        self.serviceButton = Button(self.master, text="Add Service", command=self.addService)
        self.sendEmailButton = Button(self.master, text="Send Email", command=self.SendEmail).place(x=377, y=30)

        self.addAppointmentButton = Button(self.master, text="Add Appointment", command=self.addAppointment)
        self.quitButton = Button(self.master, text="Quit", command=self.master.quit)

        ##############TREE VIEW#######################
        self.DetailsL = Label(self.master, text="Customer Details", font=("Courier", 11))

        self.table = Treeview(self.master, height=10)
        self.table["columns"]=("ID","Name","Telephone","Email","HouseNumber","PostCode")
        self.table.heading("#0", text="")
        self.table.column("#0",width=10, stretch=NO)
        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Telephone", text="Telephone")
        self.table.heading("Email", text="Email")
        self.table.heading("HouseNumber", text="HouseNumber")
        self.table.heading("PostCode", text="PostCode")
        self.table.bind("<Double-1>", self.OnDoubleClick)
        #############INSERT ID##################
        pop_tree(self)
        self.UpdateTableB = Button(self.master, text="Update Tables", command=self.UpdateTable)

        #########################################

        #############TREE VIEW FOR THE APPOINTMENTS############
        self.AppointmentsL = Label(self.master, text="Appointments", font=("Courier", 11))

        self.tree = Treeview(self.master, height=10)
        self.tree["columns"]=("AppID","Date","Time","Service")
        self.tree.heading("#0", text="")
        self.tree.column("#0",width=10, stretch=NO)
        self.tree.heading("AppID", text="AppID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Service",text="Service")
        self.tree.bind("<Double-1>", self.OnDoubleClickApp)

        pop_table(self)

        #############LAY OUT########################
        self.welcomeLabel.place(x=170, y=0)
        self.addCustomer.place(x=10, y=30)
        self.deleteCustomer.place(x=100, y=30)
        self.addAppointmentButton.place(x=189, y=30)
        self.serviceButton.place(x=300, y=30)
        self.UpdateTableB.place(x=590, y=327)
        self.quitButton.place(x=615, y=625)
        self.table.place(x = 10, y=100)

        self.AppointmentsL.place(x=300, y=330)
        self.DetailsL.place(x=290, y=68)

        self.tree.place(x=10,y=360)
        
    def tickdate(self):
        date2 = time.strftime("%d/%m/%Y")
        self.dateL.config(text=date2)
        self.dateL.after(5000, self.tickdate)
        
    def tick(self):
        time2 = time.strftime("%H:%M:%S")
        self.digitalClock.config(text=time2)
        self.digitalClock.after(1000, self.tick)

    def SendEmail(self):
        root123 = Toplevel(self.master)
        mygui = SendEmailMenu(root123)
        
    def OnDoubleClickApp(self, event):
        curItem = self.tree.focus()
        global AppList
        AppList = []
        Dictionary = self.tree.item(curItem)
        for i in Dictionary.values():
            AppList.append(i)
        
        root6 = Toplevel(self.master)
        mygui = AppSelected(root6, AppList)

    def OnDoubleClick(self, event):
        curItem = self.table.focus()
        global clientList
        clientList = []
        Dictionary = self.table.item(curItem)
        for i in Dictionary.values():
            clientList.append(i)

        root5 = Toplevel(self.master)
        mygui = TreeViewSelected(root5, clientList)


    def UpdateTable(self):
        x = self.table.get_children()
        for item in x:
            self.table.delete(item)
        pop_tree(self)

        y = self.tree.get_children()
        for item in y:
            self.tree.delete(item)
        pop_table(self)

    def addService(self):
        root4 = Toplevel(self.master)
        mygui=AddingService(root4)

    def addAppointment(self):
        root3 = Toplevel(self.master)
        mygui= AddingAppointments(root3)

    def addCustomer(self):
        root2 = Toplevel(self.master)
        mygui=addCustomers(root2)

    def deleteCustomer(self):
        root3 = Toplevel(self.master)
        mygui=deleteCustomers(root3)

    def UpdateCInfo(self):
        UpdateDetails(self)
        
    def UpdateAppointment(self):
        UpdateApps(self)
        
    def DeleteAppointment(self):
        delete_appointment(self)

class SendEmailMenu():
    def __init__(self, master):
        self.ESubject = StringVar()
        self.Eletter = StringVar()

        self.master = master
        self.master.geometry("700x400")

        Label(self.master, text="Subject").grid(row=1,column=0)
        Entry(self.master, textvariable = self.ESubject, width=40).grid(row=1,column=1,sticky=W)
        Label(self.master, text="Content").grid(row=2,column=0)
        Entry(self.master, textvariable = self.Eletter, width=100).grid(row=2,column=1)

        Button(self.master, text="Send email to all Clients", command=self.SendAllMail).grid(row=4,column=1)


    def SendAllMail(self):
        SendGlobalEmail(self)
        
class AppSelected(MainMenu):
    def __init__(self, master, AppList):
        print("The applist is", AppList)
        self.master = master
        self.master.geometry("1280x720")
        
        self.AppID = StringVar()
        self.Date = StringVar()
        self.Time = StringVar()
        self.Service = StringVar()
        self.serviceSelected = StringVar()
        self.Customer = StringVar()
        
        Label(self.master, text="Edit Appointment", font=("Courier", 13)).grid(row=1,column=1, columnspan=2)
        Label(self.master, text="Customer").grid(row=2,column=1)
        Entry(self.master, textvariable = self.Customer, state="disabled").grid(row=2,column=2)
        Label(self.master, text="App ID").grid(row=3,column=1)
        Entry(self.master, textvariable = self.AppID, state="disabled").grid(row=3,column=2)
        Label(self.master, text="Date").grid(row=4,column=1)
        Entry(self.master, textvariable = self.Date).grid(row=4,column=2)
        Label(self.master, text="Time").grid(row=5,column=1)
        Entry(self.master, textvariable = self.Time).grid(row=5,column=2)
        #Label(self.master, text="Service").grid(row=6,column=1)
        #Entry(self.master, textvariable = self.Service).grid(row=6,column=2)
        
        ServicesList = GetServices(self)
        Label(self.master, text="Select Service").grid(row=7,column=1)
        self.ServiceSelectedd = Combobox(self.master, textvariable=self.serviceSelected, width=17)
        self.ServiceSelectedd["values"] = (ServicesList)
        self.ServiceSelectedd.grid(row=7,column=2)
        
        Button(self.master, text="Update Appointment", command = self.UpdateAppointment).grid(row=8,column=1)
        Button(self.master, text="Delete Appointment", command = self.DeleteAppointment).grid(row=8,column=2)
               
        AppsL = AppList[2]
        self.AppID.set(AppsL[0])
        self.Date.set(AppsL[1])
        self.Time.set(AppsL[2])
        self.Service.set(AppsL[3])
        
        ########################################################################################################
        conn = sqlite3.connect("customers.db")
        with conn:
            c = conn.cursor()
            sql = "SELECT ID FROM Appointments WHERE AppID = ?"
            c.execute(sql,(AppsL[0],))
            answer = c.fetchone()
            names = []
            sql2 = "SELECT FirstName, LastName FROM customers WHERE ID = ?"
            c.execute(sql2,(answer[0],))            
            for row in c.fetchall():
                names += row
            name = str(names[0]) +" "+str(names[1])
            
            
            
        self.Customer.set(name)    
        ########################################################################################################
        

class TreeViewSelected(MainMenu):
    def __init__(self, master, clientList):
        self.master = master
        self.master.geometry("1280x720")
        self.ClientID = StringVar()
        self.FirstName = StringVar()
        self.LastName = StringVar()
        self.CustomerTelephone = StringVar()
        self.CustomerEmail = StringVar()
        self.CustomerHouseNumber = StringVar()
        self.CustomerPostCode = StringVar()

        ############GUI#################
        Label(self.master, text="Selected Customer Window", font=("Courier", 13)).grid(row=1,column=1, columnspan=2)
        Label(self.master, text="Client ID:").grid(row=2,column=1)
        Entry(self.master, textvariable=self.ClientID, state="readonly").grid(row=2,column=2)
        Label(self.master, text="Clients Name:").grid(row=3,column=1)

        self.FirstNameEntry = Entry(self.master, textvariable=self.FirstName).grid(row=3,column=2)

        Entry(self.master, textvariable=self.LastName,).grid(row=3,column=3)            ##last name
        Label(self.master, text="Phone Number").grid(row=4,column=1)                   ###PHONE
        Entry(self.master, textvariable=self.CustomerTelephone).grid(row=4,column=2)        ###PHONE
        Label(self.master, text="Email").grid(row=5,column=1)                           ##EMAIL
        Entry(self.master, textvariable=self.CustomerEmail).grid(row=5,column=2)        ##Email
        Label(self.master, text="HouseNumber").grid(row=6,column=1)
        Entry(self.master, textvariable=self.CustomerHouseNumber).grid(row=6,column=2)
        Label(self.master, text="Post Code").grid(row=7,column=1)
        Entry(self.master, textvariable=self.CustomerPostCode).grid(row=7,column=2)

        #Button(self.master, text="Update Details",command=self.UpdateCInfo).grid(row=8, column=1)


        #############################MAKING THE ENTRYS FILLED###################################################################
        clientInfo = clientList[2]
        Namess = re.split("\s+", clientInfo[1])
        self.ClientID.set(clientInfo[0])
        self.FirstName.set(Namess[0])
        self.LastName.set(Namess[1])
        self.CustomerTelephone.set(clientInfo[2])
        self.CustomerEmail.set(clientInfo[3])
        self.CustomerHouseNumber.set(clientInfo[4])
        self.CustomerPostCode.set(clientInfo[5])
        ##########################################################################################################################


class AddingAppointments():
    def __init__(self, master):
        self.master = master
        self.master.geometry("450x350")

        self.AppointmentDate = StringVar()
        self.AppointmentTime = StringVar()
        self.Service = StringVar()
        self.ClientSurname = StringVar()
        self.selectedSurname = StringVar()
        self.serviceSelected = StringVar()
        self.output = StringVar()

        #########################################COMBO BOX#############################################

        self.addAppointmentLabel = Label(self.master, text="Add Appointment",font=("Courier", 13)).grid(row=1,column=2, columnspan=2)

        Label(self.master, text="Search Client").grid(row=2,column=1)
        Entry(self.master, textvariable=self.ClientSurname).grid(row=2,column=2)
        Button(self.master, text="Find Client", command=self.FindClient).grid(row=2,column=3)

        self.surnameBox = Combobox(self.master, textvariable=self.selectedSurname, width=17)

        ####################################ADDING APPOINTMENTS####################################

        self.appointmentTimeLabel = Label(self.master, text="Enter Time of the appointment").grid(row=10,column=1)
        self.appointmentTimeEntry = Spinbox(self.master, from_=1, to=24,textvariable=self.AppointmentTime).grid(row=10,column=2)
        self.appointmentDateLabel = Label(self.master, text="Enter Date of Appointment dd/mm/yy").grid(row=11, column=1)
        self.appointmentDateEntry = Entry(self.master, textvariable=self.AppointmentDate).grid(row=11,column=2)
        ###################################SERVICE COMBO BOX#############################################################
        ServicesList = GetServices(self)
        Label(self.master, text="Select Service").grid(row=12,column=1)
        self.ServiceSelectedd = Combobox(self.master, textvariable=self.serviceSelected, width=17)
        self.ServiceSelectedd["values"] = (ServicesList)
        self.ServiceSelectedd.grid(row=12,column=2)
        #################################################################################################################
        Label(self.master, textvariable=self.output).grid(row=12,column=4)
        
        
        self.addAppointmentButton = Button(self.master, text="Add Appointment", command = self.AddAppointment).grid(row=13,column=1)

    def AddAppointment(self):
        Time = self.AppointmentTime.get()
        Date = self.AppointmentDate.get()
        conn = sqlite3.connect("customers.db")
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
                if add_appointment(self):
                    tkinter.messagebox.showinfo("Warning", "Invalid Date or Time")

    def FindClient(self):
        Find_Surname(self)

class AddingService():
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x400")
        self.ServicesList = StringVar()
        self.service=StringVar()
        self.ServicePrice = StringVar()
        self.DelService = StringVar()
        self.serviceSelected = StringVar()
        ##### ADDING SERVICE #####################################################################
        Label(self.master, text="Add Service").grid(row=1,column=1)
        AdditionalService = Entry(self.master, textvariable=self.service).grid(row=1,column=2)
        Label(self.master, text="Service Price").grid(row=2,column=1)
        Pricing = Entry(self.master, textvariable=self.ServicePrice).grid(row=2,column=2)

        Button(self.master, text="Add Service", command=self.addServices).grid(row=3,column=1)

        ###### DELETE SERVICES #######################################################################
        ServicesList = GetServices(self)
        print(ServicesList)
        Label(self.master, text="Select Service to Delete").grid(row=4,column=1)
        self.ServiceSelectedd = Combobox(self.master, textvariable=self.serviceSelected)
        self.ServiceSelectedd["values"] = (ServicesList)
        self.ServiceSelectedd.grid(row=4,column=2)

        Button(self.master, text="Delete Service", command=self.deleteServices).grid(row=5,column=1)
        #####################################################################################################

    def addServices(self):
        Add_Service(self)

    def deleteServices(self):
        Delete_Service(self)

class deleteCustomers():
    def __init__(self, master):
        self.find_ID = StringVar()
        self.FirstName = StringVar()
        self.LastName= StringVar()
        self.CustomerTelephone = StringVar()
        self.CustomerHouseNumber = StringVar()
        self.CustomerEmail = StringVar()
        self.CustomerTime = StringVar()
        self.CustomerDate = StringVar()
        self.CustomerPostCode = StringVar()
        self.ClientSurname = StringVar()
        self.selectedSurname = StringVar()
        self.output = StringVar()

        self.master = master
        self.master.geometry("550x350")
        self.master.title("Delete Customer")

        self.addAppointmentLabel = Label(self.master, text="Update/Delete",font=("Courier", 13)).grid(row=1,column=2, columnspan=2)

        Label(self.master, text="Search Client").grid(row=2,column=1)
        Entry(self.master, textvariable=self.ClientSurname).grid(row=2,column=2)
        Button(self.master, text="Find Client", command=self.FindClient).grid(row=2,column=3)

        self.surnameBox = Combobox(self.master, textvariable=self.selectedSurname, width=17)
        #self.surnameBox.bind("<<ComboboxSelected>>", print("Selected!"))

        Button(self.master, text="Search Details", command=self.finding_details).grid(row=3,column=3)

        #**********Found Customer************
        self.foundCustomerHeader = Label(self.master, text="Customers Details", font=("Courier", 13)).grid(row=4, column=1, columnspan=2, sticky="W")

        self.CustomerfName = Label(self.master, text="First Name").grid(row=5, column=1)
        self.CustomerfNameEntry = Entry(self.master, textvariable = self.FirstName ).grid(row=5, column=2)

        self.CustomerLName = Label(self.master, text="Last name").grid(row=7, column=1)
        self.CustomerLNameEntry = Entry(self.master, textvariable = self.LastName).grid(row=7, column=2)

        self.CustomerPhoneLabel = Label(self.master, text="Customer Number").grid(row=8, column=1)
        self.CustomerPhoneEntry = Entry(self.master, textvariable = self.CustomerTelephone).grid(row=8, column=2)

        self.CustomerHouseNumberLabel = Label(self.master, text="Customer House Number").grid(row=9, column=1)
        self.CustomerHouseNUmberEntry = Entry(self.master, textvariable = self.CustomerHouseNumber).grid(row=9, column=2)

        self.CustomerPostCodeLabel = Label(self.master, text="Customer Post Code").grid(row=10, column=1)
        self.CustomerPostCodeEntry = Entry(self.master, textvariable= self.CustomerPostCode).grid(row=10,column=2)

        self.CustomerEmailLabel = Label(self.master, text="Customer Email").grid(row=11, column=1)
        self.CustomerEmailEntry = Entry(self.master, textvariable = self.CustomerEmail).grid(row=11, column=2)

        self.UpdateCustomerButton = Button(self.master, text="Update Info", command = self.cus_update).grid(row=13, column=2)
        self.DeleteCustomerButton = Button(self.master, text="Delete Customer", command = self.deleteC).grid(row=13,column=1)
        
        Label(self.master, text="", textvariable = self.output).grid(row=11,column=3)

    def cus_update(self):
        if UpdateDetails(self):
            self.output.set("Make Sure That All Values Are Correct!")
        else:
            self.output.set("Update has been made")

    def FindClient(self):
        Find_Surname(self)

    def deleteC(self):
        delete_customer(self)

######FINDS THE CUSTOMER########
    def finding_details(self):
        try:
            self.users = find_customer(self)
            print(self.users)
            self.FirstName.set(self.users[1])
            self.LastName.set(self.users[2])
            self.CustomerTelephone.set(self.users[3])
            self.CustomerHouseNumber.set(self.users[4])
            self.CustomerPostCode.set(self.users[5])
            self.CustomerEmail.set(self.users[6])
        except:
            tkinter.messagebox.showinfo("Warning","This ID does not exist")


class addCustomers():
    def __init__(self, master):
        self.CustomerNameFirst = StringVar()
        self.CustomerNameLast = StringVar()
        self.CustomerTelephone = StringVar()
        self.CustomerHouseNumber = StringVar()
        self.CustomerPostCode = StringVar()
        self.CustomerEmail = StringVar()
        self.CusIDApp = StringVar()
        self.AppointmentTime = StringVar()
        self.AppointmentDate = StringVar()
        self.Service = StringVar()
        self.output = StringVar()

        self.master = master
        self.master.geometry("550x350")
        self.master.title("Add Customers")
        #********** Adding Customers Name ********
        self.addCustomerLabel = Label(self.master, text="Enter the first name of the customer").grid(row=1, column=1)
        self.addCustomerEntry = Entry(self.master, textvariable = self.CustomerNameFirst).grid(row=1,column=2)
        self.addCustomerLastLabel = Label(self.master, text="Etner the last name of the customer").grid(row=2, column=1)
        self.addCustomerLastEntry = Entry(self.master, textvariable = self.CustomerNameLast).grid(row=2, column=2)
        #********** Contact Details ***********
        self.addTelephoneLabel = Label(self.master, text="Enter telephone num").grid(row=3,column=1)
        self.addTelephoneEntry = Entry(self.master, textvariable = self.CustomerTelephone).grid(row=3, column=2)
        #********** Address ************
        self.addAddressLabel = Label(self.master, text="Enter House Number").grid(row=4,column=1)
        self.addAddressEntry = Entry(self.master, textvariable = self.CustomerHouseNumber).grid(row=4, column=2)
        self.addPostCostLabel = Label(self.master, text="Enter Post Code").grid(row=5, column=1)
        self.addPostCodeEntry = Entry(self.master, textvariable = self.CustomerPostCode).grid(row=5, column=2)
        #********* Email ************
        self.addEmailLabel = Label(self.master, text="Enter Customers Email").grid(row=6, column=1)
        self.addEmailEntry = Entry(self.master, textvariable = self.CustomerEmail).grid(row=6, column=2)
        self.AddCustomerButton = Button(self.master, text="Add Customer", command = self.AddCustomerDatabase).grid(column=1, row=7)

        Label(self.master, textvariable=self.output).grid(row=10,column=2)


    def AddCustomerDatabase(self):

        if add_customer(self):
            self.output.set("Make Sure That All Values Are Correct!")
        else:
            self.output.set("")
            

class showInfo():
    def __init__(self, master):
        self.master = master
        self.geometry=("450x300")
        self.master.title("Customer Infomation")



def main():
    root = Tk()
    MyMenu = MainMenu(root)
    root.mainloop()


if __name__ == '__main__':
    main()
