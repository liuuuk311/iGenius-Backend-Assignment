from flask import request
from sqlalchemy.exc import IntegrityError
import json
from datetime import datetime


from . import event
from .. import db
from ..models import Event, Calendar, User
from ..auth import requires_auth
from ..errors import UnauthorizedError, BadRequestError
from ..errors import InternalError, NotFoundError, ForbiddenError


@event.route('/calendar/<int:cal_id>/event', methods=['GET'])
@requires_auth
def get_all_event_from_calendar(cal_id):
    """
        Handle GET /calendar/<calendar_id>/event
        
        Get all the Events for a given Calendar

        Parameters:
            - from=YYYY-MM-DD HH:MM:SS (optional)
            - until=YYYY-MM-DD HH:MM:SS (optional)

        Return: The list of the events of a given calendar_id
                within the given dates if they are present
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

        # Check if the client is the user
        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Check if the user is logged-in
        if not user.active:
            raise UnauthorizedError('User is not logged-in')

        # Get the dates
        from_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        until_date = '2100-12-31'
        if 'from' in request.args:
            from_date = datetime.strptime(
                            request.args['from'], '%Y-%m-%d %H:%M:%S')
        if 'until' in request.args:
            until_date = datetime.strptime(
                            request.args['until'], '%Y-%m-%d %H:%M:%S')

        # Get all the events for the given calendar_id within the dates
        events = Event.query.filter_by(calendar_id=cal_id)          \
                            .filter(Event.start_date >= from_date)  \
                            .filter(Event.end_date <= until_date)   \
                            .all()

        return json.dumps({'status': 'ok',
                           'events': [ev.serialize() for ev in events]
                           }, indent=4), 200

    except (UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), InternalError.status_code


@event.route('/user/<int:user_id>/event', methods=['GET'])
@requires_auth
def get_all_event_from_user(user_id):
    """
        Handle GET /user/<user_id>/event
        
        Get all the Events for a given Users

        Parameters:
            - from=YYYY-MM-DD HH:MM:SS (optional)
            - until=YYYY-MM-DD HH:MM:SS (optional)

        Return: The list of the all events of a given user, no matter
                the calendar. The events are within the given dates
                if they are present.
    """
    try:
        # Get the user
        user = db.session.query(User).filter_by(id=user_id).first()

        if user is None:
            raise NotFoundError('User does not exists')

        # Check if the client is the user
        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Check if the user is logged-in
        if not user.active:
            raise UnauthorizedError('User is not logged-in')

        # Get the dates
        from_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        until_date = '2100-12-31'
        if 'from' in request.args:
            from_date = datetime.strptime(
                            request.args['from'], '%Y-%m-%d %H:%M:%S')
        if 'until' in request.args:
            until_date = datetime.strptime(
                            request.args['until'], '%Y-%m-%d %H:%M:%S')

        # Get all calendars of the given user
        calendars = db.session.query(Calendar)   \
                              .join(User)        \
                              .filter(User.id == user_id).subquery()

        # Get all the events of these calendars
        events = db.session.query(Event)                           \
                           .join(calendars)                        \
                           .filter(Event.start_date >= from_date)  \
                           .filter(Event.end_date <= until_date)   \
                           .all()

        return json.dumps({'status': 'ok',
                           'events': [ev.serialize() for ev in events]
                           }, indent=4), 200

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), InternalError.status_code


@event.route('/user/<int:user_id>/available', methods=['GET'])
def get_availability(user_id):
    """
        Handle GET /user/<user_id>/available

        Get whether or not a user is available on a given date

        Parameters:
            - from=YYYY-MM-DD HH:MM:SS
            - until=YYYY-MM-DD HH:MM:SS
    """
    try:
        # Get the user
        user = db.session.query(User).filter_by(id=user_id).first()

        if user is None:
            raise NotFoundError('User does not exists')


        # Get the dates

        if 'from' in request.args and 'until' in request.args:
            from_date = datetime.strptime(
                            request.args['from'], '%Y-%m-%d %H:%M:%S')
            until_date = datetime.strptime(
                            request.args['until'], '%Y-%m-%d %H:%M:%S')
        else:
            raise BadRequestError('Missing parameters: ' +
                                  'from and until are mandatory parameters')

        # Get all calendars of the given user
        calendars = db.session.query(Calendar)   \
                              .join(User)        \
                              .filter(User.id == user_id).subquery()

        # Get all the events of these calendars
        events = db.session.query(Event)                           \
                           .join(calendars)                        \
                           .filter(Event.start_date >= from_date)  \
                           .filter(Event.end_date <= until_date)   \
                           .all()

        if len(events) == 0:
            available = 'true'
        else:
            available = 'false'

        return json.dumps({'status': 'ok',
                           'is_available':  available
                           }, indent=4), 200

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), InternalError.status_code


@event.route('/calendar/<int:cal_id>/event', methods=['POST'])
@requires_auth
def add_one(cal_id):
    """
        Handle POST /calendar/<calendar_id>/event

        Create a new Event in a given Calendar

        Event = {
                    title: string,
                    description: string (optional),
                    start_date: datatime (YYYY-MM-DD HH:MM:SS),
                    end_date: datatime (YYYY-MM-DD HH:MM:SS),
                }
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

        # Create the new event
        event = Event(start_date=request.form['start_date'],
                      end_date=request.form['end_date'],
                      title=request.form['title'],
                      description=request.form['description'],
                      calendar_id=cal_id)

        db.session.add(event)
        db.session.commit()

        return json.dumps({'status': 'ok',
                           'message': 'Event created successfully',
                           'event': event.serialize()
                           }, indent=4)

    except IntegrityError as e:
        db.session().rollback()
        return json.dumps({'status': 'error',
                           'message': 'Cannot create calendar',
                           'details': str(e)
                           }, indent=4), BadRequestError.status_code

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)

                           }, indent=4), InternalError.status_code


