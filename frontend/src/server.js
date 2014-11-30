var express = require('express'),
    ejs = require('ejs'),
    backend = require('./lib/backend');

var app = express();
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res) {
    backend.get('/rooms').then(
        function(data) {
            res.render('index.ejs', {rooms: data});
        }
    ).done()
});

app.get('/rooms', function(req, res) {
    backend.get('/rooms').then(
        function(data) {
            res.status(200).json(data)
        }
    ).done()
});

app.get('/manifest', function(req, res) {
    backend.get('/manifest').then(
        function(data) {
            res.status(200).json(data)
        }
    ).done()
});

app.listen(5001);
console.log('Listening on ' + 5001);
