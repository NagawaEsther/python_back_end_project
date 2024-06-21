from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from hfsa_app.extensions import db
from hfsa_app.extensions import Bcrypt


bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  # Store the hashed password
    role = db.Column(db.String(20), nullable=False)  # Role of the user (e.g., student, parent, coach, admin)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, name, email, password, role, date_of_birth, contact_number, address):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.date_of_birth = date_of_birth
        self.contact_number = contact_number
        self.address = address
       

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_full_name(self):
        return self.name

    def __repr__(self):
        return f"<User {self.name}>"
