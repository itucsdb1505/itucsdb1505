Parts Implemented by Nurullah Topaloğlu
=======================================
1 TABLES
~~~~~~~~
This part explains how Players, Coaches and Referees tables are structured and what operations can run on them.

1.1 Players Table
-----------------
* Attributes of the Players Table.
+---------+--------+-------------+-------------+----------------+
| Name    | Type   | Primary Key | Foreign Key | Auto Increment |
+=========+========+=============+=============+================+
| id      | SERIAL | 1           | 0           | 1              |
+---------+--------+-------------+-------------+----------------+
| name    | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| surname | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| age     | INT    | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| nation  | INT    | 0           | 1           | 0              |
+---------+--------+-------------+-------------+----------------+
| team    | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| field   | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| goal    | INT    | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+

* *name* holds the name of the player.
* *surname* holds the surname of the player.
* *age* holds the age of the player.
* *nation* holds the id of the players nation referenced from the country table.
* *team* holds the team that player plays.
* field* holds the players field in tthe pool.
* *goal* holds number of goals that player has scored.

SQL Statement that initializes the Players Table:
   .. code-block:: python

      DROP TABLE IF EXISTS PLAYERS;
      CREATE TABLE PLAYERS(
      ID SERIAL PRIMARY KEY,
      NAME TEXT,
      SURNAME TEXT,
      AGE INT,
      NATION INT,
      TEAM TEXT,
      FIELD TEXT,
      GOAL INT);

      ALTER TABLE PLAYERS ADD CONSTRAINT FK_PLAYERS_COUNTRIES FOREIGN KEY (NATION) REFERENCES COUNTRIES (ID) ON DELETE SET NULL ON UPDATE CASCADE;

Since *Players(Nation)* is referenced from *Countries(id)* and it is *ON DELETE SET NULL ON UPDATE CASCADE*, whenever a country is deleted, it will be *NULL*

1.2 Coaches Table
-----------------
* Attributes of the Coaches Table.
+---------+--------+-------------+-------------+----------------+
| Name    | Type   | Primary Key | Foreign Key | Auto Increment |
+=========+========+=============+=============+================+
| id      | SERIAL | 1           | 0           | 1              |
+---------+--------+-------------+-------------+----------------+
| name    | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| surname | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| nation  | INT    | 0           | 1           | 0              |
+---------+--------+-------------+-------------+----------------+
| team    | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+

* *name* holds the name of the coach.
* *surname* holds the surname of the coach.
* *nation* holds the id of the coachs nation referenced from the country table.
* *team* holds the team that coach manages.


SQL Statement that initializes the Coaches Table:
   .. code-block:: python

      DROP TABLE IF EXISTS COACHES;
      CREATE TABLE COACHES(
      ID SERIAL PRIMARY KEY,
      NAME TEXT,
      SURNAME TEXT,
      NATION INT,
      TEAM TEXT);

      ALTER TABLE COACHES ADD CONSTRAINT FK_COACHES_COUNTRIES FOREIGN KEY (NATION) REFERENCES COUNTRIES (ID) ON DELETE SET NULL ON UPDATE CASCADE;

Since *Coaches(Nation)* is referenced from *Countries(Id)* and it is *ON DELETE SET NULL ON UPDATE CASCADE*, whenever a country is deleted, it will be *NULL*

1.3 Referees Table
------------------
* Attributes of the Referees Table.
+---------+--------+-------------+-------------+----------------+
| Name    | Type   | Primary Key | Foreign Key | Auto Increment |
+=========+========+=============+=============+================+
| id      | SERIAL | 1           | 0           | 1              |
+---------+--------+-------------+-------------+----------------+
| name    | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| surname | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+
| league  | INT    | 0           | 1           | 0              |
+---------+--------+-------------+-------------+----------------+
| city    | TEXT   | 0           | 0           | 0              |
+---------+--------+-------------+-------------+----------------+

* *name* holds the name of the referee.
* *surname* holds the surname of the referee.
* *league* describes the level of the referees as int referenced from the league table.
* *city* holds the city that referee is in.


