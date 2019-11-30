#query.py
Run MongoDB queries, output in an aligned table structure
##Examples
./query.py sampleQueries/aggregate.mql
./query.py sampleQueries/find.mql
./query.py sampleQueries/findWithLimit.mql
./query.py sampleQueries/findWithSort.mql
./query.py sampleQueries/findWithSortAndLimit.mql

#query.js
Node.js version 
##Issue
If a query has symbol and date condiction, the query runs fine.
If a query has date and sector condiction, the query runs null.
It seems to be a Node.js mongodb module issue.
