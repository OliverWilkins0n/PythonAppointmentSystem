import smtplib
import sqlite3
import main


EMAIL_USER = "DoggyDatabase2212@gmail.com"
EMAIL_PASSWORD = "Generic1234"



def SendGlobalEmail(self):
    EMAIL_USER = "DoggyDatabase2212@gmail.com"
    EMAIL_PASSWORD = "Generic1234"
    #########INITIALISING#########################################################

    server = smtplib.SMTP("smtp.gmail.com",587, timeout=120)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)

    ##############################################################################

    subject = self.ESubject.get()
    msg = self.Eletter.get()
    message = "Subject: {}\n\n{}".format(subject,msg)

    EmailList = GetEmailList(self)
    ##############################################################################
    for i in EmailList:
        server.sendmail(EMAIL_USER, i, message)

def GetEmailList(self):
    conn = sqlite3.connect("customers.db")
    Email_list = []
    with conn:
        c = conn.cursor()
        sql = "SELECT Email FROM customers"
        c.execute(sql)
        for row in c.fetchall():
            Email_list += row
    return Email_list




#message = "Hi testing this stuff"
#server.sendmail(EMAIL_USER,"oliver.wilkinson22@gmail.com", message)
#server.quit()

#Generic1234
#DoggyDatabase2212