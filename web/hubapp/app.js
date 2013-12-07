/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes');
var http = require('http');
var path = require('path');
var app = express();
var helpers = require('express-helpers')(app);

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(express.cookieParser('your secret here'));
app.use(express.session());
app.use(app.router);
app.use(require('stylus').middleware(__dirname + '/public'));
app.use(require('connect-assets')()); app.use(express.static(path.join(__dirname, 'public'))); // development only
if ('development' == app.get('env')) {
    app.use(express.errorHandler());
}

// define routing
app.get('/', routes.index);
app.get('/doors', routes.doors);
app.get('/luminosity', routes.luminosity);
app.get('/temperature', routes.temperature);
app.get('/lights', routes.lights);

// start server
var server = http.createServer(app).listen(app.get('port'), function(){
    console.log('Express server listening on port ' + app.get('port'));
});

// Websocket for communication with website
var io = require('socket.io').listen(server);
var cp = require('child_process');
var sensorlog = '../sensor.log';

io.sockets.on('connection', function (socket) {

    var child = cp.spawn('tail', ['-f', sensorlog]);
    child.stdout.on('data', function(data){
	data = data.toString();
	//console.log(data);
	data = data.split('\n');
	data = JSON.parse(data[0]);
    //console.log(data);
    console.log(data.luminosity);
    console.log(data.temperature);
    console.log(data.door);
    //console.log('DATA: ' + data);
	//socket.emit('news', data);
    socket.emit('door', data.door);
    socket.emit('luminosity', data.luminosity);
    socket.emit('temperature', data.temperature);
    });

});
