#!/usr/bin/env python
# -*- coding: utf-8 -*-

from calendar import monthrange
import datetime
from datetime import date
import operator
import os
import sqlite3
import sys
import time

#from DriveUpload import *
from Analytics import *
from Report import *
from Gmail import Email
from Database import *

# Will be moved to cfg file
database = 'DATABASE_NAME'
now = time.localtime()
year = date.today().year
today = datetime.date.today()
Month = datetime.date(year, int(monthinteger)-1, 1)

def createDatabase():
        try:
                open(database)
                print " [+] Database Located"
        except IOError as e:
                conn = sqlite3.connect(database)
                print " [+] New Database Created"
                cur = conn.cursor()
                cur.execute("CREATE TABLE Browsers(Browser TEXT, Users INTEGER, Date TEXT)")
                cur.execute("CREATE TABLE Versions(Browser TEXT, Version TEXT, Users INTEGER, Date TEXT)")
                cur.execute("CREATE TABLE Users(UserName TEXT, Email TEXT, Status TEXT)")
                cur.execute("CREATE TABLE Settings(Action TEXT, Status TEXT)")
                cur.execute("CREATE TABLE Historic(Browser TEXT, Users TEXT, Date TEXT)")
                print " [+] Database Tables Created"
                conn.commit()
                cur.execute("INSERT INTO Settings (Action, Status) VALUES ('runtime', '4')")
                print " [+] Database Settings Created"
                conn.commit()
                cur.execute("INSERT INTO Users (UserName, Email, Status) VALUES ('USERNAME', 'EMAIL_ADDRESS', 'active')")
                cur.execute("INSERT INTO Users (UserName, Email, Status) VALUES ('USERNAME', 'EMAIL_ADDRESS', 'inactive')")
                print " [+] Database Users Completed"
                conn.commit()
                backdateDB()
        print " [+] Database Setup Completed"
        
def backdateDB():
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        Months = 12
        print " [+] Backdating Database"
        months = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(Months)]
        for month in months:
                Year = str(month[0])
                startMonth = str(month[1])
                end = monthrange(month[0], month[1])

                if len(startMonth) > 1:
                        Date = Year+"-"+startMonth+"-01"
                        endDate = Year+"-"+startMonth+"-"+str(end[1])
                else:
                        Date = Year+"-0"+startMonth+"-01"
                        endDate = Year+"-0"+startMonth+"-"+str(end[1])

                print " [+] Adding {start}".format(start=Date)
                Top5 = Analytic(Date,endDate,"TopFive")
                print Top5
                for browser in Top5:
                        insertString = "INSERT INTO Browsers (Browser, Users, Date) VALUES ('{browser}','{users}','{date}')".format(browser=browser[0],users=int(browser[1]),date=Date)
                        cur.execute(insertString)
                        conn.commit()
                conn.commit()

def Run():
        createDatabase()
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        year = date.today().year
        today = datetime.date.today()
        lastMonth = datetime.date(year, int(monthinteger)-1, 1)
        Top5Result = Analytic(lastMonth,today,"TopFive")

        chart(Top5Result, "TopBrowsers", "Top 5 Browsers")
        androidResult = Analytic(lastMonth,today,"Android")
        chart2(androidResult, "AndroidVersions", "Top 5 Android Versions")
        ieResult = Analytic(lastMonth,today,"IE")
        chart2(ieResult, "IEVersions", "Top 5 Internet Explorer Versions")

        getUsers = cur.execute("SELECT *  FROM Users WHERE status='active'")
        users = [dict(username=row[0], email=row[1]) for row in getUsers.fetchall()]
        for user in users:
                User = str(user['username'])
                email = str(user['email'])
                print " [+] Sending Email to: {emailAddr}".format(emailAddr=email)
                #Email().SendMail(User, email)  

        # Insert Browser Details into DB
        for browser in Top5Result:
                insertString = "INSERT INTO Browsers (Browser, Users, Date) VALUES ('{browser}','{users}','{date}')".format(browser=browser[0],users=int(browser[1]),date=today)
                cur.execute(insertString)
                conn.commit()
        for browser in ieResult:
                insertString = "INSERT INTO Versions (Browser, Version, Users, Date) VALUES ('{browser}', '{ver}', '{users}','{date}')".format(browser=browser[0],ver=browser[1], users=int(browser[2]),date=today)
                cur.execute(insertString)
                conn.commit()
        for browser in androidResult:
                insertString = "INSERT INTO Versions (Browser, Version, Users, Date) VALUES ('{browser}', '{ver}', '{users}','{date}')".format(browser=browser[0],ver=browser[1], users=int(browser[2]),date=today)
                cur.execute(insertString)
        conn.commit()

if __name__=="__main__":
        Run()
