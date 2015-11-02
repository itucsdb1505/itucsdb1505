import psycopg2
import sys
import os

class DataBaseSetup:

    cursor = None

    def __init__(self):
        pass

    def initiateDataBase(self):
        try:
            #read sqlFile commands from SQLFile
            with open("initialDB.sql") as SQLFile:
                sqlFile = SQLFile.readlines()

                #execute commands readed
                for transaction in sqlFile:
                    if transaction != '\n':
                        self.cursor.execute(transaction)

        except:
            print("Database could not initialized.")


    def makeConnection(self, VCAP_APP_PORT):
        try:
             #Define our connection string
            if VCAP_APP_PORT is not None:
                connection_info = "host=" + VCAP_APP_PORT + " dbname='itucsdb' user='postgres' password='12345'"
            else:
                connection_info = "host='localhost' dbname='itucsdb' user='postgres' password='12345'"

             # get a connection, if a connect cannot be made an exception will be raised here
            connection = psycopg2.connect(connection_info)

            # connection.cursor will return a cursor object, you can use this cursor to perform queries
            self.cursor = connection.cursor()

            print("Connected!\n")

        except:
            print("Could not connected to database.")

