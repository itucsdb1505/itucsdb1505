import datetime
import psycopg2
import os
import json
import re
import sys
import hashlib


from flask import Flask, request, redirect, render_template, url_for
from flask.ext.login import login_required, LoginManager, UserMixin, login_user, logout_user, AnonymousUserMixin
from DataBaseSetup import *


app = Flask(__name__)

class AnonymousUser(AnonymousUserMixin):
    pass

login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUser

dataBaseSetup = DataBaseSetup()


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""SELECT USERS.NAME, USERS.AGE, USERS.EMAIL, USERS.PASSWORD, USERS.AUTH, USERS.COUNTRY_ID FROM USERS WHERE ID = """ + str(id) + """;""")
        self.name, self.age, self.email, self.password, self.auth, self.country_id =  cursor.fetchone()
        connection.close()

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def get_auth(self):
        return self.auth

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@login_manager.user_loader
def load_user(user_id):
    return User(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_message = ""
    now = datetime.datetime.now()
    if request.method == 'POST':
        email = request.form['email']

        m = hashlib.md5()
        m.update(request.form['password'].encode('utf-8'))
        password = m.hexdigest()

        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""select id, password from USERS WHERE email = '""" + email + """';""")
        id,db_password = cursor.fetchone()
        connection.close()



        if db_password == password:
            user = load_user(id)
            login_user(user)
            return redirect(url_for("home"))
        login_message = "Wrong Credentials ! Please try again..."
    return render_template('login.html', current_time=now.ctime(), login_message = login_message )

import hashlib
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/')
def home():
    now = datetime.datetime.now()

    return render_template('home.html', current_time=now.ctime())



@app.route('/userManagement', methods=['GET', 'POST'])
@login_required
def userManagement():

    now = datetime.datetime.now()
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = ""
    search = ""
    if request.method != 'GET':
        search = request.form['search']
    if search != "":
        query = """select users.name, users.age, users.email, users.password, users.auth, countries.name from USERS join countries on users.country_id = countries.id where users.name like '""" + search + """%';"""
    else:
        query = """select users.name, users.age, users.email, users.password, users.auth, countries.name from USERS join countries on users.country_id = countries.id;"""
    cursor.execute(query)
    userListAsTuple = cursor.fetchall()
    userListAsList = []
    for user in userListAsTuple:
        userListAsList.append(list(user))

    query = """SELECT * FROM COUNTRIES;"""
    cursor.execute(query)
    countriesAsTuple = cursor.fetchall()
    connection.close()
    countriesAsList = []
    for country in countriesAsTuple:
        countriesAsList.append(list(country))

    return render_template('userManagement.html', userList=userListAsList, user4Update=None, current_time=now.ctime(), countries = countriesAsList)

@app.route('/addUser' , methods=['POST'])
def addUser():
    errors = []
    name = request.form['name']
    if name is "":
        errors.append(["Name is empty."])
    age = request.form['age']
    if age is "":
        errors.append(["Age is empty."])
    email = request.form['email']
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append(["Email is not valid."])
    auth = request.form['auth']
    if auth != 'u' or auth != 'm' or auth != 'a':
        errors.append(["Auth should be one of u,m or a "])
    m = hashlib.md5()
    m.update(request.form['password'].encode('utf-8'))
    password = m.hexdigest()

    countryid = request.form['country']

    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """INSERT INTO USERS(NAME, AGE, EMAIL, PASSWORD, AUTH, COUNTRY_ID) values('""" + name + """','""" + age + """','""" + email + """','""" + password + """','""" + auth + """','""" + countryid + """');"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/userManagement')

@app.route('/userUpdate', methods=['POST'])
def userUpdate():
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']
    auth = request.form['auth']
    countryid = request.form['country']
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    password = request.form['password']
    if password == "":
        query = """UPDATE users SET name='""" + name + """',age='""" + age + """',email='""" + email + """',auth='""" + auth + """', country_id='""" + countryid + """' WHERE email='""" + email + """';"""
    else:
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        password = m.hexdigest()
        query = """UPDATE users SET name='""" + name + """',age='""" + age + """',email='""" + email + """',password='""" + password + """',auth='""" + auth + """', country_id='""" + countryid + """' WHERE email='""" + email + """';"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/userManagement')

