Parts Implemented by Emre EROĞLU
================================

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

Code Design For Users
---------------------

User Managements consist of 2 html files.
User class is extended from Flasks UserMixin class.
AnonymousUser class is extended from Flasks AnonymousUserMixin class.

class User(UserMixin):

    def __init__(self, id):
      Gets id of user and fills user instance wit own data.

    def is_active(self):
      Returns is user active. It is true as hard coded.
    def is_anonymous(self):
      Returns is user anonymous. It is false as hard coded.
    def is_authenticated(self):
      Returns user authentication station it is not relevant with AUTH domain in DATABASE, it is flask login required area. It returns true as hard coded.
    def get_id(self):
      Returns self primary key, id.
    def get_auth(self):
      returns authentication level which mentioned in database design section.



def login():
   Gets user credentials as POST data and redirects home page or login page in order to credentials trueness.

def logout():
   Redirects home page.

def home():
   Opens home page. -> home.html

def userManagement():
   Opens User Management Page. -> userManagement.html
   This function is login required. You cannot use it without authorized user.
   Lists user list on the botton of page.
   This page can get GET and POST data, if it gets search variable as POST data it lists only search results.


