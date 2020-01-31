from app import db
from models import Change


def convert(amount, from_curr, to_curr, date):
    coef_eur_src = amount / get_change(from_curr, date)
    return coef_eur_src * get_change(to_curr, date)


def get_change(curr, date):
    if curr == 'EUR':
        return 1

    try:
        change = db.session.query(Change)                       \
                            .filter(Change.date == date)         \
                            .filter(Change.dest_curr == curr)    \
                            .first()
        return change
    except Exception as e:
        raise e
