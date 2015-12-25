Parts Implemented by Emin OCAK
==============================
TABLES
~~~~~~
* This part explains how Leagues, Countries and Messages tables are structured and what operations can run on them.

Leagues Table
-------------

.. csv-table:: Leagues Table
      :header: "Name", "Type", "Not Null", "Foreign Key", "Primary Key"
      :widths: 40, 40, 20, 30, 30

      "ID", "SERIAL", 0, 0, 1
      "NAME", "VARCHAR(100)", 1, 0, 0
      "NATION", "INT", 1, 1, 0
      "CLASSIFICATION", "INT", 1, 0, 0

**Sql statement that initialize the leagues table:**

.. code-block:: python

      DROP TABLE IF EXISTS LEAGUES;
      CREATE TABLE LEAGUES(
         ID SERIAL PRIMARY KEY,
         NAME VARCHAR(100) NOT NULL,
         NATION INT NOT NULL REFERENCES COUNTRIES (ID),
         CLASSIFICATION INT NOT NULL
         );

* *NATION* references the *COUNTRIES* table and it is executed by **ON DELETE CASCADE ON UPDATE CASCADE**.

Countries Table
---------------

.. csv-table:: Countries Table
      :header: "Name", "Type", "Not Null", "Foreign Key", "Primary Key"
      :widths: 40, 40, 20, 30, 30

      "ID", "SERIAL", 0, 0, 1
      "NAME", "VARCHAR(50)", 1, 0, 0
      "POPULATION", "FLOAT", 1, 0, 0
      "COORDINATES", "FLOAT", 0, 0, 0

**Sql statement that initialize the countries table:**

.. code-block:: python

      DROP TABLE IF EXISTS COUNTRIES;
      CREATE TABLE COUNTRIES(
         ID SERIAL PRIMARY KEY,
         NAME VARCHAR(50) NOT NULL,
         POPULATION FLOAT NOT NULL,
         COORDINATES FLOAT);

* It does not require any foreign key since it stores independent data.

Messages Table
--------------

.. csv-table:: Messages Table
      :header: "Name", "Type", "Not Null", "Foreign Key", "Primary Key"
      :widths: 40, 40, 20, 30, 30

      "ID", "SERIAL", 0, 0, 1
      "TITLE", "VARCHAR(100)", 1, 0, 0
      "MAIL", "VARCHAR(100)", 0, 0, 0
      "MESSAGE", "FLOAT", 0, 0, 0

**Sql statement that initialize the messages table:**

.. code-block:: python

      DROP TABLE IF EXISTS MESSAGES;
      CREATE TABLE MESSAGES(
         ID SERIAL PRIMARY KEY,
         TITLE VARCHAR(100) NOT NULL,
         MAIL VARCHAR(100),
         MESSAGE TEXT NOT NULL);

* It does not require any foreign key since it stores independent data.

TABLE OPERATIONS
~~~~~~~~~~~~~~~~

Leagues Table
-------------

**List of leagues in leagues table**

.. code-block:: python

      @app.route('/leagues' , methods=['GET', 'POST'])
      def leagues():
        now = datetime.datetime.now()
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("SELECT LEAGUES.ID, COUNTRIES.NAME, LEAGUES.CLASSIFICATION, LEAGUES.NAME FROM LEAGUES JOIN COUNTRIES ON LEAGUES.NATION = COUNTRIES.ID ORDER BY COUNTRIES.NAME;")
        leagueListAsTuple = cursor.fetchall()
        connection.close()
        leagueListAsList = []
        for league in leagueListAsTuple:
            leagueListAsList.append(list(league))
        return render_template('leagues.html', leagueList=leagueListAsList, current_time=now.ctime())

* This method is used for getting all leagues. After running the query, variables are stored in the *"leagueListAsTuple"* via *"fetchall()"* function, respectively. Then it placed into *"leagueListAsList"* individual, and eventually sent to *"leagues.html"* as a parameter.

**add_league()**

