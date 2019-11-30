var mongo = require('mongodb');

var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://mongodb_host:27017/";

MongoClient.connect(url, {useUnifiedTopology: true }).then( (client) => {
	console.log("Connected to MongoDB.");
	var db = client.db('stock');
	var query = {	'date': '2019-11-27',
			'symbol': 'INTC',
			'sector': 'Technology'
	};
	db.collection('finvizDaily').find(query).toArray(function(err, result) {
		// if (err) throw err;
		console.log(result);
	});
	client.close();
});
