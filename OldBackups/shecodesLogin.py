################################################
# Login into php system using details in file
# Login file contains:
#   User: username
#   Pass: password
#   Database: databasename
#   host: hostname
#   IP: ip
#   port: xxxx
#   admin website
################################################

def login(fullFileName):
    f = open(fullFileName, "r")
    if f.mode == 'r':
        contents = f.readlines()
    f.close()
    username = contents[0].split()
    username = username[-1]
    password = contents[1].split()
    password = password[-1]
    databaseName = contents[2].split()
    databaseName = databaseName[-1]
    hostName = contents[3].split()
    hostName = hostName[-1]
    ip = contents[4].split()
    ip = ip[-1]
    portNumber = contents[5].split()
    portNumber = portNumber[-1]
    adminSite = contents[6]

    return (username, password, databaseName, hostName, ip, portNumber, adminSite)