@event.route('/event/<int:event_id>', methods=['PUT'])
@requires_auth
def put_one(event_id):
    """
        Handle PUT /event/<event_id>

        Edit a given Event
    """
    try:
        # Get the event
        event = db.session.query(Event)   \
                             .filter(Event.id == event_id).first()

        if event is None:
            raise NotFoundError('Event not found')

        # Get the calendar
        calendar = db.session.query(Event, Calendar)                       \
                             .filter(Event.calendar_id == Calendar.id)     \
                             .filter(Event.id == event_id).subquery()

        # Get the owner of the event
        user = db.session.query(User).join(calendar).first()

        # Check if the client is the calendar owner
        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Check if the user is logged-in
        if not user.active:
            raise UnauthorizedError('User is not logged-in')

        event.start_date = request.form['start_date']
        event.end_date = request.form['end_date']
        event.title = request.form['title']
        event.description = request.form['description']
        event.calendar_id = request.form['calendar_id']
        db.session.commit()

        return json.dumps({'status': 'ok',
                           'message': 'Event updated successfully'
                           }, indent=4)

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)

                           }, indent=4), InternalError.status_code


@event.route('/event/<int:event_id>', methods=['GET'])
@requires_auth
def get_one(event_id):
    """
        Handle GET /event/<event_id>

        Get a given Event
    """
    try:
        # Get the event
        event = db.session.query(Event)   \
                             .filter(Event.id == event_id).first()

        if event is None:
            raise NotFoundError('Event not found')

        # Get the calendar
        calendar = db.session.query(Event, Calendar)          \
                             .filter(Event.calendar_id == Calendar.id)     \
                             .filter(Event.id == event_id).subquery()

        # Get the owner of the event
        user = db.session.query(User).join(calendar).first()

        # Check if the client is the calendar owner
        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Check if the user is logged-in
        if not user.active:
            raise UnauthorizedError('User is not logged-in')

        return json.dumps({'status': 'ok',
                           'event': event.serialize()
                           }, indent=4)

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)

                           }, indent=4), InternalError.status_code


@event.route('/event/<int:event_id>', methods=['DELETE'])
@requires_auth
def delete_one(event_id):
    """
        Handle DELETE /event/<event_id>

        Delete a given Event
    """
    try:
        # Get the event
        event = db.session.query(Event)   \
                             .filter(Event.id == event_id).first()

        if event is None:
            raise NotFoundError('Event not found')

        # Get the calendar
        calendar = db.session.query(Event, Calendar)          \
                             .filter(Event.calendar_id == Calendar.id)     \
                             .filter(Event.id == event_id).subquery()

        # Get the owner of the event
        user = db.session.query(User).join(calendar).first()

        # Check if the client is the calendar owner
        if user.email != request.authorization['username']:
            raise ForbiddenError('Cannot access at this resource')

        # Check if the user is logged-in
        if not user.active:
            raise UnauthorizedError('User is not logged-in')

        db.session.delete(event)
        db.session.commit()

        return json.dumps({'status': 'ok',
                           'message': 'Event deleted successfully'
                           }, indent=4)

    except (NotFoundError, UnauthorizedError, ForbiddenError) as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)

                           }, indent=4), InternalError.status_code