SQL Statement that initializes the Referees Table:
   .. code-block:: python

      DROP TABLE IF EXISTS REFEREES;
      CREATE TABLE REFEREES(
      ID SERIAL PRIMARY KEY,
      NAME TEXT,
      SURNAME TEXT,
      LEAGUE INT,
      CITY TEXT);

      ALTER TABLE REFEREES ADD CONSTRAINT FK_REFEREES_LEAGUES FOREIGN KEY (LEAGUE) REFERENCES LEAGUES   (ID) ON DELETE SET NULL ON UPDATE CASCADE;

Since *Referees(League)* is referenced from *Leagues(Id)* and it is *ON DELETE SET NULL ON UPDATE CASCADE*, whenever a league is deleted, it will be *NULL*

2 TABLE OPERATIONS (Add/Delete/Update/Search)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2.1 Players Table Operations
----------------------------

   .. code-block:: python

       @app.route('/players')
       def players():
          now = datetime.datetime.now()
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          query = """select players.id, players.name, players.surname, players.age, countries.name, players.team, players.field, players.goal from PLAYERS left join countries on players.nation = countries.id;"""
          cursor.execute(query)
          playerListAsTuple = cursor.fetchall()
          playerListAsList = []
          for player in playerListAsTuple:
              playerListAsList.append(list(player))
          cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
          countryListAsTuple = cursor.fetchall()
          connection.close()
          countryListAsList = []
          for country in countryListAsTuple:
              countryListAsList.append(list(country))
          return render_template('players.html', playerList=playerListAsList, current_time=now.ctime(), countryList=countryListAsList)

Above code is the definiton of the players table. First, all columns of players table is selected and added to 'playersListAsTuple'. Since 'Nation' is foreign key referenced to Countries table, it is also selected and added to 'countryListAsTuple'. Then created tuples are passed to 'players.html' file and all players are listed.

* Add
   .. code-block:: python

      @app.route('/addPlayer' , methods=['GET','POST'])
      def addPlayer():
         name = request.form['name']
         surname = request.form['surname']
         age = request.form['age']
         nation = request.form['nation']
         team = request.form['team']
         field = request.form['field']
         goal = request.form['goal']
         connection = psycopg2.connect(app.config['dsn'])
         cursor = connection.cursor()
         cursor.execute("INSERT INTO PLAYERS (name,surname, age, nation, team, field, goal) VALUES (%s,%s, %s, %s, %s, %s, %s)", (name, surname, age, nation, team, field, goal))
         connection.commit()
         connection.close()
         return redirect('/players')
Above code adds a player object to the Database according to entered data.

* Delete
   .. code-block:: python

      @app.route('/deletePlayer' , methods=['POST'])
      def deletePlayer():
         id = request.form['id']
         connection = psycopg2.connect(app.config['dsn'])
         cursor = connection.cursor()
         query = """DELETE FROM PLAYERS WHERE id=""" + id + """;"""
         cursor.execute(query)
         connection.commit()
         connection.close()
         return redirect('/players')
Deletes a player from players table by finding it with its unique id.

* Update
   .. code-block:: python

      @app.route('/updatePlayer' , methods=['POST'])
      def updatePlayer():
      if request.method == 'POST':
           now = datetime.datetime.now()
           connection = psycopg2.connect(app.config['dsn'])
           cursor = connection.cursor()
           id = request.form['id']
           query = """select id, name, surname, age, nation, team, field, goal from players where id='""" + id + """';"""
           cursor.execute(query)
           update = list(cursor.fetchall()[0])
           cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
           countryListAsTuple = cursor.fetchall()
           countryListAsList = []
           for country in countryListAsTuple:
               countryListAsList.append(list(country))
           connection.close()
           return render_template('player_update.html', current_time=now.ctime(), updatedlist=update, countryList=countryListAsList)
Above code first gets the information of desired player to be updated according its unique id and sends it to 'player_update.html' file.

   .. code-block:: python

      @app.route('/update_Player' , methods=['POST'])
      def update_Player():
           id = request.form['id']
           name = request.form['name']
           surname = request.form['surname']
           age = request.form['age']
           nation = request.form['nation']
           team = request.form['team']
           field =request.form['field']
           goal = request.form['goal']
           connection = psycopg2.connect(app.config['dsn'])
           cursor = connection.cursor()
           query = """UPDATE PLAYERS SET NAME='""" + name + """', SURNAME='""" + surname +"""', AGE=""" + age + """,NATION=""" + nation + """,TEAM='""" + team + """', FIELD='""" + field + """', GOAL=""" + goal + """ where ID=""" + id + """;"""
           cursor.execute(query)
           connection.commit()
           connection.close()
           return redirect('/players')
