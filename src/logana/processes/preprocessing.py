#!usr/bin/env python3
#processor v1.0
#ToDO:
import glob
import gzip
import time
import io
import os
import subprocess
from lars import csv
import pandas as pd
from lars.apache import ApacheSource, COMBINED,REFERER, USER_AGENT
#from memory_profiler import profile
import swifter
from socket import gethostbyname, gethostbyaddr
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor
import gc
from scripts.bashRunner import runner


root_dir = './input'


def unpMeExt():
    """This function will recusively run trough each folder searchin for the gzip file, unzip and concatenate in one input.log file"""
    print(f"Log File Merging started at {time.strftime('%X')}")
    with open('logana/processes/input.log', 'w') as outfile:
        try:
            for file in glob.iglob('**/*', recursive=True):
                if '.zip' in file:
                    print(file)
                    print("Zip file found! Extraction started!")
                    os.chmod('./',0o755)
                    with ZipFile(file, 'r') as zfile:
                        zfile.extractall('logana/processes/input')
                    os.remove(file)
        except:
            print('No zip file in parent directory!')
        try:    
            for file in glob.iglob('**/*', recursive=True):

                if '.gz' in file:
                    with gzip.open(file, 'rb') as gzfile:
                        for line in gzfile:
                            try:
                                lines = line.decode('ISO-8859-1').strip(',')
                                outfile.write(lines)
                            except:
                                lines = line.decode('utf-8').strip(',')
                                outfile.write(lines)
        except Exception as e:
            print(e)
    print(f"Log File Merging Ended at {time.strftime('%X')}")       
             
                  

def logex(inputLog, outputCsv):
    """Using Lars to read log file and write csv as output"""
    print(f"Bot Log Conversion started at {time.strftime('%X')}")
    with io.open(inputLog, 'r', encoding="windows-1252") as infile, io.open(outputCsv, 'wb') as outfile:
       with ApacheSource(infile, log_format=COMBINED) as source, csv.CSVTarget(outfile) as target:
            for row in source:    
                target.write(row)
    os.remove(inputLog)            
    print(f"Bot Log extraction Ended at {time.strftime('%X')}")            

#@profile(precision=4)    
def colDefiner(inputCsv,outputCsv):
    """Transform initial csv and map columns producing new one"""
    print(f"Column name addition started at {time.strftime('%X')}")
    initial = pd.read_csv(inputCsv, header=None)
    colnames = {0:'host_ip', 1:'client_id', 2:'cl_username',
       3:'time_zone', 4:'request_type', 5:'status_code',
       6:'size', 7:'referrer', 8:'user_agent'}
    cols_to_keep = ['host_ip', 'time_zone', 'status_code', 'size', 'referrer', 'user_agent']
    mapper = {0:'method', 1:'referring_page', 2:'protocol'}
    initial.rename(mapper=colnames, axis=1, inplace=True)
    initial = initial[['host_ip', 'time_zone', 'request_type', 'status_code', 'size', 'referrer', 'user_agent']]
    initial.to_csv(outputCsv, index=None, columns=cols_to_keep)
    os.remove(inputCsv)
    print(f"Column name addition Ended at {time.strftime('%X')}")


def colSplitter(inputCsv, outputCsv):
    print(f"Column Splitting started at {time.strftime('%X')}")
    unsplitted = pd.read_csv(inputCsv, names=['request_type'])
    mapping = ['method', 'referring_page', 'protocol']
    unsplitted[mapping] = unsplitted['request_type'].str.split(expand=True)
    unsplitted.to_csv(outputCsv, index=None, columns=mapping)
    print(f"Column Splitting ended at {time.strftime('%X')}")
    os.remove(inputCsv)
       

def getDomain():
    pass

