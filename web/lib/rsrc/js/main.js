var cur_device;
var cur_sensor;

$(document).ready(function() {
    get_devices();
});

function get_devices() {
    var list = $('.device-list');
    $.get("/api/device/getdevices", function(data) {
	data['devices'].forEach(function(device) {
	    list.append("<li><a href=\"\" data-id=" + device['id'] + ">" + device['description'] + "</a></li>");	    
	});
    });
};