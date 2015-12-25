1.2.2.5  Parts Implemented by Caghan Caglar
===========================================
1.2.2.5.1  Tables
-----------------
1.2.2.5.1.1  Pool Table
-----------------------
Pool Table consists of 5 attributes.

   .. figure:: pooltable.png

   Pool Table

- **ID**        : New ID values for each Pool tuple

- **NAME**       : Name of the Pool (Stadium)

- **COUNTRY_ID** : Foreign key that references the COUNTRY_ID attribute of the Country Table with "ON DELETE CASCADE ON UPDATE CASCADE" option for Data Integrity

- **CAPACITY**   : Number of seats that Pool (Stadium) has

- **BUILT**      : Built year of the Pool (Stadium)

**Sql statement that initialize the Pool table:**

   .. code-block:: python

   DROP TABLE IF EXISTS POOL;
   CREATE TABLE POOL(NAME VARCHAR(40) NOT NULL, COUNTRY_ID INT,
                      CAPACITY INT NOT NULL, BUILT INT NOT NULL,
                      ID SERIAL PRIMARY KEY);
   ALTER TABLE POOL ADD CONSTRAINT FK_POOL_COUNTRIES FOREIGN KEY (COUNTRY_ID)
               REFERENCES COUNTRIES (ID) ON DELETE CASCADE ON UPDATE CASCADE;

1.2.2.5.1.2  Stats Table
------------------------
Stats Table consists of 6 attributes.

   .. figure:: statstable.png

   Stats Table

- **ID**        : New ID values for each Statistic tuple

- **PLAYER_ID** : Foreign key that references the PLAYER_ID attribute of the Player Table with "ON DELETE CASCADE ON UPDATE CASCADE" option for Data Integrity

- **LEAGUE_ID** : Foreign key that references the LEAGUE_ID attribute of the League Table with "ON DELETE CASCADE ON UPDATE CASCADE" option for Data Integrity

- **GOAL**      : Number of goals that Player scored

- **ASSIST**    : Number of assists that Player made

- **SAVE**      : Number of saves that Player made

**Sql statement that initialize the Stats table:**

   .. code-block:: python

   DROP TABLE IF EXISTS STATS;
   CREATE TABLE STATS(PLAYER_ID INT,LEAGUE_ID INT, GOAL INT DEFAULT 0,
                            ASSIST INT DEFAULT 0,SAVE INT DEFAULT 0,
                            ID SERIAL PRIMARY KEY);
   ALTER TABLE STATS ADD CONSTRAINT FK_STATS_PLAYERS FOREIGN KEY (PLAYER_ID)
               REFERENCES PLAYERS (ID) ON DELETE CASCADE ON UPDATE CASCADE;
   ALTER TABLE STATS ADD CONSTRAINT FK_STATS_LEAGUES FOREIGN KEY (LEAGUE_ID)
               REFERENCES LEAGUES (ID) ON DELETE CASCADE ON UPDATE CASCADE;