@app.route('/updateUser', methods=['POST'])
def updateUser():
    now = datetime.datetime.now()
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    email = request.form['email']
    query = """select users.name, users.age, users.email, users.auth, countries.name from USERS join countries on users.country_id = countries.id where email='""" + email + """';"""
    cursor.execute(query)
    user4Update = list(cursor.fetchall()[0])
    cursor.execute("""select users.name, users.age, users.email, users.password, users.auth, countries.name from USERS join countries on users.country_id = countries.id;""")
    userListAsTuple = cursor.fetchall()
    query = """SELECT * FROM COUNTRIES;"""
    cursor.execute(query)
    countriesAsTuple = cursor.fetchall()
    connection.close()
    userListAsList = []
    for user in userListAsTuple:
        userListAsList.append(list(user))
    return render_template('userManagement.html', userList=userListAsList, user4Update=user4Update, current_time=now.ctime(), countries = countriesAsTuple)

@app.route('/deleteUser' , methods=['POST'])
def deleteUser():
    email = request.form['email']
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """DELETE FROM USERS WHERE email='""" + email + """';"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/userManagement')


@app.route('/register' , methods=['POST'])
def register():
    errors = []
    name = request.form['name']
    if name is "":
        errors.append(["Name is empty."])
    age = request.form['age']
    if age is "":
        errors.append(["Age is empty."])
    try:
        datetime.datetime.strptime(age, '%Y-%m-%d')
    except ValueError:
        errors.append(["Age is wrong it should be like yyyy-mm-dd ."])
    email = request.form['email']
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append(["Email is not valid."])
    countryid = request.form['country']
    passwordFirst = request.form['passwordFirst']
    if passwordFirst is "":
        errors.append(["Password is empty."])
    passwordSecond = request.form['passwordSecond']
    if passwordSecond is "":
        errors.append(["Check password is empty."])
    if passwordFirst != passwordSecond:
        errors.append(["Passwords are not same."])
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """SELECT EMAIL FROM USERS WHERE EMAIL = '""" + email + """';"""
    cursor.execute(query)
    checkMail = None
    checkMail = cursor.fetchone()
    if checkMail != None:
        errors.append(["User exists. Please try another email."])


    if not errors:

        m = hashlib.md5()
        m.update(passwordFirst.encode('utf-8'))
        password = m.hexdigest()
        query = """INSERT INTO USERS(NAME, AGE, EMAIL, PASSWORD, AUTH, COUNTRY_ID) values('""" + name + """','""" + age + """','""" + email + """','""" + password + """','u','""" + countryid + """');"""
        cursor.execute(query)
        connection.commit()
        connection.close()
        return redirect('/login')
    else:
        return registerPage(errors)

@app.route('/registerPage')
def registerPage(errors=None):
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """SELECT * FROM COUNTRIES;"""
    cursor.execute(query)
    countriesAsTuple = cursor.fetchall()
    connection.close()
    countriesAsList = []
    for country in countriesAsTuple:
        countriesAsList.append(list(country))
    return render_template('register.html', countries = countriesAsList, errors=errors)


@app.route('/newsManagement', methods=['GET', 'POST'])
@login_required
def newsManagement():

    now = datetime.datetime.now()
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = ""
    search = ""
    if request.method != 'GET':
        search = request.form['search']
    if search != "":
        query = """select news.title, news.content, users.name, news.id from news join users on news.user_id = users.id where news.title like '%""" + search + """%';"""
    else:
        query = """select news.title, news.content, users.name, news.id from news join users on news.user_id = users.id;"""
    cursor.execute(query)
    newsListAsTuple = cursor.fetchall()
    newsListAsList = []
    for news in newsListAsTuple:
        newsListAsList.append(list(news))
    query = """SELECT * FROM USERS;"""
    cursor.execute(query)
    usersAsTuple = cursor.fetchall()
    connection.close()
    usersAsList = []
    for user in usersAsTuple:
        usersAsList.append(list(user))

    return render_template('newsManagement.html', newsList=newsListAsList, news4Update=None, current_time=now.ctime(), users=usersAsList)

@app.route('/addNews' , methods=['POST'])
def addNews():
    errors = []
    name = request.form['title']
    if name is "":
        errors.append(["Title is empty."])
    age = request.form['content']
    if age is "":
        errors.append(["Content is empty."])

    email = request.form['email']
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append(["Email is not valid."])
    auth = request.form['auth']

    m = hashlib.md5()
    m.update(request.form['password'].encode('utf-8'))
    password = m.hexdigest()

    countryid = request.form['country']
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """INSERT INTO USERS(NAME, AGE, EMAIL, PASSWORD, AUTH, COUNTRY_ID) values('""" + name + """','""" + age + """','""" + email + """','""" + password + """','""" + auth + """','""" + countryid + """');"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/newsManagement')