.. code-block:: python

      @app.route('/add_league' , methods=['GET', 'POST'])
      def add_league():
          if request.method == 'GET':
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
              countryListAsTuple = cursor.fetchall()
              connection.close()
              countryListAsList = []
              for country in countryListAsTuple:
                  countryListAsList.append(list(country))
              return render_template('add_league.html', current_time=now.ctime(), countryList=countryListAsList)
          else:
              name = request.form['name']
              nation = request.form['nation']
              classification = request.form['classification']
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              cursor.execute("INSERT INTO LEAGUES(NAME, NATION, CLASSIFICATION) VALUES(%s, %s, %s)",(name, nation, classification))
              connection.commit()
              connection.close()
              return redirect('/leagues')

* This method adds a new league to *"Leagues"* table according to user’s inputs by sending sql statement to database. When the **get** method is called, country query is executed to fill the drop-down list. After filling in the required data format, **post** method is called. According to the information in the page *"add_league.html"*, data is received and the insertion process is performed. After all, go to the *"leagues.html"* page.

**delete_league(id)**

.. code-block:: python

      @app.route('/delete_league/<id>', methods=['GET'])
      def delete_league(id):
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          query = """DELETE FROM LEAGUES WHERE ID=""" + id + """;"""
          cursor.execute(query)
          connection.commit()
          connection.close()
          return redirect('/leagues')

* This method deletes a league from database which is chosen by user as sending sql statement to the database. According to the ID number of records are deleted and returns to the *"leagues.html"* page.

**search_league()**

.. code-block:: python

      @app.route('/search_league' , methods=['POST'])
      def search_league():
          if request.method == 'POST':
              connection = psycopg2.connect(app.config['dsn'])
              now = datetime.datetime.now()
              cursor = connection.cursor()
              query="""SELECT LEAGUES.ID, COUNTRIES.NAME, LEAGUES.CLASSIFICATION, LEAGUES.NAME FROM LEAGUES JOIN COUNTRIES ON LEAGUES.NATION = COUNTRIES.ID WHERE LOWER(LEAGUES.NAME) LIKE LOWER('%"""+ request.form['search'] +"""%') ORDER BY COUNTRIES.NAME;"""
              cursor.execute(query)
              leagueListAsTuple = cursor.fetchall()
              connection.close()
              leagueListAsList = []
              for league in leagueListAsTuple:
                  leagueListAsList.append(list(league))
              return render_template('search_league.html', leagueList=leagueListAsList, count=len(leagueListAsList), current_time=now.ctime())

* It works like the *"leagues.html"* page. In addition, it is working with the **%like%** method for the search operation. Here, the characters are always converted to lowercase provided precision. It also again works as *"leagues.html"* page, if it is executed with the  blank search.

**edit_league(id)**

.. code-block:: python

      @app.route('/edit_league/<id>', methods=['GET','POST'])
      def edit_league(id):
          if request.method == 'GET':
              connection = psycopg2.connect(app.config['dsn'])
              now = datetime.datetime.now()
              cursor = connection.cursor()
              query = """SELECT NAME, NATION, CLASSIFICATION FROM LEAGUES WHERE ID=""" + id + """;"""
              cursor.execute(query)
              name, nation, classification = cursor.fetchone()
              cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
              countryListAsTuple = cursor.fetchall()
              connection.close()
              countryListAsList = []
              for country in countryListAsTuple:
                  countryListAsList.append(list(country))
              connection.close()
              return render_template('edit_league.html', current_time=now.ctime(),id=id, name=name , nation=nation, classification=classification, countryList=countryListAsList)

      @app.route('/update_league', methods=['GET','POST'])
      def update_league():
          if request.method == 'POST':
              connection = psycopg2.connect(app.config['dsn'])
              id = request.form['id']
              name = request.form['name']
              nation = request.form['nation']
              classification = request.form['classification']
              cursor = connection.cursor()
              query="""UPDATE LEAGUES SET NAME='"""+name+"""', NATION='"""+nation+"""', CLASSIFICATION="""+classification+""" WHERE ID="""+id+""";"""
              cursor.execute(query)
              connection.commit()
              connection.close()
              return redirect('/leagues')

