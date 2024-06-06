from hfsa_app import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    registration_required = db.Column(db.Boolean, nullable=False, default=False)
    max_participants = db.Column(db.Integer)

    def __init__(self, name, description, date, time, location, registration_required=False, max_participants=None):
        self.name = name
        self.description = description
        self.date = date
        self.time = time
        self.location = location
        self.registration_required = registration_required
        self.max_participants = max_participants

    def __repr__(self):
        return f"Event('{self.name}', '{self.date}', '{self.time}', '{self.location}')"
