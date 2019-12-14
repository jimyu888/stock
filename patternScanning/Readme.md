# pattern1.py
Eps increase
```
1 revenue increase
	pattern_1_byday.mql    group by date
	pattern_1_BigPct.mql    pct3m >= xxx%
	pattern_1_filterBigPct.mql   pct3m < xxx%
	pattern_1_perf1m_lte_-10.mql   perf1m <= -10%
1.1 by eps, by year
	1.1.1 eps > 0
	1.1.2 eps < 0
	Can further break down
1.2 by marketCap, by year
	1.2.1 > 100B
	1.2.2 10B - 100B
	1.2.3 1B - 10B
	1.2.4 < 1B
1.3 by sector, by year
	1.3.1      last digit is the sector id
1.4 by industry, by year
	1.4.10001      last digit is the industry id
1.5 by year, by month
	1.5.2019
1.6 by year, by sector
1.7 by year, by industry
1.8 certain date range, by sector
1.9 certain date range, by industry
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

# pattern6.py
Revenue decrease

# pattern7.py
Revenue or eps decrease

# pattern8.py
Revenue and eps decrease

# TODO
https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
https://optionalpha.com/13-stock-chart-patterns-that-you-cant-afford-to-forget-10585.html
