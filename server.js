const express = require('express'),
	port = process.env.PORT || 4000;


// App setup
const app = express();
var server = app.listen(port, function(){
    console.log('Started on port: ' + port);
});

// redirect
// app.all('*', function(req, res, next) {
// 	if (req.headers["x-forwarded-proto"] === "https"){
//        return next();
//     }
//     res.redirect("https://" + req.headers.host + req.url);
// })

// token auth
app.all('/', function(req, res) {
	// if (!inviteCode.includes(req.query.token)) {
	// 	return res.send('Close Alpha testing: Invalid invite token');
	// } else {
	// 	res.sendFile(__dirname + '/public/index.html')
	// }
	res.sendFile(__dirname + '/dist')
})

// Static files
app.use(express.static('dist'));