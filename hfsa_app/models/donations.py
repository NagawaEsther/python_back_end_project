from hfsa_app import db
from datetime import datetime

class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100), nullable=False)
    donor_email = db.Column(db.String(100), nullable=False)
    donation_amount = db.Column(db.Float, nullable=False)
    donation_date = db.Column(db.DateTime, default=datetime.now())
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, donor_name, donor_email, donation_amount, message=None):
        self.donor_name = donor_name
        self.donor_email = donor_email
        self.donation_amount = donation_amount
        self.message = message

    def __repr__(self):
        return f"Donation('{self.donor_name}', '{self.donation_amount}')"