@app.route('/newsUpdate', methods=['POST'])
def newsUpdate():
    id = request.form['id']
    title = request.form['title']
    content = request.form['content']
    user = request.form['author']
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """SELECT id from users where name='""" + user + """';"""
    cursor.execute(query)
    user_id = list(cursor.fetchone())
    query = """UPDATE news SET title='""" + title + """', content='""" + content + """', user_id=""" + str(user_id[0]) + """ WHERE id='""" + id + """';"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/newsManagement')

@app.route('/updateNews', methods=['POST'])
def updateNews():
    now = datetime.datetime.now()
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    id = request.form['id']
    query = """select news.id, news.title, news.content, users.name, news.id from news join users on news.user_id = users.id where news.id ='""" + id + """';"""
    cursor.execute(query)
    news4Update = list(cursor.fetchall()[0])
    cursor.execute("""select news.title, news.content, users.name, news.id from news join users on news.user_id = users.id;""")
    newsListAsTuple = cursor.fetchall()
    query = """SELECT * FROM USERS;"""
    cursor.execute(query)
    usersAsTuple = cursor.fetchall()
    connection.close()
    newsListAsList = []
    for news in newsListAsTuple:
        newsListAsList.append(list(news))
    return render_template('newsManagement.html', newsList=newsListAsList, news4Update=news4Update, current_time=now.ctime(), users = usersAsTuple)

@app.route('/deleteNews' , methods=['POST'])
def deleteNews():
    id = request.form['id']
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """DELETE FROM NEWS WHERE id='""" + id + """';"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/newsManagement')


@app.route('/news')
def news():
    now = datetime.datetime.now()
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """select news.title, news.content, users.name, news.id from news join users on news.user_id = users.id;"""
    cursor.execute(query)
    newsListAsTuple = cursor.fetchall()
    newsListAsList = []
    for news in newsListAsTuple:
        newsListAsList.append(list(news))
    query = """SELECT * FROM USERS;"""
    cursor.execute(query)
    usersAsTuple = cursor.fetchall()
    connection.close()
    return render_template('news.html', current_time=now.ctime(), newsList=newsListAsList)

