print("symbol,date,open,high,low,close,volume,deals,wap,gap");
year =  year || '2004';
symbol = symbol || 'SPY';
start = start || '00:00:00';
end = end || '23:59:59';
db.min1.find({'$and':[{'symbol':symbol}, {'date':{'$gte':year+'0101 '+start}}, {'date':{'$lte': year+'1231 '+end}}]}).sort({'date':1}).forEach(function(m) {
	var t = m.date.split(' ')[1]
	if (t>=start && t<=end) {
		print(	m.symbol + ',' +
			m.date + ',' +
			m.open + ',' +
			m.high + ',' +
			m.low + ',' +
			m.close + ',' +
			m.volume + ',' +
			m.deals + ',' +
			m.wap + ',' +
			m.gap);
	}
});
