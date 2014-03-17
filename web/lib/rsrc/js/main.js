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
    var tabs = $('.sensor-tabs');
    tabs.html('');
    var tab_contents = $('.sensor-tabs-content');
    tab_contents.html('');
    var first = true;
    var active = 'class="active">';

    $.get('/api/device/' + device_id + '/getsensors', function(data) {
	data['sensors'].forEach(function(sensor) {
	    var sensor_data = get_sensor_data(sensor['id']);

	    tabs.append('<dd ' + (first ? active : '>') + '<a href="#sen' + sensor['id'] + '">' + sensor['description'] + '</a></dd>');
	    tab_contents.append('<div class="content ' + (first ? 'active"' : '"') + 'id="sen' + sensor['id'] + '">' + sensor_data + '</div>');
	    first = false;
	});
    });
};

function get_sensor_data(sensor_id) {
    var output = '<div class="sensor-data"><table class="event-table"><tr><th>Date</th><th>Value</th></tr>';
    $.ajax({
	url:'/api/sensor/' + sensor_id + '/getevents/2014-01-01+00:00:00',
	type: 'GET',
	async: false,
	success: function(data) {
	    data['data_events'].forEach(function(data_event) {
		output += '<tr><td>' + data_event['timestamp'] + '</td><td>' + data_event['value'] + '</td></tr>';
	    });
	}});
    output += '</table></div>';
    return output;
};