@app.route('/initiateDB')
def initiateDB():
    dataBaseSetup.initiateDataBase(app)
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""select * from test;""")
    now = datetime.datetime.now()
    data=cursor.fetchall()
    connection.close()
    return render_template('initiateDB.html', current_time=now.ctime(), data=data)

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
                query = """select pool.name, countries.name, pool.capacity, pool.built, pool.id from pool join countries on pool.country_id=countries.id where pool.id=""" + poolid + """;"""
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
                return render_template('pool_update.html', current_time=now.ctime(), element=poolupdated,countryList=countryListForm)
            except :
                return redirect('/Pools')
        else:
            try:
                connection = psycopg2.connect(app.config['dsn'])
                cursor=connection.cursor()
                query = """select pool.name, countries.name, pool.capacity, pool.built, pool.id from pool join countries on pool.country_id=countries.id;"""
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
                return render_template('pool_edit.html', current_time=now.ctime(),countryList=countryListForm)
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
                query = """insert into pool values('""" + name + """',""" + countryid + """,""" + capacity + """,""" + built + """);"""
                cursor.execute(query)
                connection.commit()
                connection.close()
                return redirect('/Pools')
            except:
                return redirect('/Pools')


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
        query = """select pool.name, countries.name, pool.capacity, pool.built, pool.id from pool join countries on pool.country_id=countries.id where (pool.name like '%""" + name + """%');"""
        cursor.execute(query)
        poolfetch = cursor.fetchall()
        connection.close()
        for pool in poolfetch:
            PoolListForm.append(list(pool))
        return render_template('pools.html', current_time=now.ctime(), list=PoolListForm)
    except :
        return redirect('/Pools')


@app.route('/UpdatePool', methods=['GET','POST'])
def pool_update():
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('pool_update.html', current_time=now.ctime())
    else:
        try:
            connection = psycopg2.connect(app.config['dsn'])
            cursor=connection.cursor()
            name = request.form['name']
            countryid = request.form['countryid']
            capacity = request.form['capacity']
            built = request.form['built']
            poolid=request.form['poolid']
            query = """update pool set name='""" + name + """',country_id=""" + countryid + """,capacity=""" + capacity + """,built=""" + built + """ where id=""" + poolid + """;"""
            cursor.execute(query)
            connection.commit()
            connection.close()
            return redirect('/Pools')
        except:
            return redirect('/Pools')

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

@app.route('/delete_country/<id>', methods=['GET'])
def delete_country(id):
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """DELETE FROM COUNTRIES WHERE ID=""" + id + """;"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/countries')

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

@app.route('/delete_league/<id>', methods=['GET'])
def delete_league(id):
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """DELETE FROM LEAGUES WHERE ID=""" + id + """;"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/leagues')

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

@app.route('/delete_message/<id>', methods=['GET'])
def delete_message(id):
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """DELETE FROM MESSAGES WHERE ID=""" + id + """;"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/messages')

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


#*************************************************************************


@app.route('/teams')
def teams():
    now = datetime.datetime.now()
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("select teams.id, teams.name, teams.foundation_year, teams.colours, leagues.name,countries.name from TEAMS left join LEAGUES on teams.league = leagues.id left join COUNTRIES on leagues.nation = countries.id;")
    teamListAsTuple = cursor.fetchall()
    teamListAsList = []
    for team in teamListAsTuple:
        teamListAsList.append(list(team))

    cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
    countryListAsTuple = cursor.fetchall()
    countryListAsList = []
    for country in countryListAsTuple:
        countryListAsList.append(list(country))

    cursor.execute("SELECT * FROM LEAGUES ORDER BY NAME;")
    leagueListAsTuple = cursor.fetchall()
    leagueListAsList = []
    for league in leagueListAsTuple:
        leagueListAsList.append(list(league))
        connection.close()
    return render_template('teams.html', teamList=teamListAsList, current_time=now.ctime(), countryList=countryListAsList, leagueList=leagueListAsList)

@app.route('/addTeam' , methods=['GET','POST'])
def addTeam():
        name = request.form['name']
        foundation_year = request.form['foundation_year']
        colours = request.form['colours']
        league = request.form['league']
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        query="""SELECT COUNTRIES.ID FROM COUNTRIES JOIN LEAGUES ON COUNTRIES.ID=LEAGUES.NATION WHERE LEAGUES.ID="""+league+""";"""
        cursor.execute(query)
        country = cursor.fetchone()
        cursor.execute("INSERT INTO TEAMS(NAME, FOUNDATION_YEAR, COLOURS, LEAGUE, COUNTRY) VALUES (%s, %s, %s, %s, %s)", (name, foundation_year, colours, league, country))
        connection.commit()
        connection.close()
        return redirect('/teams')


