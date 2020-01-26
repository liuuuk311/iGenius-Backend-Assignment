from flask import request
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import json

from . import user
from .. import db
from ..models import User
from ..errors import UnauthorizedError, BadRequestError, InternalError


@user.route('signup', methods=['POST'])
def add_one():
    """
    Handle requests to the /signup route
    """

    try:
        user = User(email=request.form['email'],
                    first_name=request.form['first_name'],
                    last_name=request.form['last_name'],
                    password=request.form['password'])

        db.session.add(user)
        db.session.commit()

        return json.dumps({'status': 'ok',
                           'message': 'User created successfully',
                           'user': user.serialize()
                           }, indent=4), 201

    except IntegrityError:
        db.session().rollback()
        return json.dumps({'status': 'error',
                           'message': 'Cannot create user',
                           'details': 'Email already in use'
                           }, indent=4), BadRequestError.status_code


@user.route('login', methods=['POST'])
def login():
    """
    Handle requests to the /login route
    """
    try:
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and user.verify_password(
                request.form['password']):

            if user.active:
                raise BadRequestError('User is already logged-in')

            user.active = True
            user.last_login_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()

            return json.dumps({'status': 'ok',
                               'message': 'User logged-in successfully',
                               'user': user.serialize()
                               }, indent=4), 200
        else:
            raise UnauthorizedError('Wrong credentials')

    except (BadRequestError, UnauthorizedError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), InternalError.status_code


@user.route('logout', methods=['POST'])
def logout():
    """
    Handle requests to the /logout route
    """
    try:
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and user.verify_password(
                request.form['password']):

            if not user.active:
                raise BadRequestError('User is already logged-out')

            user.active = False
            db.session.commit()

            return json.dumps({'status': 'ok',
                               'message': 'User logged out successfully'
                               }, indent=4), 200
        else:
            raise UnauthorizedError('Wrong credentials')

    except (BadRequestError, UnauthorizedError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), InternalError.status_code
