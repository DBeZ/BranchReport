############################################################
# Connect to SQL database using username and password
############################################################

import mysql.connector #Install mysql-connector-python

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