1.2.2.5.2   Table Operations
============================
1.2.2.5.2.1 Pool Page
---------------------
There are 2 'Post' method possibilities for Pool page. Since this page initially lists the pools, update and delete options are available at the beginning. These options are coded in the pools.html file with values 'deletePoolbyid' and 'updatePoolbyid'. If one of these values are sended in the form necessary sql querry is done properly. If these values are not in form value then it is obvious that 'Get' method is used, so all datas of the pools in database is fetched and sended to the pools.html file for listing operation.
This kind of implementation of 'Get' method prevents the failures for the case of Update and Delete button clicks without any radio option selected.

   .. code-block:: python

   @app.route('/Pools', methods=['GET', 'POST'])
   def pool_list():
       if 'deletePoolbyid' in request.form:
           try:
               connection = psycopg2.connect(app.config['dsn'])
               cursor=connection.cursor()
               poolid = request.form['deletePoolbyid']
               query = """delete from pool where id=""" + poolid + """;"""
               cursor.execute(query)
               connection.commit()
               connection.close()
               return redirect('/Pools')
           except :
               return redirect('/Pools')
       elif 'updatePoolbyid' in request.form:
           try:
               connection = psycopg2.connect(app.config['dsn'])
               cursor=connection.cursor()
               poolid = request.form['updatePoolbyid']
               query = """select pool.name, countries.name, pool.capacity, pool.built,
                  pool.id from pool join countries on pool.country_id=countries.id
                  where pool.id=""" + poolid + """;"""
               cursor.execute(query)
               poolupdated = list(cursor.fetchall()[0])
               query = """ SELECT ID,NAME FROM COUNTRIES ORDER BY NAME;"""
               cursor.execute(query)
               countryfetch = cursor.fetchall()
               connection.close()
               countryListForm = []
               for country in countryfetch:
                   countryListForm.append(list(country))
               now = datetime.datetime.now()
               return render_template('pool_update.html', current_time=now.ctime(),
                  element=poolupdated,countryList=countryListForm)
           except :
               return redirect('/Pools')
       else:
           try:
               connection = psycopg2.connect(app.config['dsn'])
               cursor=connection.cursor()
               query = """select pool.name, countries.name, pool.capacity, pool.built,
                  pool.id from pool join countries on pool.country_id=countries.id;"""
               cursor.execute(query)
               poolfetch = cursor.fetchall()
               connection.close()
               PoolListForm = []
               for pool in poolfetch:
                   PoolListForm.append(list(pool))
               now = datetime.datetime.now()
               return render_template('pools.html', current_time=now.ctime(), list=PoolListForm)
           except :
               return redirect('/Pools')

Search option in Pool page is implemented by making a query by taking keyword value within the search textbox as name attribute of the Pools. In order to prevent whole database listing of search with empty keyword is prevented by the control of the length of the keyword. After a succesful query, Pool page is rendered with the name constrainted datas in the database.

   .. code-block:: python

   @app.route('/SearchPool' , methods=['POST'])
   def pool_search():
       try:
           connection = psycopg2.connect(app.config['dsn'])
           cursor=connection.cursor()
           PoolListForm = []
           now = datetime.datetime.now()
           name = request.form['searchbyname']
           if len(name)==0:
               return render_template('pools.html', current_time=now.ctime(), list=PoolListForm)
           query = """select pool.name, countries.name, pool.capacity, pool.built, pool.id
            from pool join countries on pool.country_id=countries.id
               where (pool.name like '%""" + name + """%');"""
           cursor.execute(query)
           poolfetch = cursor.fetchall()
           connection.close()
           for pool in poolfetch:
               PoolListForm.append(list(pool))
           return render_template('pools.html', current_time=now.ctime(), list=PoolListForm)
       except :
           return redirect('/Pools')

At Add Pool page, country list is fetched from database and provided to user as selection option. After the input entering process of user is finished posted form values in html file are assigned to variables and proper sql query is made with these variables. Since try-catch blocks are used wrong queries are prevented and page is redirected if necessary.

   .. code-block:: python

   @app.route('/AddPool', methods=['GET', 'POST'])
   def pool_edit():
     if request.method == 'GET':
         try:
             connection = psycopg2.connect(app.config['dsn'])
             cursor=connection.cursor()
             query = """ SELECT ID,NAME FROM COUNTRIES ORDER BY NAME;"""
             cursor.execute(query)
             countryfetch = cursor.fetchall()
             connection.close()
             countryListForm = []
             for country in countryfetch:
                 countryListForm.append(list(country))
             now = datetime.datetime.now()
             return render_template('pool_edit.html', current_time=now.ctime(),
               countryList=countryListForm)
         except :
             return redirect('/Pools')
     else:
         try:
             connection = psycopg2.connect(app.config['dsn'])
             cursor=connection.cursor()
             name = request.form['name']
             countryid = request.form['countryid']
             capacity = request.form['capacity']
             built = request.form['built']
             query = """insert into pool values('""" + name + """',""" + countryid + """,
               """ + capacity + """,""" + built + """);"""
             cursor.execute(query)
             connection.commit()
             connection.close()
             return redirect('/Pools')
         except:
             return redirect('/Pools')

