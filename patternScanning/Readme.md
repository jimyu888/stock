# pattern1.py
Eps increase
```
1.1 eps>0
1.2 eps<0
1.3 by marketCap, by year
	1.3.1 > 10B
	1.3.2 < 10B
1.4 
1.5 by sector, by year
1.6 by industry, by year
1.7 month, by year
```

# pattern2.py
Revenue increase

# pattern3.py
Revenue or eps increase

# pattern4.py
Revenue and eps increase

Note: The following query can get stats by month and an industry's stats by month:
```
./query.py ./sampleQueries/aggregate_patternStats_byMonth.mql
./query.py ./sampleQueries/aggregate_patternStats_industryByMonth.mql
```

# pattern5.py
Eps decrease
```
Year    Count   1w      1m      3m      SPY 1w  SPY 1m  SPY 3m      1w diff  1m diff  3m diff
2014     9029    0.16%  0.31%   0.62%    0.36%  1.28%   2.95%       -0.20%   -0.97%   -2.33%
2015    14999   -0.20% -0.29%  -3.26%   -0.25% -0.90%  -1.92%        0.05%    0.61%   -1.34%
2016    14207    0.94%  4.26%   9.75%    0.30%  1.73%   4.44%        0.64%    2.53%    5.31%
2017    12303    0.23%  1.95%   4.52%    0.18%  1.51%   3.99%        0.05%    0.44%    0.53%
2018    12076    0.15%  0.43%   0.44%   -0.03% -0.47%  -0.78%        0.18%    0.90%    1.22%
2019     2613    2.20%  2.87%   2.87%    0.41%  0.68%   0.68%        1.79%    2.19%    2.19%
                                            
        65227    0.58%  1.59%   2.49%    0.16%  0.64%   1.56%        0.42%    0.95%    0.93%
```

# pattern6.py
Revenue decrease
```
Year    Count   1w      1m      3m      SPY 1w  SPY 1m  SPY 3m          1w diff  1m diff  3m diff
2014	30534	0.85%	1.27%	1.99%	0.29%	1.15%	2.79%		0.56%	0.12%	-0.80%
2015	57328	0.42%	0.76%	3.44%	-0.03%	-0.50%	-1.27%		0.45%	1.26%	4.71%
2016	59737	3.84%	15.57%	36.66%	0.23%	1.59%	4.73%		3.61%	13.98%	31.93%
2017	49277	2.81%	9.39%	23.24%	0.32%	1.63%	4.11%		2.49%	7.76%	19.13%
2018	39634	1.08%	3.73%	12.09%	-0.20%	-0.91%	-0.24%		1.28%	4.64%	12.33%
2019	10363	2.20%	5.32%	7.70%	0.54%	1.51%	2.49%		1.66%	3.81%	5.21%
											
	246,873	1.87%	6.01%	14.19%	0.19%	0.75%	2.10%		1.68%	5.26%	12.09%
```

# pattern7.py
Revenue or eps decrease
```
Year    Count   1w      1m      3m      SPY 1w  SPY 1m  SPY 3m          1w diff  1m diff  3m diff

```

# pattern8.py
Revenue and eps decrease
```
Year    Count   1w      1m      3m      SPY 1w  SPY 1m  SPY 3m          1w diff  1m diff  3m diff
2014	2743	-0.15%	 0.09%	-1.22%	 0.28%	 1.03%	 2.84%		-0.43%	-0.94%	-4.06%
2015	5867	-0.26%	-1.57%	-4.85%	-0.28%	-1.02%	-2.10%		 0.02%	-0.55%	-2.75%
2016	5405	 1.23%	 5.02%	11.99%	 0.30%	 1.76%	 4.67%		 0.93%	 3.26%	 7.32%
2017	3504	-0.09%	 2.01%	 5.88%	 0.18%	 1.54%	 4.08%		-0.27%	 0.47%	 1.80%
2018	3551	-0.11%	 0.62%	 3.40%	-0.09%	-0.69%	 0.00%		-0.02%	 1.31%	 3.40%
2019	3186	 1.82%	 1.46%	 1.67%	 0.29%	 1.14%	 1.57%		 1.53%	 0.32%	 0.10%
										
	24,256	 0.41%	 1.27%	 2.81%	 0.11%	 0.63%	 1.84%		 0.29%	 0.65%	 0.97%
```

# TODO
https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
