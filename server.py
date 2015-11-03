import datetime
import os

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

@app.route('/Pools')
def pool_list():
    cursor = dataBaseSetup.connection.cursor()
    query = """select name,city,capacity,built from pool;"""
    cursor.execute(query)
    poolfetch = cursor.fetchall()
    PoolListForm = []
    for pool in poolfetch:
        PoolListForm.append(list(pool))
    now = datetime.datetime.now()
    return render_template('pools.html', current_time=now.ctime(),list=PoolListForm)

@app.route('/AddPool',methods=['GET','POST'])
def pool_edit():
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('pool_edit.html',current_time=now.ctime())
    elif 'pool_to_delete' in request.form:
        name = request.form['pool_to_delete']
        cursor = dataBaseSetup.connection.cursor()
        query = """delete from pool where name='""" + name + """';"""
        cursor.execute(query)
        dataBaseSetup.connection.commit()
        return redirect('/Pools')
    else:
        name = request.form['name']
        city = request.form['city']
        capacity = request.form['capacity']
        built = request.form['built']
        cursor = dataBaseSetup.connection.cursor()
        query = """insert into pool values('""" + name + """','""" +  city + """',""" + capacity + """,""" + built + """);"""
        cursor.execute(query)
        dataBaseSetup.connection.commit()
        return redirect('/Pools')
    
@app.route('/players')
def players():
    now = datetime.datetime.now()
    cursor = dataBaseSetup.connection.cursor()
    query="""select id, name, age, nation, team, field from PLAYERS;"""
    cursor.execute(query)
    playerListAsTuple = cursor.fetchall()
    playerListAsList = []
    for player in playerListAsTuple:
        playerListAsList.append(list(player))

    return render_template('players.html', playerList=playerListAsList, current_time=now.ctime())
    
    
    
    
    
    cursor = dataBaseSetup.connection.cursor()
    query="""select id, name, age, nation, team, field from PLAYERS;"""
    cursor.execute(query)
    return render_template('players.html', playerList = cursor.fetchall())


@app.route('/addPlayer' , methods = ['POST'])
def addPlayer():
    id= request.form['id']
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


if __name__ == '__main__':
    try:
        VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')

        if VCAP_APP_PORT is not None:
            port, debug = int(VCAP_APP_PORT), False
        else:
            port, debug = 5000, True

        dataBaseSetup.makeConnection(VCAP_APP_PORT)
        app.run(host='0.0.0.0', port=port, debug=True)

    except:
        print("Error in server setup. Exception: ")
        print(sys.exc_info()[0])

