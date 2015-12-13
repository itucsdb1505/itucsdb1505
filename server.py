import datetime
import psycopg2
import os
import json
import re
import sys

from flask import Flask
from flask import render_template
from flask import request, redirect
from DataBaseSetup import *


app = Flask(__name__)
dataBaseSetup = DataBaseSetup()





@app.route('/')
def home():
    now = datetime.datetime.now()

    return render_template('home.html', current_time=now.ctime())

@app.route('/userManagement')
def userManagement():
    now = datetime.datetime.now()
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""select users.name, users.age, users.email, users.auth, countries.name from USERS join countries on users.country_id = countries.id;""")
    userListAsTuple = cursor.fetchall()
    connection.close()
    userListAsList = []
    for user in userListAsTuple:
        userListAsList.append(list(user))

    return render_template('userManagement.html', userList=userListAsList, user4Update=None, current_time=now.ctime())


@app.route('/addUser' , methods=['POST'])
def addUser():
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']
    auth = request.form['auth']
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """INSERT INTO USERS(NAME, AGE, EMAIL, AUTH) values('""" + name + """',""" + age + """,'""" + email + """','""" + auth + """')"""
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
    connection = psycopg2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = """UPDATE users SET name='""" + name + """',age=""" + age + """,email='""" + email + """',auth='""" + auth + """' WHERE email='""" + email + """';"""
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
    cursor.execute("""select users.name, users.age, users.email, users.auth, countries.name from USERS join countries on users.country_id = countries.id;""")
    userListAsTuple = cursor.fetchall()
    connection.close()
    userListAsList = []
    for user in userListAsTuple:
        userListAsList.append(list(user))
    return render_template('userManagement.html', userList=userListAsList, user4Update=user4Update, current_time=now.ctime())

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

#*************************************************************************
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


#*************************************************************************
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
#*************************************************************************
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
#*************************************************************************
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
        phone = request.form['phone']
        mail = request.form['mail']
        message = request.form['message']
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("INSERT INTO MESSAGES(TITLE, PHONE, MAIL, MESSAGE) VALUES(%s, %s, %s, %s)",(title, phone, mail, message))
        connection.commit()
        connection.close()
        return redirect('/')

@app.route('/edit_message/<id>', methods=['GET','POST'])
def edit_message(id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        query = """SELECT TITLE, PHONE, MAIL, MESSAGE FROM MESSAGES WHERE ID=""" + id + """;"""
        cursor.execute(query)
        title, phone, mail, message = cursor.fetchone()
        connection.close()
        return render_template('edit_message.html', current_time=now.ctime(),id=id, title=title , phone=phone , mail=mail, message=message)

@app.route('/update_message', methods=['GET','POST'])
def update_message():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        phone = request.form['phone']
        mail = request.form['mail']
        message = request.form['message']
        connection = psycopg2.connect(app.config['dsn'])
        cursor = connection.cursor()
        query="""UPDATE MESSAGES SET TITLE='"""+title+"""', PHONE="""+phone+""", MAIL='"""+mail+"""', MESSAGE='"""+message+"""' WHERE ID="""+id+""";"""
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
        app.run(host='0.0.0.0', port=port, debug=True)

    except:
        print("Error in server setup. Exception: ")
        print(sys.exc_info()[0])
