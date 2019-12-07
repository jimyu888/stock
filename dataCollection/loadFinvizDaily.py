#!/usr/bin/python

import sys
import MySQLdb as mysql
import pymongo
from datetime import date, datetime
from decimal import Decimal

def getDailyData(startDate, endDate):
	connection = mysql.connect('192.168.0.199','stock','dreaming','stock')
	cursor = connection.cursor(mysql.cursors.DictCursor)
	sql = 'SELECT	s.symbol,s.date,s.company,s.sector,s.industry,s.country,s.marketCap,s.pe,s.price,s.pct,s.volume, ' + \
		'	d.forwardPE,d.peg,d.ps,d.pb,d.pc,d.pfcf,d.dividendYield,d.payoutRatio,d.eps,d.epsTY,d.epsNY,d.epsPast5Y,d.epsNext5Y,d.salesPast5Y,d.epsQQ,d.salesQQ,d.outstandingShares,d.floatShares,d.insiderOwn,d.insiderTrans,d.instituteOwn,d.instituteTrans,d.floatShort,d.shortRatio,d.roa,d.roe,d.roi,d.currentRatio,d.quickRatio,d.longTermDebtToEquity,d.debtToEquity,d.grossMargin,d.operatingMargin,d.profitMargin,d.perfWeek,d.perfMonth,d.perfQuarter,d.perfHalfYear,d.perfYear,d.perfYTD,d.beta,d.atr,d.volatilityWeek,d.volatilityMonth,d.sma20,d.sma50,d.sma200,d.high50D,d.low50D,d.high52W,d.low52W,d.rsi,d.pctFromOpen,d.gap,d.recom,d.volumeAvg,d.volumeRel,d.er ' + \
		' FROM finvizDailySummary s' + \
		' LEFT JOIN finvizDailyDetails d ON (s.symbol=d.symbol and s.date=d.date) ' + \
		" WHERE s.date>='" + startDate + "'" + \
		"   AND s.date<='" + endDate + "'"
	# print(sql)
	cursor.execute(sql)
	data = cursor.fetchall()
	daily = []
	fields = ['marketCap','pe','price','pct','volume','forwardPE','peg','ps','pb','pc','pfcf','dividendYield','payoutRatio','eps','epsTY','epsNY','epsPast5Y','epsNext5Y','salesPast5Y','epsQQ','salesQQ','outstandingShares','floatShares','insiderOwn','insiderTrans','instituteOwn','instituteTrans','floatShort','shortRatio','roa','roe','roi','currentRatio','quickRatio','longTermDebtToEquity','debtToEquity','grossMargin','operatingMargin','profitMargin','perfWeek','perfMonth','perfQuarter','perfHalfYear','perfYear','perfYTD','beta','atr','volatilityWeek','volatilityMonth','sma20','sma50','sma200','high50D','low50D','high52W','low52W','rsi','pctFromOpen','gap','recom','volumeAvg','volumeRel']
	for d in data:
		d['date'] = d['date'].strftime("%Y-%m-%d")
		d['er'] = d['er'].strftime("%Y-%m-%d %H:%M:%S") if d['er']!=None else ''
		for f in fields:
			# print(f, d[f], type(d[f]))
			if type(d[f])==type(Decimal('1.23')):
				d[f] = float(d[f])
		daily.append(d)
	return daily

def saveDailyToMongo(data):
	client = pymongo.MongoClient('mongodb://mongodb_host:27017/')
	db = client['stock']
	finvizDaily = db['finvizDaily']
	for d in data:
		finvizDaily.update({"symbol": d['symbol'], "date": d['date']}, {"$set": d}, upsert=True)


## MAIN ##

# get command line parameters
startDate = sys.argv[1] if (len(sys.argv)>=2 and sys.argv[1]!='') else date.today().strftime("%Y-%m-%d")
endDate = sys.argv[2] if (len(sys.argv)>=3 and sys.argv[2]!='') else date.today().strftime("%Y-%m-%d")
print 'Start Date :', startDate
print 'End Date   :', endDate
data = getDailyData(startDate, endDate)
saveDailyToMongo(data)
