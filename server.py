import datetime
import os

from flask import Flask
from flask import render_template
from DataBaseSetup import *


app = Flask(__name__)
dataBaseSetup = DataBaseSetup()

@app.route('/')
def home():
    now = datetime.datetime.now()

    return render_template('home.html', current_time=now.ctime(), data = dataBaseSetup.initiateDataBase())


if __name__ == '__main__':
    try:
        VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')

        if VCAP_APP_PORT is not None:
            port, debug = int(VCAP_APP_PORT), False
        else:
            port, debug = 5000, True

        dataBaseSetup.makeConnection(VCAP_APP_PORT)

        app.run(host='0.0.0.0', port=port, debug= True)

    except:
        print("Error in server setup. Exception: ")
        print(sys.exc_info()[0])

