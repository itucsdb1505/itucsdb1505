import datetime
import os
import json
import os
import re

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
    cursor = dataBaseSetup.connection.cursor()
    cursor.execute("""select name, age, email, auth from USERS;""")
    userListAsTuple = cursor.fetchall()
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
    cursor = dataBaseSetup.connection.cursor()
    query = """INSERT INTO USERS values('""" + name + """',""" + age + """,'""" + email + """','""" + auth + """')"""
    cursor.execute(query)
    dataBaseSetup.connection.commit()
    return redirect('/userManagement')


@app.route('/userUpdate', methods=['POST'])
def userUpdate():
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']
    auth = request.form['auth']
    cursor = dataBaseSetup.connection.cursor()
    query = """UPDATE users SET name='""" + name + """',age=""" + age + """,email='""" + email + """',auth='""" + auth + """' WHERE email='""" + email + """';"""
    cursor.execute(query)
    dataBaseSetup.connection.commit()
    return redirect('/userManagement')

@app.route('/updateUser', methods=['POST'])
def updateUser():
    now = datetime.datetime.now()
    cursor = dataBaseSetup.connection.cursor()
    email = request.form['email']
    query = """select name, age, email, auth from users where email='""" + email + """';"""
    cursor.execute(query)
    user4Update = list(cursor.fetchall()[0])

    cursor.execute("""select name, age, email, auth from USERS;""")
    userListAsTuple = cursor.fetchall()
    userListAsList = []
    for user in userListAsTuple:
        userListAsList.append(list(user))
    return render_template('userManagement.html', userList=userListAsList, user4Update=user4Update, current_time=now.ctime())

@app.route('/deleteUser' , methods=['POST'])
def deleteUser():
    email = request.form['email']
    cursor = dataBaseSetup.connection.cursor()
    query = """DELETE FROM USERS WHERE email='""" + email + """';"""
    cursor.execute(query)
    dataBaseSetup.connection.commit()
    return redirect('/userManagement')

@app.route('/initiateDB')
def initiateDB():
    dataBaseSetup.initiateDataBase()
    cursor = dataBaseSetup.connection.cursor()
    cursor.execute("""select * from test;""")
    now = datetime.datetime.now()
    return render_template('initiateDB.html', current_time=now.ctime(), data=cursor.fetchall())

@app.route('/Pools', methods=['GET', 'POST'])
def pool_list():
    if request.method == 'GET':
        cursor = dataBaseSetup.connection.cursor()
        query = """select * from pool;"""
        cursor.execute(query)
        poolfetch = cursor.fetchall()
        PoolListForm = []
        for pool in poolfetch:
            PoolListForm.append(list(pool))
        now = datetime.datetime.now()
        return render_template('pools.html', current_time=now.ctime(), list=PoolListForm)
    elif 'deletePoolbyname' in request.form:
        name = request.form['deletePoolbyname']
        cursor = dataBaseSetup.connection.cursor()
        query = """delete from pool where name='""" + name + """';"""
        cursor.execute(query)
        dataBaseSetup.connection.commit()
        return redirect('/Pools')


@app.route('/AddPool', methods=['GET', 'POST'])
def pool_edit():
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('pool_edit.html', current_time=now.ctime())
    else:
        name = request.form['name']
        city = request.form['city']
        capacity = request.form['capacity']
        built = request.form['built']
        cursor = dataBaseSetup.connection.cursor()
        query = """insert into pool values('""" + name + """','""" + city + """',""" + capacity + """,""" + built + """);"""
        cursor.execute(query)
        dataBaseSetup.connection.commit()
        return redirect('/Pools')

@app.route('/players')
def players():
    now = datetime.datetime.now()
    cursor = dataBaseSetup.connection.cursor()
    query = """select id, name, age, nation, team, field from PLAYERS;"""
    cursor.execute(query)
    playerListAsTuple = cursor.fetchall()
    playerListAsList = []
    for player in playerListAsTuple:
        playerListAsList.append(list(player))

    return render_template('players.html', playerList=playerListAsList, current_time=now.ctime())


@app.route('/addPlayer' , methods=['POST'])
def addPlayer():
    id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    nation = request.form['nation']
    team = request.form['team']
    field = request.form['field']
    cursor = dataBaseSetup.connection.cursor()
    cursor.execute("INSERT INTO PLAYERS (id, name, age, nation, team, field) VALUES (%s, %s, %s, %s, %s, %s)", (id, name, age, nation, team, field))
    dataBaseSetup.connection.commit()
    return redirect('/players')

