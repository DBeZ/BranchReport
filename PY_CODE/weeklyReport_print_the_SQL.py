
import mysql.connector
from mysql.connector.constants import ClientFlag

import datetime
import time
from datetime import timedelta

import sqlLines_9_20
from sqlLines_9_20 import getSQL_line9, getSQL_line10, getSQL_line11, getSQL_line13_19, getSQL_line_20_branch

import sqlPersistence
from sqlPersistence import getSQL_Persistence_Data_By_Tracks_Openings

import sqlPersistenceAug
from sqlPersistenceAug import getSQL_Persistence_Data_Aug_1, getSQL_Persistence_Data_Aug_2, getSQL_Persistence_Data_Aug_1_2


config = {
    'user': 'shecodes_ricky',  # 'shecodes',
    'password': 'hCCd!?C6U${g',  # 'S4tvwtbh!@',
    'host': '109.199.118.218',  # '3.15.239.185',
    'database': 'shecodes_monster_2_0',  # 'shecodes_shecodes'   # 'myddl',
}

mydb = mysql.connector.connect(**config)

#print(mydb)


def getNum(sqlStr):
    mycursor = mydb.cursor()

    mycursor.execute(sqlStr)

    myresult = mycursor.fetchall()
    return myresult[0][0]
   # for x in myresult:
    #   print(x)
 

def pgetNum(sqlStr):
    mycursor = mydb.cursor()

    mycursor.execute(sqlStr)

    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
 

def getDataByWeeks():

    d7 = timedelta(days=7)
    d4 = timedelta(days=4)
    # d1 = timedelta(days=1)
    #f1 = datetime.datetime(2019, 9, 1, 1, 10, 10)
    #f2 = datetime.datetime(2019, 12, 31, 12, 12, 12)
    f1 = datetime.datetime(2019, 11, 10, 1, 10, 10)
    f2 = datetime.datetime(2020, 2, 1, 12, 12, 12)
     
    r1_feb = datetime.datetime(2019, 1, 15, 1, 10, 10)
    r2_feb = datetime.datetime(2019, 2, 14, 12, 12, 12)
    
    r1_may = datetime.datetime(2019, 4, 20, 1, 10, 10)
    r2_may = datetime.datetime(2019, 5, 16, 12, 12, 12)
    
    r1_nov = datetime.datetime(2019, 10, 16, 1, 10, 10)
    r2_nov = datetime.datetime(2019, 11, 16, 12, 12, 12)
     
    # print(f1, ' ', f2)
    f3 = f1
    r1 = 1
    while f3 < f2:
        f5 = f3 + d4
        print (' * * * = * * * = * * * = * * *  * * * = * * * = * * * = * * *   * * * = * * * = * * * = * * * ')
        print (' * * * = Week start    = unixtime * * = * * * = end = * * *  unixtime = * * * = * * * = * * * ')
        #  * * * = Week start    = * * *  * * * = * * * = * * * = * * *   * * * = * * * = * * * = * * * 
        #  * * * = 2019-09-01    1567289410.0    2019-09-05    1567635010.0

        print(' * * * =',f3.date(), '    ', time.mktime(f3.timetuple()),
              '        ', f5.date(), '  ', time.mktime(f5.timetuple()))
#        print(getSQL_line9(f3, f5))
#        print(getSQL_line10(f3, f5))
#        print(getSQL_line11(f3, f5))
#        
#        print (' * * * = * * * = * * * = * * * ')
#        print (' LINE 9   -   LINE 10   -   LINE 11 ')
#        print (' * * * = * * * = * * * = * * * ')
#        
#        #print(r1, ' ', r2, ' ', r3)
#        print (' * ')
#        print (' * ')
#        
#        print (' * * * = * * * = * * * = * * * ')
#        print (' LINE 13   -   LINE 19    ')
#        print (' * * * = * * * = * * * = * * * ')
#         
#        pgetNum(getSQL_line13_19(f3, f5))
#        print (' * ')
#        print (' * ')
#        
#        print (' * * * = * * * = * * * = * * * ')
#        print (' Branches : LINE 20   -   LINE 30    ')
#        print (' * * * = * * * = * * * = * * * ')

        print('ma?:',(getSQL_line_20_branch(f3, f5)))
        print (' * ')
        print (' * ')

#        print (' * * * = * * * = * * * = * * * ')
#        print (' Persistence Data - by Tracks Openings    ')
#        print (' * * * = * * * = * * * = * * * ')
# 
        #print('Feb 2019: ', (getSQL_Persistence_Data_By_Tracks_Openings(f3, f5, r1_feb, r2_feb)) )
        #print('May 2019: ', (getSQL_Persistence_Data_By_Tracks_Openings(f3, f5, r1_may, r2_may)) )
        #print('Aug 2019 - 1: ', (getSQL_Persistence_Data_Aug_1(f3, f5)) )
        #print('Aug 2019 - 2 : ', (getSQL_Persistence_Data_Aug_2(f3, f5)) )
        #print('Aug 2019 - 1,2: ', (getSQL_Persistence_Data_Aug_1_2(f3, f5)) )
        #print('Nov 2019: ', (getSQL_Persistence_Data_By_Tracks_Openings(f3, f5, r1_nov, r2_nov)) )
        
        print (' * ')
        print (' * ')
        f3 += d7


getDataByWeeks()
