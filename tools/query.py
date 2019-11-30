#!/usr/bin/python

'''
This script runs mongo queries and output in an aligned structure(like MySQL) unlike the default output in Mongo shell

It connects to mongodb_host(defined in your hosts file)'s stock database.

Its first parameter is a file which contains a Mongo query.

If not parameter specified, usuage will be printed out.
'''

import ast
import pymongo
import re
import sys
import time

'''
    Parse mongo query string, split it to three parts
    Input: mongo query string
    Output: query string part, sort part, limit part
'''
def parseMongoQuery(queryStr):
    sort = '{}'
    limit = ''
    parts = queryStr.split('.sort')
    query = parts[0]
    if len(parts)>1:
        sort = parts[1]
        parts = sort.split('.limit')
        if len(parts)>1:
            sort = parts[0]
            sort = sort[1:len(sort)-1]
            limit = parts[1]
            limit = limit[1:len(limit)-1]
        else:
            sort = sort[1:len(sort)-1]
    else:
        parts = queryStr.split('.limit')
        if len(parts)>1:
            query = parts[0]
	    limit = parts[1]
            limit = limit[1:len(limit)-1]

    return (query, sort, limit)

'''
    Turn json like sortStr into Python array that can be used in pymongo sort()
    Input: sort string
    Output: pymongo sort() array
'''
def getSortParams(sortStr):
    sortParamsArray = []
    if sortStr == '{}':
	return sortParamsArray
    sortStr = sortStr[1:len(sortStr)-1]
    parts = sortStr.split(',')
    for p in parts:
	params = p.split(':')
	key = params[0].strip()
	key = key[1:len(key)-1]
	value = params[1].strip()
	value = int(value)
	sortParamsArray.append((key, value))
    return sortParamsArray

client = pymongo.MongoClient("mongodb://mongodb_host:27017/")
db = client['stock']

if len(sys.argv)<2:
    print '''
    Usage:
        python query.py <mongo query file>
    '''
    sys.exit()

filename = sys.argv[1]

f = open(filename, 'r')
queryStr = f.read().replace('\n', '')
(queryStr, sortStr, limitStr) = parseMongoQuery(queryStr)

# main regular expression
matches = re.match('db\.(\w+)\.(\w+)\((.*)\)(\.sort\(.*\))?(\.limit\(.*\))?', queryStr)
if matches:

    start = time.time()

    collectionName = matches.groups()[0]
    action = matches.groups()[1]
    sortParams = getSortParams(sortStr)
    limitParam = limitStr
    if limitStr!='':
        limitParam = int(limitStr)

    # get collection and run the query
    collection = db[collectionName]
    if action=='aggregate':
        params = ast.literal_eval(matches.groups()[2])
        cursor = collection.aggregate(params)
    elif action=='find':
        params = ast.literal_eval('[' + matches.groups()[2] + ']')
        cond = params[0]
        output = {}
        if len(params)>1:
            output = params[1]
	if len(sortParams)>0 and limitParam:
            cursor = collection.find(cond, output).sort(sortParams).limit(limitParam)
        elif len(sortParams)>0:
            cursor = collection.find(cond, output).sort(sortParams)
        elif limitParam:
            cursor = collection.find(cond, output).limit(limitParam)
        else:
            cursor = collection.find(cond, output)

    # get result
    result = list(cursor)

    columns = []
    maxLength = {}
    align = {}

    # get columns
    if result[0]:
        columns = result[0].keys()

    # figure out each column's max length
    for x in result:
        for k in columns:
            if k not in maxLength or len(str(x[k]))>maxLength[k]:
                maxLength[k] = len(str(x[k]))
            if k not in align:
                if type(x[k])==type(1) or type(x[k])==type(0.1):
                    align[k] = ''
                else:
                    align[k] = '-'

    # figure out header and data row's format string
    fmtHeader =  ''
    fmtData = ''
    for k in columns:
        fmtHeader += '%-' + str(maxLength[k]) + 's' + '    '
        fmtData += '%' + align[k] + str(maxLength[k]) + 's' + '    '

    # print header
    print(fmtHeader % tuple(columns))

    # print data
    for x in result:
        data = []
        for k in columns:
	    value = x[k]
	    # do not output \N, make it blank
	    if value == '\\N':
		value = ''
            data.append(value)
        print(fmtData % tuple(data))

    end = time.time()
    print('%d row in set (%f sec)' % (len(result), end - start))

else:
    print("Do not find a Mongo query.")
