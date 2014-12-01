var express = require('express'),
    ejs = require('ejs'),
    bodyParser = require('body-parser'),
    backend = require('./util/backend');

var app = express();
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.get('/', function(req, res) {
    backend.get('/rooms').then(
        function(data) {
            res.render('index.ejs', {rooms: data});
        }
    ).done()
});

app.get('/rooms', function(req, res) {
    res.render('rooms.ejs');
});

app.post('/rooms', function(req, res) {
    backend.post('/rooms', {'name': req.body.name}).then(
        function(data) {
            res.redirect('/');
        },
        function(error) {
            // TODO - add error handling
            res.redirect('/');
        }
    ).done()
});

app.delete('/rooms', function(req, res) {
    // TODO
});

app.get('/items', function(req, res) {
    res.render('items.ejs');
});

app.post('/items', function(req, res) {

    var endpoint = '/rooms/' + req.body.room + '/items/' + req.body.name;
    var data = {
        'description': req.body.description,
        'weight': req.body.weight,
        'is_fragile': req.body.is_fragile == 'on' ? true : false
    };

    backend.put(endpoint, data).then(
        function(data) {
            res.redirect('/');
        },
        function(error) {
            // TODO - add error handling
            res.redirect('/');
        }
    ).done()
});

app.delete('/items', function(req, res) {
    // TODO
});

app.get('/manifest', function(req, res) {
    backend.get('/manifest').then(
        function(data) {
            res.render('manifest.ejs', {manifest: data});
        }
    ).done()
});

app.listen(5001);
console.log('Listening on ' + 5001);
