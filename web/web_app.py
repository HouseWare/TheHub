from bottle import route, get, post, request, run, template

@get('/')
def index():
    return '<a href="/login">Login</a>'


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

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if (username == 'kyle' and password=='admin'):
        return '<p>Welcome back sir.</p>'
    else:
        return '<p>Login failed.</P>'

run(host='', port=3000, debug=True)