@app.route('/deletePlayer' , methods=['POST'])
def deletePlayer():
    id = request.form['id']
    cursor = dataBaseSetup.connection.cursor()
    query = """DELETE FROM PLAYERS WHERE id=""" + id + """;"""
    cursor.execute(query)
    dataBaseSetup.connection.commit()
    return redirect('/players')

@app.route('/countries' , methods=['GET', 'POST'])
def countries():
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        cursor.execute("SELECT * FROM COUNTRIES;")
        countryListAsTuple = cursor.fetchall()
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
        cursor = dataBaseSetup.connection.cursor()
        cursor.execute("INSERT INTO COUNTRIES(NAME, POPULATION, COORDINATES) VALUES(%s, %s, %s)",(name, population, coordinates))
        dataBaseSetup.connection.commit()
        return redirect('/countries')

@app.route('/delete_country/<id>', methods=['GET'])
def delete_country(id):
    cursor = dataBaseSetup.connection.cursor()
    query = """DELETE FROM COUNTRIES WHERE ID=""" + id + """;"""
    cursor.execute(query)
    dataBaseSetup.connection.commit()
    return redirect('/countries')

@app.route('/search_country' , methods=['POST'])
def search_country():
    if request.method == 'POST':
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        query="""SELECT * FROM COUNTRIES WHERE LOWER(NAME) LIKE LOWER('%"""+ request.form['search'] +"""%');"""
        cursor.execute(query)
        countryListAsTuple = cursor.fetchall()
        countryListAsList = []
        for country in countryListAsTuple:
            countryListAsList.append(list(country))
        return render_template('search_country.html', countryList=countryListAsList, current_time=now.ctime())

# @app.route('/edit_country/<id>', methods=['GET','POST'])
# def edit_country(id):
#     if request.method == 'GET':
#         now = datetime.datetime.now()
#         name = request.form['name']
#         population = request.form['population']
#         coordinates = request.form['coordinates']
#         return render_template('edit_country.html', current_time=now.ctime())
#     else:
#         cursor = dataBaseSetup.connection.cursor()
#         query = """SELECT NAME, POPULATION, COORDINATES FROM COUNTRIES WHERE ID=""" + id + """;"""
#         cursor.execute(query)
#         return redirect('/countries')

@app.route('/leagues' , methods=['GET', 'POST'])
def leagues():
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        cursor.execute("SELECT * FROM LEAGUES;")
        leagueListAsTuple = cursor.fetchall()
        leagueListAsList = []
        for league in leagueListAsTuple:
            leagueListAsList.append(list(league))
        return render_template('leagues.html', leagueList=leagueListAsList, current_time=now.ctime())

@app.route('/add_league' , methods=['GET', 'POST'])
def add_league():
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('add_league.html', current_time=now.ctime())
    else:
        name = request.form['name']
        nation = request.form['nation']
        classification = request.form['classification']
        cursor = dataBaseSetup.connection.cursor()
        cursor.execute("INSERT INTO LEAGUES(NAME, NATION, CLASSIFICATION) VALUES(%s, %s, %s)",(name, nation, classification))
        dataBaseSetup.connection.commit()
        return redirect('/leagues')

@app.route('/delete_league/<id>', methods=['GET'])
def delete_league(id):
    cursor = dataBaseSetup.connection.cursor()
    query = """DELETE FROM LEAGUES WHERE ID=""" + id + """;"""
    cursor.execute(query)
    dataBaseSetup.connection.commit()
    return redirect('/leagues')

@app.route('/search_league' , methods=['POST'])
def search_league():
    if request.method == 'POST':
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        query="""SELECT * FROM LEAGUES WHERE LOWER(NAME) LIKE LOWER('%"""+ request.form['search'] +"""%');"""
        cursor.execute(query)
        leagueListAsTuple = cursor.fetchall()
        leagueListAsList = []
        for league in leagueListAsTuple:
            leagueListAsList.append(list(league))
        return render_template('search_league.html', leagueList=leagueListAsList, current_time=now.ctime())











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



        dataBaseSetup.makeConnection(app)
        app.run(host='0.0.0.0', port=port, debug=True)

    except:
        print("Error in server setup. Exception: ")
        print(sys.exc_info()[0])