@app.route('/deleteTeam' , methods=['POST'])
def deleteTeam():
    id = request.form['id']
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """DELETE FROM TEAMS WHERE id=""" + id + """;"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect('/teams')

@app.route('/edit_Team' , methods=['POST'])
def edit_Team():
    if request.method == 'POST':
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        id = request.form['id']
        name=request.form['name']
        foundation_year=request.form['foundation_year']
        colours=request.form['colours']
        league=request.form['league']
        country=request.form['country']
        query = """update teams set NAME='"""+name+"""', FOUNDATION_YEAR="""+foundation_year+""", COLOURS='"""+colours+"""', LEAGUE="""+league+""", COUNTRY="""+country+"""  where id=""" + id + """;"""
        cursor.execute(query)
        connection.commit()
        connection.close()
        return redirect('/teams')

@app.route('/update_Team' , methods=['POST'])
def update_Team():
   if request.method == 'POST':
        now = datetime.datetime.now()
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        id = request.form['id']
        query = """select * from teams where id='""" + id + """';"""
        cursor.execute(query)
        update = list(cursor.fetchall()[0])
        cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
        countryListAsTuple = cursor.fetchall()
        countryListAsList = []
        for country in countryListAsTuple:
            countryListAsList.append(list(country))

        cursor.execute("SELECT * FROM LEAGUES ORDER BY NAME;")
        leagueListAsTuple = cursor.fetchall()
        leagueListAsList = []
        for league in leagueListAsTuple:
            leagueListAsList.append(list(league))

        connection.close()
        return render_template('team_update.html', current_time=now.ctime(), updatedlist=update, countryList=countryListAsList, leagueList=leagueListAsList)

@app.route('/searchTeam' , methods=['POST'])
def searchTeam():
    if request.method == 'POST':
        search = request.form['search_team']
        now = datetime.datetime.now()
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        query="""SELECT * FROM TEAMS WHERE (NAME LIKE '%""" + search + """%');"""
        cursor.execute(query)
        teamListAsTuple = cursor.fetchall()
        teamListAsList = []
        for team in teamListAsTuple:
            teamListAsList.append(list(team))

            connection.close()
        return render_template('team_search.html', teamList=teamListAsList, current_time=now.ctime())

@app.route('/matches')
def matches():
        now = datetime.datetime.now()
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("select matches.id, matches.home, matches.away, matches.referee, leagues.name from MATCHES left join LEAGUES on matches.league = leagues.id;")
        matchesListAsTuple = cursor.fetchall()
        matchesListAsList = []
        for matches in matchesListAsTuple:
            matchesListAsList.append(list(matches))

        cursor.execute("SELECT * FROM LEAGUES ORDER BY NAME;")
        leagueListAsTuple = cursor.fetchall()
        leagueListAsList = []
        for league in leagueListAsTuple:
            leagueListAsList.append(list(league))
            connection.close()
        return render_template('matches.html', matchesList=matchesListAsList, current_time=now.ctime(), leagueList=leagueListAsList)


@app.route('/addMatches' , methods=['POST'])
def addMatches():
    home = request.form['home']
    away = request.form['away']
    referee = request.form['referee']
    league = request.form['league']
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("INSERT INTO MATCHES (home, away, referee, league) VALUES (%s, %s, %s, %s)", (home, away, referee, league))
    connection.commit()
    connection.close()
    return redirect('/matches')

@app.route('/deleteMatches' , methods=['POST'])
def deleteMatches():
        id = request.form['id']
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        query = """DELETE FROM MATCHES WHERE id=""" + id + """;"""
        cursor.execute(query)
        connection.commit()
        connection.close()
        return redirect('/matches')

@app.route('/edit_Matches' , methods=['POST'])
def edit_Matches():
        if request.method == 'POST':
            connection = psycopg2.connect(app.config['dsn'])
            cursor = connection.cursor()
            id = request.form['id']
            home=request.form['home']
            away=request.form['away']
            referee=request.form['referee']
            league=request.form['league']
            query = """update matches set HOME='"""+home+"""', AWAY='"""+away+"""', REFEREE='"""+referee+"""', LEAGUE="""+league+"""  where id=""" + id + """;"""
            cursor.execute(query)
            connection.commit()
            connection.close()
            return redirect('/matches')

@app.route('/update_Matches' , methods=['POST'])
def update_Matches():
        now = datetime.datetime.now()
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        id = request.form['id']
        query = """select * from matches where id='""" + id + """';"""
        cursor.execute(query)
        update = list(cursor.fetchall()[0])
        cursor.execute("SELECT * FROM LEAGUES ORDER BY NAME;")
        leagueListAsTuple = cursor.fetchall()
        leagueListAsList = []
        for league in leagueListAsTuple:
            leagueListAsList.append(list(league))

        connection.close()
        return render_template('matches_update.html', current_time=now.ctime(), updatedlist=update, leagueList=leagueListAsList)


@app.route('/searchMatches' , methods=['POST'])
def searchMatches():
        if request.method == 'POST':
            search = request.form['search_matches']
            now = datetime.datetime.now()
            connection = psycopg2.connect(app.config['dsn'])
            cursor = connection.cursor()
            query="""SELECT * FROM MATCHES WHERE (HOME LIKE '%""" + search + """%');"""
            cursor.execute(query)
            matchesListAsTuple = cursor.fetchall()
            connection.close()
            matchesListAsList = []
            for matches in matchesListAsTuple:
                matchesListAsList.append(list(matches))

            return render_template('matches_search.html', matchesList=matchesListAsList, current_time=now.ctime())

@app.route('/competition')
def competition():
        now = datetime.datetime.now()
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM COMPETITION;")
        competitionListAsTuple = cursor.fetchall()
        competitionListAsList = []
        for competition in competitionListAsTuple:
            competitionListAsList.append(list(competition))

        return render_template('competition.html', competitionList=competitionListAsList, current_time=now.ctime())

@app.route('/addCompetition' , methods=['GET','POST'])
def addCompetition():
        name = request.form['name']
        type = request.form['type']
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("INSERT INTO COMPETITION(NAME, TYPE) VALUES (%s, %s)", (name, type))
        connection.commit()
        connection.close()
        return redirect('/competition')


@app.route('/deleteCompetition' , methods=['POST'])
def deleteCompetition():
        id = request.form['id']
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        query = """DELETE FROM COMPETITION WHERE id=""" + id + """;"""
        cursor.execute(query)
        connection.commit()
        connection.close()
        return redirect('/competition')

@app.route('/edit_Competition' , methods=['POST'])
def edit_Competition():
    if request.method == 'POST':
        now = datetime.datetime.now()
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        id = request.form['id']
        name = request.form['name']
        type = request.form['type']
        query = """update competition set NAME='"""+name+"""',  TYPE='"""+type+"""'  where id=""" + id + """;"""
        cursor.execute(query)
        connection.commit()
        connection.close()
        return redirect('/competition')

@app.route('/update_Competition' , methods=['POST'])
def update_Competition():
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        id = request.form['id']
        query = """select * from competition where id='""" + id + """';"""
        cursor.execute(query)
        update = list(cursor.fetchall()[0])

        connection.close()
        return render_template('competition_update.html', updatedlist=update)


@app.route('/searchCompetition' , methods=['POST'])
def searchCompetition():
        if request.method == 'POST':
            search = request.form['search_competition']
            now = datetime.datetime.now()
            connection = psycopg2.connect(app.config['dsn'])
            cursor = connection.cursor()
            query="""SELECT * FROM COMPETITION WHERE (NAME LIKE '%""" + search + """%');"""
            cursor.execute(query)
            competitionListAsTuple = cursor.fetchall()
            connection.close()
            competitionListAsList = []
            for competition in competitionListAsTuple:
                competitionListAsList.append(list(competition))
            return render_template('competition_search.html', competitionList=competitionListAsList, current_time=now.ctime())



def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


if __name__ == '__main__':
    try:
        VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')

        if VCAP_APP_PORT is not None:
            port, debug = int(VCAP_APP_PORT), False
        else:
            port, debug = 5000, True

        VCAP_SERVICES = os.getenv('VCAP_SERVICES')

        if VCAP_SERVICES is not None:
            app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
        else:
            app.config['dsn'] = "host='localhost' dbname='itucsdb' user='postgres' password='12345'"

        dataBaseSetup.initiateDataBase(app)

        app.secret_key = 'super secret key'

        login_manager.init_app(app)
        app.run(host='0.0.0.0', port=port, debug=True)

    except:
        print("Error in server setup. Exception: ")
        print(sys.exc_info()[0])
