# calSharpe.py
A sample program to demonstrate sharpe calculation

# exportMin1.js
Export stock.min1 data from MongoDB to csv
```
mongo stock export.js > SPY_2004.csv 

mongo stock export.js --eval "var year='2005'" > SPY_2005.csv  

mongo stock export.js --eval "var symbol='SPY'; var year='2004'; var start='09:30:00'; var end='16:00:00';" > SPY_2004_regular_hours.csv 

for y in `seq 2004 2019`; do mongo stock export.js --eval "var symbol='SPY'; var year='$y'; var start='09:30:00'; var end='16:00:00';" > SPY_"$y"_regular_hours.csv; done 
```

# loadFinvizDaily.py
Load finviz daily data from MySQL database to MongoDB
```
# No parameters, load today's data
./loadFinvizDaily.py

# With parameters: ./loadFinvizDaily.py [startDate] [endDate]
./loadFinvizDaily.py 2019-12-16 2019-12-18
```

# loadMin1.py
Load min1 data files(retrieved from IB) to MongoDB
```
./loadMin1.py SPY /home/ec2-user/ib/SPY/2019
```

# query.py
Run MongoDB queries, output in an aligned table structure
## Examples
```
./query.py sampleQueries/aggregate.mql
./query.py sampleQueries/find.mql
./query.py sampleQueries/findWithLimit.mql
./query.py sampleQueries/findWithSort.mql
./query.py sampleQueries/findWithSortAndLimit.mql
```

# sampleQueries
Sample MongoDB queries for query.py

For more MongoDB queries, see patternScanning/queries/

All MongoDB queries can be run under Mongo console.

# query.js
Node.js version mongodb query tool
## Issue
```
If a query has symbol and date condiction, the query runs fine.
If a query has date and sector condiction, the query runs null.
It seems to be a Node.js mongodb module issue.
```
