from bottle import route, run

@route('/')
def hello():
    return "Hello WOrld"


run(host='thehub.cs.wwu.edu', port=3000, debug=True)
