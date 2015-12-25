Parts Implemented by Emre EROĞLU
================================

Database Initialization
=======================
Initialization operation is executing initialDB.sql file and committing it to database.

**This class helps initialization of the database.**
**Parameters: initiateDatabase takes app as parameter. It gives us to connection information.**

   .. code-block:: python

      import psycopg2
      import sys
      import os

      class DataBaseSetup:

          def initiateDataBase(self, app):
              try:
                  connection = psycopg2.connect(app.config['dsn'])
                  #read sqlFile commands from SQLFile
                  with open("initialDB.sql") as SQLFile:
                      sqlFile = SQLFile.readlines()
                      cursor = connection.cursor()
                      #execute commands readed
                      for transaction in sqlFile:
                          if transaction != '\n':
                              cursor.execute(transaction)

                      connection.commit()

                      print("Database initialized.")

                  connection.close()
              except:
                  print("Database could not initialized. Err : ")
                  print(sys.exc_info()[0])


   def initiateDB():
      **Calls initialize function from DataBaseSetup class.**
      **Sends example data to browser.**

Login Management
================

flask-login appliacation is required for session management.

Database Design For Users
-------------------------

CREATE DOMAIN AUTH VARCHAR(10) CHECK (VALUE IN ('u', 'm', 'a'));

CREATE TABLE USERS(ID SERIAL PRIMARY KEY, NAME TEXT, AGE DATE, EMAIL CHAR(50), PASSWORD CHAR(32), AUTH AUTH,  COUNTRY_ID INT);

There is 7 columns in USERS table, it has a primary key named id and it's type is SERIAL.

EMAIL is determiner of uniqueness of user. It checked in code.
AUTH is shows user authentication levels.
PASSWORDS are stored as MD5 hashes in database.
AGE column was INT value I did not changed it when I made it DATE.

Has foreign key with countries.

Code Design For Users
---------------------

User Managements consist of 2 html files.

AnonymousUser class is extended from Flasks AnonymousUserMixin class.

class AnonymousUser(AnonymousUserMixin):
    pass


User class is extended from Flasks UserMixin class.

class User(UserMixin):

..code    def __init__(self, id):
      **Gets id of user and fills user instance wit own data.**

    def is_active(self):
      **Returns is user active. It is true as hard coded.**
    def is_anonymous(self):
      **Returns is user anonymous. It is false as hard coded.**
    def is_authenticated(self):
      **Returns user authentication station it is not relevant with AUTH domain in DATABASE, it is flask login required area. It returns true as hard coded.**
    def get_id(self):
     **Returns self primary key, id.**
    def get_auth(self):
      **returns authentication level which mentioned in database design section.**

**unauthorized_callback function provides url fix for after login**
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

**login manager uses @login_manager.user_loader annotation for start session**
@login_manager.user_loader
def load_user(user_id):
    return User(int(user_id))


def login():
   **Gets user credentials as POST data and redirects home page or login page in order to credentials trueness.**

def logout():
   **Redirects home page.**

def home():
   **Opens home page. -> home.html**

def userManagement():
   **Opens User Management Page. -> userManagement.html**
   **This function is login required. You cannot use it without authorized user.**
   **Lists user list on the botton of page.**
   **This function can get GET and POST data, if it gets search variable as POST data it lists only search results.**

def addUser():
   **This function inserts user to table it gets POST data as user information.**
   **It is called from userManagement page.**

def userUpdate():
   **This function updates usert to table it gets POST data as user information.**
   **It is called from userManagement page.**

def deleteUser():
   **This function deletes user from database.**

def register():
   **Inserts user to database.**
   **It called from user register page.**

def registerPage(errors=None):
   **Opens register.html **
   **Makes back-end data validation for user registration.**
   **Takes errors parameter for validation.**


News Management
===============

Database Design For News
------------------------

CREATE TABLE NEWS(ID SERIAL PRIMARY KEY, TITLE CHAR(50), CONTENT TEXT, USER_ID INT);

It has PRIMARY KEY ID as SERIAL type.

It has foreign key with users.

Code Design For News
--------------------

News consists of 2 html files.


def newsManagement():
   **Opens News Management Page. -> newsManagement.html**
   **This function is login required. You cannot use it without authorized user.**
   **Lists user list on the botton of page.**
   **This function can get GET and POST data, if it gets search variable as POST data it lists only search results.**
   **Normal users cannot manage News, Moderators can edit and add own News and Administrators manages all of News.**

def addNews():
   **Validates and inserts news to database.**

def newsUpdate():
   **Updates news on database.**

def updateNews():
   **Fills to manage page for update.**

def deleteNews():
   **Deletes news from database.**

def news():
   **News read page.**
   **Every user can see.**

