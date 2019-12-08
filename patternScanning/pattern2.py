#!/usr/bin/python

from datetime import datetime, timedelta
import pymongo
import StockLib
import sys

client = pymongo.MongoClient('mongodb://mongodb_host:27017/')
db = client['stock']

stockLib = StockLib.StockLib()

startDate = sys.argv[1] if len(sys.argv)>=2 else '2014-01-01'
endDate = sys.argv[2] if len(sys.argv)>=3 else '2020-01-01'
limit = int(sys.argv[3]) if len(sys.argv)>=4 else 0

symbols = stockLib.getStockSymbols(db, startDate, endDate, 10)
for i in range(len(symbols)):
    if i<limit:
        continue
    symbol = symbols[i]
    print('Processing ' + symbol)

    data = stockLib.getRevenueIncrease(db, symbol, startDate, endDate)
    totalReturn = 0
    for d in data:
        # print(d)
        sharpe = stockLib.calSharpe(db, d['symbol'], d['date'])
        sharpe1w = stockLib.calSharpe(db, d['symbol'], (datetime.strptime(d['date'], '%Y-%m-%d') + timedelta(days=7)).date().strftime("%Y-%m-%d"))
        sharpe1m = stockLib.calSharpe(db, d['symbol'], (datetime.strptime(d['date'], '%Y-%m-%d') + timedelta(days=30)).date().strftime("%Y-%m-%d"))
        sharpe3m = stockLib.calSharpe(db, d['symbol'], (datetime.strptime(d['date'], '%Y-%m-%d') + timedelta(days=92)).date().strftime("%Y-%m-%d"))
        sharpe1y = stockLib.calSharpe(db, d['symbol'], (datetime.strptime(d['date'], '%Y-%m-%d') + timedelta(days=365)).date().strftime("%Y-%m-%d"))
        ir1w = stockLib.calIR(db, d['symbol'], d['date'], (datetime.strptime(d['date'], '%Y-%m-%d') + timedelta(days=7)).date().strftime("%Y-%m-%d"))
        ir1m = stockLib.calIR(db, d['symbol'], d['date'], (datetime.strptime(d['date'], '%Y-%m-%d') + timedelta(days=30)).date().strftime("%Y-%m-%d"))
        ir3m = stockLib.calIR(db, d['symbol'], d['date'], (datetime.strptime(d['date'], '%Y-%m-%d') + timedelta(days=92)).date().strftime("%Y-%m-%d"))
        ir1y = stockLib.calIR(db, d['symbol'], d['date'], (datetime.strptime(d['date'], '%Y-%m-%d') + timedelta(days=365)).date().strftime("%Y-%m-%d"))
        (pct1w, minPct1w, maxPct1w) = stockLib.getReturn(db, d['symbol'], d['date'], 7)
        (pct2w, minPct2w, maxPct2w) = stockLib.getReturn(db, d['symbol'], d['date'], 14)
        (pct3w, minPct3w, maxPct3w) = stockLib.getReturn(db, d['symbol'], d['date'], 21)
        (pct1m, minPct1m, maxPct1m) = stockLib.getReturn(db, d['symbol'], d['date'], 30)
        (pct2m, minPct2m, maxPct2m) = stockLib.getReturn(db, d['symbol'], d['date'], 61)
        (pct3m, minPct3m, maxPct3m) = stockLib.getReturn(db, d['symbol'], d['date'], 92)
        (pct6m, minPct6m, maxPct6m) = stockLib.getReturn(db, d['symbol'], d['date'], 183)
        (pct1y, minPct1y, maxPct1y) = stockLib.getReturn(db, d['symbol'], d['date'], 365)
        # print(i, symbol, d['date'], d['eps'], d['revenue'], d['earnings'], pct1m*100, minPct1m*100, maxPct1m*100, sharpe3m, ir3m)
        print('%d %-8s Date=%s\teps=%6.02f\trevenue=%8.02f\tearnings=%8.02f\tPct1m = %6.02f%%\tMin Pct1m = %6.02f%%\tMax Pct1m = %6.02f%%\tSharpe=%6.03f IR=%6.03f' % (i, symbol, d['date'], d['eps'] if d['eps']!=None else 0, d['revenue'], d['earnings'], pct1m*100, minPct1m*100, maxPct1m*100, sharpe3m, ir3m))
        totalReturn += pct1m
        # save to patternStats
        stockLib.savePatternStats(db, 2, d['date'], symbol, \
            d['price'], d['marketCap'], d['eps'], d['revenue'], d['earnings'], d['pe'], d['sector'], d['industry'], \
            d['perfMonth'], d['perfQuarter'], \
            sharpe, sharpe1w, sharpe1m, sharpe3m, sharpe1y, \
            ir1w, ir1m, ir3m, ir1y, \
            pct1w, minPct1w, maxPct1w, \
            pct2w, minPct2w, maxPct2w, \
            pct3w, minPct3w, maxPct3w, \
            pct1m, minPct1m, maxPct1m, \
            pct2m, minPct2m, maxPct2m, \
            pct3m, minPct3m, maxPct3m, \
            pct6m, minPct6m, maxPct6m, \
            pct1y, minPct1y, maxPct1y)
    if len(data):
        totalReturn /= len(data)
    print('Average 1m return for %s revenue increase between %s and %s: %6.02f%% (%d)\n' % (symbol, startDate, endDate, totalReturn*100, len(data)))

    print('')
