#!usr/bin/env python3
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np
from datetime import date, datetime
from matplotlib import pyplot as plt
from queries import gen_bot_main_stats_query,gen_bot_main_by_target_query, gen_bot_main_by_source_query, gen_bot_main_by_method_query, gen_bot_main_by_verification, gen_bot_main_by_ref_page_query, google_bot_main_by_source_query,google_bot_main_by_target_query,google_bot_direct_hit_main_query,google_bot_direct_hit_by_stcode_query, google_bot_direct_hit_by_bigimage_query,google_bot_direct_hit_main_query,google_bot_direct_hit_by_page_query,google_bot_direct_hit_by_bigcss_query, google_bot_direct_hit_by_bigjson_query, google_bot_ndirect_hit_main_query, google_bot_ndirect_hit_by_stcode_query, google_bot_direct_hit_by_php_query, google_bot_ndirect_hit_by_bigimage_query, google_bot_ndirect_hit_by_bigcss_query, google_bot_ndirect_hit_by_bigjson_query, google_bot_ndirect_hit_by_page_query, google_bot_ndirect_hit_by_php_query 


#These should be declared in the global namespace or pooled from the database
finalCsv = 'results/goalpl.csv'
today = date.today()


def getStats():
    #This is invoked in the inser namespace
    df = pd.read_csv(finalCsv)


    def conn():
        print('Connecting DB...')
        try:
            cnx = mysql.connector.connect(
                user='opatrwuser',
                password='yEmRCxI69oE8g0T8',
                host='opat-staging.cnd60fnqzkzb.eu-west-1.rds.amazonaws.com',
                database='opat_staging')
            print("Connected!")                          
            return cnx                                                      
        except mysql.connector.Error as err:
            print("Connection problem.")
        

    def getMainStats():
        '''Fetch user id, project id, month and year along with specific column names and return data in inner space'''
        tmp_list = []
        cnx = conn()
        cursor = cnx.cursor()
        ftch = cursor.execute('''SELECT project_id, user_id, logsStartDate, noRows  FROM opat.projects where pr_status= 0''')
        data = cursor.fetchone()
        dataLst = list(data)
        cnx.commit()
        colNames = [i[0] for i in cursor.description]
        print(colNames)
        clsData = dict(zip(colNames, dataLst))
        projectId = clsData['project_id']
        userId = clsData['user_id']
        month = clsData['logsStartDate'].date().month
        year = clsData['logsStartDate'].date().year
        noRows = clsData['noRows']
        tmp_list = [projectId, userId, month, year, noRows]
        cursor.close()
        cnx.close()
        return tmp_list

    initStats = getMainStats()
    initStats = list(initStats)
    print(initStats)

    def saveToDb(insertQuery, insertQueryList, many=False):
        '''Open db connection and combine insertQuery and insertQueryList'''
        cnx = conn()
        cursor = cnx.cursor()
        if many == False:
            cursor.executemany(insertQuery, insertQueryList)
        else:
            cursor.execute(insertQuery, insertQueryList)
        cnx.commit()
        cursor.close()
        cnx.close()


    def updateDb(insertQuery, insertQueryList, insert = False):
        '''Opendb connection and combine insertQuery and insertQueryList'''
        cnx = conn()
        cursor = cnx.cursor()
        if insert == False:
            cursor.executemany(insertQuery, insertQueryList)
        else:
            cursor.execute(insertQuery, insertQueryList)
        cnx.commit()
        cnx.close()



    def getFirstLastDate():
        '''Extract start and ending date from the input log csv'''
        df['time_zone'] = pd.to_datetime(df['time_zone'])
        dt = df.sort_values(by='time_zone')
        dateDesc = dt['time_zone'].describe(datetime_is_numeric=True)
        fdate = dateDesc.loc['min'].strftime('%Y-%m-%d')
        ldate = dateDesc.loc['max'].strftime('%Y-%m-%d')
        return(fdate, ldate)



    def updateMainStats():
        '''Update projects main table'''
        pr_status=1
        vals=df.shape
        noRows,noCols = vals
        fdate,ldate = getFirstLastDate()
        insertQueryList=(fdate, ldate, noRows, noCols, pr_status)
        print(insertQueryList)
        updateDb(insertQuery='UPDATE projects SET logsStartDate=%s, logsEndDate=%s, noRows=%s, noCols=%s, pr_status=%s WHERE pr_status=0', insertQueryList=(fdate, ldate, noRows, noCols, pr_status), insert=True)

    #print('Updating main stats')    
    #updateMainStats() #Invoking this function to update main stats and to set project status to 0.

    def isNumericBoolFilter(names):
        '''Filter out boolean true or false and returns a masked list where true if number othervise false'''
        isNum = []
        for botName in names:
            if any(map(str.isdigit, botName)):
                isNum.append(True)
            else:
                isNum.append(False)
        return isNum

    def filterBots(botName, nDirect, inverse=False):
        '''This function filters dataset by the bot name and by direct hit'''
        if isinstance(botName, type(None)) and nDirect == False:
            print('No bots no filter!')
            #print(df.shape[0])
            return df
        elif isinstance(botName, str) & nDirect == False:
            print('Bot name no direct traffic filter active')
            dfb = df[df['botName'] == botName]
            print(dfb.shape[0])
            return dfb
            #print(dfb['botName'].value_counts())
        elif isinstance(botName, str) & nDirect == True:
            print('Bot name plus direct hit filter On')
            if inverse == True:
                print('Inversion On')
                dfbdhi = df[(df['botName'] == botName) & ~(df['referrer'] == 'Direct Hit')]
                print(dfbdhi.shape[0])
                return dfbdhi
            else:
                print('Inversion Off!')
                dfbdh = df[(df['botName'] == botName) & (df['referrer'] == 'Direct Hit')]
                print(dfbdh.shape[0])
                return dfbdh                


    def insertBotsMainStats(botName, nDirect, specInsertQuery, colName, inverse):
        '''Populate main stats table for all bots separatelly for different table format'''
        insertQueryList = []
        df = filterBots(botName, nDirect, inverse)
        valCount = df[colName].value_counts()
        valNames = valCount.index.tolist()
        valStats = valCount.values.tolist()
        
        for names, stats, isNumeric in zip(valNames, valCount, isNumericBoolFilter(names=valNames)):
            insertQueryList.append((0, initStats[1], names, stats, (stats/df.shape[0])*100, isNumeric, initStats[2], initStats[3], None))
        print('Inserting...')
        saveToDb(insertQuery=specInsertQuery, insertQueryList=insertQueryList)
        print(insertQueryList)

    def insertMainStats(botName, nDirect, specInsertQuery, colName, inverse):
        '''Populates main bot stats for similar tables'''
        insertQueryList = []
        dfm = filterBots(botName, nDirect, inverse)
        valCount = dfm[colName].value_counts()
        valNames = valCount.index.tolist()
        valStats = valCount.values.tolist()
        for names, stats in zip(valNames, valCount):
            insertQueryList.append((0, str(names), str(stats), (stats/dfm.shape[0])*100, initStats[2], initStats[3], initStats[1]))

        #saveToDb(insertQuery=specInsertQuery, insertQueryList=insertQueryList, many=False)
        print('Inserting')
        print(insertQueryList)


    def insertBotStatsDhitByTarget(botName, nDirect, target, size, insertQuery, inverse):
        '''Predefined document size threshold 1MB -- 1000000b for direct hits'''
        insertQueryList = []
        din = filterBots(botName, nDirect, inverse)
        dtar = din[din['target'] == target]

        dh = dtar[(dtar['size'] > int(size))]

        targets = dh['referring_page'].values.tolist()
        sizes = df['size'].values.tolist()
        for target, size in zip(targets, sizes):
            insertQueryList.append((0, target, size, initStats[2], initStats[3], initStats[0]))

        print(insertQueryList)
        saveToDb(insertQuery, insertQueryList=insertQueryList)          


    def paginationCheck(botName, nDirect, term, specInsertQuery, inverse):
        '''This function check how pagination is crawled by specific bot'''
        insertQueryList = []
        dts = filterBots(botName, nDirect, inverse)
        pgdts = dts[dts['referrer'].str.contains(term)]
        print(pgdts['referrer'], pgdts['referring_page'])
        return pgdts
        
        
            


   
        
        





                       
           
        
    #Main Stats
    insertBotsMainStats(botName=None, nDirect=False, specInsertQuery=gen_bot_main_stats_query, colName='botName', inverse=False)
    #insertMainStats(botName=None, nDirect=False, specInsertQuery=gen_bot_main_by_method_query, colName='method', inverse=False)
    #insertMainStats(botName=None, nDirect=False, specInsertQuery=gen_bot_main_by_ref_page_query, colName='referring_page', inverse=False)
    #insertMainStats(botName=None, nDirect=False, specInsertQuery=gen_bot_main_by_source_query, colName='source', inverse=False)
    #insertMainStats(botName=None, nDirect=False, specInsertQuery=gen_bot_main_by_target_query, colName='target', inverse=False)

    #Google Bot Main Stats
    #insertMainStats(botName='googlebot.com', nDirect=False, specInsertQuery=google_bot_main_by_source_query, colName='source', inverse=False)
    #insertMainStats(botName='googlebot.com', nDirect=False, specInsertQuery=google_bot_main_by_target_query, colName='target', inverse=False)


    #Populate Google Bots Stat Area - Direct Hits
    #insertMainStats(botName='googlebot.com', nDirect=False, specInsertQuery=google_bot_direct_hit_main_query, colName='referring_page', inverse=False)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = False, target='CSS', size=10, insertQuery=google_bot_direct_hit_by_bigcss_query, inverse=False)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = False,  target='Image', size=80000, insertQuery=google_bot_direct_hit_by_bigimage_query, inverse=False)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = False, target='JSON', size=10000, insertQuery=google_bot_direct_hit_by_bigjson_query, inverse=False)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = False,  target='Page', size=10000, insertQuery=google_bot_direct_hit_by_page_query, inverse=False)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = False, target='PHP', size=100, insertQuery=google_bot_direct_hit_by_php_query, inverse=False)
    #insertMainStats(botName='googlebot.com', nDirect=False, specInsertQuery=google_bot_direct_hit_by_stcode_query, colName='status_code', inverse=False)


    #Populate Google Bots Stat Area -Non Direct Hits
    #insertMainStats(botName='googlebot.com', nDirect=True, specInsertQuery=google_bot_ndirect_hit_main_query, colName='referring_page', inverse=True)
    #insertMainStats(botName='googlebot.com', nDirect=True, specInsertQuery=google_bot_ndirect_hit_by_stcode_query, colName='status_code', inverse=True)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = True, target='CSS', size=10, insertQuery=google_bot_ndirect_hit_by_bigcss_query, inverse=True)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = True,  target='Image', size=80000, insertQuery=google_bot_ndirect_hit_by_bigimage_query, inverse=True)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = True, target='JSON', size=10000, insertQuery=google_bot_ndirect_hit_by_bigjson_query, inverse=True)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = True,  target='Page', size=10000, insertQuery=google_bot_ndirect_hit_by_page_query, inverse=True)
    #insertBotStatsDhitByTarget(botName='googlebot.com', nDirect = True, target='PHP', size=100, insertQuery=google_bot_ndirect_hit_by_php_query, inverse=True)


    #Pagination check
    #paginationCheck(botName='googlebot.com', nDirect=False, term = 'strona', specInsertQuery=google_bot_ndirect_hit_by_php_query, inverse=False)
    
def main():
    getStats()




if __name__=="__main__":
    main()            

