var cur_device;
var cur_sensor;

$(document).ready(function() {
    get_devices();
    $(document).foundation();
});

$(document).on('click', '.sensor-btn', function(btnClick) {
    var device_id = btnClick.target.attributes['data-id'].value;
    get_sensor_data(device_id);
    //$(document).foundation();
});

function get_devices() {
    var list = $('.device-list');
    var first = true;
    $.get('/api/device/getdevices', function(data) {
	data['devices'].forEach(function(device) {
	    list.append("<li><a class=\"device-btn\" data-id=" + device['id'] + ">" + device['description'] + "</a></li>");
	    if (first) {
		get_sensors(device['id']);
		cur_device = device['id'];
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
	    btnsGrp.append('<li ' + (first ? active : '>') + '<a class="button sensor-btn" data-id=' + sensor['id'] + '>' + sensor['description'] + '</a></li>');
	    if(first) {
		cur_sensor = sensor['id'];
	    }
	    first = false;
	});
	get_sensor_data(cur_sensor);
    });
};

function get_sensor_data(sensor_id) {

    $.get('/api/sensor/' + sensor_id + '/getevents/2014-01-01+00:00:00', function(response) {
	var data = response.data_events;
	var margin = {top: 20, right: 30, bottom: 30, left: 40},
	width = 960 - margin.left - margin.right,
	height = 500 - margin.top - margin.bottom;

	var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
	var y = d3.scale.linear().range([height, 0]);
	var xAxis = d3.svg.axis().scale(x).orient("bottom");
	var yAxis = d3.svg.axis().scale(y).orient("left");

	d3.select(".chart").selectAll("*").remove();
	var chart = d3.select(".chart")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	    .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	x.domain(data.map(function(d) { return d.timestamp; }));
	y.domain([0, d3.max(data, function(d) { return d.value; })]);
	
	chart.append("g")
	    .attr("class", "x axis")
	    .attr("transform", "rotate(-90)")
	    .attr("transform", "translate(0," + height + ")")
	    .call(xAxis);

	chart.append("g")
	    .attr("class", "y axis")
	    .call(yAxis);

	var bars = chart.selectAll(".bar")
	    .data(data)
	    .enter().append("rect");

	bars.transition()
	    .attr("class", "bar")
	    .attr("x", function(d) { return x(d.timestamp); })
	    .attr("y", function(d) { return y(d.value); })
	    .delay(function(d,i) { return i * 5; })
	    .attr("height", function(d) { return height - y(d.value); })
	    .attr("width", x.rangeBand()-1);
    });
};