* With the data will be updated according to the id's, it is gone to "*edit_league.html*" page. Again, a second query is executed for the drop-down list. After completion, data are taken by **post** method to *"update_league"*. Here, after the update is performed, it is gone to the *"leagues.html"* page.

Countries Table
---------------

**List of countries in countries table**

.. code-block:: python

      @app.route('/countries' , methods=['GET', 'POST'])
      def countries():
          now = datetime.datetime.now()
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
          countryListAsTuple = cursor.fetchall()
          connection.close()
          countryListAsList = []
          for country in countryListAsTuple:
              countryListAsList.append(list(country))
          return render_template('countries.html', countryList=countryListAsList, current_time=now.ctime())

* After running the query, variables are stored in the *"countryListAsTuple"* via *"fetchall()"* function, respectively. Then it placed into *"countryListAsList"* individual, and eventually sent to *"countries.html"* as a parameter.

**add_country()**

.. code-block:: python

      @app.route('/add_country' , methods=['GET', 'POST'])
      def add_country():
          if request.method == 'GET':
              now = datetime.datetime.now()
              return render_template('add_country.html', current_time=now.ctime())
          else:
              name = request.form['name']
              population = request.form['population']
              coordinates = request.form['coordinates']
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              cursor.execute("INSERT INTO COUNTRIES(NAME, POPULATION, COORDINATES) VALUES(%s, %s, %s)",(name, population, coordinates))
              connection.commit()
              connection.close()
              return redirect('/countries')

* When the **get** method is called, returns *"add_country.html"*. After filling in the required data format, **post** method is called. According to the information in the page *"add_country.html"*, data is received and the insertion process is performed. After all, go to the *"countries.html"* page.

**delete_country(id)**

.. code-block:: python

      @app.route('/delete_country/<id>', methods=['GET'])
      def delete_country(id):
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          query = """DELETE FROM COUNTRIES WHERE ID=""" + id + """;"""
          cursor.execute(query)
          connection.commit()
          connection.close()
          return redirect('/countries')

* According to the ID number of records are deleted and returns to the *"countries.html"* page.

**search_country()**

.. code-block:: python

      @app.route('/search_country' , methods=['POST'])
      def search_country():
          if request.method == 'POST':
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query="""SELECT * FROM COUNTRIES WHERE LOWER(NAME) LIKE LOWER('%"""+ request.form['search'] +"""%') ORDER BY NAME;"""
              cursor.execute(query)
              countryListAsTuple = cursor.fetchall()
              connection.close()
              countryListAsList = []
              for country in countryListAsTuple:
                  countryListAsList.append(list(country))
              return render_template('search_country.html', countryList=countryListAsList, count=len(countryListAsList), current_time=now.ctime())

* It works like the *"countries.html"* page. In addition, it is working with the **%like%** method for the search operation. Here, the characters are always converted to lowercase provided precision. It also again works as *"countries.html"* page, if it is executed with the  blank search.

**edit_country(id)**

.. code-block:: python

      @app.route('/edit_country/<id>', methods=['GET','POST'])
      def edit_country(id):
          if request.method == 'GET':
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query = """SELECT NAME, POPULATION, COORDINATES FROM COUNTRIES WHERE ID=""" + id + """;"""
              cursor.execute(query)
              name, population, coordinates = cursor.fetchone()
              connection.close()
              return render_template('edit_country.html', current_time=now.ctime(),id=id, name=name , population=population , coordinates=coordinates)

      @app.route('/update_country', methods=['GET','POST'])
      def update_country():
          if request.method == 'POST':
              id = request.form['id']
              name = request.form['name']
              population = request.form['population']
              coordinates = request.form['coordinates']
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query="""UPDATE COUNTRIES SET NAME='"""+name+"""', POPULATION="""+population+""", COORDINATES="""+coordinates+""" WHERE ID="""+id+""";"""
              cursor.execute(query)
              connection.commit()
              connection.close()
              return redirect('/countries')

* With the data will be updated according to the id's, it is gone to "*edit_country.html*" page. Again, a second query is executed for the drop-down list. After completion, data are taken by **post** method to *"update_country"*. Here, after the update is performed, it is gone to the *"countries.html"* page.

