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
            try:
                cursor=dataBaseSetup.connection.cursor()
                query = """select * from pool;"""
                cursor.execute(query)
                poolfetch = cursor.fetchall()
                PoolListForm = []
                for pool in poolfetch:
                    PoolListForm.append(list(pool))
                now = datetime.datetime.now()
                return render_template('pools.html', current_time=now.ctime(), list=PoolListForm)
            except :
                return redirect('/Pools')
        elif 'deletePoolbyname' in request.form:
            try:
                cursor=dataBaseSetup.connection.cursor()
                name = request.form['deletePoolbyname']
                query = """delete from pool where name='""" + name + """';"""
                cursor.execute(query)
                dataBaseSetup.connection.commit()
                return redirect('/Pools')
            except :
                return redirect('/Pools')
        elif 'updatepool' in request.form:
            try:
                cursor=dataBaseSetup.connection.cursor()
                name = request.form['updatepool']
                query = """select * from pool where name='""" + name + """';"""
                cursor.execute(query)
                poolupdated = list(cursor.fetchall()[0])
                now = datetime.datetime.now()
                return render_template('pool_update.html', current_time=now.ctime(), element=poolupdated)
            except :
                return redirect('/Pools')

@app.route('/AddPool', methods=['GET', 'POST'])
def pool_edit():
        if request.method == 'GET':
            now = datetime.datetime.now()
            return render_template('pool_edit.html', current_time=now.ctime())
        else:
            try:
                cursor=dataBaseSetup.connection.cursor()
                name = request.form['name']
                city = request.form['city']
                capacity = request.form['capacity']
                built = request.form['built']
                query = """insert into pool values('""" + name + """','""" + city + """',""" + capacity + """,""" + built + """);"""
                cursor.execute(query)
                dataBaseSetup.connection.commit()
                return redirect('/Pools')
            except:
                return redirect('/Pools')


@app.route('/SearchPool' , methods=['POST'])
def pool_search():
    try:
        cursor=dataBaseSetup.connection.cursor()

        name = request.form['searchbyname']
        query = """select * from pool where (name like '%""" + name + """%');"""
        cursor.execute(query)
        poolfetch = cursor.fetchall()
        PoolListForm = []
        for pool in poolfetch:
            PoolListForm.append(list(pool))
        now = datetime.datetime.now()
        return render_template('pools.html', current_time=now.ctime(), list=PoolListForm)
    except :
        return redirect('/Pools')


@app.route('/UpdatePool', methods=['GET', 'POST'])
def pool_update():
        if request.method == 'GET':
            now = datetime.datetime.now()
            return render_template('pool_update.html', current_time=now.ctime())
        else:
            try:
                cursor=dataBaseSetup.connection.cursor()
                name = request.form['name']
                city = request.form['city']
                capacity = request.form['capacity']
                built = request.form['built']
                oldname=request.form['oldname']
                oldcity=request.form['oldcity']
                query = """update pool set name='""" + name + """',city='""" + city + """',capacity=""" + capacity + """,built=""" + built + """ where name='""" + oldname + """' and city='""" + oldcity + """';"""
                cursor.execute(query)
                dataBaseSetup.connection.commit()
                return redirect('/Pools')
            except:
                return redirect('/Pools')

@app.route('/SearchStat' , methods=['POST'])
def stat_search():
    try:
        cursor=dataBaseSetup.connection.cursor()

        name = request.form['searchbyname']
        query = """select * from stats where (name like '%""" + name + """%');"""
        cursor.execute(query)
        statfetch = cursor.fetchall()
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
                cursor=dataBaseSetup.connection.cursor()
                name = request.form['name']
                surname = request.form['surname']
                team = request.form['team']
                league = request.form['league']
                goal = request.form['goal']
                assist = request.form['assist']
                save = request.form['save']
                oldname=request.form['oldname']
                oldsurname=request.form['oldsurname']
                query = """update stats set name='""" + name + """',surname='""" + surname + """',team='""" + team + """',league='""" + league + """',goal=""" + goal + """,assist=""" + assist + """,save=""" + save + """ where name='""" + oldname + """' and surname='""" + surname + """';"""
                cursor.execute(query)
                dataBaseSetup.connection.commit()
                return redirect('/Statistic')
            except :
                return redirect('/Statistic')

@app.route('/Statistic',methods=['GET', 'POST'])
def statistics():
        if request.method == 'GET':
            now = datetime.datetime.now()
            StatsListForm = []
            return render_template('statistics.html', current_time=now.ctime(),list=StatsListForm)
        elif 'deletestatbyname' in request.form:
            try:
                cursor=dataBaseSetup.connection.cursor()
                name = request.form['deletestatbyname']
                query = """delete from stats where name='""" + name + """';"""
                cursor.execute(query)
                dataBaseSetup.connection.commit()
                return redirect('/Statistic')
            except :
                return redirect('/Statistic')
        elif 'updatestat' in request.form:
            try:
                cursor=dataBaseSetup.connection.cursor()
                name = request.form['updatestat']
                query = """select * from stats where name='""" + name + """';"""
                cursor.execute(query)
                statupdated = list(cursor.fetchall()[0])
                now = datetime.datetime.now()
                return render_template('stat_update.html', current_time=now.ctime(), element=statupdated)
            except :
                return redirect('/Statistic')
        elif 'stattype' in request.form:
            try:
                cursor=dataBaseSetup.connection.cursor()
                league=request.form['league']
                stattype=request.form['stattype']
                query = """select * from stats where league='"""+league+"""' order by """+stattype+""" desc;"""
                cursor.execute(query)
                statsfetch = cursor.fetchall()
                StatsListForm = []
                for stats in statsfetch:
                    StatsListForm.append(list(stats))
                now = datetime.datetime.now()
                return render_template('statistics.html', current_time=now.ctime(), list=StatsListForm)
            except :
                return redirect('/Statistic')