Selected player information is updated and new data is send to the Database.

* Search
   .. code-block:: python

      @app.route('/searchPlayer' , methods=['POST'])
      def searchPlayer():
          if request.method == 'POST':
              search = request.form['search_player']
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query="""SELECT * FROM PLAYERS WHERE (NAME LIKE '%""" + search + """%');"""
              cursor.execute(query)
              playerListAsTuple = cursor.fetchall()
              connection.close()
              playerListAsList = []
              for player in playerListAsTuple:
                  playerListAsList.append(list(player))
              return render_template('player_search.html', playerList=playerListAsList, current_time=now.ctime())
Searches a player object in DB by its name using %LIKE% and returns the matches in a list.

2.2 Coaches Table Operations
----------------------------

   .. code-block:: python

      @app.route('/coaches')
      def coaches():
          now = datetime.datetime.now()
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          query = """select coaches.id, coaches.name, coaches.surname, countries.name, coaches.team from COACHES left join COUNTRIES on coaches.nation = countries.id;"""
          cursor.execute(query)
          coachListAsTuple = cursor.fetchall()
          coachListAsList = []
          for coach in coachListAsTuple:
              coachListAsList.append(list(coach))
          cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
          countryListAsTuple = cursor.fetchall()
          connection.close()
          countryListAsList = []
          for country in countryListAsTuple:
              countryListAsList.append(list(country))

          return render_template('coaches.html', coachList=coachListAsList, current_time=now.ctime(), countryList=countryListAsList)
Above code holds the list of all coaches in DB and display them as a list on *coaches.html* file. First all data of coaches are selected and kept in coachListAsList, then countries are selected and kept in countryListAslist. They are all pass to the hmtl file.

* Add
   .. code-block:: python

      @app.route('/addCoach' , methods=['POST'])
      def addCoach():
          name = request.form['name']
          surname = request.form['surname']
          nation = request.form['nation']
          team = request.form['team']
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          cursor.execute("INSERT INTO COACHES (name,surname, nation, team) VALUES (%s, %s, %s, %s)", (name, surname, nation, team))
          connection.commit()
          connection.close()
          return redirect('/coaches')
Adds a new coach object to the DB.

* Delete
   .. code-block:: python

      @app.route('/deleteCoach' , methods=['POST'])
      def deleteCoach():
          id = request.form['id']
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          query = """DELETE FROM COACHES WHERE id=""" + id + """;"""
          cursor.execute(query)
          connection.commit()
          connection.close()
          return redirect('/coaches')
Deletes a coach from Db using its uniqu id.

* Update
   .. code-block:: python

      @app.route('/updateCoach' , methods=['POST'])
      def updateCoach():
          if request.method == 'POST':
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              id = request.form['id']
              query = """select id, name, surname, nation, team from COACHES where id='""" + id + """';"""
              cursor.execute(query)
              update = list(cursor.fetchall()[0])
              cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
              countryListAsTuple = cursor.fetchall()
              connection.close()
              countryListAsList = []
              for country in countryListAsTuple:
                  countryListAsList.append(list(country))
              return render_template('coach_update.html', current_time=now.ctime(), updatedlist=update, countryList=countryListAsList)
Above code first gets the information of desired coach to be updated according its unique id and sends it to 'coach_update.html' file.

   .. code-block:: python

      @app.route('/update_Coach' , methods=['POST'])
      def update_Coach():
              id = request.form['id']
              name = request.form['name']
              surname = request.form['surname']
              nation = request.form['nation']
              team = request.form['team']
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query = """UPDATE COACHES SET NAME='""" + name + """' ,SURNAME='""" +surname+ """', NATION='""" + nation + """',TEAM='""" + team + """' where ID=""" + id + """;"""
              cursor.execute(query)
              connection.commit()
              connection.close()
              return redirect('/coaches')
Selected coach information is updated and new data is send to the Database.

