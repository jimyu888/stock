# pattern1.py
Eps increase
```
2014-04-08 ~ 2019-11-29 marketCap>$10M, 2019 only has data since 2019-11-18
6881 symbols, 74131 times

Timeframe	Count	1w return	1m return	3m return	SPY 1w rtn	SPY 1m rtn	SPY 3m rtn
All		74131	0.93%		2.47%		 5.09%		 0.16%		 0.64%		 1.57%		BEAT, BETTER THAN pattern4
2014		10100	0.28%		1.00%		 1.79%		 0.54%		 1.64%		 3.06%		LOSE
2015		15082	1.39%		1.34%		-0.10%		-0.22%		-0.84%		-1.72%		BEAT
2016		15043	1.42%		5.43%		15.01%	 	 0.30%		 1.77%		 4.42%		BEAT BIG, BETTER THAN pattern4
2017		15350	0.39%		2.15%		 6.83%		 0.23%		 1.48%	 	 4.01%		BEAT
2018		15757	0.54%		1.59%		 1.09%		 0.03%		-0.46%		-1.17%		BEAT
2019		2799	3.41%		4.58%	 	 4.58%		 0.42%		 0.68%		 0.68%		BEAT BIG, BETTER THAN pattern4
```

# pattern2.py
Revenue increase
```
2014-04-08 ~ 2019-11-29 marketCap>$10M, 2019 only has data since 2019-11-18
xxx symbols, xxx times

Timeframe	Count	1w return	1m return	3m return	SPY 1w rtn	SPY 1m rtn	SPY 3m rtn
```

# pattern3.py
Revenue or eps increase
```
2014-04-08 ~ 2019-11-29 marketCap>$10M, 2019 only has data since 2019-11-18
xxx symbols, xxx times

Timeframe	Count	1w return	1m return	3m return	SPY 1w rtn	SPY 1m rtn	SPY 3m rtn
```

# pattern4.py
Revenue and eps increase
```
2014-04-08 ~ 2019-11-29 marketCap>$10M, 2019 only has data since 2019-11-18
5785 symbols, 38300 times

Timeframe	Count	1w return	1m return	3m return	SPY 1w rtn	SPY 1m rtn	SPY 3m rtn
All		38300	1.08%		2.19%		 4.07%		 0.19%		 0.71%		 1.46%		BEAT
2014		5167	0.50%		1.02%		 1.26%		 0.62%		 1.79%		 3.12%		BEAT
2015		7430	2.99%		2.24%		-0.38%		-0.21%		-0.88%		-1.62%		BEAT
2016		7200	1.05%		4.30%		11.77%		 0.34%		 1.87%		 4.39%		BEAT BIG
2017		8078	0.03%		1.52%		 7.26%		 0.19%		 1.46%		 4.10%		BEAT
2018		8670	0.62%		1.56%		 0.42%		 0.11%		-0.22%		-1.63%		BEAT
2019		1755	1.82%		2.95%		 2.95%		 0.42%		 0.70%		 0.70%		BEAT
```
The following query can get stats by month:
```
./query.py ./sampleQueries/aggregate_patternStats_byMonth.mql
```
