from flask import request
import json


from . import convert_api
from ..converter import convert
from ..errors import BadRequestError
from ..errors import InternalError, NotFoundError


@convert_api.route('/convert', methods=['GET'])
def get_one(event_id):
    """
        Handle GET /convert

    """
    try:
        # Check for the parms
        if 'amount' not in request.args:
            raise BadRequestError('Amount is a mandatory parameter')

        if 'src​_currency' not in request.args:
            raise BadRequestError('The source currency ' +
                                  'is a mandatory parameter')

        if 'des​t_currency' not in request.args:
            raise BadRequestError('The destination currency ' +
                                  'is a mandatory parameter')

        if 're​ference_date' not in request.args:
            raise BadRequestError('The reference date ' +
                                  'is a mandatory parameter')

        # Get the params
        amount = request.args['amount']
        src_currency = request.args['src​_currency']
        dest_currency = request.args['des​t_currency']
        reference_date = request.args['re​ference_date']

        converted_amount = convert(amount, src_currency,
                                   dest_currency, reference_date)

        return json.dumps({'amount': converted_amount,
                           'event': dest_currency
                           }, indent=4)

    except NotFoundError as e:
        return json.dumps({'status': 'error',
                           'message': str(e)
                           }, indent=4), e.status_code

    except Exception as e:
        return json.dumps({'status': 'error',
                           'message': str(e)

                           }, indent=4), InternalError.status_code
