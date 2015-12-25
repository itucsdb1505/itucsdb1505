Parts Implemented by İhsan HALICI
=================================


Code and Database Definitions
*****************************

1.1 Database Definitions
------------------------
   .. code-block:: python

      CREATE TABLE TEAMS(ID SERIAL PRIMARY KEY, NAME VARCHAR(50) NOT NULL, FOUNDATION_YEAR INT NOT NULL, COLOURS VARCHAR(50), LEAGUE INT NOT NULL, COUNTRY INT NOT NULL);
      CREATE TABLE MATCHES(ID SERIAL PRIMARY KEY, HOME VARCHAR(50) NOT NULL, AWAY VARCHAR(50) NOT NULL, REFEREE VARCHAR(50), LEAGUE INT NOT NULL);
      CREATE TABLE COMPETITION(ID SERIAL PRIMARY KEY, NAME VARCHAR(100) NOT NULL, TYPE VARCHAR(50) NOT NULL);

**Here ID SERIAL PRIMARY KEY definition is done for all tables. This does the increasing one-by-one order for the tuples.**
**League and Country variables are defined as integer. Becaues they are referenced from the Leagues and Countries Tables.**
**And ID of the Lagues and Countries table is referenced, so they are defined as integer.**

1.2 PYTHON CODE EXPLANATIONS
----------------------------

.. code

def teams():
  **this is the definition of the teams table**
  **and it goes the teams.html here**

def addTeam():
  **we insert a new team to the database here**

def deleteTeam():
  **we delete the row from the database here**

def edit_Team():
  **we update the values here**

def update_Team():
  **this code block is used for the update operations, it goes to the team_update.html file**

def searchTeam():
  **with this code block we can search strings**
  **and it goes the team_search.html here**



def matches():
  **this is the definition of the matches table**
  **and it goes the matches.html here**

def addMatches():
  **we insert a new match to the database here**

def deleteMatches():
  **we delete the row from the database here**

def edit_Matches():
  **we update the values here**

def update_Matches():
  **this code block is used for the update operations, it goes to the matches_update.html file**

def searchMatches():
  **with this code block we can search strings**
  **and it goes the matches_search.html here**



def competition():
  **this is the definition of the competition table**
  **and it goes the competition.html here**

def addCompetition():
  **we insert a new competition to the database here**

def deleteCompetition():
  **we delete the row from the database here**

def edit_Competition():
  **we update the values here**

def update_Competition():
  **this code block is used for the update operations, it goes to the competition_update.html file**

def searchCompetition():
  **with this code block we can search strings**
  **and it goes the competition_search.html here**




TABLE EXPLANATIONS
******************

2.1 TEAMS TABLE EXPLANATIONS
----------------------------
Teams Table includes the columns below

ID (SERIAL PRIMARY KEY)
NAME (VARCHAR(50))
FOUNDATION_YEAR (INT)
COLOURS (VARCHAR(50))
LEAGUE (INT)
COUNTRY (INT)

   .. figure:: teams.png

   Teams Table


2.2 MATCHES TABLE EXPLANATIONS
------------------------------
Matches Table includes the columns below

ID (SERIAL PRIMARY KEY)
HOME (VARCHAR(50))
AWAY (VARCHAR(50))
REFEREE (VARCHAR(50))
LEAGUE (INT)

   .. figure:: matches.png

   Matches Table


2.3 COMPETITION TABLE EXPLANATIONS
----------------------------------
Competition Table includes the columns below

ID (SERIAL PRIMARY KEY)
NAME (VARCHAR(100))
TYPE (VARCHAR(50))

   .. figure:: competition.png

   Competition Table