@app.route('/AddStat', methods=['GET', 'POST'])
def stat_add():
        if request.method == 'GET':
            now = datetime.datetime.now()
            return render_template('stat_add.html', current_time=now.ctime())
        else:
            try:
                cursor=dataBaseSetup.connection.cursor()
                name = request.form['name']
                surname = request.form['surname']
                team = request.form['team']
                league = request.form['league']
                goal = request.form['goal']
                assist = request.form['assist']
                save = request.form['save']
                query = """insert into stats values('""" + name + """','""" + surname + """','""" + team + """','""" + league + """',""" + goal + """,""" + assist + """,""" + save +""");"""
                cursor.execute(query)
                dataBaseSetup.connection.commit()
                return redirect('/Statistic')
            except :
                 return redirect('/Statistic')


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

@app.route('/updatePlayer' , methods=['POST'])
def updatePlayer():
    if request.method == 'POST':
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        id = request.form['id']
        query = """select id, name, age, nation, team, field from players where id='""" + id + """';"""
        cursor.execute(query)
        update = list(cursor.fetchall()[0])
        return render_template('player_update.html', current_time=now.ctime(), updatedlist=update)

@app.route('/update_Player' , methods=['POST'])
def update_Player():
        id = request.form['id']
        name = request.form['name']
        age = request.form['age']
        nation = request.form['nation']
        team = request.form['team']
        field =request.form['field']
        cursor = dataBaseSetup.connection.cursor()
        query = """UPDATE PLAYERS SET NAME='""" + name + """',AGE=""" + age + """,NATION='""" + nation + """',TEAM='""" + team + """', FIELD='""" + field + """' where ID=""" + id + """;"""
        cursor.execute(query)
        dataBaseSetup.connection.commit()
        return redirect('/players')

@app.route('/searchPlayer' , methods=['POST'])
def searchPlayer():
    if request.method == 'POST':
        search = request.form['search_player']
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        query="""SELECT * FROM PLAYERS WHERE (NAME LIKE '%""" + search + """%');"""
        cursor.execute(query)
        playerListAsTuple = cursor.fetchall()
        playerListAsList = []
        for player in playerListAsTuple:
            playerListAsList.append(list(player))

        return render_template('player_search.html', playerList=playerListAsList, current_time=now.ctime())

@app.route('/countries' , methods=['GET', 'POST'])
def countries():
    now = datetime.datetime.now()
    cursor = dataBaseSetup.connection.cursor()
    cursor.execute("SELECT * FROM COUNTRIES ORDER BY NAME;")
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
        query="""SELECT * FROM COUNTRIES WHERE LOWER(NAME) LIKE LOWER('%"""+ request.form['search'] +"""%') ORDER BY NAME;"""
        cursor.execute(query)
        countryListAsTuple = cursor.fetchall()
        countryListAsList = []
        for country in countryListAsTuple:
            countryListAsList.append(list(country))
        return render_template('search_country.html', countryList=countryListAsList, count=len(countryListAsList), current_time=now.ctime())

@app.route('/edit_country/<id>', methods=['GET','POST'])
def edit_country(id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        query = """SELECT NAME, POPULATION, COORDINATES FROM COUNTRIES WHERE ID=""" + id + """;"""
        cursor.execute(query)
        name, population, coordinates = cursor.fetchone()
        return render_template('edit_country.html', current_time=now.ctime(),id=id, name=name , population=population , coordinates=coordinates)

@app.route('/update_country', methods=['GET','POST'])
def update_country():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        population = request.form['population']
        coordinates = request.form['coordinates']
        cursor = dataBaseSetup.connection.cursor()
        query="""UPDATE COUNTRIES SET NAME='"""+name+"""', POPULATION="""+population+""", COORDINATES="""+coordinates+""" WHERE ID="""+id+""";"""
        cursor.execute(query)
        dataBaseSetup.connection.commit()
        return redirect('/countries')

@app.route('/leagues' , methods=['GET', 'POST'])
def leagues():
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        cursor.execute("SELECT * FROM LEAGUES ORDER BY NAME;")
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
        query="""SELECT * FROM LEAGUES WHERE LOWER(NAME) LIKE LOWER('%"""+ request.form['search'] +"""%') ORDER BY NAME;"""
        cursor.execute(query)
        leagueListAsTuple = cursor.fetchall()
        leagueListAsList = []
        for league in leagueListAsTuple:
            leagueListAsList.append(list(league))
        return render_template('search_league.html', leagueList=leagueListAsList, count=len(leagueListAsList), current_time=now.ctime())

@app.route('/edit_league/<id>', methods=['GET','POST'])
def edit_league(id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        cursor = dataBaseSetup.connection.cursor()
        query = """SELECT NAME, NATION, CLASSIFICATION FROM LEAGUES WHERE ID=""" + id + """;"""
        cursor.execute(query)
        name, nation, classification = cursor.fetchone()
        return render_template('edit_league.html', current_time=now.ctime(),id=id, name=name , nation=nation , classification=classification)

@app.route('/update_league', methods=['GET','POST'])
def update_league():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        nation = request.form['nation']
        classification = request.form['classification']
        cursor = dataBaseSetup.connection.cursor()
        query="""UPDATE LEAGUES SET NAME='"""+name+"""', NATION='"""+nation+"""', CLASSIFICATION="""+classification+""" WHERE ID="""+id+""";"""
        cursor.execute(query)
        dataBaseSetup.connection.commit()
        return redirect('/leagues')









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
