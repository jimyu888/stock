#!/usr/bin/python

import csv
from   os import listdir
import pymongo
import re
import sys

def saveMin1ToMongo(min1, data):
	for d in data:
		min1.update({"symbol": d['symbol'], "date": d['date']}, {"$set": d}, upsert=True)

## MAIN ##
if len(sys.argv)<2:
	print('Usage: ./loadMin1.py <min 1 data file dir>')
	sys.exit(0)
dir = sys.argv[1]

client = pymongo.MongoClient('mongodb://mongodb_host:27017/')
db = client['stock']
min1 = db['min1']

files = [f for f in listdir(dir) if re.match(r'SPY_\d+.min1', f)]
for file in files:
	print('Processing %s ...' % (file))
	min1_data = []
	filename = dir + '/' + file
	with open(filename, 'r') as f:
	    reader = csv.reader(f, dialect='excel-tab')
	    i = 0
	    for data in reader:
		i = i + 1
		md = {
			'symbol': data[0],
			'date': data[1],
			'open': data[2],
			'high': data[3],
			'low': data[4],
			'close': data[5],
			'volume': data[6],
			'deals': data[7],
			'wap': data[8],
			'gap': data[9]
		}
		min1_data.append(md)
	print('\tLoading %d rows of data' % (len(min1_data)))
	saveMin1ToMongo(min1, min1_data)
