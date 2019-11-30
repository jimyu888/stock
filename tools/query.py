#!/usr/bin/python

import ast
import pymongo
import re
import sys

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
    return (query, sort, limit)

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

matches = re.match('db\.(\w+)\.(\w+)\((.*)\)(\.sort\(.*\))?(\.limit\(.*\))?', queryStr)
if matches:
    collectionName = matches.groups()[0]
    action = matches.groups()[1]
    sortParams = eval(sortStr)
    limitParam = limitStr
    if limitStr!='':
        limitParam = int(limitStr)

    collection = db[collectionName]
    if action=='aggregate':
        params = ast.literal_eval(matches.groups()[2])
        cursor = collection.aggregate(params).sort(sortParams).limit(limitParam)
    elif action=='find':
        params = ast.literal_eval('[' + matches.groups()[2] + ']')
        cond = params[0]
        output = {}
        if len(params)>1:
            output = params[1]
        print('DEBUG')
        print(sortParams)
        print(limitParam)
        # cursor = collection.find(cond, output).sort(sortParams).limit(limitParam)
        cursor = collection.find(cond, output).limit(limitParam)

    result = list(cursor)
    keys = []
    maxLength = {}
    align = {}
    if result[0]:
        keys = result[0].keys()
    for x in result:
        for k in keys:
            if k not in maxLength or len(str(x[k]))>maxLength[k]:
                maxLength[k] = len(str(x[k]))
            if k not in align:
                if type(x[k])==type(1) or type(x[k])==type(0.1):
                    align[k] = ''
                else:
                    align[k] = '-'
    fmtHeader =  ''
    fmtData = ''
    for k in keys:
        fmtHeader += '%-' + str(maxLength[k]) + 's' + '    '
        fmtData += '%' + align[k] + str(maxLength[k]) + 's' + '    '
    print(fmtHeader % tuple(keys))
    for x in result:
        data = []
        for k in keys:
            data.append(x[k])
        print(fmtData % tuple(data))
