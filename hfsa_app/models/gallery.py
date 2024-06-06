from hfsa_app import db
from datetime import datetime

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, description, image_url):
        self.title = title
        self.description = description
        self.image_url = image_url

    def __repr__(self):
        return f"Gallery(title={self.title}, description={self.description}, image_url={self.image_url}, upload_date={self.upload_date})"
