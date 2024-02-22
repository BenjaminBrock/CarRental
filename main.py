""" Digital Application Development Coursework"""
#Import Dependancies:
import sqlite3          #Local Database management package
import os               #For handling files within the project
import re               #Package used to verify email address 
import numpy as np      #NumPy expands the functionality of arrays / lists within python
import pandas as pd     #For this project, Pandas is non essential, however displays better than NumPy when printed
import csv

global activeUser , activeUserName  #By declaring these variables as global, they can be used across functions and class methods

#   The Connect_DB function estabishes the link to the database if there.
#   However, if the database has not been established - this function will generate it.
#   The conn and cur variables must also be declared as global, to be used across the program.

def Connect_DB():                               
    global conn ,cur
    conn = sqlite3.connect('CarRentalDB.db')
    cur = conn.cursor()

#   The file_setup function will use the os library to check if the database exists.
#   If the database exists, then the function uses the nested Connect_DB function to connect to it.
#   Id the database doesn't exsist, the Connect_DB function will generate it, then file_setup populates it.

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
#   intCheck function is used to verify the user input is an integer greater than 0.
#   Provides the same functionality as the isnumeric() built in function.
def intCheck(x):
    try:                    
        x = int(x)
        if x > 0: 
            return(True)    
        else:
            return(False)
    except ValueError: 
        return(False)

#   A validation function to check that the email input meets the desire syntax.
def validate_email_syntax(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" # Syntax example: Hell0@w0rld.com
        return re.match(pattern, email) is not None

#   The sign up function allows users to enter their desired username, password and email.
#   Once these inputs have been validated - they are then inserted into the user directory.
def sign_up():
    
    UserName = input('Input Username:')
    while UserName in np.array(cur.execute('SELECT Username FROM UserDir').fetchall) :          #This query checks username doesn't already exist.
        UserName = input('Username Already Taken \n Try inputting a different Username :')
    
    Pass = 'pass'
    cnf_Pass = 'cnf'
    
    while Pass != cnf_Pass:                                 #While loop prevents user progressing without matching passwords.

        Pass = input('Input Password:')                     #User inputs Password.
        cnf_Pass = input('Confirm Password')                #User inputs Password again to confirm it.
        if Pass != cnf_Pass:
            print('Passwords do not match, try again')
    
    Mail = input('Input Email:')
    while validate_email_syntax(Mail) is not True:                   #While loop prevents user from progressing without a valid email syntax.
        Mail = input('invalid Email, try again \n Input Email:')     #Note : This only verifies email SYNTAX and not whether the email exists.
    
    print('Thank you for signing up, your account is now ready to use!') 
    cur.execute("INSERT INTO UserDir(Username, Password, Email, VIP, Admin) Values(?,?,?,?,?)",(UserName, Pass, Mail, 0, 0))
    
    #Username, Password and email is inserted into the user directory along with a 0 user and admin status as these cannot be set by a user.

    conn.commit()       #Changes to the database must then be commited to the database.

    print('User Added, Continue to Login')
    login()
    
#   The main menu function provides the user with the option to sign up or log in using a simple if / elif statement.
def MainMenu():
    print('Main Menu')
               
    signlog = (input("Select one of the following options: \n [1] Login \n [2] Sign Up\n"))
    
    if signlog == '1':
        print('login')
        login()
    elif signlog == '2':
        print('signup')
        sign_up()
    else:
        MainMenu()
    
#   The login function verifies that the username input is in the directory and that the password input, matches that in the directory.
def login():
    user = input('Press [x] to return to main menu or \nEnter Username:')
    if user == 'x':
        MainMenu() #This if statement allows the user to return to the main menu, preventing a user without an account from getting stuck here.
    
    while user not in np.array(cur.execute('SELECT Username FROM UserDir').fetchall()) :    #As the query provides a list of usernames (there should only be one), the 'not in' statement is used rather than !=.
        user = input('User not found, try again or enter [x] to return to the main menu \nEnter Username:')
        if user == 'x':
            MainMenu()
    global activeUserName   #Here the global variable is called 
    activeUserName = user   #Global variable set to the username of the user who has just logged in.
    
    
    Pass = input('Press [x] to return to main menu or \nEnter Password :')

    if Pass == 'x':
        MainMenu()
    while Pass not in np.array(cur.execute("SELECT Password FROM UserDir WHERE Username = ?", (user,)).fetchone()): #Using the username to filter the userdirecctory, the password is verfied in this statement.
        Pass = input('Incorrect, Try again \n Enter Password :')
    
    global activeUser
    if np.array(cur.execute("SELECT VIP FROM UserDir WHERE Username = ?", (user,)).fetchone())[0] == '1':   #This statement checks for VIP status.
        
        
        activeUser = VIPUser(user)  #active user object is created under the VIPUser class.

    else:
       
        activeUser = User(user)     #active user object is created under the regular User class.
        

    OpenUserMenu()

#   The OneCar function is used to check the Activity Log within the database, to see if the user already has a car on loan. Limiting them to one car at a time.
def OneCar(y):
    x = y
    UsrAct = np.array(cur.execute('SELECT Type FROM ActivityLog WHERE Username = ?',(x,)).fetchall()) # Query returns all transaction types that the active user has performed within the activity log.
    if UsrAct.shape[0]<1:   #   This if statement checks for first time users, who haven't returned a vehicle yet.
        return True
    
    else:
        LastAct = UsrAct[int(UsrAct.shape[0])-1]    #   LastAct is the last entry in the query.
    
        
        if LastAct == 'Return':
            return True 
        else:
            return False
        
#   The first of the three classes is the User Class and its child class VIPUser.
class User:
    def __init__(self,UserName):
        self.Username = UserName
        self.P_list = [30,50,100,25,40,90]  #This feature allows for price generation.
    
    def priceGen(self,TimeFrame,VehicleType):
        if (TimeFrame < 7):
            i=0                             #The timeframe input is passed through the if/else statement to generate an appropriate index for the price lists/
        else: 
            i=3
        i=i+VehicleType
        Price = self.P_list[i]*TimeFrame    #Using the Price list feature, the vehicle type to index and time frame to multiply over, a price is generated.
        return(Price)
    
    def Return(self):
            if OneCar(self.Username) == True:
                if self.Username =='Admin': #Filters for the admin profile that cannot rent or return vehicles.
                    print('Admin Profile cannot Rent or Return Vehicles')
                    OpenUserMenu()
                else:
                    print('It appears you do not have a car to return. \nReturning to main menu now.')  #Filters for users without a car on loan.
                    OpenUserMenu()            
            else:

                cur.execute("SELECT * FROM ActivityLog WHERE UserName = ?",(self.Username,))    #Query searches database for the user's transactions within the activity log.
                A_Log_Pull = np.array(cur.fetchall())
                RowSelector = int(A_Log_Pull.shape[0]) -1   #   The last row / most recent transaction is then located using this index.
                A_Log_Pull = A_Log_Pull[RowSelector]        #   The array is then reduced to only the most recent transaction.
                A_Log_Pull[2] = 'Return'                    #   The transaction type is changed to 'return'
                A_ID = (np.array(cur.execute('SELECT activityID FROM ActivityLog').fetchall())) 
                A_ID = int(A_ID[A_ID.shape[0]-1])+1         #   The return transaction is then given an activity id number.
                cur.execute("INSERT INTO ActivityLog VALUES(?,?,?,?,?,?)",A_Log_Pull)
                conn.commit()                               #   The new transaction is then inserted into the activity log.
                Available_Update = np.array(cur.execute("SELECT Available FROM Inventory WHERE Car = ? " ,(A_Log_Pull[3],)).fetchall())
                Available_Update = int(Available_Update[0]) + 1 #   The number of available vehicles of that model is then increased by 1, signifying that the vehicle has returned.
                cur.execute("UPDATE Inventory SET Available = ? WHERE Car = ?", (Available_Update, A_Log_Pull[3]))
                conn.commit()                                   #   Inventory is then updated with the correct number of available vehicles.
                print('Thank you for returning the %s , we hope you had a good journey!\nYour total bill is:    %s'% (A_Log_Pull[3],A_Log_Pull[5]) )
                OpenUserMenu()
            

class VIPUser(User):
    def __init__(self, UserName):
        super().__init__(User)
        self.P_list = [20,35,80]    #VIP users require a different pricelist that doesn't adjust for longer time periods.
        self.Username = UserName
        
    def priceGen(self, TimeFrame, VehcileType):
        Price = self.P_list[VehcileType] * TimeFrame #Similar to the regular user price gen method - the VIP method only requires the vehicle type to index the pricelist.
        return(Price)
    
#The second class is the vehicle class - this creates an object for the vehicles rented. This class contains 2 features and 0 methods.
class Vehicle:
    def __init__(self,Model,Type):
        self.Model = Model
        self.Type = int(Type)

#The third class is the CarRental class. When scaled across multiple branches, each branch would be its own object of this class.
class CarRental():
    def __init__(self):
        
        self.inventory = cur.execute("SELECT Car FROM Inventory WHERE Available > 0").fetchall()    #   The inventory feature is generated through a database query. 
                                                                                                    #   However, this feature needs updating after each change.
    def displayInv (CarRentalName): 
        
        CarRentalName.inventory = cur.execute("SELECT * FROM Inventory WHERE Available > 0").fetchall() #   Inventory is updated before displaying the available vehicles.
        df = pd.DataFrame(CarRentalName.inventory).rename(columns={0:'Model',1:'TypeNum',2:'Available',3:'Vehicle Type'})   #   Pandas is used here for improved readability.
        df.pop('TypeNum')   #This column is dropped for improved readability.
        print('Total Number of different Cars Available :', len(np.array(CarRentalName.inventory)))
        print(df)
        OpenUserMenu()
    #   CheckCar function is used to verify that the vehicle is in the CarRental inventory.
    def CheckCar (self, Car):
        if Car not in np.array(self.inventory):
             return (False)
        elif Car in np.array(self.inventory):
            return (True)
   
    def RentCar (self, User):
        global activeUser
        
        self.inventory = cur.execute("SELECT Car FROM Inventory WHERE Available > 0").fetchall()    #   Inventory is updated before displaying the available vehicles.

        if OneCar(activeUser.Username) == False:
            print('It appears you already have a car on loan. Return this vehicle in order to rent another.')
            OpenUserMenu()
        else:
            print('Select from the following:\n',pd.DataFrame(self.inventory).rename(columns={0:'Vehicle Model'})) #    Prints a DataFrame of the available models
            Car = input('Input the Vehicle Model you wish to Rent: ')
            Check = self.CheckCar(Car)
            while Check == False:   #   While loop prevents progression if the vehicle input is not found within the inventory.
                Car= input('Vehicle not found \nInput the model name again or input "m" to return to menu\n')
                Check = self.CheckCar(Car)
                if Car == 'm':
                    OpenUserMenu()
            q_Car = cur.execute("SELECT * FROM Inventory WHERE Car = ? ",(Car,)).fetchone() #   Query fetches the inventory entry for the chosen vehicle.
            
            selectedVehicle = Vehicle(q_Car[0],q_Car[1])    #   Object is created for the vehicle.
            TimeFrame = (input('Input the number of days you wish to rent the vehicle: '))
            while intCheck(TimeFrame) == False:
                TimeFrame = (input('Input must be an integer greater than 0, please input again: '))
            TimeFrame=int(TimeFrame)   
            Price = activeUser.priceGen(TimeFrame,selectedVehicle.Type) #   Calls the price generator method from the User/VIPUser class
            confirm = False
            while confirm == False:
                    Choice = (input("You selected the %s for %s days, this will cost you £%s. \n [1] Confirm Transaction \n [2] Cancel\n" % (Car, TimeFrame, Price)))
                    if Choice == '1':
                        #   Next, an array is created to match the columns found in the avtivity log: (activityID, Username, Type, Car, Days, Price)
                        A_ID = (np.array(cur.execute('SELECT activityID FROM ActivityLog').fetchall())) 
                        A_ID = int(A_ID[A_ID.shape[0]-1])+1
                        Usr = activeUserName
                        Type = 'Borrow'
                        car = selectedVehicle.Model 
                        days = TimeFrame
                        Price = Price 
                        T_Log_Entry = [A_ID, Usr, Type, car, days, Price]
                        cur.execute("INSERT INTO ActivityLog VALUES(?,?,?,?,?,?)",T_Log_Entry)  #   Values are inserted into the database.
                        conn.commit()                                                           #   This change must then be commited to the database in order to make the change permanent.
                        Available_Update = np.array((cur.execute("SELECT Available FROM Inventory WHERE Car = ? ", (Car,))).fetchone())[0]  #   Here, the number of available cars of that model is pulled from the inventory table.
                        Available_Update = int(Available_Update) -1
                        cur.execute("UPDATE Inventory SET Available = ? WHERE Car = ?" ,(Available_Update, car))                            #   Next, the number of available cars is reduced, as the vehicle is now on loan.
                        conn.commit()
                        print('Transaction Confirmed. \n Have a safe journey!')
                        OpenUserMenu()
                    elif Choice == '2': 
                        OpenUserMenu()


def OpenUserMenu():
    #   The user menu function provides a simple looping if/elif/else then statement, allowing the user to select their next operation.
    global activeUser   #   The global activeUser variable is called here, in order to pass it into the rent car function if selected.
    choice = 0
    
    choice = input('Welcome, please select an option from the following:\n [1] View Available Vehicles \n [2] Rent a Vehicle \n [3] Return a Vehicle\n [4] Log Out\n') 
    
    if choice == '1':
        Branch.displayInv() 
    elif choice == '2':
        Branch.RentCar(activeUserName)
    elif choice == '3':
        
        activeUser.Return()
    
    elif choice == '4':
        activeUser = 0  #   Whilst not essential to operation, the activeUser value is cleared.
        MainMenu()
    else:
        OpenUserMenu()
   


#The first function to be run is the fileSetup - without this, the classes will not work

file_setup()

#Next Setup the Car Rental Branch by generating a new object for the branch.

global Branch

Branch = CarRental()

#Finally, run the program by initialising the main menu

MainMenu()