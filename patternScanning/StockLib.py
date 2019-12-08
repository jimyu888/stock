#!/usr/bin/python

from datetime import datetime, timedelta
import pymongo
import pandas as pd
import numpy as np
import sys
import re

class StockLib:

    def getDaysDiff(self, date1, date2):
        return (datetime.strptime(date2, '%Y-%m-%d') - datetime.strptime(date2, '%Y-%m-%d')).days

    def getReturn(self, db, symbol, startDate, days, endDate=None):
        finvizDaily = db['finvizDaily']
        splitHistory = db['splitHistory']
        match = re.search(r'\d{4}-\d{2}-\d{2}', startDate)
        date = datetime.strptime(match.group(), '%Y-%m-%d').date()
        days_later = date + timedelta(days=days)
        if not endDate:
            endDate = days_later.strftime('%Y-%m-%d')
        queryStart = {
            'symbol': symbol,
            'date': {'$gte': startDate}
        }
        queryEnd = {
            'symbol': symbol,
            'date': {'$lte': endDate}
        }
        queryAll = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDate}},
                {'date': {'$lte': endDate}}
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
        (pct, maxPct, minPct) = (0, 0, 0)

        if type(priceStart)!=type('string') and priceStart>0 and type(priceEnd)!=type('string') and priceEnd>0:
            pct = (priceEnd - priceStart) / priceStart
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
                if type(price)!=type('string') and price > maxPrice:
                    maxPrice = price
                if type(price)!=type('string') and price < minPrice:
                    minPrice = price
            maxPct = (maxPrice - priceStart) / priceStart
            minPct = (minPrice - priceStart) / priceStart

        return (pct, minPct, maxPct)

    def calcRevenue(self, data):
        if 'marketCap' in data and data['marketCap'] and data['marketCap']!='\\N' and 'ps' in data and data['ps'] and data['ps']!='\\N':
            data['revenue'] = data['marketCap'] / data['ps']
        else:
            data['revenue'] = 0

    def calcEarnings(self, data):
        if 'outstandingShares' in data and data['outstandingShares'] and data['outstandingShares']!='\\N' and 'eps' in data and data['eps'] and data['eps']!='\\N':
            data['earnings'] = data['outstandingShares'] * data['eps']
        else:
            data['earnings'] = 0

    def getEpsIncrease(self, db, symbol, startDateStr, endDateStr, increase=True):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}}
            ]
        }
        output = {'symbol':1, 'marketCap':1, 'ps':1, 'eps':1, 'date':1, '_id':0, 'price':1, 'pe':1, 'sector':1, 'industry':1, 'outstandingShares':1, 'perfMonth':1, 'perfQuarter':1}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        data = []
        for i in range(1,len(result)):
            if result[i]['eps']!='\\N' and result[i-1]['eps']!='\\N' and self.getDaysDiff(result[i-1]['date'], result[i]['date'])<=3:
                self.calcRevenue(result[i])
                self.calcEarnings(result[i])
                if increase and result[i]['eps']>result[i-1]['eps']:		# eps increase case
                    data.append(result[i])
                elif not increase and result[i]['eps']<result[i-1]['eps']:	# eps decrease case
                    data.append(result[i])
        return data

    def getRevenueIncrease(self, db, symbol, startDateStr, endDateStr, increase=True):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}}
            ]
        }
        output = {'symbol':1, 'marketCap':1, 'ps':1, 'eps':1, 'date':1, '_id':0, 'price':1, 'pe':1, 'sector':1, 'industry':1, 'outstandingShares':1, 'perfMonth':1, 'perfQuarter':1}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        data = []
        for i in range(1,len(result)):
            if result[i]['ps']!='\\N' and result[i-1]['ps']!='\\N' and result[i-1]['ps'] and result[i]['ps'] and result[i]['marketCap']!='\\N' and result[i-1]['marketCap']!='\\N' and self.getDaysDiff(result[i-1]['date'], result[i]['date'])<=3:
                previousRevenue = result[i-1]['marketCap'] / result[i-1]['ps']
                currentRevenue = result[i]['marketCap'] / result[i]['ps']
                revenueChange = (currentRevenue - previousRevenue)/previousRevenue
                if result[i]['eps']=='\\N':
                    result[i]['eps'] = 0
                self.calcRevenue(result[i])
                self.calcEarnings(result[i])
                if increase and revenueChange>0.01:		# revenue increase case
                    data.append(result[i])
                elif not increase and revenueChange<-0.01:	# revenue decrease case
                    data.append(result[i])
        return data

    def getRevenueAndEpsIncrease(self, db, symbol, startDateStr, endDateStr, increase=True):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}}
            ]
        }
        output = {'symbol':1, 'marketCap':1, 'ps':1, 'eps':1, 'date':1, '_id':0, 'price':1, 'pe':1, 'sector':1, 'industry':1, 'outstandingShares':1, 'perfMonth':1, 'perfQuarter':1}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        data = []
        for i in range(1,len(result)):
            if result[i]['ps']!='\\N' and result[i-1]['ps']!='\\N' and result[i-1]['ps'] and result[i]['ps'] and result[i]['marketCap']!='\\N' and result[i-1]['marketCap']!='\\N' and result[i]['eps']!='\\N' and result[i-1]['eps']!='\\N' and self.getDaysDiff(result[i-1]['date'], result[i]['date'])<=3:
                previousRevenue = result[i-1]['marketCap'] / result[i-1]['ps']
                currentRevenue = result[i]['marketCap'] / result[i]['ps']
                revenueChange = (currentRevenue - previousRevenue)/previousRevenue
                self.calcRevenue(result[i])
                self.calcEarnings(result[i])
                if increase and revenueChange>0.01 and result[i]['eps']>result[i-1]['eps']:
                    # print('%s previous revenue %8.02f current revenue %8.02f increase %6.02f%%; previous eps %6.02f current eps %6.02f increase %6.02f%%' % (result[i]['date'], previousRevenue, currentRevenue, (currentRevenue-previousRevenue)/previousRevenue*100.0, result[i-1]['eps'], result[i]['eps'], (result[i]['eps']-result[i-1]['eps'])/result[i-1]['eps']*100.0))
                    data.append(result[i])
                elif not increase and revenueChange<-0.01 and result[i]['eps']<result[i-1]['eps']:
                    data.append(result[i])
        return data

    def getRevenueOrEpsIncrease(self, db, symbol, startDateStr, endDateStr, increase=True):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDateStr}},
                {'date': {'$lte': endDateStr}}
            ]
        }
        output = {'symbol':1, 'marketCap':1, 'ps':1, 'eps':1, 'date':1, '_id':0, 'price':1, 'pe':1, 'sector':1, 'industry':1, 'outstandingShares':1, 'perfMonth':1, 'perfQuarter':1}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        data = []
        for i in range(1,len(result)):
            if      result[i]['ps']!='\\N' and result[i-1]['ps']!='\\N' and \
                    result[i]['ps']!=None and result[i-1]['ps']!=None and \
                    result[i]['ps'] and result[i-1]['ps'] and \
                    result[i]['marketCap']!='\\N' and result[i-1]['marketCap']!='\\N' and \
                    result[i]['marketCap']!=None and result[i-1]['marketCap']!=None and \
                    result[i]['eps']!='\\N' and result[i-1]['eps']!='\\N' and \
                    result[i]['eps']!=None and result[i-1]['eps']!=None and \
                    self.getDaysDiff(result[i-1]['date'], result[i]['date'])<=3:
                previousRevenue = result[i-1]['marketCap'] / result[i-1]['ps']
                currentRevenue = result[i]['marketCap'] / result[i]['ps']
                revenueChange = (currentRevenue - previousRevenue)/previousRevenue
                self.calcRevenue(result[i])
                self.calcEarnings(result[i])
                if increase and ((revenueChange>0.01 and result[i]['eps']>result[i-1]['eps']) or (abs(revenueChange)<0.005 and result[i]['eps']>result[i-1]['eps']) or (revenueChange>0.01 and result[i]['eps']==result[i-1]['eps'])):
                    data.append(result[i])
                elif not increase and ((revenueChange<-0.01 and result[i]['eps']<result[i-1]['eps']) or (abs(revenueChange)<0.005 and result[i]['eps']<result[i-1]['eps']) or (revenueChange<-0.01 and result[i]['eps']==result[i-1]['eps'])):
                    data.append(result[i])
        return data

    def getOneMonthDailyPct(self, db, symbol, dateStr):
        finvizDaily = db['finvizDaily']
        startDateStr = (datetime.strptime(dateStr, '%Y-%m-%d') - timedelta(days=30.4167)).date().strftime("%Y-%m-%d")
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

    def getDailyPct(self, db, symbol, startDate, endDate):
        finvizDaily = db['finvizDaily']
        query = {
            'symbol': symbol,
            '$and': [
                {'date': {'$gte': startDate}},
                {'date': {'$lte': endDate}}
            ]
        }
        output = {'symbol':1, 'date':1, '_id':0, 'price':1, 'pct':1}
        cursor = finvizDaily.find(query, output).sort([('date',1)])
        result = list(cursor)
        return result

    def getTNX(self, db, dateStr):
        TNX = db['TNX']
        startDateStr = (datetime.strptime(dateStr, '%Y-%m-%d') - timedelta(days=30.4167)).date().strftime("%Y-%m-%d")
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

    def calSharpe(self, db, symbol, date):
        data = self.getOneMonthDailyPct(db, symbol, date)
        rate = 0
        sharpe = 0

        if len(data)>=15:
            tnx = self.getTNX(db, date)
            df = pd.DataFrame()
            daily = []
            for d in data:
                if d['date'] in tnx:
                    rate = tnx[d['date']]
                # print("%s %8.02f %8.02f %f" % (d['date'], d['price'], d['pct'], rate))
                if d['pct']!='\\N' and rate!='\\N':
                    daily.append(d['pct']/100.0 - rate/100.0/252.0)
            df['daily'] = daily
            sharpe = df['daily'].mean()/df['daily'].std()*np.sqrt(252)

        return sharpe

    def calIR(self, db, symbol, startDate, endDate, irSymbol='SPY'):
        data = self.getDailyPct(db, symbol, startDate, endDate)
        dataIR = self.getDailyPct(db, irSymbol, startDate, endDate)
        ir = 0
    
        irHash = {}
        for d in dataIR:
            irHash[d['date']] = d['pct']

        if len(data)>0:
            (pct, minPct, maxPct) = self.getReturn(db, symbol, startDate, 0, endDate)
            (pctIR, minPctIR, maxPctIR) = self.getReturn(db, irSymbol, startDate, 0, endDate)
            df = pd.DataFrame()
            daily = []
            for d in data:
                if d['pct']!='\\N' and d['date'] in irHash and irHash[d['date']]!='\\N':
                    # print(d['pct'], irHash[d['date']])
                    daily.append(d['pct']/100.0 - irHash[d['date']]/100.0)
            df['daily'] = daily
            ir = (pct - pctIR) / df['daily'].std()

        return ir


    def getStockSymbols(self, db, startDateStr, endDateStr, marketCapThreshold):
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
                {'marketCap': {'$gte': marketCapThreshold}}
            ]
        }
        cursor = finvizDaily.distinct('symbol', query)
        result = list(cursor)
        result.sort()
        return result

    def savePatternStats(self, db, patternId, \
            date, symbol, \
            price, marketCap, eps, revenue, earnings, pe, sector, industry, \
            perfMonth, perfQuarter, \
            sharpe, sharpe1w, sharpe1m, sharpe3m, sharpe1y, \
            ir1w, ir1m, ir3m, ir1y, \
            pct1w, minPct1w, maxPct1w, \
            pct2w, minPct2w, maxPct2w, \
            pct3w, minPct3w, maxPct3w, \
            pct1m, minPct1m, maxPct1m, \
            pct2m, minPct2m, maxPct2m, \
            pct3m, minPct3m, maxPct3m, \
            pct6m, minPct6m, maxPct6m, \
            pct1y, minPct1y, maxPct1y):
        patternStats = db['patternStats']
        (pct1wSPY, minPct1wSPY, maxPct1wSPY) = self.getReturn(db, 'SPY', date, 7)
        (pct1mSPY, minPct1mSPY, maxPct1mSPY) = self.getReturn(db, 'SPY', date, 30)
        (pct3mSPY, minPct3mSPY, maxPct3mSPY) = self.getReturn(db, 'SPY', date, 92)
        (pct1ySPY, minPct1ySPY, maxPct1ySPY) = self.getReturn(db, 'SPY', date, 365)
        data = {
            'patternId': patternId,
            'date': date,
            'symbol': symbol,
            'price': price,
            'marketCap': marketCap,
            'eps': eps,
            'revenue': revenue,
            'earnings': earnings,
            'pe': pe,
            'sector': sector,
            'industry': industry,
            'perfMonth': perfMonth,
            'perfQuarter': perfQuarter,
            'sharpe': sharpe, 'sharpe1w': sharpe1w, 'sharpe1m': sharpe1m, 'sharpe3m': sharpe3m, 'sharpe1y': sharpe1y,
            'ir1w': ir1w, 'ir1m': ir1m, 'ir3m': ir3m, 'ir1y': ir1y,
            'pct1w': pct1w, 'minPct1w': minPct1w, 'maxPct1w': maxPct1w,
            'pct2w': pct2w, 'minPct2w': minPct2w, 'maxPct2w': maxPct2w,
            'pct3w': pct3w, 'minPct3w': minPct3w, 'maxPct3w': maxPct3w,
            'pct1m': pct1m, 'minPct1m': minPct1m, 'maxPct1m': maxPct1m,
            'pct2m': pct2m, 'minPct2m': minPct2m, 'maxPct2m': maxPct2m,
            'pct3m': pct3m, 'minPct3m': minPct3m, 'maxPct3m': maxPct3m,
            'pct6m': pct6m, 'minPct6m': minPct6m, 'maxPct6m': maxPct6m,
            'pct1y': pct1y, 'minPct1y': minPct1y, 'maxPct1y': maxPct1y,
            'pct1wSPY': pct1wSPY,
            'pct1mSPY': pct1mSPY,
            'pct3mSPY': pct3mSPY,
            'pct1ySPY': pct1ySPY
        }
        patternStats.update({"patternId": patternId, "date": date, "symbol": symbol}, {"$set": data}, upsert=True)
        pass

    pass
