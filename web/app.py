from bottle import route, get, post, request, run, static_file
from jinja2 import Template, Environment, FileSystemLoader
from sqlalchemy import or_, and_
from ..database import db 

env = Environment(loader=FileSystemLoader('lib/templates'))

@get('/')
@get('/:page_title')
def index(page_title = 'Main'):
    if page_title in ['Main', 'Home']:
        return env.get_template('main.html').render(page_title=page_title)
    else:
        return env.get_template('main.html').render(page_title='Main', error='No page {0}'.format(page_title))


@get('/foundation/<resource:re:.*(\.js|\.css)>')
def resources(resource):
    return static_file(resource, root='bower_components/foundation')

@get('/foundation-icons/<resource:re:.*(\.js|\.css|\.woff|\.ttf|\.svg)>')
def resources(resource):
    return static_file(resource, root='bower_components/foundation-icons')

@get('/rsrc/<resource:re:.*(\.js|\.css|\.woff|\.ttf|\.svg)>')
def resources(resource):
    return static_file(resource, root='lib/rsrc')

@get('/login')
def login():
    return '''
<div class="login-form">
<form action="/login" method="post">
Username: <input name="username" type="text" placeholder="password"/>
Password: <input name="password" type="password" placeholder="password" />
<hr>
<input vlaue="Login" type="submit" />
</form>
</div>
'''

@get('/api/device/getdevices')
def get_devices():
    devicesQuery = db.session.query(db.Device)
    devicesAsJson = list(map(lambda device: device.to_dictionary(), devicesQuery))
    return { 'devices' : devicesAsJson }

@get('/api/device/<device_id>/getsensors')
def get_sensors(device_id):
    sensorsQuery = db.session.query(db.Device).filter(db.Device.id == device_id)
    sensorsAsJson = list(map(lambda sensor: sensor.to_dictionary(), sensorsQuery.one().sensors))
    return { 'sensors' : sensorsAsJson }

@get('/api/sensors/<sensor_id>/getevents/<timestamp>')
def get_sensor_events(sensor_id, timestamp):
    data_events = db.session.query(db.DataEvent).filter(and_(db.DataEvent.sensor_id == sensor_id, db.DataEvent.timestamp >= timestamp))
    data_events_json = list(map(lambda data_event: data_event.to_dictionary(), data_events))
    return { 'data_events' : data_events_json }

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if (username == 'kyle' and password=='admin'):
        return '<p>Welcome back sir.</p>'
    else:
        return '<p>Login failed.</P>'

run(host='', port=3000, debug=True)
