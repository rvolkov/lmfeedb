import os
from flask import render_template, request, jsonify, Response, send_from_directory
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from app import app
from app import rpi
from app import restbox
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

RPI = rpi.RPI()
RPI.init_check()
RPI.check_vibromotor()  # start thread

RestBox = restbox.RESTbox(RPI)
RestBox.check_controller()

# ==== entry points for one-page web application - no auth ====
@app.route('/')
def index():
  return render_template("indexpy.html")

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'cisco', 'cisco'),
    User(2, 'cisco1', 'cisco'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    print(username, password)
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

# ==== JWT ===
jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

# = end of JWT =

# ==== here is REST API calls ===

# get for tests
@app.route('/api/auth/test', methods=['GET'])
@jwt_required()
def call_auth_test():
    return jsonify({'message': 'ok'}), 200

# post
@app.route('/api/v1/stop/<finger>', methods=['POST'])
@jwt_required()
def call_stop(finger):
    RPI.stop(finger)
    return jsonify( { 'message': 'ok' } ), 200

# post
#@app.route('/stop/<finger>', methods=['POST'])
#def call_nosec_stop(finger):
#    RPI.stop(finger)
#    return jsonify( { 'message': 'ok' } ), 200

# post
@app.route('/api/v1/start/<finger>/<s>/<l>', methods=['POST'])
@jwt_required()
def call_start(finger, s, l):
    RPI.start(finger, s, l)
    return jsonify( { 'message': 'ok' } ), 200

# post
#@app.route('/start/<finger>/<s>/<l>', methods=['POST'])
#def call_nosec_start(finger, s, l):
#    RPI.start(finger, s, l)
#    return jsonify( { 'message': 'ok' } ), 200

@app.route('/api/v1/starttest', methods=['POST'])
@jwt_required()
def call_starttest():
    RPI.starttest()
    return jsonify( { 'message': 'ok' } ), 200

@app.route('/api/v1/stoptest', methods=['POST'])
@jwt_required()
def call_stoptest():
    RPI.stoptest()
    return jsonify( { 'message': 'ok' } ), 200

# ==== end of API calls ====

if __name__ == '__main__':
  app.run()
