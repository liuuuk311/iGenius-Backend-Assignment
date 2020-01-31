from datetime import datetime

from app import db
from models import Change
from .errors import NotFoundError


def convert(amount, from_curr, to_curr, date):
    coef_eur_src = amount / get_change(from_curr, date)
    return coef_eur_src * get_change(to_curr, date)


def get_change(curr, date):
    if curr == 'EUR':
        return 1

    try:
        changes_on_date = db.session.query(Change)                       \
                            .filter(Change.date == date).subquery() 
        if changes_on_date is None:
            if date == datetime.now().strftime('%Y-%m-%d'):
                download_new_data()
                get_change(curr, date)

            raise NotFoundError('Date not Found')

        change = db.session.query(changes_on_date)                          \
                            .filter(Change.destination_currency == curr)    \
                            .first()

        return change.amount

    except Exception as e:
        raise e

def download_new_data():
    pass