Messages Table
--------------

**List of messages in messages table**

.. code-block:: python

      @app.route('/messages' , methods=['GET', 'POST'])
      def messages():
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              cursor.execute("SELECT * FROM MESSAGES ORDER BY ID DESC;")
              messageListAsTuple = cursor.fetchall()
              connection.close()
              messageListAsList = []
              for message in messageListAsTuple:
                  messageListAsList.append(list(message))
              return render_template('messages.html', messageList=messageListAsList, current_time=now.ctime())

* After running the query, variables are stored in the *"messageListAsTuple"* via *"fetchall()"* function, respectively. Then it placed into *"messageListAsList"* individual, and eventually sent to *"messages.html"* as a parameter.

**add_message()**

.. code-block:: python

      @app.route('/add_message' , methods=['POST'])
      def add_message():
              title = request.form['title']
              mail = request.form['mail']
              message = request.form['message']
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              cursor.execute("INSERT INTO MESSAGES(TITLE, MAIL, MESSAGE) VALUES(%s, %s, %s)",(title, mail, message))
              connection.commit()
              connection.close()
              return redirect('/')

* Messages are added using a message board on the home page. After filling in the required data format, **post** method is called. After that, it is gone to the home page.

**delete_message(id)**

.. code-block:: python

      @app.route('/delete_message/<id>', methods=['GET'])
      def delete_message(id):
          connection = psycopg2.connect(app.config['dsn'])
          cursor = connection.cursor()
          query = """DELETE FROM MESSAGES WHERE ID=""" + id + """;"""
          cursor.execute(query)
          connection.commit()
          connection.close()
          return redirect('/messages')

* According to the ID number of records are deleted and returns to the *"messages.html"* page.

**search_message()**

.. code-block:: python

      @app.route('/search_message' , methods=['POST'])
      def search_message():
          if request.method == 'POST':
              connection = psycopg2.connect(app.config['dsn'])
              now = datetime.datetime.now()
              cursor = connection.cursor()
              query="""SELECT * FROM MESSAGES WHERE LOWER(TITLE) LIKE LOWER('%"""+ request.form['search'] +"""%') ORDER BY ID DESC;"""
              cursor.execute(query)
              messageListAsTuple = cursor.fetchall()
              connection.close()
              messageListAsList = []
              for message in messageListAsTuple:
                  messageListAsList.append(list(message))
              return render_template('search_message.html', messageList=messageListAsList, count=len(messageListAsList), current_time=now.ctime())

* It works like the *"messages.html"* page. In addition, it is working with the **%like%** method for the search operation. Here, the characters are always converted to lowercase provided precision. It also again works as *"messages.html"* page, if it is executed with the blank search for title textbox.

**edit_message(id)**

.. code-block:: python

      @app.route('/edit_message/<id>', methods=['GET','POST'])
      def edit_message(id):
          if request.method == 'GET':
              now = datetime.datetime.now()
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query = """SELECT TITLE, MAIL, MESSAGE FROM MESSAGES WHERE ID=""" + id + """;"""
              cursor.execute(query)
              title, mail, message = cursor.fetchone()
              connection.close()
              return render_template('edit_message.html', current_time=now.ctime(),id=id, title=title , mail=mail, message=message)

      @app.route('/update_message', methods=['GET','POST'])
      def update_message():
          if request.method == 'POST':
              id = request.form['id']
              title = request.form['title']
              mail = request.form['mail']
              message = request.form['message']
              connection = psycopg2.connect(app.config['dsn'])
              cursor = connection.cursor()
              query="""UPDATE MESSAGES SET TITLE='"""+title+"""', MAIL='"""+mail+"""', MESSAGE='"""+message+"""' WHERE ID="""+id+""";"""
              cursor.execute(query)
              connection.commit()
              connection.close()
              return redirect('/messages')

* With the data will be updated according to the id's, it is gone to "*edit_message.html*" page. Again, a second query is executed for the drop-down list. After completion, data are taken by **post** method to *"update_message"*. Here, after the update is performed, it is gone to the *"messages.html"* page.

