var http = require('http'),
    director = require('director'),
    ejs = require('ejs'),
    fs = require('fs');

var viewDir = __dirname + '/views/';

function index() {
    var that = this;
    ejs.renderFile(viewDir + 'index.ejs', function (err, output) {
        if (err) {
           throw err;
        }
        that.res.writeHead(200, {
            'Content-Type': 'text/html',
        });
        that.res.end(output);
    });
}

function serveStatic(path) {
    fs.readFile(__dirname + '/static/' + path, function(error, contents) {
        this.res.writeHead(200, {
            'Content-Type': 'text/css'
        });
        this.res.end(contents);
    }.bind(this));
}

function status() {
    this.res.writeHead(200, { 'Content-Type': 'text/plain' })
    this.res.end('status: ok');
}

var router = new director.http.Router({
    '/': {
        get: index
    },
    '/static/(.+)': {
        get: serveStatic
    },
    '/status': {
        get: status
    }
});

var server = http.createServer(function (request, response) {
    router.dispatch(request, response, function (err) {
      if (err) {
        response.writeHead(404);
        response.end();
      }
    });
});

server.listen(5001);
console.log('Listening on ' + 5001);
