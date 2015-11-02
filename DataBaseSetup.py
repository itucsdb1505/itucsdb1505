import psycopg2
import sys
import os

class DataBaseSetup:

    def __init__(self):
        self.cursor = None

    def initiateDataBase(self):
        try:
            #read sqlFile commands from SQLFile
            with open("initialDB.sql") as SQLFile:
                sqlFile = SQLFile.readlines()

                #execute commands readed
                for transaction in sqlFile:
                    self.cursor.execute(transaction)

            self.cursor.execute("""select * from test""")
            data = self.cursor.fetchall();
            return data
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
            
            sq = """CREATE TABLE COMPANY(
                   ID INT PRIMARY KEY     NOT NULL,
                   NAME           TEXT    NOT NULL,
                   AGE            INT     NOT NULL,
                   ADDRESS        CHAR(50),
                   SALARY         REAL)"""
                   
                   
            self.execute(sq)
            
            

        except:
            print("Could not connected to database.")

