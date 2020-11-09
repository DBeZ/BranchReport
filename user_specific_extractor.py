###############################################################
# Extract variables stored in txt files
###############################################################
# Text file used to simplify editing by users

import os
import datetime as dt

# Load track opening dates from file
# file format -
# "
# May20: 17/5/2020
# Mar20: 18/3/2020
# Nov19: 3/11/2019
# Aug19: 4/8/2019
# May19: 12/5/2019
# Feb19: 3/2/2019
# Nov18: 4/11/2018
# Aug18: 5/8/2018
# May18: 6/5/2018
# "
#TODO: should be replaced SQL table retrieved. Please note this table should contain
# The first date of TRACK OPENING and NOT the registration opening
def track_openings(text_file):
    track_openings_dict = {}
    f = open(text_file, "r")
    if f.mode == 'r':
        contents = f.readlines()
    f.close()
    contents = filter(lambda x: x.strip(), contents)
    for line in contents:
        splitted = line.split(":")
        key_name=splitted[0].strip()
        value=splitted[-1].strip()
        value=dt.datetime.strptime(value, '%d/%m/%Y')
        track_openings_dict[key_name] = value
    return track_openings_dict

# def sql_fields_and_types(text_file):
#     sql_fields_dict = {}
#     sql_type_dict = {}
#
#     f = open(text_file, "r")
#     if f.mode == 'r':
#         contents = f.readlines()
#     f.close()
#
#     if len(contents/2)%2==0:
#         sql_fields = contents[0:len(contents/2)]
#         sql_types = contents[len(contents / 2):-1]
#         for line in sql_fields:
#             splitted = line.split(":")
#             sql_fields_dict[splitted[0].strip()] = splitted[-1].strip()
#         for line in sql_types:
#             splitted = line.split(":")
#             sql_type_dict[splitted[0].strip()] = splitted[-1].strip()
#     else:
#         print("Each sql field must have a filetype specified")
#
#     return sql_fields_dict, sql_type_dict


def login_google(filename):
    login_dict = {}

    working_dir = os.getcwd()
    os.chdir("..")
    os.chdir("User_specific_security_files")
    f = open(filename, "r")
    if f.mode == 'r':
        contents = f.readlines()
    f.close()
    os.chdir(working_dir)
    for line in contents:
        splitted = line.split(":")
        login_dict[splitted[0].strip()] = splitted[-1].strip()

    return login_dict


## SQL database login.
# file format -
# "
#   User:
#   Pass:
#   Database:
#   Host:
#   IP:
#   Port:
#   Site:
# "
def login_sql(filename, user_specific_dir):
    sql_login_dict = {}

    working_dir = os.getcwd()
    os.chdir("..")
    os.chdir(user_specific_dir)

    f = open(filename, "r")
    if f.mode == 'r':
        contents = f.readlines()
    f.close()
    os.chdir(working_dir)
    for line in contents:
        splitted = line.split(":")
        key_name=splitted[0].strip()
        value=splitted[-1].strip()
        sql_login_dict[key_name] = value

    os.chdir(working_dir)
    return sql_login_dict
