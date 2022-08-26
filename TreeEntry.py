###TREE VIEW ENTRYS#####
from main import *
from AddCustomerSQL import *
import sqlite3


##SELECT customers.ID, customers.FirstName, 
##customers.LastName, customers.Telephone, 
##customers.Email, Appointments.Time, 
##Appointments.Date FROM customers, 
##Appointments WHERE customers.ID = 4 
##and customers.ID = Appointments.ID


def pop_tree(self):
    conn = sqlite3.connect("customers.db")
    ID = []
    with conn:
        c = conn.cursor()
        sql = """SELECT customers.ID, customers.FirstName, 
                customers.LastName, customers.Telephone, 
                customers.Email, customers.HouseNumber, customers.PostCode FROM customers"""
        c.execute(sql)
        for row in c.fetchall():
            print(row)
 #           self.table.insert("","end", text=row[0])
            self.table.insert("", 0, values=(row[0], str(row[1] + " " + row[2]),row[3],row[4],row[5],row[6]))

def pop_table(self):
    conn = sqlite3.connect("customers.db")
    with conn:
        c = conn.cursor()
        sql = "SELECT Appointments.AppID, Appointments.Date," \
              " Appointments.Time, Appline.ServiceID FROM Appointments, " \
              "Appline WHERE Appointments.AppID = Appline.AppID"
        c.execute(sql)
        for row in c.fetchall():
            self.tree.insert("",0,values=(row[0],row[1],row[2],row[3]))
            

    
        
        
    