def domainSetter(inputCsv, domain, outputCsv):
    print(f"Domain setting started at {time.strftime('%X')}")
    unsetted = pd.read_csv(inputCsv)
    unsetted['referring_page'] = unsetted['referring_page'].swifter.apply(lambda x: domain+x)
    unsetted.to_csv(outputCsv, index= False)
    print(f"Domain setting ended at {time.strftime('%X')}")
    os.remove(inputCsv)

def concater(finputCsv, sinputCsv,thinputCsv, outputCsv):
    print(f"Concatenation started at {time.strftime('%X')}")
    df1 = pd.read_csv(finputCsv)
    df2 = pd.read_csv(sinputCsv)
    if sinputCsv !=None:
        df3 = pd.read_csv(thinputCsv)
        df = pd.concat([df1, df2, df3], axis=1)
        df.to_csv(outputCsv, index=False)
    else:
        df = pd.concat([df1, df2], axis=1)
        df.to_csv(outputCsv, index=False)    
    os.remove(finputCsv)
    os.remove(sinputCsv)
    print(f"Concatenation ended at {time.strftime('%X')}")

def agentTweaker(inputFile, outputFile):
    print(f"Agent splitter started at {time.strftime('%X')}")
    df = pd.read_csv(inputFile)
    agents = list(df['user_agent'].values)
    src = []
    for agent in agents:
        agent = str(agent)
        if 'Mobile' in agent:
            src.append('Mobile')
        elif 'Googlebot-News' in agent:
            src.append('NewsBot')
        elif 'Googlebot-Video' in agent:
            src.append('VideoBot')
        elif 'AdsBot-Google' in agent:
            src.append('AdsBot')
        elif 'Mediapartners' in agent:
            src.append('AdsenseBot')
        elif 'Image' in agent:
            src.append('ImageBot')
        else:
            src.append('Desktop') 
    df['source'] = src
    df.to_csv(outputFile, index = False)
    os.remove(inputFile)
    print(f"Agent splitter ended at {time.strftime('%X')}")


def typeTweaker(inputFile, outputFile):
    print(f"Type extraction started at {time.strftime('%X')}")
    df = pd.read_csv(inputFile)
    refs = list(df['referring_page'].values)
    target = []
    for ref in refs:
        ref = str(ref)
        if '.jpg' in ref:
            target.append('Image')
        elif '.png' in ref:
            target.append('Image')
        elif '.jpeg' in ref:
            target.append('Image')
        elif '.gif' in ref:
            target.append('Image')
        elif '.swg' in ref:
            target.append('Image')
        elif '.php' in ref:
            target.append('PHP')
        elif '.css' in ref:
            target.append('CSS')
        elif '.json' in ref:
            target.append('JSON')
        elif '.js' in ref:
            target.append('JavaScript')
        else:
            target.append('Page')
    df['target'] = target
    df.to_csv(outputFile, index = False)
    os.remove(inputFile)
    print(f"Type extraction ended at {time.strftime('%X')}")

def listGetter(unqFileList):
    print(f"List obtaining started at {time.strftime('%X')}")
    iplist = []
    with open(unqFileList, 'r') as ips:
        for line in ips:
            stripped_lines = line.strip()
            iplist.append(stripped_lines)
    print(f"List obtaining ended at {time.strftime('%X')}")        
    return iplist
   

def proVerific(address):
    verified = []
    try:
        res = gethostbyaddr(address)[0]
        part = res.partition(".")
        verified.append([address, part[2], True])
    except Exception as a:
        verified.append([address, a, False])
        
    return verified     
        
    
    
def verificator(unqFileList,unQoutputCsv, cond):
    '''Does reverse DNS lockup in order to verify Bot by address and return a list of 3 elements, ip, info and status'''
    if cond:
        iplist = listGetter(unqFileList)
        print(f"Verification started at {time.strftime('%X')}")
        with ThreadPoolExecutor(max_workers=15) as executor:
            verGen =list(executor.map(proVerific, iplist))
            el = [tuple(elem[0]) for elem in verGen]
            colmap = ['host_ip', 'botName', 'verified']
            verdf = pd.DataFrame(el, columns=colmap)
            verdf.to_csv(unQoutputCsv, index=False)
        os.remove(unqFileList)
        print(f"Verification ended at {time.strftime('%X')}")
    else:
        unqFileList = None
    
