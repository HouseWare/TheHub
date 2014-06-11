from bottle import route, get, post, request, response, run, static_file
from jinja2 import Template, Environment, FileSystemLoader
from sqlalchemy import or_, and_
from ..database import db 

env = Environment(loader=FileSystemLoader('TheHub/web/lib/templates'))

@get('/')
@get('/:page_title')
def index(page_title = 'Main'):
    if page_title.lower() in ['main', 'home']:
        return env.get_template('main.html').render(page_title=page_title)
    elif page_title.lower() in ['about', 'about_us']:
        return env.get_template('about.html').render(page_title='About Us')
    else:
        return env.get_template('main.html').render(page_title='Main', error='No page {0}'.format(page_title))


@get('/foundation/<resource:re:.*(\.js|\.css)>')
def resources(resource):
    return static_file(resource, root='TheHub/web/bower_components/foundation')

@get('/foundation-icons/<resource:re:.*(\.js|\.css|\.woff|\.ttf|\.svg)>')
def resources(resource):
    return static_file(resource, root='TheHub/web/bower_components/foundation-icon-fonts')

@get('/rsrc/<resource:re:.*(\.js|\.css|\.woff|\.ttf|\.svg)>')
def resources(resource):
    return static_file(resource, root='TheHub/web/lib/rsrc')

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
    db.session.close()
    db.session = db.Session(bind=db.engine)
    return { 'devices' : devicesAsJson }

@get('/api/device/<device_id>/getsensors')
def get_sensors(device_id):
    sensorsQuery = db.session.query(db.Device).filter(db.Device.id == device_id)
    sensorsAsJson = list(map(lambda sensor: sensor.to_dictionary(), sensorsQuery.one().sensors))
    db.session.close()
    db.session = db.Session(bind=db.engine)
    return { 'sensors' : sensorsAsJson }

@get('/api/sensor/<sensor_id>/getevents/<limit>')
def get_sensor_events(sensor_id, limit):
    data_events = db.session.query(db.DataEvent).filter(db.DataEvent.sensor_id == sensor_id).order_by(db.DataEvent.timestamp.desc()).limit(limit)
    data_events_json = list(map(lambda data_event: data_event.to_dictionary(), data_events))
    db.session.close()
    db.session = db.Session(bind=db.engine)
    return { 'data_events' : data_events_json }

@get('/api/notifications')
def get_notifications():
    unread_notifications = db.session.query(db.Notification).filter(db.Notification.read == False)
    json_notifications = list(map(lambda notification: notification.to_dictionary(), unread_notifications))
    db.session.close()
    db.session = db.Session(bind=db.engine)
    return { 'notifications' : json_notifications }

@post('/api/notifications/<notification_id>/markread')
def mark_notification(notification_id):
    notification = db.session.query(db.Notification).filter(db.Notification.id == notification_id).one()
    notification.read = True
    db.session.commit()
    db.session.close()
    db.session = db.Session(bind=db.engine)
    response.status = 200
    return { 'success' : 'true' }

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if (username == 'kyle' and password=='admin'):
        return '<p>Welcome back sir.</p>'
    else:
        return '<p>Login failed.</P>'

run(host='', port=3000, debug=True)
