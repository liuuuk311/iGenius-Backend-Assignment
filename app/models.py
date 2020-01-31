from app import db


class Change(db.Model):
    """
    Create an Employee table
    """

    __tablename__ = 'changes'

    id = db.Column(db.Integer, primary_key=True)
    reference_date = db.Column(db.Date, index=True)
    source_currency = db.Column(db.String(3))
    destination_currency = db.Column(db.String(3), index=True)
    amount = db.Column(db.Float(10))

    def serialize(self):
        return {'id': self.id,
                'reference_date': self.reference_date.strftime('%Y-%m-%d'),
                'source_currency': self.source_currency,
                'destination_currency': self.destination_currency,
                'amount': self.amount}

    def __repr__(self):
        return 'Users(id={}, on={}, from={}, to={}, {})'\
                .format(self.id,
                        self.reference_date.strftime('%Y-%m-%d'),
                        self.source_currency,
                        self.destination_currency,
                        self.amount)

