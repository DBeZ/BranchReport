import os


def login_google():
    login_dict = {}

    working_dir = os.getcwd()
    os.chdir("..")
    os.chdir("User_specific_security_files")
    f = open("user_specific.txt", "r")
    if f.mode == 'r':
        contents = f.readlines()
    f.close()
    os.chdir(working_dir)
    for line in contents:
        splitted = line.split(":")
        login_dict[splitted[0].strip()] = splitted[-1].strip()

    return login_dict


def login_sql(login_dict):
    working_dir = os.getcwd()
    os.chdir("..")
    os.chdir(login_dict[login_dict])

    f = open(login_dict["sql_login"], "r")
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

    os.chdir(working_dir)
    return (username, password, databaseName, hostName, ip, portNumber, adminSite)
