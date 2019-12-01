#!/usr/bin/python

from datetime import datetime, timedelta
import pymongo
import re

class StockLib:

    def getReturn(self, db, symbol, dateStr, days):
        finvizDaily = db['finvizDaily']
        splitHistory = db['splitHistory']
        match = re.search(r'\d{4}-\d{2}-\d{2}', dateStr)
        date = datetime.strptime(match.group(), '%Y-%m-%d').date()
        days_later = date + timedelta(days=days)
        queryStart = {
            'symbol': symbol,
            'date': {'$gte': date.strftime('%Y-%m-%d')}
        }
        queryEnd = {
            'symbol': symbol,
            'date': {'$lte': days_later.strftime('%Y-%m-%d')}
        }
        queryAll = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': date.strftime('%Y-%m-%d')}},
                {'date': {'$lte': days_later.strftime('%Y-%m-%d')}}
            ]
        }

        cursor = splitHistory.find(queryAll).sort([('date',1)])
        resultSplitHistory = list(cursor)
        totalSplitRatio = 1
        for s in resultSplitHistory:
            totalSplitRatio *= s['ratio']

        cursor = finvizDaily.find(queryStart).sort([('date',1)]).limit(1)
        resultStart = list(cursor)[0]
        cursor = finvizDaily.find(queryEnd).sort([('date',-1)]).limit(1)
        resultEnd = list(cursor)[0]
        priceStart = resultStart['price']
        priceEnd = resultEnd['price'] * totalSplitRatio
        pct = (priceEnd- priceStart) / priceStart

        cursor = finvizDaily.find(queryAll).sort([('date',1)])
        result = list(cursor)
        minPrice = priceStart
        maxPrice = priceStart
        splitRatio = 1
        splitRatioIndex = 0
        for r in result:
            if r['date']==resultStart['date']:
                next
            if len(resultSplitHistory)>0 and splitRatioIndex<len(resultSplitHistory) and r['date']==resultSplitHistory[splitRatioIndex]['date']:
                splitRatio *= resultSplitHistory[splitRatioIndex]['ratio']
                splitRatioIndex += 1
            price = r['price'] * splitRatio
            if price > maxPrice:
                maxPrice = price
            if price < minPrice:
                minPrice = price
        maxPct = (maxPrice - priceStart) / priceStart
        minPct = (minPrice - priceStart) / priceStart

        return (pct, minPct, maxPct)

    def getEpsIncrease(self, db, symbol, startDateStr, endDateStr):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}}
            ]
        }
        output = {'symbol':1, 'eps':1, 'date':1,'_id':0}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        data = []
        for i in range(1,len(result)):
            if result[i]['eps']!='\N' and result[i-1]['eps']!='\N' and result[i]['eps']>result[i-1]['eps']:
                data.append(result[i])
        return data

    def getRevenueIncrease(self, db, symbol, startDateStr, endDateStr):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}}
            ]
        }
        output = {'symbol':1, 'marketCap':1, 'ps':1, 'date':1,'_id':0}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        data = []
        for i in range(1,len(result)):
            if result[i]['ps']!='\N' and result[i-1]['ps']!='\N' and result[i]['marketCap']!='\N' and result[i-1]['marketCap']!='\N':
                previousRevenue = result[i-1]['marketCap'] / result[i-1]['ps']
                currentRevenue = result[i]['marketCap'] / result[i]['ps']
                revenueChange = (currentRevenue - previousRevenue)/previousRevenue
                if revenueChange>0.01:
                    result[i]['revenue'] = result[i]['marketCap'] / result[i]['ps']
                    data.append(result[i])
        return data

    def getRevenueAndEpsIncrease(self, db, symbol, startDateStr, endDateStr):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}}
            ]
        }
        output = {'symbol':1, 'marketCap':1, 'eps':1, 'ps':1, 'date':1,'_id':0}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        data = []
        for i in range(1,len(result)):
            if result[i]['ps']!='\N' and result[i-1]['ps']!='\N' and result[i]['marketCap']!='\N' and result[i-1]['marketCap']!='\N' and result[i]['eps']!='\N' and result[i-1]['eps']!='\N':
                previousRevenue = result[i-1]['marketCap'] / result[i-1]['ps']
                currentRevenue = result[i]['marketCap'] / result[i]['ps']
                revenueChange = (currentRevenue - previousRevenue)/previousRevenue
                if revenueChange>0.01 and result[i]['eps']>result[i-1]['eps']:
                    result[i]['revenue'] = result[i]['marketCap'] / result[i]['ps']
                    data.append(result[i])
        return data

    def getRevenueOrEpsIncrease(self, db, symbol, startDateStr, endDateStr):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}}
            ]
        }
        output = {'symbol':1, 'marketCap':1, 'eps':1, 'ps':1, 'date':1,'_id':0}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        data = []
        for i in range(1,len(result)):
            if result[i]['ps']!='\N' and result[i-1]['ps']!='\N' and result[i]['marketCap']!='\N' and result[i-1]['marketCap']!='\N' and result[i]['eps']!='\N' and result[i-1]['eps']!='\N':
                previousRevenue = result[i-1]['marketCap'] / result[i-1]['ps']
                currentRevenue = result[i]['marketCap'] / result[i]['ps']
                revenueChange = (currentRevenue - previousRevenue)/previousRevenue
                if (revenueChange>0.01 and result[i]['eps']>result[i-1]['eps']) or (abs(revenueChange)<0.005 and result[i]['eps']>result[i-1]['eps']) or (revenueChange>0.01 and result[i]['eps']==result[i-1]['eps']):
                    result[i]['revenue'] = result[i]['marketCap'] / result[i]['ps']
                    data.append(result[i])
        return data

    def getStockSymbols(self, db, startDateStr, endDateStr):
        finvizDaily = db['finvizDaily']
        query = {
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}},
                {'symbol': {'$ne':'GOOG'}},
                {'symbol': {'$ne':'BRK-B'}},
                {'symbol': {'$ne':'RDS-B'}},
                {'symbol': {'$ne':'PBR-A'}},
                {'industry': { '$ne': 'Exchange Traded Fund' }},
                {'marketCap': {'$gte': 100000}}
            ]
        }
        cursor = finvizDaily.distinct('symbol', query)
        result = list(cursor)
	return result

    pass
