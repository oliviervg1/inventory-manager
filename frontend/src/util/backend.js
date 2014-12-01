var q = require('q'),
    request = require('request');

var backend_url = 'http://backend:5000'

exports.get = function(endpoint) {
    var d = q.defer();
    request({
            'url': backend_url + endpoint,
            'json': true,
            'timeout': '10000'
        },
        function (error, response, body) {
            if (error || response.statusCode != 200) {
                d.reject(new Error(error));
            } else {
                d.resolve(body);
            }
        }
    );
    return d.promise;
}

exports.put = function(endpoint, data) {
    var d = q.defer();
    request({
            'method': 'PUT',
            'url': backend_url + endpoint,
            'body': data,
            'json': true,
            'timeout': '10000'
        },
        function (error, response, body) {
            if (error || response.statusCode != 201) {
                d.reject(new Error(error));
            } else {
                d.resolve(body);
            }
        }
    );
    return d.promise;
}

exports.post = function(endpoint, data) {
    var d = q.defer();
    request({
            'method': 'POST',
            'url': backend_url + endpoint,
            'body': data,
            'json': true,
            'timeout': '10000'
        },
        function (error, response, body) {
            if (error || response.statusCode != 201) {
                d.reject(new Error(error));
            } else {
                d.resolve(body);
            }
        }
    );
    return d.promise;
}
