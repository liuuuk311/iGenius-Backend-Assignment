from ..models import User
from flask import jsonify, request
from functools import wraps


def check_auth(email, password):
    user = User.query.filter_by(email=email).first()
    if user is not None and user.verify_password(password):

        return True

    return False


def authenticate():
    message = {'status': 'error',
               'message': "Unauthorized request, please authenticate"}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated