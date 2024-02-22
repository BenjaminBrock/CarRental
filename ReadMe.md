# ABOUT 

This project was a university assignment. The criteria was to create a a car rental system with conditional pricing and tracked inventory. In order to make the program more applicable to a real world implementation, I included a SQL database locally that could be encrypted and decrypted as required. Further functionality would be required for implementation - predominantly on the admin side, that needs to be able to edit the user database.


## File structure:

Within this folder are 4 CSV files and 2 Python files. 
The CSV files are used to populate and initiate the database for use.

Admin.py:
This file is used to monitor the database and initially populate it.

main.py:

This is the user program, it does not have access to the admin program's features to ensure GDPR regulations are maintained.



### INSTRUCTIONS: ###

* 1 - Run the Admin.py file
* 2 - Use the Password ' AdminP '
* 3 - Select the populate database function
* 4 - Close Admin.py 
* 5 - Run main.py file


### VIP USERS ###
The list of sample users within the Populate_Inventory csv file can be read to find the sample logins. 
The 'Grace' profile can be used when testing out the VIP functionality.
