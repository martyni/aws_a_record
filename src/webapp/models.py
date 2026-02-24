'''Basic flask app'''
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Basic(db.Model):  # pylint: disable=too-few-public-methods
    '''Basic class to hold message data'''
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    mandatory = db.Column(db.String(100), nullable=False)
    optional = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        '''Return sql data as dict'''
        return {
            "id": self.id,
            "mandatory": self.mandatory,
            "optional": self.optional,
            "date": self.date.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.mandatory}><Date {self.date}>"
