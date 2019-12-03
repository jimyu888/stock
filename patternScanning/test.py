#!/usr/bin/python

import pymongo
import StockLib

client = pymongo.MongoClient('mongodb://mongodb_host:27017/')
db = client['stock']

stockLib = StockLib.StockLib()

startDate = '2015-04-30'
endDate = '2015-04-30'

symbols = stockLib.getStockSymbols(db, startDate, endDate, 100)
for i in range(len(symbols)):
    symbol = symbols[i]
    if type(symbol)==type('abc'):
        continue
    print(symbol)
    print(type(symbol))
print(len(symbols))
