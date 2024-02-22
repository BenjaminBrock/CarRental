""" Digital Application Development Coursework"""
#Import Dependancies:
import sqlite3
import csv
import os
import numpy as np
import pandas as pd

def file_setup():
    if os.path.isfile('CarRentalDB.db') is True:
        Connect_DB()
    elif os.path.isfile('CarRentalDB.db') is False:
        Connect_DB()
        cur.execute("CREATE TABLE UserDir(Username, Password, Email, VIP, Admin)")
        cur.execute("CREATE TABLE Inventory(Car, TypeNum , Available, Category)")
        cur.execute("CREATE TABLE ActivityLog(activityID, Username, Type, Car, Days, Price)")
        AdminSetupFile = open('Admin.csv')
        AdminSetup = csv.reader(AdminSetupFile)
        Insert_Admin =  "INSERT INTO UserDir (Username, Password, Email, VIP, Admin) VALUES (?,?,?,?,?)"
        cur.executemany(Insert_Admin,AdminSetup)
        conn.commit()
        PopALFile = open('Populate_ActivityLog.csv')
        PopAL = csv.reader(PopALFile)
        Insert_AL = "INSERT INTO ActivityLog (activityID, Username, Type, Car, Days, Price) VALUES (?,?,?,?,?,?)"
        cur.executemany(Insert_AL,PopAL)
        conn.commit()



def Connect_DB():
    global conn ,cur
    conn = sqlite3.connect('CarRentalDB.db')
    cur = conn.cursor()


def checkUsrDir():
    cur.execute("SELECT * FROM UserDir")
    x = cur.fetchall()
    df = pd.DataFrame(x)
    df = df.rename(columns={0:'Username', 1:'Password', 2:'Email',3:'VIP', 4:'Admin'})
    print(df)

def PopulateDB():
    if len(np.array(cur.execute('SELECT Car FROM Inventory').fetchall()))> 1:
        print('DB already populated.\nReturning to menu')
    else:
        
        PopInvfile = open('Populate_Inventory.csv')
        PopInv = csv.reader(PopInvfile)
        PopUsrDirFile = open('Populate_UserDir.csv')
        PopUsrDir = csv.reader(PopUsrDirFile)
       


        Insert_User = "INSERT INTO UserDir (Username, Password, Email, VIP, Admin) VALUES (?,?,?,?,?)"
        Insert_Inventory = "INSERT INTO Inventory (Car, TypeNum , Available, Category) VALUES (?,?,?,?)"
        
        cur.executemany(Insert_User,PopUsrDir)
        cur.executemany(Insert_Inventory,PopInv)
       
        conn.commit()
        print('Populated')

def checkAL():
    cur.execute('SELECT * FROM ActivityLog')
    x = np.array(cur.fetchall())
    df = pd.DataFrame(x)
    df = df.rename(columns={0:'ActivityID', 1:'Username', 2:'Type',3:'Car', 4:'Days',5:'Price'})
    print(df)

def checkInv():
    cur.execute('SELECT * FROM Inventory')
    x = np.array(cur.fetchall())
    df = pd.DataFrame(x)
    df = df.rename(columns={0:'Car', 1:'TypeNum', 2:'Available',3:'Category'})
    print(df)

def LoginAdmin():
    Pass = input('Please enter Admin Password: ')
    if Pass not in np.array(cur.execute('SELECT Password FROM UserDir WHERE Username = ?',('Admin',)).fetchone()):
        LoginAdmin()
    else:
        OpenAdminMenu()  


def OpenAdminMenu():
    select = input('Please select from the following options:\n  [1] Open User Directory\n  [2] Open Acitivty Log \n  [3] View Inventory \n  [4] Populate Inventory\n')
    if select == '1':
        checkUsrDir()
        OpenAdminMenu()
    elif select == '2':
        checkAL()
        OpenAdminMenu()
    elif select == '3':
        checkInv()
        OpenAdminMenu()
    elif select == '4':
        PopulateDB()
        OpenAdminMenu()

    





file_setup()
LoginAdmin()















