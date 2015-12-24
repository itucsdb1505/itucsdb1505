import psycopg2
import sys
import os

class DataBaseSetup:


    def initiateDataBase(self, app):
        try:
            connection = psycopg2.connect(app.config['dsn'])
            #read sqlFile commands from SQLFile
            with open("initialDB.sql") as SQLFile:
                sqlFile = SQLFile.readlines()
                cursor = connection.cursor()
                #execute commands readed
                for transaction in sqlFile:
                    if transaction != '\n':
                        cursor.execute(transaction)

                connection.commit()

                print("Database initialized.")

            connection.close()
        except:
            print("Database could not initialized. Err : ")
            print(sys.exc_info()[0])