At Update Pool page, html design is in same form as Pool Adding page except this page takes the attribute values of the tuple that will be updated and fills the necessary parts automatically for making this page easy o use for user. When the form data is posted to this function, it makes an update query with the provided form data.

   .. code-block:: python

   @app.route('/UpdatePool', methods=['POST'])
   def pool_update():
       try:
           connection = psycopg2.connect(app.config['dsn'])
           cursor=connection.cursor()
           name = request.form['name']
           countryid = request.form['countryid']
           capacity = request.form['capacity']
           built = request.form['built']
           poolid=request.form['poolid']
           query = """update pool set name='""" + name + """',country_id=""" + countryid +
            """,capacity=""" + capacity + """,built=""" + built + """
            where id=""" + poolid + """;"""
           cursor.execute(query)
           connection.commit()
           connection.close()
           return redirect('/Pools')
       except:
           return redirect('/Pools')

1.2.2.5.2.2 Statistic Page
--------------------------
Statistics page initialy takes league lists from league table for selection option in 'statistics.html' file. After the 2 selection is made by user, these values posted to the same page. Values at the html file are assigned to the variables for sql queries from the join of Stats and Players tables. Players that satisfies selection constraints listed according to the stat type (goal,assist or save) in decreasing order.
Delete and update operations serves as almost same way as described in the Pool page.

   .. code-block:: python

   @app.route('/Statistic',methods=['GET', 'POST'])
   def statistics():
           if 'deletestatbyid' in request.form:
               try:
                   connection = psycopg2.connect(app.config['dsn'])
                   cursor=connection.cursor()
                   statid = request.form['deletestatbyid']
                   query = """delete from stats where id=""" + statid + """;"""
                   cursor.execute(query)
                   connection.commit()
                   connection.close()
                   return redirect('/Statistic')
               except :
                   return redirect('/Statistic')
           elif 'updatestatbyid' in request.form:
               try:
                   connection = psycopg2.connect(app.config['dsn'])
                   cursor=connection.cursor()
                   statid = request.form['updatestatbyid']
                   query = """select players.name, players.surname, players.team, stats.goal, stats.assist, stats.save, stats.id from stats join players on players.id=stats.player_id where stats.id="""+statid+""";"""
                   cursor.execute(query)
                   statupdated = list(cursor.fetchall()[0])
                   connection.close()
                   now = datetime.datetime.now()
                   return render_template('stat_update.html', current_time=now.ctime(), element=statupdated)
               except :
                   return redirect('/Statistic')
           elif 'stattype' in request.form:
               try:
                   connection = psycopg2.connect(app.config['dsn'])
                   cursor=connection.cursor()
                   league=request.form['league']
                   stattype=request.form['stattype']
                   query = """select players.name, players.surname, players.team, stats.goal, stats.assist, stats.save, stats.id from stats join players on players.id=stats.player_id where stats.league_id="""+league+""" order by """+stattype+""" desc;"""
                   cursor.execute(query)
                   statsfetch = cursor.fetchall()
                   connection.close()
                   StatsListForm = []
                   for stats in statsfetch:
                       StatsListForm.append(list(stats))
                   leagueListForm = []
                   now = datetime.datetime.now()
                   return render_template('statistics.html', current_time=now.ctime(), list=StatsListForm,leagueList=leagueListForm)
               except :
                   return redirect('/Statistic')
           else:
               try:
                   connection = psycopg2.connect(app.config['dsn'])
                   cursor=connection.cursor()
                   query = """ SELECT ID,NAME FROM LEAGUES ORDER BY NAME;"""
                   cursor.execute(query)
                   leaguesfetch = cursor.fetchall()
                   connection.close()
                   StatsListForm = []
                   leagueListForm = []
                   for league in leaguesfetch:
                       leagueListForm.append(list(league))
                   now = datetime.datetime.now()
                   return render_template('statistics.html', current_time=now.ctime(), list=StatsListForm,leagueList=leagueListForm)
               except :
                   return redirect('/Statistic')

