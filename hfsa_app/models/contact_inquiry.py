from hfsa_app import db
from datetime import datetime

class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    received_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(20), nullable=False, default='new')

    def __init__(self, name, email, subject, message, status='new'):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.status = status

    def __repr__(self):
        return f"ContactInquiry(name='{self.name}', email='{self.email}', subject='{self.subject}', status='{self.status}')"
