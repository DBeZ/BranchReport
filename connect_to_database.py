############################################################
# Connect to the database using username and password
############################################################

#import pymysql.cursors #Install pymysql
import mysql.connector #Install mysql-connector-python
#import sqlite3

## connect to database using SQL
def connect_to_database(username, password, databaseName, hostName, portNumber):
    cnx = mysql.connector.connect(
        user=username,
        password=password,
        database=databaseName,
        host=hostName,
        port=portNumber
    )
    return cnx
