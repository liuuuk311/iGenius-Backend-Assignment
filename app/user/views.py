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
        Handle POST requests to the /user/signup route
        Note: /user is prefixed so it can be left out
        
        Create a new user
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
        Handle POST requests to the /user/login route
        Note: /user is prefixed so it can be left out
        
        Log in a given user
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
        Handle POST requests to the /user/logout route
        Note: /user is prefixed so it can be left out
        
        Log out a given user
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
