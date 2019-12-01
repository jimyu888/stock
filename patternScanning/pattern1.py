#!/usr/bin/python

import pymongo
import StockLib

client = pymongo.MongoClient('mongodb://mongodb_host:27017/')
db = client['stock']

stockLib = StockLib.StockLib()

startDate = '2014-01-01'
endDate = '2019-01-01'

symbols = stockLib.getStockSymbols(db, startDate, endDate)
for i in range(len(symbols)):
    if i>2:
	break
    symbol = symbols[i]

    '''
    data = stockLib.getEpsIncrease(db, symbol, startDate, endDate)
    totalReturn = 0
    for d in data:
        (pct, minPct, maxPct) = stockLib.getReturn(db, d['symbol'], d['date'], 90)
        print('Date=%s\teps=%6.02f\tPct = %6.02f%%\tMin Pct = %6.02f%%\tMax Pct = %6.02f%%' % (d['date'], d['eps'], pct*100, minPct*100, maxPct*100))
        totalReturn += pct
    totalReturn /= len(data)
    print('Average return for %s eps increase between %s and %s: %6.02f%% (%d)\n' % (symbol, startDate, endDate, totalReturn*100, len(data)))

    totalReturn = 0
    data = stockLib.getRevenueIncrease(db, symbol, startDate, endDate)
    for d in data:
        (pct, minPct, maxPct) = stockLib.getReturn(db, d['symbol'], d['date'], 90)
        print('Date=%s\tRevenue=%10.02f\tPct = %6.02f%%\tMin Pct = %6.02f%%\tMax Pct = %6.02f%%' % (d['date'], d['revenue'], pct*100, minPct*100, maxPct*100))
        totalReturn += pct
    totalReturn /= len(data)
    print('Average return for %s revenue increase between %s and %s: %6.02f%% (%d)\n' % (symbol, startDate, endDate, totalReturn*100, len(data)))

    totalReturn = 0
    data = stockLib.getRevenueOrEpsIncrease(db, symbol, startDate, endDate)
    for d in data:
        (pct, minPct, maxPct) = stockLib.getReturn(db, d['symbol'], d['date'], 90)
        print('Date=%s\tRevenue=%10.02f\teps=%6.02f\tPct = %6.02f%%\tMin Pct = %6.02f%%\tMax Pct = %6.02f%%' % (d['date'], d['revenue'], d['eps'], pct*100, minPct*100, maxPct*100))
        totalReturn += pct
    totalReturn /= len(data)
    print('Average return for %s revenue|eps increase between %s and %s: %6.02f%% (%d)\n' % (symbol, startDate, endDate, totalReturn*100, len(data)))
    '''

    totalReturn = 0
    data = stockLib.getRevenueAndEpsIncrease(db, symbol, startDate, endDate)
    for d in data:
        (pct1w, minPct1w, maxPct1w) = stockLib.getReturn(db, d['symbol'], d['date'], 7)
        (pct2w, minPct2w, maxPct2w) = stockLib.getReturn(db, d['symbol'], d['date'], 14)
        (pct3w, minPct3w, maxPct3w) = stockLib.getReturn(db, d['symbol'], d['date'], 21)
        (pct1m, minPct1m, maxPct1m) = stockLib.getReturn(db, d['symbol'], d['date'], 30)
        (pct2m, minPct2m, maxPct2m) = stockLib.getReturn(db, d['symbol'], d['date'], 61)
        (pct3m, minPct3m, maxPct3m) = stockLib.getReturn(db, d['symbol'], d['date'], 92)
        print('Date=%s\tRevenue=%10.02f\teps=%6.02f\tPct = %6.02f%%\tMin Pct = %6.02f%%\tMax Pct = %6.02f%%' % (d['date'], d['revenue'], d['eps'], pct1w*100, minPct1w*100, maxPct1w*100))
        totalReturn += pct1m
        # TODO:
        # save to patternStats

    totalReturn /= len(data)
    print('Average return for %s revenue and eps increase between %s and %s: %6.02f%% (%d)\n' % (symbol, startDate, endDate, totalReturn*100, len(data)))

    print('')
