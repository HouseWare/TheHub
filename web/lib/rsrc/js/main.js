var cur_device;
var cur_sensor;

$(document).ready(function() {
    console.log($.fn.jquery);
    get_devices();
    $(document).foundation();
});

$(document).on('click', '.device-btn', function(btnClick) {
    var device_id = btnClick.target.attributes['data-id'].value;
    get_sensors(device_id);
    $(document).foundation();
});

function get_devices() {
    var list = $('.device-list');
    var first = true;
    $.get('/api/device/getdevices', function(data) {
	data['devices'].forEach(function(device) {
	    list.append("<li><a class=\"device-btn\" data-id=" + device['id'] + ">" + device['description'] + "</a></li>");
	    if (first) {
		get_sensors(device['id']);
		first = false;
	    };
	});
    });
};

function get_sensors(device_id) {
    var btnsGrp = $('.sensor-btn-group');
    btnsGrp.html('');

    var first = true;
    var active = 'class="active">';

    $.get('/api/device/' + device_id + '/getsensors', function(data) {
	data['sensors'].forEach(function(sensor) {
	    btnsGrp.append('<li ' + (first ? active : '>') + '<a class="button button-small" href="#sen' + sensor['id'] + '">' + sensor['description'] + '</a></li>');
	    first = false;
	});
    });
};

function get_sensor_data(sensor_id) {
    var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    
    $.ajax({
	url:'/api/sensor/' + sensor_id + '/getevents/2014-01-01+00:00:00',
	type: 'GET',
	async: false,
	success: function(data) {
	    output = data['data_events'];
	}});
};