#!/usr/bin/python

import pymongo
import StockLib

client = pymongo.MongoClient('mongodb://mongodb_host:27017/')
db = client['stock']

stockLib = StockLib.StockLib()

startDate = '2014-01-01'
endDate = '2019-01-01'

symbols = stockLib.getStockSymbols(db, startDate, endDate, 10)
for i in range(len(symbols)):
    if i>2:
	break
    symbol = symbols[i]

    data = stockLib.getEpsIncrease(db, symbol, startDate, endDate)
    totalReturn = 0
    for d in data:
        (pct1w, minPct1w, maxPct1w) = stockLib.getReturn(db, d['symbol'], d['date'], 7)
        (pct2w, minPct2w, maxPct2w) = stockLib.getReturn(db, d['symbol'], d['date'], 14)
        (pct3w, minPct3w, maxPct3w) = stockLib.getReturn(db, d['symbol'], d['date'], 21)
        (pct1m, minPct1m, maxPct1m) = stockLib.getReturn(db, d['symbol'], d['date'], 30)
        (pct2m, minPct2m, maxPct2m) = stockLib.getReturn(db, d['symbol'], d['date'], 61)
        (pct3m, minPct3m, maxPct3m) = stockLib.getReturn(db, d['symbol'], d['date'], 92)
        (pct6m, minPct6m, maxPct6m) = stockLib.getReturn(db, d['symbol'], d['date'], 183)
        (pct1y, minPct1y, maxPct1y) = stockLib.getReturn(db, d['symbol'], d['date'], 365)
        print('Date=%s\teps=%6.02f\trevenue=%8.02f\tearnings=%8.02f\tPct1w = %6.02f%%\tMin Pct1w = %6.02f%%\tMax Pct1w = %6.02f%%' % (d['date'], d['eps'], d['revenue'], d['earnings'], pct1w*100, minPct1w*100, maxPct1w*100))
        totalReturn += pct1w
        # save to patternStats
        stockLib.savePatternStats(db, 1, d['date'], symbol, \
            d['price'], d['marketCap'], d['eps'], d['revenue'], d['earnings'], d['pe'], d['sector'], d['industry'], \
            d['perfMonth'], d['perfQuarter'], \
            pct1w, minPct1w, maxPct1w, \
            pct2w, minPct2w, maxPct2w, \
            pct3w, minPct3w, maxPct3w, \
            pct1m, minPct1m, maxPct1m, \
            pct2m, minPct2m, maxPct2m, \
            pct3m, minPct3m, maxPct3m, \
            pct6m, minPct6m, maxPct6m, \
            pct1y, minPct1y, maxPct1y)
    totalReturn /= len(data)
    print('Average return for %s eps increase between %s and %s: %6.02f%% (%d)\n' % (symbol, startDate, endDate, totalReturn*100, len(data)))

    print('')
