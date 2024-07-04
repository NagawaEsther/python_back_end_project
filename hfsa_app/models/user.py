
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
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    sports = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    

    def __init__(self, name, email, password_hash, role, date_of_birth, contact_number, address, sports):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.date_of_birth = date_of_birth
        self.contact_number = contact_number
        self.address = address
        self.sports = sports

    def check_password(self, password_hash):
        return bcrypt.check_password_hash(self.password_hash, password_hash)

    def get_full_name(self):
        return self.name

    def __repr__(self):
        return f"<User {self.name}>"

    @classmethod
    def check_and_update_role(cls, email, password):
        """Check if the user logging in has admin credentials and update their role."""
        if email == 'HopeField@info.com' and password == 'Hope256':
            user = cls.query.filter_by(email=email).first()
            if user:
                user.role = 'admin'
                db.session.commit()
                return True
        return False

    @staticmethod
    def is_strong_password(password):
        """Validate if the password is strong enough."""
        return len(password) >= 7
    
      