* Search
   .. code-block:: python

      @app.route('/searchCoach' , methods=['POST'])
      def searchCoach():
          if request.method == 'POST':
              search = request.form['search_coach']
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query="""SELECT * FROM COACHES WHERE (NAME LIKE '%""" + search + """%');"""
              cursor.execute(query)
              coachListAsTuple = cursor.fetchall()
              connection.close()
              coachListAsList = []
              for coach in coachListAsTuple:
                  coachListAsList.append(list(coach))
              return render_template('coach_search.html', coachList=coachListAsList, current_time=now.ctime())
Searches a coach object in DB by its name using %LIKE% and returns the matches in a list.

2.3 Referees Table Operations
-----------------------------

   .. code-block:: python

      @app.route('/referees')
      def referees():
          now = datetime.datetime.now()
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          query = """select referees.id, referees.name, referees.surname, leagues.name, referees.city from REFEREES left join leagues on referees.league = leagues.id;"""
          cursor.execute(query)
          refereeListAsTuple = cursor.fetchall()
          refereeListAsList = []
          for referee in refereeListAsTuple:
              refereeListAsList.append(list(referee))
          cursor.execute("SELECT * FROM LEAGUES ORDER BY NAME;")
          leagueListAsTuple = cursor.fetchall()
          connection.close()
          leagueListAsList = []
          for league in leagueListAsTuple:
              leagueListAsList.append(list(league))
          return render_template('referees.html', refereeList=refereeListAsList, current_time=now.ctime(), leagueList=leagueListAsList)
Lists all referees in the Database. Since *Referees(league)* is foreign key, all leagues are kept in leagueListAsList and sends to *referees.html* file.

* Add
   .. code-block:: python

      @app.route('/addReferee' , methods=['GET','POST'])
      def addReferee():
              name = request.form['name']
              surname = request.form['surname']
              league = request.form['league']
              city = request.form['city']
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              cursor.execute("INSERT INTO REFEREES (name,surname, league, city) VALUES (%s,%s, %s, %s)", (name, surname, league, city))
              connection.commit()
              connection.close()
              return redirect('/referees')
Adds a new referee object to the Db.

* Delete
   .. code-block:: python

      @app.route('/deleteReferee' , methods=['POST'])
      def deleteReferee():
          id = request.form['id']
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          query = """DELETE FROM REFEREES WHERE id=""" + id + """;"""
          cursor.execute(query)
          connection.commit()
          connection.close()
          return redirect('/referees')
Deletes a referee from Db using its uniqu id.

* Update
   .. code-block:: python

      @app.route('/updateReferee' , methods=['POST'])
      def updateReferee():
          if request.method == 'POST':
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              id = request.form['id']
              query = """select id, name, surname, league, city from REFEREES where id='""" + id + """';"""
              cursor.execute(query)
              update = list(cursor.fetchall()[0])
              cursor.execute("SELECT * FROM LEAGUES ORDER BY NAME;")
              leagueListAsTuple = cursor.fetchall()
              connection.close()
              leagueListAsList = []
              for league in leagueListAsTuple:
                  leagueListAsList.append(list(league))
              return render_template('referee_update.html', current_time=now.ctime(), updatedlist=update, leagueList=leagueListAsList)
First gets the information of desired referee to be updated according its unique id and sends it to 'referee_update.html' file.

    .. code-block:: python

      @app.route('/update_Referee' , methods=['POST'])
      def update_Referee():
              id = request.form['id']
              name = request.form['name']
              surname = request.form['surname']
              league= request.form['league']
              city = request.form['city']
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query = """UPDATE REFEREES SET NAME='""" + name + """' ,SURNAME='""" +surname+ """', LEAGUE='""" + league + """',CITY='""" + city + """' where ID=""" + id + """;"""
              cursor.execute(query)
              connection.commit()
              connection.close()
              return redirect('/referees')
Selected referee information is updated and new data is send to the Database.

* Search
   .. code-block:: python

      @app.route('/searchReferee' , methods=['POST'])
      def searchReferee():
          if request.method == 'POST':
              search = request.form['search_referee']
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query="""SELECT * FROM REFEREES WHERE (NAME LIKE '%""" + search + """%');"""
              cursor.execute(query)
              refereeListAsTuple = cursor.fetchall()
              connection.close()
              refereeListAsList = []
              for referee in refereeListAsTuple:
                  refereeListAsList.append(list(referee))
              return render_template('referee_search.html', refereeList=refereeListAsList, current_time=now.ctime())
Searches a referee object in DB by its name using %LIKE% and returns the matches in a list.


