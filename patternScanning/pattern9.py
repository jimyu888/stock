#!/usr/bin/python

import pymongo
import StockLib
from datetime import datetime, timedelta

client = pymongo.MongoClient('mongodb://mongodb_host:27017/')
db = client['stock']

stockLib = StockLib.StockLib()

startDate = '2014-01-01'
endDate = '2020-01-01'

'''
Each day, get top earnings estimates increased top 20 industries, check its stocks' performance

SET @date = '2019-11-25'; 

SELECT	s.sector, REPLACE(s.industry, '&amp;', '&') AS industry, count(*) as count, 
	SUM(d.marketCap) AS marketCap, 
	SUM(d.marketCap/d.ps) AS revenue, 
	SUM(d.eps*d.outstandingShares) AS earnings, 
	SUM(d.marketCap)/SUM(d.eps*d.outstandingShares) AS PE, 
	SUM(IF(d.forwardPE>0, d.marketCap/d.forwardPE, d.eps*d.outstandingShares)) AS forwardEarnings, 
	SUM(d.marketCap)/SUM(IF(d.forwardPE>0, d.marketCap/d.forwardPE, d.eps*d.outstandingShares)) AS ForwardPE, 
	SUM(IF(d.forwardPE>0, d.marketCap/d.forwardPE, d.eps*d.outstandingShares)) - SUM(d.outstandingShares*d.eps) AS earningsDiff, 
	(SUM(IF(d.forwardPE>0, d.marketCap/d.forwardPE, d.eps*d.outstandingShares)) - SUM(d.outstandingShares*d.eps))*100/SUM(d.marketCap/d.ps) AS MarginImprovement, 
	AVG(d.epsQQ), 
	AVG(d.epsTY), 
	AVG(d.epsNY), 
	AVG(d.epsNext5Y) 

 FROM finvizDailySummary s 
 JOIN finvizDailyDetails d ON (d.symbol = s.symbol AND d.date = s.date) 

WHERE s.date = @date 
  AND d.symbol not in ('GOOG', 'BRK-B', 'RDS-B', 'PBR-A') 
  AND s.industry <> 'Exchange Traded Fund' 
  AND s.marketCap > 10

GROUP BY 1, 2 
HAVING MarginImprovement > 10 and count>=3
ORDER BY MarginImprovement DESC
LIMIT 20; 

'''
