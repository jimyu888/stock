#!/usr/bin/python

'''
This script calculates sharpe ratio

'''

import datetime
import pymongo
import pandas as pd
import numpy as np
import sys

def getDailyPct(db, symbol, dateStr):
    finvizDaily = db['finvizDaily']
    startDateStr = (datetime.datetime.strptime(dateStr, '%Y-%m-%d') - datetime.timedelta(days=30.4167)).date().strftime("%Y-%m-%d")
    query = {
        'symbol': symbol,
        '$and': [
            {'date': {'$gt': startDateStr}},
            {'date': {'$lte': dateStr}}
        ]
    }
    output = {'symbol':1, 'date':1, '_id':0, 'price':1, 'pct':1}
    cursor = finvizDaily.find(query, output).sort([('date',1)])
    result = list(cursor)
    return result

def getTNX(db, dateStr):
    TNX = db['TNX']
    startDateStr = (datetime.datetime.strptime(dateStr, '%Y-%m-%d') - datetime.timedelta(days=30.4167)).date().strftime("%Y-%m-%d")
    query = {
        '$and': [
            {'Date': {'$gt': startDateStr}},
            {'Date': {'$lte': dateStr}}
        ]
    }
    output = {'Date':1, '_id':0, 'Close':1}
    cursor = TNX.find(query, output).sort([('date',1)])
    result = list(cursor)
    tnx = {}
    for d in result:
        tnx[d['Date']] = d['Close']
    return tnx

def calSharpe(db, symbol, date):
    data = getDailyPct(db, symbol, date)
    tnx = getTNX(db, date)
    rate = 0

    df = pd.DataFrame()
    daily = []
    for d in data:
        if d['date'] in tnx:
            rate = tnx[d['date']]
        print("%s %8.02f %8.02f %f" % (d['date'], d['price'], d['pct'], rate))
        daily.append(d['pct']/100.0 - rate/100.0/252.0)
    df['daily'] = daily

    sharpe = df['daily'].mean()/df['daily'].std()*np.sqrt(252)
    return sharpe

client = pymongo.MongoClient("mongodb://mongodb_host:27017/")
db = client['stock']

symbol = sys.argv[1] if len(sys.argv)>1 else 'AAPL'
date = sys.argv[2] if len(sys.argv)>2 else '2019-01-31'

sharpe = calSharpe(db, symbol, date)
print('Sharpe = %f' % (sharpe))
