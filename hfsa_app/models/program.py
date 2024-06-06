from hfsa_app import db
from datetime import datetime

class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    schedule = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    fees = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, name, description, schedule, capacity, duration, fees):
        self.name = name
        self.description = description
        self.schedule = schedule
        self.capacity = capacity
        self.duration = duration
        self.fees = fees

    def __repr__(self):
        return f"Program('{self.name}', '{self.schedule}')"