def merger(ffile, sfile, mergeOn, cond=False):
    if cond:
        print(sfile)
        print(f"Final merging started at {time.strftime('%X')}")
        df1 = pd.read_csv(ffile)
        df2 = pd.read_csv(sfile)
        df = df1.merge(df2, on=mergeOn)
        df.to_csv('logana/processes/finalVerified.csv', index=False)
        os.remove(ffile)
        os.remove(sfile)
        print(f"Final merging ended at {time.strftime('%X')}")
    else:
        sfile=None
        pass
    
def typeSetter(inputCsv, outputCsv):
    print(f"Type setting started at {time.strftime('%X')}")
    ntype = pd.read_csv(inputCsv, low_memory=False)
    print(ntype.columns)
    ntype['datetime'] = pd.to_datetime(ntype['time_zone'])
    ntype['referrer'] = ntype['referrer'].fillna('Direct Hit')
    ntype['user_agent'] = ntype['user_agent'].fillna('No User Agent')
    ntype['protocol'] = ntype['protocol'].fillna('No protocol Specified')
    ntype['botName'] = ntype['botName'].fillna('No botName specified-er-01')
    ntype.to_csv(outputCsv, index=False)
    os.remove(inputCsv)
    print(f"Type setting ended at {time.strftime('%X')}")

def dateSplitter(inputCsv, outputCsv):
    df = pd.read_csv(inputCsv)
    df['time_zone'] = pd.to_datetime(df['time_zone'])
    df['year'] = df['time_zone'].dt.year.astype('int')
    df['month'] = df['time_zone'].dt.month.astype('int')
    df['day'] = df['time_zone'].dt.day.astype('int')
    cols_to_save = ['day', 'month', 'year']
    df.to_csv(outputCsv, columns=cols_to_save, index=False, mode='a')
    os.remove(inputCsv)
        
    
def main():
    unpMeExt()
    runner(bashFile ="logana/processes/scripts/extractBots.sh", inputFile='logana/input.log')
    logex('logana/processes/bots.log', 'logana/processes/bots.csv')
    runner(bashFile="logana/processes/scripts/rtsplit.sh")
    colDefiner('logana/processes/bots.csv', 'logana/processes/semiPreparedTemp.csv')
    runner(bashFile="logana/processes/scripts/dateExtractor.sh")
    colSplitter('logana/processes/rt.csv', 'logana/processes/semiPreparedTempSpl.csv')
    dateSplitter('logana/processes/dates.csv', 'logana/processes/splittedDates.csv')
    domainSetter('logana/processes/semiPreparedTempSpl.csv', 'https://www.goal.pl', 'logana/processes/semiPreparedSplitted.csv')
    concater('logana/processes/semiPreparedTemp.csv', 'logana/processes/semiPreparedSplitted.csv','logana/processes/splittedDates.csv', 'logana/processes/concatenated.csv')
    agentTweaker('logana/processes/concatenated.csv', 'logana/processes/semi_1Prepared.csv')
    typeTweaker('logana/processes/semi_1Prepared.csv', 'logana/processes/finalUnverified.csv')
    verificator('logana/processes/uniq.txt', 'logana/processes/verIps.csv', cond=True)
    merger('logana/processes/finalUnverified.csv', 'logana/processes/verIps.csv', mergeOn='host_ip', cond=True)
    typeSetter('logana/processes/finalVerified.csv', 'logana/processes/final.csv')
    runner(bashFile="logana/processes/scripts/mover.sh")
    runner(bashFile="logana/processes/scripts/finalCleaner.sh")
    gc.collect()


    
if __name__=="__main__":
    main()                               