Search option in Statistic page is implemented by making a query by taking keyword value within the search textbox
as name attribute of the Player. In order to prevent whole database listing of search with empty keyword is pre-
vented by the control of the length of the keyword. After a succesful query, Statistic page is rendered with the name
constrainted datas in the database.

   .. code-block:: python

   @app.route('/SearchStat' , methods=['POST'])
   def stat_search():
       try:
           connection = psycopg2.connect(app.config['dsn'])
           cursor=connection.cursor()
           name = request.form['searchbyname']
           if len(name)==0:
               return redirect('/Statistic')
           query = """select players.name, players.surname, players.team, stats.goal, stats.assist, stats.save, stats.id from stats join players on players.id=stats.player_id where (players.name like '%""" + name + """%');"""
           cursor.execute(query)
           statfetch = cursor.fetchall()
           connection.close()
           StatListForm = []
           for stat in statfetch:
               StatListForm.append(list(stat))
           now = datetime.datetime.now()
           return render_template('statistics.html', current_time=now.ctime(), list=StatListForm)

       except :
           return redirect('/Statistic')

At Update Statistic page, html design is in same form as Statistic Adding page except this page takes the attribute values
of the tuple that will be updated and fills the necessary parts automatically for making this page easy o use for
user. When the form data is posted to this function, it makes an update query with the provided form data.

   .. code-block:: python

   @app.route('/UpdateStats', methods=['GET', 'POST'])
   def stat_update():
           if request.method == 'GET':
               now = datetime.datetime.now()
               return render_template('stat_update.html', current_time=now.ctime())
           else:
               try:
                   connection = psycopg2.connect(app.config['dsn'])
                   cursor=connection.cursor()
                   goal = request.form['goal']
                   assist = request.form['assist']
                   save = request.form['save']
                   statid=request.form['updatebyid']
                   query = """update stats set goal=""" + goal + """,assist=""" + assist + """,save=""" + save + """ where id=""" + statid + """;"""
                   cursor.execute(query)
                   connection.commit()
                   connection.close()
                   return redirect('/Statistic')
               except :
                   return redirect('/Statistic')

At Add Statistic page, country list is fetched from database and provided to user as selection option. After the input
entering process of user is finished posted form values in html file are assigned to variables and proper sql query
is made with these variables. Since try-catch blocks are used wrong queries are prevented and page is redirected
if necessary.

   .. code-block:: python

   @app.route('/AddStat', methods=['GET', 'POST'])
   def stat_add():
           if request.method == 'GET':
               try:
                   connection = psycopg2.connect(app.config['dsn'])
                   cursor=connection.cursor()
                   query = """ SELECT ID,NAME,SURNAME,TEAM FROM PLAYERS ORDER BY NAME;"""
                   cursor.execute(query)
                   playersfetch = cursor.fetchall()
                   playerListForm = []
                   for player in playersfetch:
                       playerListForm.append(list(player))
                   query = """ SELECT ID,NAME FROM LEAGUES ORDER BY NAME;"""
                   cursor.execute(query)
                   leaguesfetch = cursor.fetchall()
                   connection.close()
                   leagueListForm = []
                   for league in leaguesfetch:
                       leagueListForm.append(list(league))
                   now = datetime.datetime.now()
                   return render_template('stat_add.html', current_time=now.ctime(),playerList=playerListForm,leagueList=leagueListForm)
               except:
                   return redirect('/Statistic')
           else:
               try:
                   connection = psycopg2.connect(app.config['dsn'])
                   cursor=connection.cursor()
                   playerid=request.form['playerid']
                   leagueid=request.form['leagueid']
                   goal = request.form['goal']
                   assist = request.form['assist']
                   save = request.form['save']
                   query = """insert into stats values(""" + playerid + """,""" + leagueid + """,""" + goal + """,""" + assist + """,""" + save +""");"""
                   cursor.execute(query)
                   connection.commit()
                   connection.close()
                   return redirect('/Statistic')
               except :
                    return redirect('/Statistic')

