from flask import request
from sqlalchemy.exc import IntegrityError
import json

from . import calendar
from .. import db
from ..models import Calendar, User
from ..auth import requires_auth
from ..errors import UnauthorizedError, BadRequestError
from ..errors import InternalError, NotFoundError, ForbiddenError


@calendar.route('/user/<int:user_id>/calendar', methods=['GET'])
@requires_auth
def get_all(user_id):
    """
        Handle GET requests to the /user/<int:user_id>/calendar route
        Returns the list of all calendars for a given user
    """
    try:
        user = __get_logged_in_user(user_id)

        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        calendars = Calendar.query.filter_by(user_id=user_id).all()

        return json.dumps({'status': 'ok',
                           'calendars': [cal.serialize() for cal in calendars]
                           }, indent=4), 201

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), InternalError.status_code


@calendar.route('/user/<int:user_id>/calendar', methods=['POST'])
@requires_auth
def add_one(user_id):
    """
        Handle POST requests to the /user/<int:user_id>/calendar route
        Create a new calendar for a given user
    """
    try:
        user = __get_logged_in_user(user_id)

        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Create the new calendar
        calendar = Calendar(name=request.form['name'],
                            description=request.form['description'],
                            user_id=user_id)

        db.session.add(calendar)
        db.session.commit()

        return json.dumps({'status': 'ok',
                           'message': 'Calendar created successfully',
                           'calendar': calendar.serialize()
                           }, indent=4), 201

    except IntegrityError as e:
        db.session().rollback()
        errorInfo = e.orig.args
        return json.dumps({'status': 'error',
                           'message': 'Cannot create calendar, ' +
                                      'user_id does not exists.',
                           'details': errorInfo[1]
                           }, indent=4), BadRequestError.status_code

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), InternalError.status_code


@calendar.route('/calendar/<int:cal_id>', methods=['GET'])
@requires_auth
def get_one(cal_id):
    """
        Handle GET requests to the /calendar/<calendar_id> route

        Get a specific Calendar
    """
    try:
        # Get the calendar
        calendar = db.session.query(Calendar)   \
                             .filter(Calendar.id == cal_id).first()

        if calendar is None:
            raise NotFoundError('Calendar not found')

        # Get the owner of the calendar
        user = db.session.query(User)       \
                         .join(Calendar)    \
                         .filter(Calendar.id == cal_id).first()

        # Check if the client is the calendar owner
        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Check if the user is logged-in
        if not user.active:
            raise UnauthorizedError('User is not logged-in')

        return json.dumps({'status': 'ok',
                           'calendar': calendar.serialize()
                           }, indent=4)

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)

                           }, indent=4), InternalError.status_code


@calendar.route('/calendar/<int:cal_id>', methods=['PUT'])
@requires_auth
def put_one(cal_id):
    """
        Handle PUT requests to the /calendar/<calendar_id> route

        Update a specific Calendar
    """
    try:
        # Get the calendar
        calendar = db.session.query(Calendar)   \
                             .filter(Calendar.id == cal_id).first()

        if calendar is None:
            raise NotFoundError('Calendar not found')

        # Get the owner of the calendar
        user = db.session.query(User)       \
                         .join(Calendar)    \
                         .filter(Calendar.id == cal_id).first()

        # Check if the client is the calendar owner
        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Check if the user is logged-in
        if not user.active:
            raise UnauthorizedError('User is not logged-in')

        calendar.name = request.form['name']
        calendar.description = request.form['description']

        db.session.commit()

        return json.dumps({'status': 'ok',
                           'message': 'Calendar updated successfully'
                           }, indent=4)

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)

                           }, indent=4), InternalError.status_code


@calendar.route('/calendar/<int:cal_id>', methods=['DELETE'])
@requires_auth
def delete_one(cal_id):
    """
        Handle DELETE requests to the /calendar/<calendar_id> route

        Delete a specific Calendar
    """
    try:
        # Get the calendar
        calendar = db.session.query(Calendar)   \
                             .filter(Calendar.id == cal_id).first()

        if calendar is None:
            raise NotFoundError('Calendar not found')

        # Get the owner of the calendar
        user = db.session.query(User)       \
                         .join(Calendar)    \
                         .filter(Calendar.id == cal_id).first()

        # Check if the client is the calendar owner
        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Check if the user is logged-in
        if not user.active:
            raise UnauthorizedError('User is not logged-in')

        db.session.delete(calendar)
        db.session.commit()

        return json.dumps({'status': 'ok',
                           'message': 'Calendar deleted successfully'
                           }, indent=4)

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)

                           }, indent=4), InternalError.status_code


def __get_logged_in_user(user_id):
    """" Helper function: Get a user from db if he/she is logged-in """

    user = db.session.query(User).filter_by(id=user_id).first()

    if user is None:
        raise NotFoundError('User does not exists')

    if not user.active:
        raise UnauthorizedError('User is not logged-in')

    return user
