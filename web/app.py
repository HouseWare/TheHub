from bottle import route, get, post, request, run, static_file
from jinja2 import Template, Environment, FileSystemLoader
import db

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

@get('/resr/<resource:re:.*(\.js|\.css|\.woff|\.ttf|\.svg)>')
def resources(resource):
    return static_file(resource, root='lib/resr')

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

@get('/api/devices')
def get_devices():
    devicesQuery = db.session.query(db.Device)
    devicesAsJson = list(map(lambda device: device.to_dictionary(), devicesQuery))
    return { 'devices' : devicesAsJson }

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if (username == 'kyle' and password=='admin'):
        return '<p>Welcome back sir.</p>'
    else:
        return '<p>Login failed.</P>'

run(host='', port=3000, debug=True)
