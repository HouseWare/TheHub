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
	    tabs.append('<dd ' + (first ? active : '>') + '<a href="#sen' + sensor['id'] + '">' + sensor['description'] + '</a></dd>');
	    tab_contents.append('<div class="content ' + (first ? 'active"' : '"') + 'id="sen' + sensor['id'] + '">' + sensor['description'] + ' - graph here</div>');
	    first = false;
	});
    });
};